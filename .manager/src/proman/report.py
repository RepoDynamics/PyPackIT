import functools
import io
from typing import Literal

import htmp
import mdit
import pyserials as ps
from github_contexts import github as _gh_context
from loggerman import logger, style
from mdit.target.rich import (
    HeadingConfig,
    InlineHeadingConfig,
    PanelConfig,
    RuleConfig,
    StyleConfig,
)
from rich.text import Text

from proman.dtype import _TitledEmoji
from proman.exception import ProManException

EMOJI = {
    "pass": _TitledEmoji("Passed", "✅"),
    "skip": _TitledEmoji("Skipped", "⏭️"),
    "fail": _TitledEmoji("Failed", "❌"),
    "warning": _TitledEmoji("Passed with Warning", "⚠️"),
}


class Reporter:
    _process_name = {
        "main": "Main",
        "event": "Event",
        "file_change": "File Changes",
        "cca": "CCA",
        "hooks": "Hooks",
    }

    def __init__(self, github_context: _gh_context.GitHubContext | None = None):
        self._summary_table: dict[str, SummaryTableEntry] = {}
        self._sections: dict[str, Section] = {}
        self._generate_event_context(github_context=github_context)
        return

    def update(
        self,
        process_id: str,
        status: Literal["pass", "fail", "skip", "warning"] | None = None,
        summary: str | None = None,
        body=None,
        section=None,
        section_is_container: bool = False,
    ) -> None:
        """Update the entry for a given process ID.

        Parameters
        ----------
        process_id
            ID of the process to update.
        status
            Status to set for the process. If None, the status will not be updated.
        summary
            Summary to add for the process. If None, the summary will not be updated.
        body
            Body content to add to the section. If None, the body will not be updated.
        section
            Section content to add to the section. If None, the section will not be updated.
        section_is_container
            Whether the section is a container or not. Default is False.
        """
        self.update_summary(process_id=process_id, status=status, summary=summary)
        self.update_section(
            process_id=process_id,
            body=body,
            section=section,
            section_is_container=section_is_container,
        )
        return

    def update_summary(
        self,
        process_id: str,
        status: Literal["pass", "fail", "skip", "warning"] | None = None,
        summary: str | None = None,
    ) -> None:
        """Update the summary table entry for a given process ID.

        Parameters
        ----------
        process_id
            ID of the process to update.
        status
            Status to set for the process. If None, the status will not be updated.
        summary
            Summary to add for the process. If None, the summary will not be updated.
        """
        self._summary_table.setdefault(
            process_id,
            SummaryTableEntry(self._process_name[process_id]),
        ).update(status=status, summary=summary)
        return

    def update_section(
        self,
        process_id: str,
        body=None,
        section=None,
        section_is_container: bool = False,
    ) -> None:
        """Update the section entry for a given process ID.

        Parameters
        ----------
        process_id
            ID of the process to update.
        body
            Body content to add to the section. If None, the body will not be updated.
        section
            Section content to add to the section. If None, the section will not be updated.
        section_is_container
            Whether the section is a container or not. Default is False.
        """
        self._sections.setdefault(
            process_id,
            Section(self._process_name[process_id]),
        ).update(body=body, section=section, section_is_container=section_is_container)
        return

    def update_event_summary(
        self,
        summary: str | None = None,
        status: Literal["pass", "fail", "skip", "warning"] | None = None,
    ):
        """Update the event summary.

        Parameters
        ----------
        status
            Status to set for the event. If None, the status will not be updated.
        summary
            Summary to add for the event. If None, the summary will not be updated.
        """
        self.update_summary(process_id="event", status=status, summary=summary)
        return

    def error_unsupported_triggering_action(self):
        action_err_msg = f"Unsupported triggering action for event type."
        self.update(
            "main",
            status="fail",
            summary=action_err_msg,
        )
        raise ProManException()

    @staticmethod
    def api_response_code_block(response_data, api_name: str = "GitHub") -> mdit.element.CodeBlock:
        return mdit.element.code_block(
            ps.write.to_yaml_string(response_data),
            language="yaml",
            caption=f"{api_name} API Response",
        )

    @property
    def failed(self) -> bool:
        """Check if any of the processes failed."""
        return any(entry.status == "fail" for entry in self._summary.values())

    def generate(self, gha: bool = False) -> str:
        body = mdit.block_container(*self._generate_summary())
        section = {section_id: section.document for section_id, section in self._sections.items()}
        target_config, output = make_sphinx_target_config()
        report = mdit.document(
            heading="Workflow Summary",
            body=body,
            section=section,
            target_configs_md={"sphinx": target_config},
        )
        if gha:
            return report.source(
                target="github", filters=["short, github"], separate_sections=False
            )
        full_summary = report.render(target="sphinx", filters=["full"], separate_sections=False)
        logger.info(
            "Report Generation Logs",
            mdit.element.rich(Text.from_ansi(output.getvalue())),
        )
        return full_summary

    def _generate_summary(self) -> tuple[mdit.element.InlineImage, mdit.element.Table]:
        failed = False
        warning = False
        skipped = False
        table_rows = [["Process", "Status", "Summary"]]
        for pipeline in self._summary_table.values():
            status = pipeline.current_status
            if status == "fail":
                failed = True
            elif status == "warning":
                warning = True
            elif status == "skip":
                skipped = True
            table_rows.append(pipeline.row)
        table = mdit.element.table(
            rows=table_rows,
            num_rows_header=1,
            align_table="center",
        )
        if failed:
            workflow_status = "fail"
            color = "rgb(200, 0, 0)"
        elif warning:
            workflow_status = "warning"
            color = "rgb(255, 200, 0)"
        elif skipped:
            workflow_status = "skip"
            color = "rgb(0, 0, 200)"
        else:
            workflow_status = "pass"
            color = "rgb(0, 200, 0)"
        workflow_status_emoji = EMOJI[workflow_status]
        status_badge = mdit.element.badge(
            service="static",
            args={"message": workflow_status_emoji.title},
            label="Status",
            style="for-the-badge",
            color=color,
            align="center",
        )
        return status_badge, table

    def _generate_event_context(
        self, github_context: _gh_context.GitHubContext | None = None
    ) -> None:
        if github_context:
            body = []
            event_type = github_context.event_name.value
            if hasattr(github_context, "action"):
                event_type += f" {github_context.event.action.value}"
            field_list = mdit.element.field_list(
                [
                    ("Event Type", event_type),
                    ("Ref Type", github_context.ref_type.value),
                    ("Ref", github_context.ref),
                    ("SHA", github_context.sha),
                    ("Actor", github_context.actor),
                    ("Triggering Actor", github_context.triggering_actor),
                    ("Run ID", github_context.run_id),
                    ("Run Number", github_context.run_number),
                    ("Run Attempt", github_context.run_attempt),
                    ("Workflow Ref", github_context.workflow_ref),
                ]
            )
            logger.info("Context Summary", field_list)
            dropdown = mdit.element.admonition(
                title="Context Summary",
                body=field_list,
                dropdown=True,
                opened=True,
                emoji="🎬",
            )
            body.append(dropdown)
            for data, summary, icon in (
                (github_context, "GitHub Context", "🎬"),
                (github_context.event, "Event Payload", "📥"),
            ):
                code = mdit.element.code_block(
                    ps.write.to_yaml_string(data.as_dict), language="yaml"
                )
                dropdown = mdit.element.dropdown(
                    title=summary,
                    body=code,
                    color="info",
                    icon=icon,
                )
                body.append((dropdown, "full"))
            self.update_section(
                "event",
                body=body,
            )
        return


