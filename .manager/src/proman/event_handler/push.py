"""Push event handler."""

from __future__ import annotations as _annotations

import shutil
from typing import TYPE_CHECKING

import fileex as _fileex
from github_contexts import github as _gh_context
from loggerman import logger
from versionman.pep440_semver import PEP440SemVer

from proman.dtype import BranchType, InitCheckAction
from proman.main import EventHandler

if TYPE_CHECKING:
    from pathlib import Path


class PushEventHandler(EventHandler):
    """Push event handler.

    This handler is responsible for the setup process of new and existing repositories.
    It also runs Continuous pipelines on forked repositories.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.payload: _gh_context.payload.PushPayload = self.gh_context.event
        self.head_commit = self.gh_context.event.head_commit
        if self.manager and self.head_commit:
            self.head_commit_msg = self.manager.commit.create_from_msg(self.head_commit.message)
            logger.info("Head Commit", repr(self.head_commit_msg))
        return

    @logger.sectioner("Push Handler Execution")
    def run(self):
        if self.gh_context.ref_type is not _gh_context.enum.RefType.BRANCH:
            self.reporter.event(f"Push to tag `{self.gh_context.ref_name}`")
            self.reporter.add(
                name="event", status="skip", summary="Push to tags does not trigger the workflow."
            )
            return None
        action = self.payload.action
        if action not in (_gh_context.enum.ActionType.CREATED, _gh_context.enum.ActionType.EDITED):
            self.reporter.event(f"Deletion of branch `{self.gh_context.ref_name}`")
            self.reporter.add(
                name="event",
                status="skip",
                summary="Branch deletion does not trigger the workflow.",
            )
            return None
        is_main = self.gh_context.ref_is_main
        has_tags = bool(self._git_head.get_tags())
        if action is _gh_context.enum.ActionType.CREATED:
            if not is_main:
                self.reporter.event(f"Creation of branch `{self.gh_context.ref_name}`")
                self.reporter.add(
                    name="event",
                    status="skip",
                    summary="Branch creation does not trigger the workflow.",
                )
                return None
            if not has_tags:
                self.reporter.event("Repository creation")
                return self._run_repository_creation()
            self.reporter.event(f"Creation of default branch `{self.gh_context.ref_name}`")
            self.reporter.add(
                name="event",
                status="skip",
                summary="Default branch created while a git tag is present. "
                "This is likely a result of renaming the default branch.",
            )
            return None
        # Branch edited
        if self.gh_context.event.repository.fork:
            return self._run_branch_edited_fork()
        if not is_main:
            self.reporter.event(f"Modification of branch `{self.gh_context.ref_name}`")
            self.reporter.add(
                name="event",
                status="skip",
                summary="Modification of non-default branches does not trigger the workflow.",
            )
            return None
        # Main branch edited
        if not has_tags:
            # The repository is in the initialization phase
            return self._run_init()
        return self._run_branch_edited_main_normal()

    def _run_repository_creation(self):
        def move_and_merge_directories(src: Path, dest: Path):
            """
            Moves the source directory into the destination directory.
            All files and subdirectories from src will be moved to dest.
            Existing files in dest will be overwritten.

            Parameters
            ----------
                src (str): Path to the source directory.
                dest (str): Path to the destination directory.
            """
            for item in src.iterdir():
                dest_item = dest / item.name
                if item.is_dir():
                    if dest_item.exists():
                        # Merge the subdirectory
                        move_and_merge_directories(item, dest_item)
                    else:
                        shutil.move(str(item), str(dest_item))  # Move the whole directory
                else:
                    # Move or overwrite the file
                    if dest_item.exists():
                        dest_item.unlink()  # Remove the existing file
                    shutil.move(str(item), str(dest_item))
            # Remove the source directory if it's empty
            src.rmdir()
            return

        with logger.sectioning("Repository Preparation"):
            _fileex.directory.delete_contents(
                path=self._path_head,
                exclude=[".git", ".github", "template", ".devcontainer"],
            )
            _fileex.directory.delete_contents(
                path=self._path_head / ".github",
                exclude=["workflows"],
            )
            _fileex.directory.delete_contents(
                path=self._path_head / ".devcontainer",
                exclude=["install.py", "build_conda.py", "build_python.py", "pre_commit.py"],
            )
            move_and_merge_directories(self._path_head / "template", self._path_head)
            self._git_head.commit(
                message=f"init: Create repository from PyPackIT template.",
                amend=True,
                stage="all",
            )
        main_manager, _ = self.run_cca(
            branch_manager=None,
            action=InitCheckAction.AMEND,
            future_versions={self.gh_context.event.repository.default_branch: "0.0.0"},
        )
        self.run_refactor(
            branch_manager=main_manager,
            action=InitCheckAction.AMEND,
            ref_range=None,
        )
        with logger.sectioning("Repository Update"):
            main_manager.git.push(force_with_lease=True)
        main_manager.repo.reset_labels()
        self.reporter.add(
            name="event",
            status="pass",
            summary="Repository created from RepoDynamics template.",
        )
        return

    def _run_init(self):
        user_input = self.head_commit_msg.footer
        init = user_input.initialize_project
        self.reporter.event("Project initialization" if init else "Repository initialization phase")
        version = user_input.version or PEP440SemVer(self.manager.changelog.current["version"])
        version_tag = self.manager.release.create_version_tag(version)
        self.manager.changelog.update_version(version_tag)
        self.manager.changelog.update_date()
        gh_draft = self.manager.release.github.get_or_make_draft(tag=version_tag)
        zenodo_draft, zenodo_sandbox_draft = self.manager.release.zenodo.get_or_make_drafts()

        if init:
            for changelog_key, do_publish in (
                ("github", user_input.publish_github),
                ("zenodo", user_input.publish_zenodo),
                ("zenodo_sandbox", user_input.publish_zenodo_sandbox),
            ):
                changelog_entry = (
                    self.manager.changelog.current.get(changelog_key, {})
                    if changelog_key != "zenodo_sandbox"
                    else self.manager.changelog.current.get("dev", {})
                )
                if do_publish is False:
                    changelog_entry.pop(changelog_key, None)
                else:
                    changelog_entry.pop("draft", None)
                    if changelog_key != "github":
                        self.manager.variable[changelog_key]["concept"]["draft"] = False
            self.manager.changelog.finalize(pre=False)

        hash_vars = self.manager.variable.commit_changes()
        hash_changelog = self.manager.changelog.commit_changes()
        new_manager, _ = self.run_cca(
            branch_manager=self.manager,
            action=InitCheckAction.COMMIT,
            future_versions={self.gh_context.ref_name: version},
        )
        new_manager.release.binder.set_image_tag(
            version=version_tag if init else version_tag.version, branch_type=BranchType.MAIN
        )
        new_manager.release.binder.commit_changes()
        self.jinja_env_vars["ccc"] = new_manager.data
        self.run_refactor(
            branch_manager=new_manager,
            action=InitCheckAction.COMMIT,
            ref_range=(
                self.gh_context.hash_before,
                hash_changelog or hash_vars or self.gh_context.hash_after,
            ),
        ) if new_manager.data["workflow.refactor.pre_commit_config"] else None
        gh_release_output = zenodo_output = zenodo_sandbox_output = None
        if init:
            if gh_draft:
                if self.head_commit_msg.footer.publish_github is False:
                    new_manager.release.github.delete_draft(release_id=gh_draft["id"])
                else:
                    gh_release_output = new_manager.release.github.update_draft(
                        tag=version_tag,
                        on_main=True,
                        publish=True,
                        release_id=gh_draft["id"],
                    )
            if zenodo_draft or zenodo_sandbox_draft:
                zenodo_output, zenodo_sandbox_output = new_manager.release.zenodo.update_drafts(
                    version=version,
                    publish_main=self.head_commit_msg.footer.publish_zenodo is not False,
                    publish_sandbox=self.head_commit_msg.footer.publish_zenodo_sandbox is not False,
                    id_main=zenodo_draft["id"] if zenodo_draft else None,
                    id_sandbox=zenodo_sandbox_draft["id"] if zenodo_sandbox_draft else None,
                )
            if self.head_commit_msg.footer.squash is not False:
                self._squash()
            else:
                new_manager.git.push()
            new_manager.release.tag_version(version=version)
        else:
            if gh_draft:
                gh_release_output = new_manager.release.github.update_draft(
                    tag=version_tag, on_main=True
                )
            if zenodo_draft or zenodo_sandbox_draft:
                zenodo_output, zenodo_sandbox_output = new_manager.release.zenodo.update_drafts(
                    version=version
                )
            new_manager.git.push()

        new_manager.repo.update_all(
            manager_before=self.manager, update_rulesets=init, reset_labels=True
        )
        self._output_manager.set(
            main_manager=new_manager,
            branch_manager=new_manager,
            version=version_tag if init else version_tag.version,
            website_deploy=True,
            package_lint=True,
            test_lint=True,
            package_test=True,
            package_build=True,
            binder_deploy=True,
            package_publish_testpypi=init
            and self.head_commit_msg.footer.publish_testpypi is not False,
            package_publish_pypi=init and self.head_commit_msg.footer.publish_pypi is not False,
            package_publish_anaconda=True,
            github_release_config=gh_release_output,
            zenodo_config=zenodo_output,
            zenodo_sandbox_config=zenodo_sandbox_output,
        )
        return

    def _squash(self):
        # Ref: https://blog.avneesh.tech/how-to-delete-all-commit-history-in-github
        #      https://stackoverflow.com/questions/55325930/git-how-to-squash-all-commits-on-master-branch
        self._git_base.checkout("temp", orphan=True)
        self._git_base.commit(
            message=f"{self.head_commit_msg.conv_msg.footerless.strip()}\n[skip ci]".strip()
        )
        self._git_base.branch_delete(self.gh_context.ref_name, force=True)
        self._git_base.branch_rename(self.gh_context.ref_name, force=True)
        self._git_base.push(target="origin", ref=self.gh_context.ref_name, force_with_lease=True)
        return

    def _run_branch_edited_fork(self):
        self.reporter.event("CI on fork")
        branch_manager = self.manager_from_metadata_file(repo="head")
        new_manager, job_runs, latest_hash = self.run_sync_fix(
            branch_manager=branch_manager,
            action=InitCheckAction.COMMIT,
        )
        website_deploy = False
        if self._has_admin_token:
            new_manager.repo.activate_gh_pages()
            if job_runs["web_build"]:
                website_deploy = True
            new_manager.repo.update_all(
                manager_before=branch_manager,
                update_rulesets=False,
            )
        self._output_manager.set(
            main_manager=new_manager,
            branch_manager=new_manager,
            website_deploy=website_deploy,
        )
        return

    def _run_branch_edited_main_normal(self):
        self.reporter.event("Push to main branch")
        new_manager, _ = self.run_cca(
            branch_manager=self.manager,
            action=InitCheckAction.COMMIT,
        )
        self.jinja_env_vars["ccc"] = new_manager.data
        self.run_refactor(
            branch_manager=new_manager,
            action=InitCheckAction.COMMIT,
            ref_range=(self.gh_context.hash_before, self.gh_context.hash_after),
        ) if new_manager.data["tool.pre-commit.config.file.content"] else None
        new_manager.git.push()
        new_manager.repo.update_all(manager_before=self.manager)
        self._output_manager.set(
            main_manager=new_manager,
            branch_manager=new_manager,
            version=new_manager.release.latest_version(),
            website_deploy=True,
            package_lint=True,
            test_lint=True,
            package_test=True,
            package_build=True,
        )
        return
