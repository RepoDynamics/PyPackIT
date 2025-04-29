"""Initialize a new project."""

from __future__ import annotations

from typing import TYPE_CHECKING

import fileex
from loggerman import logger

from proman import script

if TYPE_CHECKING:
    from proman.manager import Manager


@logger.sectioner("Project Initialization")
def run(manager: Manager):
    repo_path = manager.git.repo_path
    web_source_path = manager.data["web.path.source"]
    fileex.directory.delete(
        path=repo_path,
        exclude=[
            f"{manager.data["pypkg_ci.path.root"]}/",
            f"{web_source_path}/conf.py",
            f"{web_source_path}/_media/icon",
            f"{web_source_path}/_media/image",
            f"{web_source_path}/_media/logo_ext",
            ".devcontainer/",
            ".git/",
            ".github/actions/",
            ".github/workflows/",
            "template/",
        ],
    )
    fileex.directory.merge(source=repo_path / "template", destination=repo_path)
    new_manager, _, _ = script.cca.run(
        manager=manager,
        action="apply",
        control_center=".control",
        clean_state=True,
        branch_version={manager.branch.default_branch_name: "0.0.0"},
    )
    script.lint.run(
        manager=new_manager,
        action="apply",
        hook_state="manual",
        all_files=True,
    )
    return new_manager
