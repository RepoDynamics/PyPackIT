import re

import conventional_commits.message
import pyshellman
from github_contexts.github.payload.schedule import SchedulePayload

from proman.dtype import InitCheckAction
from proman.main import EventHandler


class ScheduleEventHandler(EventHandler):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._payload: SchedulePayload = self.gh_context.event
        return

    def _run_event(self):
        cron = self._payload.schedule
        for schedule_id, schedule in self._data_main["workflow"]["schedule"].items():
            if schedule["cron"] == cron:
                break
        else:
            self.reporter.update_event_summary("Unknown scheduled workflow")
            self.reporter.update(
                "event",
                status="fail",
                summary="Unknown cron expression for scheduled workflow.",
                body=[
                    f"The cron expression `{cron}` is not defined.",
                    "Valid cron expressions defined in `$.workflow.schedule` are:",
                    "\n".join(
                        [
                            f"- `{schedule['cron']}`"
                            for schedule in self._data_main["workflow"]["schedule"].values()
                        ]
                    ),
                ],
            )
            return
        self.reporter.update_event_summary(f"Scheduled workflow `{schedule_id}`")
        job = schedule["job"]
        for branch_name in self._get_target_branches(schedule):
            self._git_base.checkout(branch=branch_name)
            commit_hashes = []
            if "sync" in job:
                self._data_branch_before = self.manager_from_metadata_file(base=True)
                cc_manager = self.get_cc_manager(base=True)
                commit_hash = self.run_cca(
                    action=InitCheckAction(job["sync"]["action"]),
                    cc_manager=cc_manager,
                    base=True,
                )
                commit_hashes.append(commit_hash)
                self._data_branch = cc_manager.generate_data()
            else:
                self._data_branch = self.manager_from_metadata_file(base=True)
            if "announcement_expiry" in job:
                pass
            if "refactor" in job:
                commit_hash = self.run_refactor(
                    action=InitCheckAction(job["refactor"]["action"]),
                    branch_manager=self._data_branch,
                    base=True,
                )
                commit_hashes.append(commit_hash)
            if any(commit_hashes):
                self._git_base.push()
            latest_hash = self._git_base.commit_hash_normal()
            if "website" in job:
                self._output_manager._set_web()

            self._output_manager.set(
                data_branch=self._data_branch,
                ref=latest_hash or sha,
                ref_before=sha,
                version=self._get_latest_version(base=False),
                website_url=self._data_main["url"]["website"]["base"],
                website_build=True,
                package_lint=True,
                package_test=True,
                package_test_source="PyPI",
                package_build=True,
            )

        return

    def _get_target_branches(self, schedule: dict):
        types = schedule.get("branch_types")
        regex = re.compile(schedule["branch_regex"]) if "branch_regex" in schedule else None
        target_branches = []
        for branch_data in self._gh_api.branches:
            branch_name = branch_data["name"]
            branch = self.resolve_branch(branch_name=branch_name)
            if types and branch.type.value not in types:
                continue
            if regex and not regex.match(branch_name):
                continue
            target_branches.append(branch_name)
        self._git_base.fetch_remote_branches_by_name(branch_names=target_branches)
        return target_branches

    def _web_announcement_expiry_check(self) -> str | None:
        name = "Website Announcement Expiry Check"
        current_announcement = self.read_announcement_file(base=False, data=self._data_main)
        if current_announcement is None:
            self.add_summary(
                name=name,
                status="skip",
                oneliner="Announcement file does not exist❗",
                details=html.ul(
                    [
                        "❎ No changes were made.",
                        "🚫 The announcement file was not found.",
                    ]
                ),
            )
            return None
        (commit_date_relative, commit_date_absolute, commit_date_epoch, commit_details) = (
            self._git_head.log(
                number=1,
                simplify_by_decoration=False,
                pretty=pretty,
                date=date,
                paths=self._data_main["path"]["file"]["website_announcement"],
            )
            for pretty, date in (
                ("format:%cd", "relative"),
                ("format:%cd", None),
                ("format:%cd", "unix"),
                (None, None),
            )
        )
        if not current_announcement:
            last_commit_details_html = html.details(
                content=md.code_block(commit_details),
                summary="📝 Removal Commit Details",
            )
            self.add_summary(
                name=name,
                status="skip",
                oneliner="📭 No announcement to check.",
                details=html.ul(
                    [
                        "❎ No changes were made.📭 The announcement file is empty.\n",
                        f"📅 The last announcement was removed {commit_date_relative} on {commit_date_absolute}.\n",
                        last_commit_details_html,
                    ]
                ),
            )
            return None
        current_date_epoch = int(pyshellman.run(["date", "-u", "+%s"]).output)
        elapsed_seconds = current_date_epoch - int(commit_date_epoch)
        elapsed_days = elapsed_seconds / (24 * 60 * 60)
        retention_days = self._data_main.web["announcement_retention_days"]
        retention_seconds = retention_days * 24 * 60 * 60
        remaining_seconds = retention_seconds - elapsed_seconds
        remaining_days = retention_days - elapsed_days
        if remaining_seconds > 0:
            current_announcement_html = html.details(
                content=md.code_block(current_announcement, "html"),
                summary="📣 Current Announcement",
            )
            last_commit_details_html = html.details(
                content=md.code_block(commit_details),
                summary="📝 Current Announcement Commit Details",
            )
            self.add_summary(
                name=name,
                status="skip",
                oneliner=f"📬 Announcement is still valid for another {remaining_days:.2f} days.",
                details=html.ul(
                    [
                        "❎ No changes were made.",
                        "📬 Announcement is still valid.",
                        f"⏳️ Elapsed Time: {elapsed_days:.2f} days ({elapsed_seconds} seconds)",
                        f"⏳️ Retention Period: {retention_days} days ({retention_seconds} seconds)",
                        f"⏳️ Remaining Time: {remaining_days:.2f} days ({remaining_seconds} seconds)",
                        current_announcement_html,
                        last_commit_details_html,
                    ]
                ),
            )
            return None
        # Remove the expired announcement
        removed_announcement_html = html.details(
            content=md.code_block(current_announcement, "html"),
            summary="📣 Removed Announcement",
        )
        last_commit_details_html = html.details(
            content=md.code_block(commit_details),
            summary="📝 Removed Announcement Commit Details",
        )
        self.write_announcement_file(announcement="", base=False, data=self._data_main)
        commit_msg = conventional_commits.message.create(
            typ=self._data_main["commit"]["secondary_action"]["auto-update"]["type"],
            description="Remove expired website announcement",
            body=(
                f"The following announcement made {commit_date_relative} on {commit_date_absolute} "
                f"was expired after {elapsed_days:.2f} days and thus automatically removed:\n\n"
                f"{current_announcement}"
            ),
            scope="web-announcement",
        )
        commit_hash = self._git_head.commit(message=str(commit_msg), stage="all")
        commit_link = str(self._gh_link.commit(commit_hash))
        self.add_summary(
            name=name,
            status="pass",
            oneliner="🗑 Announcement was expired and thus removed.",
            details=html.ul(
                [
                    f"✅ The announcement was removed (commit {html.a(commit_link, commit_hash)}).",
                    f"⌛ The announcement had expired {abs(remaining_days):.2f} days ({abs(remaining_seconds)} seconds) ago.",
                    f"⏳️ Elapsed Time: {elapsed_days:.2f} days ({elapsed_seconds} seconds)",
                    f"⏳️ Retention Period: {retention_days} days ({retention_seconds} seconds)",
                    removed_announcement_html,
                    last_commit_details_html,
                ]
            ),
        )
        return commit_hash
