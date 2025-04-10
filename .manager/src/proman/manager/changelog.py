from __future__ import annotations as _annotations

import copy
from typing import TYPE_CHECKING as _TYPE_CHECKING

import pyserials as ps
from controlman import data_validator
from controlman import exception as _exception
from github_contexts.github.payload.object import Issue
from loggerman import logger

from proman import const
from proman.dstruct import Version, VersionTag
from proman.dtype import LabelType
from proman.util import date

if _TYPE_CHECKING:
    from github_contexts.github.payload.object import Milestone, PullRequest
    from versionman.pep440_semver import PEP440SemVer

    from proman.dstruct import IssueForm, Label, Tasklist
    from proman.manager import Manager, ProtocolManager


class ChangelogManager:
    def __init__(self, manager: Manager):
        self._manager = manager
        log_title = "Changelog Load"
        self._filepath = self._manager.git.repo_path / const.FILEPATH_CHANGELOG
        try:
            self._changelog = ps.read.json_from_file(self._filepath)
        except ps.exception.read.PySerialsReadException as e:
            raise _exception.load.ControlManInvalidMetadataError(cause=e, filepath=self._filepath) from None
        self._read = copy.deepcopy(self._changelog)
        logger.success(
            log_title,
            f"Loaded changelog from file '{const.FILEPATH_CHANGELOG}':",
            logger.data_block(self._changelog),
        )
        data_validator.validate(self._changelog, schema="changelog")
        if self._changelog[0].get("phase") != "dev":
            self._current = {"phase": "dev"}
            self._changelog.insert(0, self._current)
        else:
            self._current = self._changelog[0]
        return

    @property
    def current(self) -> dict:
        return self._current

    @property
    def full(self) -> list:
        return self._changelog

    def update_from_issue(
        self,
        issue_form: IssueForm,
        issue: Issue,
        labels: list[Label],
        pull: dict,
        protocol: ProtocolManager,
        base_version: Version,
        target_version: Version | VersionTag,
    ):
        self.update_version(version=target_version)
        self.update_date()
        self._update_type(issue_form=issue_form)
        self._update_issue(issue=issue, issue_form=issue_form, protocol=protocol)
        self._update_labels(labels=labels)
        if issue.milestone:
            self._update_milestone(milestone=issue.milestone)
        self._update_parent(version=base_version)
        self._update_pull_request(pull=pull, base_version=base_version, head_version=base_version)

        self._update_contributors_with_assignees(issue=issue, issue_form=issue_form)
        for assignee in issue_form.pull_assignees + issue_form.review_assignees:
            self.update_contributor(
                id=assignee.id,
                member=assignee.member,
                roles=assignee.current_role,
            )
        if issue_form.role["submitter"]:
            submitter = self._manager.user.from_issue_author(issue, add_to_contributors=True)
            self.update_contributor(
                member=submitter.member, id=submitter.id, roles=issue_form.role["submitter"]
            )
        return

    def update_from_pull(
        self,
        issue_form: IssueForm,
        pull: PullRequest,
        labels: dict[LabelType, list[Label]],
        protocol: ProtocolManager,
        tasklist: Tasklist,
        base_version: Version,
        head_version: Version,
        target_version: Version | PEP440SemVer,
    ):
        self.update_date()
        self._update_labels(labels)
        if pull.milestone:
            self._update_milestone(milestone=pull.milestone)
        self._update_parent(version=base_version)
        self.update_protocol_data(protocol.get_all_data())
        self.update_protocol_tasklist(tasklist)
        self.update_public(public=bool(issue_form.commit.action))
        self._update_pull_request(pull=pull, base_version=base_version, head_version=head_version)
        self.update_type_id(type_id=issue_form.id)
        self.update_version(version=target_version)
        self._update_contributors_with_assignees(issue=pull, issue_form=issue_form)
        if not pull.draft:
            self.update_pull_reviewers(pull=pull, issue_form=issue_form)
        return

    def update_pull_reviewers(self, pull: PullRequest, issue_form: IssueForm):
        for reviewer in pull.requested_reviewers:
            user = self._manager.user.get_from_github_rest_id(reviewer.id, add_to_contributors=True)
            for predefined_reviewer in issue_form.review_assignees:
                if predefined_reviewer == user:
                    roles = predefined_reviewer.current_role
                    break
            else:
                roles = issue_form.role["review_assignee"]
            if roles:
                self.update_contributor(id=user.id, member=user.member, roles=roles)
        return

    def commit_changes(self, amend: bool = False) -> str | None:
        written = self.write_file()
        if not written:
            return None
        commit = self._manager.commit.create_auto(id="changelog_sync")
        return self._manager.git.commit(message=str(commit.conv_msg), amend=amend)

    def update_contributor(self, id: str, member: bool, roles: dict[str, int]):
        category = "member" if member else "collaborator"
        contributor_roles = (
            self.current.setdefault("contributor", {})
            .setdefault(category, {})
            .setdefault(id, {})
            .setdefault("role", {})
        )
        for role_id, role_priority in roles.items():
            if role_id not in contributor_roles:
                contributor_roles[role_id] = role_priority
        return

    def update_date(self):
        self.current["date"] = date.to_internal(date.from_now())
        return

    def _update_contributors_with_assignees(
        self, issue: Issue | PullRequest, issue_form: IssueForm
    ):
        assignee_gh_ids = []
        if issue.assignee:
            assignee_gh_ids.append(issue.assignee.id)
        if issue.assignees:
            for assignee in issue.assignees:
                if assignee:
                    assignee_gh_ids.append(assignee.id)
        for assignee_gh_id in set(assignee_gh_ids):
            user = self._manager.user.get_from_github_rest_id(
                assignee_gh_id, add_to_contributors=True
            )
            predefined_assignees = (
                issue_form.issue_assignees
                if isinstance(issue, Issue)
                else issue_form.pull_assignees
            )
            for predefined_assignee in predefined_assignees:
                if predefined_assignee == user:
                    roles = predefined_assignee.current_role
                    break
            else:
                roles = issue_form.role[
                    "issue_assignee" if isinstance(issue, Issue) else "pull_assignee"
                ]
            if roles:
                self.update_contributor(
                    id=user.id,
                    member=user.member,
                    roles=roles,
                )
        return

    def _update_issue(self, issue: Issue, issue_form: IssueForm, protocol: ProtocolManager):
        entry = {
            "type": issue_form.id,
            "number": issue.number,
            "id": issue.id,
            "node_id": issue.node_id,
            "url": issue.html_url,
            "date": date.to_internal(date.from_github(issue.created_at)),
            "title": issue.title,
        }
        for datum_id, datum in self._manager.data["issue.protocol.data"].items():
            if datum.get("changelog"):
                entry.setdefault("protocol", {}).setdefault("data", {})[datum_id] = (
                    protocol.data.get(datum_id)
                )
        for body_elem in issue_form.body:
            if body_elem.get("changelog"):
                elem_id = body_elem.get("id")
                if elem_id:
                    entry.setdefault("protocol", {}).setdefault("input", {})[elem_id] = (
                        protocol.input.get(elem_id)
                    )
        self.current["issue"] = entry
        return

    def _update_labels(self, labels: list[Label] | dict[LabelType, list[Label]]):
        if isinstance(labels, list):
            label_list = labels
        else:
            label_list = []
            for label_type, label_entries in labels.items():
                if label_type in (LabelType.CUSTOM_SINGLE, LabelType.CUSTOM_GROUP):
                    label_list.extend(label_entries)
        out = []
        for label in label_list:
            if label.category is LabelType.CUSTOM_GROUP:
                out.append({"group": label.group_id, "id": label.id})
            elif label.category is LabelType.CUSTOM_SINGLE:
                out.append({"group": "single", "id": label.id})
        self.current["labels"] = out
        return

    def _update_milestone(self, milestone: Milestone):
        self.current["milestone"] = {
            "number": milestone.number,
            "id": milestone.id,
            "node_id": milestone.node_id,
            "url": milestone.html_url,
            "title": milestone.title,
            "description": milestone.description,
            "due_on": date.to_internal(date.from_github(milestone.due_on)),
            "created_at": date.to_internal(date.from_github(milestone.created_at)),
        }
        return

    def _update_parent(self, version: Version):
        self.current["parent"] = {
            "version": str(version.public),
            "distance": version.distance,
            "sha": version.sha,
            "date": date.to_internal(version.date),
        }
        return

    def _update_protocol(self, protocol: ProtocolManager):
        self.update_protocol_data(protocol.data)
        self.update_protocol_tasklist(protocol.tasklist)
        return

    def update_protocol_data(self, data: dict):
        self.current["protocol"] = data
        return

    def update_protocol_tasklist(self, tasklist: Tasklist):
        self.current["tasks"] = tasklist.as_list
        return

    def _update_pull_request(
        self,
        pull: PullRequest | dict,
        base_version: Version,
        head_version: Version,
    ):
        self.current["pull_request"] = {
            "number": pull["number"],
            "id": pull["id"],
            "node_id": pull["node_id"],
            "url": pull["html_url"],
            "date": date.to_internal(date.from_github(pull["created_at"])),
            "title": pull["title"],
            "additions": pull.get("additions", 0),
            "deletions": pull.get("deletions", 0),
            "commits": pull.get("commits", 0),
            "changed_files": pull.get("changed_files", 0),
            "base": {
                "ref": pull["base"].name,
                "version": str(base_version.public),
                "distance": base_version.distance,
                "sha": pull["base"].sha,
            },
            "head": {
                "ref": pull["head"].name,
                "version": str(head_version.public),
                "distance": head_version.distance,
                "sha": pull["head"].sha,
            },
        }
        return

    def update_github(self, id: int, node_id: str):
        self.current["github"] = {"id": id, "node_id": node_id}
        return

    def update_zenodo(self, id: str, doi: str, draft: bool, sandbox: bool):
        entry = {"id": id, "doi": doi, "draft": draft}
        if sandbox:
            self.current.setdefault("dev", {})["zenodo_sandbox"] = entry
        else:
            self.current["zenodo"] = entry
        return

    def update_release_zenodo_draft_status(self, sandbox: bool, draft: bool = False):
        release_data = (
            self.current.get("dev", {}).get("zenodo_sandbox", {})
            if sandbox
            else self.current.get("zenodo")
        )
        release_data["draft"] = draft
        return

    def update_version(self, version: VersionTag | Version | PEP440SemVer):
        if isinstance(version, VersionTag):
            self.current["version"] = str(version.version)
            self.current["tag"] = str(version)
            return
        if isinstance(version, Version) and not version.is_local:
            tag_prefix = self._manager.data["tag.version.prefix"]
            self.current["tag"] = f"{tag_prefix}{version}"
        self.current["version"] = str(version)
        return

    def finalize(self, pre: bool):
        self.current.pop("dev", None)
        if pre:
            self.current["phase"] = pre
        else:
            self.current.pop("phase")
        return self.current

    def write_file(self):
        if self._changelog == self._read:
            return False
        self._filepath.write_text(
            ps.write.to_json_string(self._changelog, sort_keys=True, indent=3).strip() + "\n",
            newline="\n",
        )
        return True

    def _update_type(self, issue_form: IssueForm):
        self.current["type"] = issue_form.commit.action.value or "local"
