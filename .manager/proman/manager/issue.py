from __future__ import annotations as _annotations

import re
from typing import TYPE_CHECKING as _TYPE_CHECKING

from loggerman import logger

from proman.dstruct import IssueForm
from proman.exception import PromanError

if _TYPE_CHECKING:
    from typing import Literal
    from proman.manager import Manager


class IssueManager:
    def __init__(self, manager: Manager):
        self._manager = manager
        return

    def form_from_id(self, form_id: str) -> IssueForm:
        for issue_form in self._manager.data["issue.forms"]:
            if issue_form["id"] == form_id:
                return self._make_issue_form(issue_form)
        raise ValueError(f"Could not find issue form with ID '{form_id}'.")

    def form_from_id_labels(self, label_names: list[str]) -> IssueForm:
        for issue_form_data in self._manager.data["issue.forms"]:
            issue_form = self._make_issue_form(issue_form_data)
            if all(label.name in label_names for label in issue_form.id_labels):
                return issue_form
        raise ValueError(f"Could not find issue form from labels {label_names}.")

    def form_from_issue_body(self, issue_body: str) -> IssueForm:
        ids = [form["id"] for form in self._manager.data["issue.forms"]]
        id_pattern = "|".join(map(re.escape, ids))
        pattern = rf"<!-- ISSUE-ID: ({id_pattern}) -->"
        match = re.search(pattern, issue_body)
        if not match:
            logger.critical(
                "Issue ID Extraction", "Could not match the issue ID in the issue body."
            )
            raise PromanError()
        return self.form_from_id(match.group(1))

    def forms_from_id_regex(
        self,
        regex: str,
        form_type: Literal["issue", "discussion"] = "issue",
    ) -> list[dict]:
        """Get issue forms and discussion categories matching a RegEx.

        This function is used to filter issue forms and discuttsion categories
        (from `ccc.issue.forms` and `ccc.discussion.category`, respectively)
        based on a RegEx pattern.
        """
        out = []
        pattern = re.compile(regex)
        if form_type == "issue":
            forms = self._manager.get_data("issue.forms", [])
            out.extend([form for form in forms if pattern.match(form["id"])])
            return out
        for category_slug, category_data in self._manager.get_data("discussion.category", {}).items():
            if pattern.match(category_slug):
                out.append(category_data)
        return out

    def _make_issue_form(self, issue_form: dict) -> IssueForm:
        id_labels = [
            self._manager.label.from_id(group_id, label_id)
            for group_id, label_id in issue_form["id_labels"]
        ]
        return IssueForm(
            id=issue_form["id"],
            commit=self._manager.commit.create_release(id=issue_form["commit"]),
            id_labels=id_labels,
            issue_assignees=self._manager.user.from_issue_form_id(
                issue_form_id=issue_form["id"],
                assignment="issue",
            ),
            pull_assignees=self._manager.user.from_issue_form_id(
                issue_form_id=issue_form["id"],
                assignment="pull",
            ),
            review_assignees=self._manager.user.from_issue_form_id(
                issue_form_id=issue_form["id"],
                assignment="review",
            ),
            labels=[
                self._manager.label.from_id(group_id, label_id)
                for group_id, label_id in issue_form.get("labels", [])
            ],
            role={
                "submitter": None,
                "issue_assignee": None,
                "pull_assignee": None,
                "review_assignee": None,
                "commit_author": None,
                "commit_committer": None,
            }
            | self._manager.data.get("issue.form.role", {})
            | issue_form.get("role", {}),
            name=issue_form["name"],
            description=issue_form["description"],
            projects=issue_form.get("projects", []),
            title=issue_form.get("title", ""),
            body=issue_form.get("body", []),
            processed_body=issue_form.get("processed_body", []),
        )
