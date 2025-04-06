from __future__ import annotations as _annotations

from typing import TYPE_CHECKING as _TYPE_CHECKING

from github_contexts import github as gh_context
from loggerman import logger

from proman.dtype import IssueStatus, LabelType
from proman.main import EventHandler
from proman.manager.protocol import ProtocolManager

if _TYPE_CHECKING:
    from proman.dstruct import Branch, IssueForm, Label, Version


class IssuesEventHandler(EventHandler):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.payload: gh_context.payload.IssuesPayload = self.gh_context.event
        self.issue = self.payload.issue
        issue = self.manager.add_issue_jinja_env_var(self.issue)
        self.issue_author = issue["user"]

        self.issue_form: IssueForm = None
        self.labels: dict[LabelType, list[Label]] = {}
        self._protocol_comment_id: int | None = None
        self._protocol_issue_nr: int | None = None
        return

    @logger.sectioner("Issues Handler Execution")
    def run(self):
        action = self.payload.action
        if action == gh_context.enum.ActionType.OPENED:
            self.issue_form = self.manager.issue.form_from_issue_body(self.issue.body)
            return self._run_opened()
        self.issue_form = self.manager.issue.form_from_id_labels(self.issue.label_names)
        self.labels = self.manager.label.resolve_labels(self.issue.label_names)
        self.manager.protocol.load_from_issue(
            issue=self.issue, issue_form=self.issue_form, labels=self.labels
        )
        if action == gh_context.enum.ActionType.LABELED:
            return self._run_labeled()
        if action == gh_context.enum.ActionType.ASSIGNED:
            return self._run_assignment(assigned=True)
        if action == gh_context.enum.ActionType.UNASSIGNED:
            return self._run_assignment(assigned=False)
        self.manager.protocol.add_event()
        self.manager.protocol.update_on_github()
        return None

    def _run_opened(self):
        self.reporter.update_event_summary(f"Issue #{self.issue.number} opened")
        issue_inputs, body_processed, labels = self.manager.protocol.initialize_issue(
            issue=self.issue, issue_form=self.issue_form
        )
        api_response_label = self._gh_api.issue_labels_set(
            self.issue.number, [label_obj.name for label_obj in labels]
        )
        logger.info(
            "Issue Labels Update", self.reporter.api_response_code_block(api_response_label)
        )
        api_response_assign = self._gh_api.issue_add_assignees(
            number=self.issue.number,
            assignees=[assignee["github"]["id"] for assignee in self.issue_form.issue_assignees],
        )
        logger.info("Issue Assignment", self.reporter.api_response_code_block(api_response_assign))
        protocol = self.manager.protocol.generate()
        if self.manager.data["doc.protocol.as_comment"]:
            response = self._gh_api.issue_update(number=self.issue.number, body=body_processed)
            logger.info("Issue Body Update", logger.pretty(response))
            response = self._gh_api.issue_comment_create(number=self.issue.number, body=protocol)
            logger.info("Dev Protocol Comment", logger.pretty(response))
        else:
            response = self._gh_api.issue_update(number=self.issue.number, body=protocol)
            logger.info("Issue Body Update", logger.pretty(response))
        return

    def _run_labeled(self):
        label = self.manager.label.resolve_label(self.payload.label.name)
        self.manager.protocol.add_event(env_vars={"label": label})
        if label.category is not LabelType.STATUS:
            self.reporter.update_event_summary(f"Issue #{self.issue.number} labeled `{label.name}`")
            self.manager.protocol.update_on_github()
            return
        self.manager.protocol.add_env_var(status_label=label)
        # Remove all other status labels
        self.manager.label.update_status_label_on_github(
            issue_nr=self.issue.number,
            old_status_labels=self.labels[LabelType.STATUS],
            new_status_label=label,
        )
        if label.id in [IssueStatus.REJECTED, IssueStatus.DUPLICATE, IssueStatus.INVALID]:
            self._gh_api.issue_update(
                number=self.issue.number, state="closed", state_reason="not_planned"
            )
        elif label.id is IssueStatus.IMPLEMENTATION:
            self._run_labeled_status_implementation()
        self.manager.protocol.update_on_github()
        return

    def _run_labeled_status_implementation(self):
        def get_base_branches() -> list[tuple[Branch, list[Label]]]:
            base_branches_and_labels = []
            common_labels = []
            for label_group, group_labels in self.labels.items():
                if label_group not in [LabelType.BRANCH, LabelType.VERSION]:
                    common_labels.extend(group_labels)
            if self.labels.get(LabelType.VERSION):
                for version_label in self.labels[LabelType.VERSION]:
                    branch_label = self.manager.label.label_version_to_branch(version_label)
                    branch = self.manager.branch.from_name(branch_label.suffix)
                    all_labels_for_branch = common_labels + [version_label, branch_label]
                    base_branches_and_labels.append((branch, all_labels_for_branch))
            else:
                for branch_label in self.labels[LabelType.BRANCH]:
                    branch = self.manager.branch.from_name(branch_label.suffix)
                    base_branches_and_labels.append((branch, common_labels + [branch_label]))
            return base_branches_and_labels

        def create_head_branch(base: Branch) -> tuple[Branch, Version]:
            head = self.manager.branch.new_dev(issue_nr=self.issue.number, target=base.name)
            api_response = self._gh_api_admin.branch_create_linked(
                issue_id=self.issue.node_id,
                base_sha=base.sha,
                name=head.name,
            )
            logger.success(
                "Head Branch Creation", self.reporter.api_response_code_block(api_response)
            )
            self._git_base.fetch_remote_branches_by_name(branch_names=head.name)
            self._git_base.checkout(head.name)
            base_version = self.manager.release.latest_version()
            # Write initial commit on dev branch to be able to open a draft pull request
            # Ref: https://stackoverflow.com/questions/46577500/why-cant-i-create-an-empty-pull-request-for-discussion-prior-to-developing-chan
            self._git_base.commit(message="[skip ci]", allow_empty=True)
            self._git_base.push(target="origin", set_upstream=True)
            return head, base_version

        def create_pull(head: Branch, base: Branch, labels: list[Label]) -> dict:
            api_response_pull = self._gh_api.pull_create(
                head=head.name,
                base=base.name,
                title=self.manager.protocol.config.get("pr_title", self.issue.title),
                maintainer_can_modify=True,
                draft=True,
            )
            logger.success(
                f"Pull Request Creation ({head.name} -> {base.name})",
                self.reporter.api_response_code_block(api_response_pull),
            )
            api_response_labels = self._gh_api.issue_labels_set(
                number=api_response_pull["number"], labels=[label.name for label in labels]
            )
            logger.success(
                f"Pull Request Labels Update ({head.name} -> {base.name})",
                self.reporter.api_response_code_block(api_response_labels),
            )
            if self.issue_form.pull_assignees:
                api_response_assignment = self._gh_api.issue_add_assignees(
                    number=api_response_pull["number"],
                    assignees=[user["github"]["id"] for user in self.issue_form.pull_assignees],
                )
                logger.info(
                    "Pull Request Assignment",
                    self.reporter.api_response_code_block(api_response_assignment),
                )
            else:
                logger.info("Pull Request Assignment", "No assignees found for pull request.")
            pull = self.manager.add_pull_request_jinja_env_var(
                pull=api_response_pull,
                author=self.payload_sender,
            )
            self.manager.protocol.add_event(
                env_vars={"event": "pull_request", "action": "opened"},
            )
            pull_protocol = ProtocolManager(manager=self.manager)
            pull_protocol.initialize_pull(
                pull=pull,
                issue=self.issue,
                issue_form=self.issue_form,
                labels=labels,
            )
            pull_protocol.update_on_github()
            return pull

        pull_requests = []
        for base_branch, labels in get_base_branches():
            head_branch, base_version = create_head_branch(base=base_branch)
            pull = create_pull(head=head_branch, base=base_branch, labels=labels)
            pull_requests.append(pull)
            head_manager = (
                self.manager_from_metadata_file(repo="base")
                if (base_branch.name != self.payload.repository.default_branch)
                else self.manager
            )
            target_version = head_manager.release.next_version(
                base_version=base_version,
                issue_num=self.issue.number,
                deploy_type=IssueStatus.DEPLOY_ALPHA,
                action=self.issue_form.commit.action,
            )
            head_manager.changelog.update_from_issue(
                issue_form=self.issue_form,
                issue=self.issue,
                labels=labels,
                pull=pull,
                protocol=self.manager.protocol,
                base_version=base_version,
                target_version=target_version,
            )
            head_manager.variable.write_file()
            head_manager.user.contributors.write_file()
            head_manager.changelog.write_file()
            self._git_base.commit(
                message=str(
                    self.manager.commit.create_auto(
                        id="dev_branch_creation",
                        env_vars={
                            "head": head_branch,
                            "base": base_branch,
                            "pull_request": pull,
                            "changelog": head_manager.changelog.current,
                        },
                    )
                ),
                amend=True,
            )
            self._git_base.push(force_with_lease=True)
        self.manager.protocol.add_env_var(pull_requests=pull_requests)
        return

    def _run_assignment(self, assigned: bool):
        assignee = self.manager.user.get_from_github_rest_id(self.payload.assignee.id)
        action_desc = "assigned to" if assigned else "unassigned from"
        self.reporter.update_event_summary(f"Issue #{self.issue.number} {action_desc} {assignee['github']['id']}")
        self.manager.protocol.add_event(env_vars={"assignee": assignee})
        self.manager.protocol.update_on_github()
        return
