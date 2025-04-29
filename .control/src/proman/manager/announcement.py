from pathlib import Path


class AnnouncementManager:
    def read_announcement_file(self, base: bool, data: _ps.NestedDict) -> str | None:
        filepath = data["announcement.path"]
        if not filepath:
            return None
        path_root = self._path_base if base else self._path_head
        fullpath = path_root / filepath
        return fullpath.read_text() if fullpath.is_file() else None

    def write_announcement_file(self, announcement: str, base: bool, data: _ps.NestedDict) -> None:
        announcement_data = data["announcement"]
        if not announcement_data:
            return
        if announcement:
            announcement = f"{announcement.strip()}\n"
        path_root = self._path_base if base else self._path_head
        with open(path_root / announcement_data["path"], "w") as f:
            f.write(announcement)
        return

    def __init__(
        self,
        metadata_main: ControlCenterContentManager,
        context_manager: ContextManager,
        state_manager: StateManager,
        git: Git,
        path_root: str,
        logger: Logger | None = None,
    ):
        self._metadata = metadata_main
        self._context = context_manager
        self._state = state_manager
        self._git = git
        self._path_root = path_root
        self._logger = logger or Logger()

        self._path_announcement_file = Path(self._metadata["path"]["file"]["website_announcement"])
        return

    def update(self):
        name = "Website Announcement Manual Update"
        self.logger.h1(name)
        if not self.ref_is_main:
            self.add_summary(
                name=name,
                status="skip",
                oneliner="Announcement can only be updated from the main branch❗",
            )
            self.logger.warning("Announcement can only be updated from the main branch; skip❗")
            return
        announcement = self._website_announcement
        self.logger.input(f"Read announcement from workflow dispatch input: '{announcement}'")
        if not announcement:
            self.add_summary(
                name=name,
                status="skip",
                oneliner="No announcement was provided.",
            )
            self.logger.skip("No announcement was provided.")
            return
        old_announcement = self._read_web_announcement_file().strip()
        old_announcement_details = self._git.log(
            number=1,
            simplify_by_decoration=False,
            pretty=None,
            date=None,
            paths=self._metadata["path"]["file"]["website_announcement"],
        )
        old_md = md.code_block(old_announcement_details)

        if announcement == "null":
            announcement = ""

        if announcement.strip() == old_announcement.strip():
            details_list = ["❎ No changes were made."]
            if not announcement:
                oneliner = "No announcement to remove❗"
                details_list.extend(
                    [
                        "🚫 The 'null' string was passed to delete the current announcement, "
                        "but the announcement file is already empty.",
                        html.details(content=old_md, summary="📝 Last Removal Commit Details"),
                    ]
                )
            else:
                oneliner = "The provided announcement was identical to the existing announcement❗"
                details_list.extend(
                    [
                        "🚫 The provided announcement was the same as the existing one.",
                        html.details(
                            content=old_md, summary="📝 Current Announcement Commit Details"
                        ),
                    ]
                )
            self.add_summary(
                name=name, status="skip", oneliner=oneliner, details=html.ul(details_list)
            )
            return
        self._write(announcement)
        new_html = html.details(
            content=md.code_block(announcement, "html"),
            summary="📣 New Announcement",
        )
        details_list = []
        if not announcement:
            oneliner = "Announcement was manually removed 🗑"
            details_list.extend(
                [
                    "✅ The announcement was manually removed.",
                    html.details(content=old_md, summary="📝 Removed Announcement Details"),
                ]
            )
            commit_title = "Manually remove announcement"
            commit_body = f"Removed announcement:\n\n{old_announcement}"
        elif not old_announcement:
            oneliner = "A new announcement was manually added 📣"
            details_list.extend(["✅ A new announcement was manually added.", new_html])
            commit_title = "Manually add new announcement"
            commit_body = announcement
        else:
            oneliner = "Announcement was manually updated 📝"
            details_list.extend(
                [
                    "✅ The announcement was manually updated.",
                    new_html,
                    html.details(content=old_md, summary="📝 Old Announcement Details"),
                ]
            )
            commit_title = "Manually update announcement"
            commit_body = f"New announcement:\n\n{announcement}\n\nRemoved announcement:\n\n{old_announcement}"

        commit_hash, commit_url = self._commit(
            commit_title=commit_title,
            commit_body=commit_body,
            change_title=commit_title,
            change_body=commit_body,
        )
        details_list.append(f"✅ Changes were applied (commit {html.a(commit_url, commit_hash)}).")
        self.add_summary(name=name, status="pass", oneliner=oneliner, details=html.ul(details_list))
        return

    def _commit(
        self,
        commit_title: str,
        commit_body: str,
        change_title: str,
        change_body: str,
    ):
        changelog_id = self._metadata["commit"]["primary"]["website"]["announcement"].get(
            "changelog_id"
        )
        if changelog_id:
            changelog_manager = ChangelogManager(
                changelog_metadata=self._metadata["changelog"],
                ver_dist=f"{self.last_ver}+{self.dist_ver}",
                commit_type=self._metadata["commit"]["primary"]["website"]["type"],
                commit_title=commit_title,
                parent_commit_hash=self._state.hash_latest,
                parent_commit_url=str(self.gh_link.commit(self.hash_after)),
                path_root=self._path_root_self,
                logger=self._logger,
            )
            changelog_manager.add_change(
                changelog_id=changelog_id,
                section_id=self._metadata["commit"]["primary"]["website"]["announcement"][
                    "changelog_section_id"
                ],
                change_title=change_title,
                change_details=change_body,
            )
            changelog_manager.write_all_changelogs()
        commit = CommitMsg(
            typ=self._metadata["commit"]["primary"]["website"]["type"],
            title=commit_title,
            body=commit_body,
            scope=self._metadata["commit"]["primary"]["website"]["announcement"]["scope"],
        )
        commit_hash = self.commit(message=str(commit), stage="all")
        commit_link = str(self.gh_link.commit(commit_hash))
        self._hash_latest = commit_hash
        return commit_hash, commit_link
