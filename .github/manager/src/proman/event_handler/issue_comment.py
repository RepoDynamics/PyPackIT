"""Event handler for comments on issues and pull requests."""
from __future__ import annotations
from typing import TYPE_CHECKING
from functools import partial

import github_contexts
from loggerman import logger
from proman.dtype import BranchType
import pysyntax

from proman.dtype import RepoDynamicsBotCommand
from proman.main import EventHandler

if TYPE_CHECKING:
    from typing import Callable
    from github_contexts.github.payload import IssueCommentPayload


class IssueCommentEventHandler(EventHandler):
    """Event handler for the `issue_comment` event type.

    This event is triggered when a comment on an issue or pull request
    is created, edited, or deleted.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._payload: IssueCommentPayload = self.gh_context.event
        self._comment = self._payload.comment
        self._issue = self._payload.issue
        self._command_runner = {
            "pull": {
                RepoDynamicsBotCommand.CREATE_DEV_BRANCH: self._create_dev_branch,
            },
            "issue": {}
        }
        return

    @logger.sectioner("Issue-Comment Handler Execution")
    def run(self):
        action = self._payload.action
        is_pull = self._payload.is_on_pull
        logger.info("Comment source", "pull request" if is_pull else "issue")
        action_type = github_contexts.github.enum.ActionType
        if action in (action_type.CREATED, action_type.EDITED):
            command_runner = self._process_comment()
            if command_runner:
                command_runner()
        else:
            self.error_unsupported_triggering_action()
        return

    @logger.sectioner("Create Development Branch")
    def _create_dev_branch(self, kwargs: dict):
        if "task" not in kwargs:
            logger.critical("Missing argument", "task")
            return
        if not isinstance(kwargs["task"], int):
            logger.critical("Incorrect argument type", "'task' is not an integer.")
            return
        task_nr = kwargs["task"]
        pull_data = self._gh_api.pull(self._issue.number)
        head_branch = self.resolve_branch(branch_name=pull_data["head"]["ref"])
        if head_branch.type is not BranchType.IMPLEMENT:
            logger.critical("Invalid head branch type", head_branch.type.value)
            return
        dev_branch_name = self.create_branch_name_development(
            issue_nr=head_branch.suffix[0],
            base_branch_name=head_branch.suffix[1],
            task_nr=task_nr,
        )
        _, branch_names = self._git_base.get_all_branch_names()
        if dev_branch_name in branch_names:
            logger.critical("Development branch already exists", dev_branch_name)
            return
        tasklist = self._extract_tasklist(body=self._issue.body)
        if len(tasklist) < task_nr:
            logger.critical(
                "Invalid task number",
                f"No task {task_nr} in tasklist; it has only {len(tasklist)} entries."
            )
            return
        self._git_base.fetch_remote_branches_by_name(branch_names=head_branch.name)
        self._git_base.checkout(branch=head_branch.name)
        self._git_base.checkout(branch=dev_branch_name, create=True)
        self._git_base.commit(
            message=(
                f"init: Create development branch '{dev_branch_name}' "
                f"from implementation branch '{head_branch.name}' for task {task_nr}"
            ),
            allow_empty=True,
        )
        self._git_base.push(target="origin", set_upstream=True)
        logger.info("Create and push development branch", dev_branch_name)
        task = tasklist[task_nr - 1]
        sub_tasklist_str = self.write_tasklist(entries=[task])
        pull_body = (
            f"This pull request implements task {task_nr} of the "
            f"pull request #{self._issue.number}:\n\n"
            f"{self._MARKER_TASKLIST_START}\n{sub_tasklist_str}\n{self._MARKER_TASKLIST_END}"
        )
        pull_data = self._gh_api.pull_create(
            head=dev_branch_name,
            base=head_branch.name,
            title=task["summary"],
            body=pull_body,
            maintainer_can_modify=True,
            draft=True,
        )
        self._gh_api.issue_labels_set(number=pull_data["number"], labels=self._issue.label_names)
        logger.info("Create draft pull request", pull_data["html_url"])
        return

    @logger.sectioner("Process Comment")
    def _process_comment(self) -> Callable | None:
        body = self._comment.body
        if not body.startswith("@RepoDynamicsBot"):
            logger.info("Comment is not a command as it does not start with '@RepoDynamicsBot'.")
            return
        author_association = github_contexts.github.enum.AuthorAssociation
        if self._comment.author_association not in (
            author_association.OWNER, author_association.MEMBER, author_association.CONTRIBUTOR
        ):
            logger.info("Ignore command", "Comment author is not an owner, member, or contributor.")
            return
        command_str = body.removeprefix("@RepoDynamicsBot").strip()
        try:
            command_name, kwargs = pysyntax.parse.function_call(command_str)
        except Exception as e:
            logger.critical("Failed to parse command.", e)
            return
        try:
            command_type = RepoDynamicsBotCommand(command_name)
        except ValueError:
            logger.critical("Invalid command name", command_name)
            return
        is_pull = self._payload.is_on_pull
        command_runner_map = self._command_runner["pull" if is_pull else "issue"]
        if command_type not in command_runner_map:
            event_name = "pull request" if is_pull else "issue"
            logger.critical(
                f"Unsupported command for {event_name} comments",
                f"Command {command_type.value} is not supported for {event_name} comments."
            )
            return
        logger.info("Command", command_type.value)
        logger.debug(code_title="Arguments", code=kwargs)
        return partial(command_runner_map[command_type], kwargs)