class SummaryTableEntry:
    _status_weight = {
        None: 0,
        "skip": 1,
        "pass": 2,
        "warning": 3,
        "fail": 4,
    }
    _status_log_level = {
        None: "info",
        "skip": "debug",
        "pass": "success",
        "warning": "warning",
        "fail": "error",
    }

    def __init__(
        self,
        name: str,
        status: Literal["skip", "pass", "warning", "fail"] | None = None,
        summary: str | None = None,
    ):
        self._name = name
        self._status = None
        self._summary = []
        self.update(
            status=status,
            summary=summary,
        )
        return

    def update(
        self, status: Literal["skip", "pass", "warning", "fail"] | None = None, summary: str = ""
    ):
        if self._status_weight[status] >= self._status_weight[self._status]:
            self._status = status
        if summary:
            self._summary.append(summary)
        logger.log(
            self._status_log_level[status],
            self._name,
            summary,
        )
        return

    @property
    def current_status(self) -> Literal["skip", "pass", "warning", "fail"]:
        """Get the current status of the entry.

        This will return 'pass' if the status is None.
        """
        return self._status or "pass"

    @property
    def row(self) -> list[str]:
        status_emoji = EMOJI[self.current_status]
        return [
            self._name,
            htmp.element.span(status_emoji.emoji, title=status_emoji.title),
            " ".join(self._summary),
        ]


