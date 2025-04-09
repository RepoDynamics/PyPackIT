"""Initialize a new project."""

from __future__ import annotations

from typing import TYPE_CHECKING

import fileex
from loggerman import logger

from proman import script

if TYPE_CHECKING:
    from proman.manager import Manager


@logger.sectioner("Project Initialization")
def run(
    manager: Manager,
):
    repo_path = manager.git.repo_path
    fileex.directory.delete(
        path=repo_path,
        exclude=[
            ".devcontainer/install.py",
            ".git/",
            ".github/actions/",
            ".github/workflows/",
            ".manager/",
            "template/",
        ],
    )
    fileex.directory.merge(source=repo_path / "template", destination=repo_path)
    main_manager, _ = script.cca.run(
        branch_manager=None,
        action=InitCheckAction.AMEND,
        future_versions={self.gh_context.event.repository.default_branch: "0.0.0"},
    )
    script.lint.run(
        branch_manager=main_manager,
        action=InitCheckAction.AMEND,
        ref_range=None,
    )
    return
