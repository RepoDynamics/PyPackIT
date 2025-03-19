from __future__ import annotations as _annotations

from functools import partial
from typing import TYPE_CHECKING as _TYPE_CHECKING

import conventional_commits
from conventional_commits import ConventionalCommitMessage
from loggerman import logger as _logger

from proman.dstruct import Commit
from proman.dtype import ReleaseAction

if _TYPE_CHECKING:
    from gittidy import Git

    from proman.manager import Manager


class CommitManager:
    def __init__(self, manager: Manager):
        self._manager = manager
        self._msg_parser = conventional_commits.create_parser(
            type_regex=self._manager.data["commit.config.regex.validator.type"],
            scope_regex=self._manager.data["commit.config.regex.validator.scope"],
            description_regex=self._manager.data["commit.config.regex.validator.description"],
            scope_start_separator_regex=self._manager.data[
                "commit.config.regex.separator.scope_start"
            ],
            scope_end_separator_regex=self._manager.data["commit.config.regex.separator.scope_end"],
            scope_items_separator_regex=self._manager.data[
                "commit.config.regex.separator.scope_items"
            ],
            description_separator_regex=self._manager.data[
                "commit.config.regex.separator.description"
            ],
            body_separator_regex=self._manager.data["commit.config.regex.separator.body"],
            footer_separator_regex=self._manager.data["commit.config.regex.separator.footer"],
        )
        self._msg_writer = partial(
            conventional_commits.create,
            scope_start=self._manager.data["commit.config.scope_start"],
            scope_separator=self._manager.data["commit.config.scope_separator"],
            scope_end=self._manager.data["commit.config.scope_end"],
            description_separator=self._manager.data["commit.config.description_separator"],
            body_separator=self._manager.data["commit.config.body_separator"],
            footer_separator=self._manager.data["commit.config.footer_separator"],
            type_regex=self._manager.data["commit.config.regex.validator.type"],
            scope_regex=self._manager.data["commit.config.regex.validator.scope"],
            description_regex=self._manager.data["commit.config.regex.validator.description"],
        )
        return

    def create_from_msg(self, message: str) -> Commit:
        def get_dev_id(conv_msg: ConventionalCommitMessage):
            def get_scope(data: dict):
                scope = data.get("scope", tuple())
                return {scope} if isinstance(scope, str) else set(scope)

            for commit_id, commit_data in self._manager.data["commit.dev"].items():
                if commit_data["type"] == conv_msg.type and get_scope(commit_data) == set(
                    msg.scope
                ):
                    return commit_id
            return None

        try:
            msg = self._msg_parser.parse(message)
            _logger.info(
                "Commit Parse", "Plain message:", repr(message), "Parsed message:", repr(msg)
            )
            return Commit(
                writer=self._msg_writer,
                type=msg.type,
                scope=msg.scope,
                description=msg.description,
                body=msg.body,
                footer=msg.footer,
                dev_id=get_dev_id(msg),
            )
        except Exception as e:
            _logger.warning(
                "Commit Message Processing",
                f"Failed to parse commit message: {e}",
                message,
            )
            parts = message.split("\n", 1)
            description = parts[0]
            body = parts[1] if len(parts) > 1 else ""
            return Commit(
                writer=self._msg_writer,
                description=description,
                body=body,
            )

    def create_auto(self, id: str, env_vars: dict | None = None) -> Commit:
        # Skipping workflow runs: https://docs.github.com/en/actions/managing-workflow-runs-and-deployments/managing-workflow-runs/skipping-workflow-runs
        commit_data = self._manager.data[f"commit.auto.{id}"]
        scope = commit_data.get("scope")
        if isinstance(scope, str):
            scope = (scope,)
        return Commit(
            writer=self._msg_writer,
            type=commit_data["type"],
            description=commit_data["description"],
            scope=scope,
            body=f"{commit_data.get('body', '').strip()}\n[skip ci]".strip(),
            footer=commit_data.get("footer"),
            type_description=commit_data.get("type_description"),
            jinja_env_vars=self._manager.jinja_env_vars | (env_vars or {}),
        )

    def create_release(self, id: str, env_vars: dict | None = None) -> Commit:
        commit_data = self._manager.data["commit.release"][id]
        return Commit(
            writer=self._msg_writer,
            type=commit_data["type"],
            description=commit_data["description"],
            scope=commit_data.get("scope"),
            body=commit_data.get("body"),
            footer=commit_data.get("footer"),
            action=ReleaseAction(commit_data["action"]) if commit_data.get("action") else None,
            type_description=commit_data.get("type_description"),
            jinja_env_vars=self._manager.jinja_env_vars | (env_vars or {}),
        )

    def from_git(
        self,
        revision_range: str | None = None,
        git: Git | None = None,
    ) -> list[Commit]:
        git = git or self._manager.git
        commits = git.get_commits(
            revision_range
            or f"{self._manager.gh_context.hash_before}..{self._manager.gh_context.hash_after}"
        )
        return [self.create_from_msg(commit["msg"]) for commit in commits]

    def from_pull_request(
        self,
        pull_nr: int | str,
        head_manager: Manager | None = None,
        revision_range: str | None = None,
        add_to_contributors: bool = True,
    ) -> list[Commit]:
        def make_user(user: dict):
            github_username = user.get("user", {}).get("login")
            if github_username:
                return head_manager.user.from_github_username(
                    username=github_username,
                    add_to_contributors=add_to_contributors,
                )
            return head_manager.user.from_name_and_email(
                name=user["name"],
                email=user["email"],
                add_to_contributors=add_to_contributors,
            )

        if not head_manager:
            head_manager = self._manager
        commits = []
        commits_data = self._manager.gh_api_actions.pull_commits(
            number=pull_nr,
            count=len(self.from_git(revision_range=revision_range, git=head_manager.git)),
            sort="last",
        )
        for commit_data in commits_data:
            commit = self.create_from_msg(commit_data["commit"]["message"])
            commit.authors = [make_user(author) for author in commit_data["commit"]["authors"]]
            if not commit_data["commit"]["authoredByCommitter"]:
                commit.committer = make_user(commit_data["commit"]["committer"])
            commits.append(commit)
        return commits
