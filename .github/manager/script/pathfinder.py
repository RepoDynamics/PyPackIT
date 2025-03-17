#!/usr/bin/env python3

import sys

import controlman
import actionman
from loggerman import logger
from proman.report import initialize_logger as proman_logger_initialize


def get_local_dir_paths():
    needs_sec = {"base": False, "head": False, "pre-commit": False}
    for repo_path, repo_name in (("repo_base", "base"), ("repo_head", "head")):
        try:
            meta = controlman.from_json_file(repo_path=repo_path)
        except controlman.exception.ControlManException:
            logger.warning(
                "Cache Load: Missing Project Metadata File",
                f"Could not find the metadata file for the {repo_name} repository.",
                logger.traceback(),
            )
        else:
            has_set = set_local_dir_path(metadata=meta, repo_path=repo_path, repo_name=repo_name)
            needs_sec[repo_name] = has_set
            if repo_name == "head":
                has_set = set_pre_commit_config_path(metadata=meta, repo_path=repo_path, repo_name=repo_name)
                needs_sec["pre-commit"] = has_set
    curr_section_num = 1
    for key in ("base", "head", "pre-commit"):
        if needs_sec[key]:
            actionman.step_output.write(f"secnum_cache_{key}", curr_section_num)
            curr_section_num += 1
    return


def set_pre_commit_config_path(metadata, repo_path: str, repo_name: str) -> bool:
    key = "workflow.refactor.pre_commit_config"
    pre_commit_config_path = metadata[key]
    if not pre_commit_config_path:
        logger.warning(
            "Cache Load: Missing Pre-Commit Config",
            f"Could not find the key `{key}` in the metadata file of the {repo_name} repository. "
            "The pre-commit cache will not be restored.",
        )
        return False
    logger.info(
        "Cache Load: Pre-Commit Config Path",
        f"Located the pre-commit configuration for the {repo_name} repository.",
    )
    actionman.step_output.write(f"pre_commit_config_{repo_name}", "true")
    return True


def set_local_dir_path(metadata, repo_path: str, repo_name: str) -> bool:
    local_dir_path = metadata["local.cache.path"]
    if not local_dir_path:
        logger.warning(
            "Cache Load: Missing Local Cache Directory Path"
            f"Could not find the key `local.cache.path` in the metadata file of the {repo_name} repository. "
            "The local cache will not be restored."
        )
        return False
    logger.info(
        "Cache Load: Local Cache Directory Path",
        f"Located the local cache directory path for the {repo_name} repository at `{local_dir_path}`.",
    )
    actionman.step_output.write(f"local_dirpath_{repo_name}", f"{repo_path}/{local_dir_path}")
    return True


if __name__ == "__main__":
    proman_logger_initialize(title_number=[1, 4])
    logger.section("Cache Load")
    get_local_dir_paths()
    sys.exit(0)
