from __future__ import annotations

from typing import TYPE_CHECKING

from github_contexts import github as _gh_context
from loggerman import logger

from proman.dtype import BranchType

if TYPE_CHECKING:
    from github_contexts.github.payload import PullRequestPayload
    from github_contexts.github.payload.object import PullRequest

    from proman.dstruct import Branch


class PullRequestTargetEventHandler:
    def __init__(self, **kwargs):
        self.payload: PullRequestPayload = self.gh_context.event
        self.pull: PullRequest = self.payload.pull_request
        pull_internalized = self.manager.add_pull_request_jinja_env_var(self.pull)
        self.pull_author = pull_internalized["user"]
        self.branch_base: Branch = pull_internalized["base"]
        self.branch_head: Branch = pull_internalized["head"]
        logger.info("Base Branch Resolution", str(self.branch_base))
        logger.info("Head Branch Resolution", str(self.branch_head))
        return

    def run(self):
        if self.payload.internal:
            return None
        action = self.payload.action
        if action != _gh_context.enum.ActionType.OPENED:
            self.reporter.error_unsupported_triggering_action()
            return None
        if self.branch_head.type is BranchType.DEV:
            return self.opened_head_dev()
        return None

    def run_assigned(self):
        return

    def opened_head_dev(self):
        if self.branch_head.name != self.branch_base.name:
            # Update base branch to corresponding dev branch and inform user
            pass
        return