class Section:
    def __init__(self, name: str, body=None, section=None, section_is_container: bool = False):
        self._name = name
        self._body = mdit.block_container()
        self._section = mdit.section_container()
        self.update(
            body=body,
            section=section,
            section_is_container=section_is_container,
        )
        return

    def update(
        self,
        body=None,
        section=None,
        section_is_container: bool = False,
    ) -> None:
        if body:
            self._body.extend(body)
        if section:
            if section_is_container:
                for content, conditions in section.values():
                    self._section.append(content, conditions=conditions)
            else:
                self._section.extend(section)
        return

    @property
    def document(self) -> mdit.Document:
        return mdit.document(
            heading=self._name,
            body=self._body,
            section=self._section,
        )


def initialize_logger(
    title_number: int | list[int] = 1,
):
    logger.initialize(
        realtime_levels=list(range(7)),
        github_debug=True,
        title_number=title_number,
        level_style_debug=style.log_level(
            color="muted",
            icon="🔘",
            rich_config=PanelConfig(
                title_style=StyleConfig(color=(200, 255, 255), bold=True),
            ),
        ),
        level_style_success=style.log_level(
            color="success",
            icon="✅",
            rich_config=PanelConfig(
                title_style=StyleConfig(color=(0, 250, 0), bold=True),
            ),
        ),
        level_style_info=style.log_level(
            color="info",
            icon="ℹ️",
            rich_config=PanelConfig(
                title_style=StyleConfig(color=(0, 200, 255), bold=True),
            ),
        ),
        level_style_notice=style.log_level(
            color="warning",
            icon="⚠️",
            rich_config=PanelConfig(
                title_style=StyleConfig(color=(255, 230, 0), bold=True),
            ),
        ),
        level_style_warning=style.log_level(
            color="warning",
            icon="🚨",
            rich_config=PanelConfig(
                title_style=StyleConfig(color=(255, 185, 0), bold=True),
            ),
        ),
        level_style_error=style.log_level(
            color="danger",
            icon="🚫",
            rich_config=PanelConfig(
                title_style=StyleConfig(color=(255, 100, 50), bold=True),
            ),
        ),
        level_style_critical=style.log_level(
            color="danger",
            opened=True,
            icon="⛔",
            rich_config=PanelConfig(
                title_style=StyleConfig(color=(255, 30, 30), bold=True),
            ),
        ),
        target_configs_rich={
            "console": mdit.target.console(
                heading=(
                    HeadingConfig(
                        inline=InlineHeadingConfig(
                            style=StyleConfig(color=(255, 200, 255), bold=True),
                            rule=RuleConfig(style=StyleConfig(color=(250, 250, 230))),
                        )
                    ),
                    HeadingConfig(
                        inline=InlineHeadingConfig(
                            style=StyleConfig(color=(235, 160, 255), bold=True),
                            rule=RuleConfig(style=StyleConfig(color=(220, 220, 200))),
                        )
                    ),
                    HeadingConfig(
                        inline=InlineHeadingConfig(
                            style=StyleConfig(color=(215, 120, 255), bold=True),
                            rule=RuleConfig(style=StyleConfig(color=(190, 190, 170))),
                        )
                    ),
                    HeadingConfig(
                        inline=InlineHeadingConfig(
                            style=StyleConfig(color=(195, 80, 255), bold=True),
                            rule=RuleConfig(style=StyleConfig(color=(160, 160, 140))),
                        )
                    ),
                    HeadingConfig(
                        inline=InlineHeadingConfig(
                            style=StyleConfig(color=(175, 40, 255), bold=True),
                            rule=RuleConfig(style=StyleConfig(color=(130, 130, 110))),
                        )
                    ),
                    HeadingConfig(
                        inline=InlineHeadingConfig(
                            style=StyleConfig(color=(155, 0, 255), bold=True),
                            rule=RuleConfig(style=StyleConfig(color=(100, 100, 80))),
                        )
                    ),
                )
            )
        },
    )


def make_sphinx_target_config():
    output = io.StringIO()
    target_config = mdit.target.sphinx(
        renderer=functools.partial(
            mdit.render.sphinx,
            status=output,
            warning=output,
            config={
                "extensions": [
                    "myst_nb",
                    "sphinx_design",
                    "sphinx_togglebutton",
                    "sphinx_copybutton",
                    "sphinxcontrib.mermaid",
                    "sphinx_tippy",
                ],
                "myst_enable_extensions": [
                    "amsmath",
                    "attrs_inline",
                    "colon_fence",
                    "deflist",
                    "dollarmath",
                    "fieldlist",
                    "html_admonition",
                    "html_image",
                    "linkify",
                    "replacements",
                    "smartquotes",
                    "strikethrough",
                    "substitution",
                    "tasklist",
                ],
                "html_theme": "pydata_sphinx_theme",
                "html_theme_options": {
                    "pygments_light_style": "default",
                    "pygments_dark_style": "monokai",
                },
                "html_title": "ProMan Report",
            },
        )
    )
    return target_config, output
