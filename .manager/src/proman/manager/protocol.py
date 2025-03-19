from __future__ import annotations

import re
from typing import TYPE_CHECKING

import mdit
import pyserials as ps
from loggerman import logger

from proman.dstruct import MainTasklistEntry, SubTasklistEntry, Tasklist
from proman.dtype import IssueStatus, LabelType
from proman.exception import ProManException

if TYPE_CHECKING:
    from collections.abc import Sequence
    from typing import Literal

    from github_contexts.github.payload.object.issue import Issue
    from github_contexts.github.payload.object.pull_request import PullRequest

    from proman.dstruct import IssueForm, Label
    from proman.manager import Manager


class ProtocolManager:
    def __init__(self, manager: Manager):
        self._manager = manager
        self._protocol = ""
        self._protocol_comment_id = None
        self._protocol_issue_nr = None
        self._protocol_pull_nr = None
        self._config: dict = {}
        self._protocol_data: dict[str, str] = {}
        self._protocol_config: dict = {}
        self._issue_inputs: dict = {}
        self._tasklist: Tasklist | None = None
        self._env_vars: dict = {"config": self._protocol_config, "input": self._issue_inputs}
        self._type: Literal["Issue", "Pull Request"] = "Issue"
        return

    @property
    def config(self) -> dict:
        config_resolved = self._manager.fill_jinja_templates(
            self._protocol_config,
            jsonpath="protocol.config",
            env_vars=self._env_vars | {"data": self._protocol_data},
        )
        return config_resolved

    @property
    def data(self) -> dict:
        return self._protocol_data

    @property
    def input(self) -> dict:
        return self._issue_inputs

    @property
    def tasklist(self) -> Tasklist:
        return self._tasklist

    def add_event(self, env_vars: dict | None = None):
        for data_id, data in self._config.get("data", {}).items():
            if "template" in data:
                template_resolved = self._resolve_to_str(
                    data["template"], jsonpath=f"issue.protocol.data.{data_id}", env_vars=env_vars
                )
                existing_data = self._protocol_data[data_id]
                self._protocol_data[data_id] = (
                    f"{existing_data}{template_resolved}"
                    if data["template_type"] == "append"
                    else f"{template_resolved}{existing_data}"
                )
        return

    def add_env_var(
        self,
        status_label: Label | None = None,
        pull_requests: list[dict] | None = None,
    ):
        env_vars = {
            key: value for key, value in locals().items() if key != "self" and value is not None
        }
        self._env_vars.update(env_vars)
        return

    def update_on_github(self):
        protocol = self.generate()
        if self._protocol_issue_nr:
            return self._manager.gh_api_actions.issue_update(
                number=self._protocol_issue_nr, body=protocol
            )
        if self._protocol_pull_nr:
            return self._manager.gh_api_actions.pull_update(
                number=self._protocol_pull_nr, body=protocol
            )
        return self._manager.gh_api_actions.issue_comment_update(
            comment_id=self._protocol_comment_id, body=protocol
        )

    def generate(self) -> str:
        def make_config() -> str:
            config_str = ps.write.to_yaml_string(self._protocol_config).strip()
            return self._wrap_in_markers(config_str, self._config["config"])

        def make_inputs() -> str:
            if not self._issue_inputs:
                return ""
            inputs = ps.write.to_yaml_string(self._issue_inputs).strip()
            return self._wrap_in_markers(inputs, self._config["inputs"])

        def make_data() -> dict:
            return {
                element_id: self._wrap_in_markers(element_data, self._config["data"][element_id])
                for element_id, element_data in self._protocol_data.items()
            }

        def make_tasklist() -> str:
            """Write an implementation tasklist as Markdown string
            and update it in the protocol.

            Parameters
            ----------
            tasklist
                A list of dictionaries, each representing a tasklist entry.
                The format of each dictionary is the same as that returned by
                `_extract_tasklist_entries`.
            """

            def write(entry_list: Sequence[MainTasklistEntry | SubTasklistEntry], level=0):
                for entry in entry_list:
                    check = "X" if entry.complete else " "
                    string.append(f"{' ' * level * 2}- [{check}] {entry.summary.strip()}")
                    if entry.body:
                        for line in entry.body.splitlines():
                            string.append(f"{' ' * (level + 1) * 2}{line}")
                    write(entry.subtasks, level + 1)
                return

            if not self._tasklist:
                return self._env_vars.get("tasklist", "")
            string = []
            write(self._tasklist.tasks)
            return self._wrap_in_markers(
                "\n".join(string).strip(),
                marker=self._config["tasklist"],
            )

        output = self._resolve_to_str(
            self._config["template"],
            jsonpath="issue.protocol.template",
            env_vars={
                "config": make_config(),
                "data": make_data(),
                "inputs": make_inputs(),
                "tasklist": make_tasklist(),
            },
        )
        return output

    def initialize_issue(
        self, issue: Issue, issue_form: IssueForm
    ) -> tuple[dict, str, list[Label]]:
        self._config = self._manager.data["issue.protocol"]
        self._issue_inputs.update(self._extract_issue_ticket_inputs(issue.body, issue_form.body))
        labels, status_label = self._make_auto_labels_from_issue_ticket_inputs(
            issue_form=issue_form
        )
        self._env_vars.update(
            {
                "form": issue_form,
                "labels": labels,
                "status_label": status_label,
            }
        )
        self._protocol_config.update(self._config["config"].get("default", {}))
        for data_id, data in self._config.get("data", {}).items():
            self._protocol_data[data_id] = self._resolve_to_str(
                data["value"], jsonpath=f"issue.protocol.data.{data_id}"
            )
        self.add_event(env_vars={"action": "opened"})
        for assignee in issue_form.issue_assignees:
            self.add_event(env_vars={"action": "assigned", "assignee": assignee})
        all_labels = [label for label_list in labels.values() for label in label_list] + [
            status_label
        ]
        for label in all_labels:
            self.add_event(env_vars={"action": "labeled", "label": label})

        # if issue_form.processed_body:
        #     body_processed = self._generate(
        #         template=issue_form.processed_body,
        #         issue_form=issue_form,
        #         issue_inputs=issue_entries,
        #         issue_body=issue.body
        #     )
        # else:
        #     logger.info("Issue Post Processing", "No post-process action defined in issue form.")
        #     body_processed = issue.body
        # self.protocol = self._generate(
        #     template=self._manager.data["doc.protocol.template"],
        #     issue_form=issue_form,
        #     issue_inputs=issue_entries,
        #     issue_body=body_processed,
        # )
        body_processed = ""
        return self._issue_inputs, body_processed, all_labels

    def initialize_pull(self, pull: dict, issue: Issue, issue_form: IssueForm, labels: list[Label]):
        self._type = "Pull Request"
        self._protocol_pull_nr = pull["number"]
        self._config = self._manager.data["pull.protocol"]
        labels_env = {}
        status_label = None
        for label in labels:
            if label.category is LabelType.STATUS:
                status_label = label
            else:
                labels_env.setdefault(label.category.value, []).append(label)
        tasklist_str = self._resolve_to_str(
            self._config["tasklist"]["value"], jsonpath="pull.protocol.tasklist.value"
        )
        self._env_vars.update(
            {
                "event": "pull_request",
                "action": "opened",
                "form": issue_form,
                "pull_request": pull,
                "issue": issue,
                "labels": labels_env,
                "status_label": status_label,
                "tasklist": self._wrap_in_markers(tasklist_str, marker=self._config["tasklist"]),
            }
        )
        self._protocol_config.update(self._config["config"].get("default", {}))
        for data_id, data in self._config.get("data", {}).items():
            self._protocol_data[data_id] = self._resolve_to_str(
                data["value"], jsonpath=f"pull.protocol.data.{data_id}"
            )
        self.add_event(env_vars={"action": "opened"})
        for assignee in issue_form.pull_assignees:
            self.add_event(env_vars={"action": "assigned", "assignee": assignee})
        for label in labels:
            self.add_event(env_vars={"action": "labeled", "label": label})
        return

    def load_from_issue(
        self, issue: Issue, issue_form: IssueForm, labels: dict[LabelType, list[Label]]
    ):
        self._config = self._manager.data["issue.protocol"]
        self._env_vars.update({"form": issue_form})
        self._add_labels_env_var(labels)
        if self._config["as_comment"]:
            comments = self._manager.gh_api_actions.issue_comments(
                number=issue.number, max_count=10
            )
            protocol_comment = comments[0]
            self._protocol_comment_id = protocol_comment.get("id")
            protocol = protocol_comment.get("body")
        else:
            protocol = issue.body
            self._protocol_issue_nr = issue.number
        logger.info(
            "Issue Protocol Load",
            mdit.element.code_block(protocol, language="markdown", caption="Protocol"),
        )
        self._issue_inputs.update(self._extract_yaml(protocol, marker=self._config["inputs"]))
        self._protocol_config.update(self._extract_yaml(protocol, marker=self._config["config"]))
        for data_id, data in self._config.get("data", {}).items():
            self._protocol_data[data_id] = self._extract_marker_wrapped(text=protocol, marker=data)
        return

    def load_from_pull(self, pull: PullRequest) -> str:
        self._protocol_pull_nr = pull.number
        protocol = pull.body
        return

    def _resolve_to_str(
        self, value: str | dict | list, jsonpath: str, env_vars: dict | None = None
    ):
        env_vars = env_vars or {}
        value_filled = self._manager.fill_jinja_templates(
            value, jsonpath=jsonpath, env_vars=self._env_vars | env_vars
        )
        if isinstance(value, str):
            return value_filled
        return mdit.generate(value_filled).source(target="github")

    def _extract_yaml(self, protocol: str, marker: dict) -> dict:
        yaml_str = self._extract_marker_wrapped(text=protocol, marker=marker)
        return ps.read.yaml_from_string(yaml_str)

    def _extract_tasklist(self, protocol: str) -> Tasklist | None:
        """
        Extract the implementation tasklist from the pull request body.

        Returns
        -------
        A list of dictionaries, each representing a tasklist entry.
        Each dictionary has the following keys:
        - complete : bool
            Whether the task is complete.
        - summary : str
            The summary of the task.
        - description : str
            The description of the task.
        - sublist : list[dict[str, bool | str | list]]
            A list of dictionaries, each representing a subtask entry, if any.
            Each dictionary has the same keys as the parent dictionary.
        """
        log_title = "Tasklist Extraction"

        def extract(
            tasklist_string: str, level: int = 0
        ) -> list[MainTasklistEntry] | list[SubTasklistEntry]:
            # Regular expression pattern to match each task item
            task_pattern = rf"{' ' * level * 2}- \[(X| )\] (.+?)(?=\n{' ' * level * 2}- \[|\Z)"
            # Find all matches
            matches = re.findall(task_pattern, tasklist_string, flags=re.DOTALL)
            # Process each match into the required dictionary format
            tasklist_entries = []
            for match in matches:
                complete, summary_and_desc = match
                summary_and_body_split = summary_and_desc.split("\n", 1)
                summary = summary_and_body_split[0].strip()
                body = summary_and_body_split[1] if len(summary_and_body_split) > 1 else ""
                if body:
                    sublist_pattern = r"^( *- \[(?:X| )\])"
                    parts = re.split(sublist_pattern, body, maxsplit=1, flags=re.MULTILINE)
                    body = parts[0]
                    if len(parts) > 1:
                        sublist_str = "".join(parts[1:])
                        sublist = extract(sublist_str, level + 1)
                    else:
                        sublist = []
                else:
                    sublist = []
                body = "\n".join(
                    [line.removeprefix(" " * (level + 1) * 2) for line in body.splitlines()]
                )
                task_is_complete = complete or (
                    sublist and all(subtask.complete for subtask in sublist)
                )
                if level == 0:
                    conv_msg = self._manager.commit.create_from_msg(summary)
                    tasklist_entries.append(
                        MainTasklistEntry(
                            commit=conv_msg,
                            body=body.rstrip(),
                            complete=task_is_complete,
                            subtasks=tuple(sublist),
                        )
                    )
                else:
                    tasklist_entries.append(
                        SubTasklistEntry(
                            description=summary.strip(),
                            body=body.rstrip(),
                            complete=task_is_complete,
                            subtasks=tuple(sublist),
                        )
                    )
            return tasklist_entries

        tasklist_str = self._extract_marker_wrapped(
            text=protocol, marker=self._config["tasklist"]
        ).strip()
        body_md = mdit.element.code_block(protocol, language="markdown", caption="Protocol")
        if not tasklist_str:
            logger.warning(
                log_title,
                "No tasklist found in the protocol.",
                body_md,
            )
            return None
        tasklist = Tasklist(extract(tasklist_str))
        logger.success(
            log_title,
            "Extracted tasklist from the document.",
            mdit.element.code_block(
                ps.write.to_yaml_string(tasklist.as_list), language="yaml", caption="Tasklist"
            ),
            body_md,
        )
        return tasklist

    def _make_auto_labels_from_issue_ticket_inputs(
        self, issue_form: IssueForm
    ) -> tuple[dict[str, list[Label]], Label]:
        version_labels = []
        branch_labels = []
        if "version" in self._issue_inputs:
            for version in self._issue_inputs["version"]:
                version_labels.append(self._manager.label.label_version(version))
                branch = self._manager.branch.from_version(version)
                branch_labels.append(self._manager.label.label_branch(branch.name))
        elif "branch" in self._issue_inputs:
            for branch in self._issue_inputs["branch"]:
                branch_labels.append(self._manager.label.label_branch(branch))
        else:
            logger.info(
                "Issue Label Update",
                "Could not match branch or version in issue body to pattern defined in metadata.",
            )
        labels = {
            "version": version_labels,
            "branch": branch_labels,
        }
        for label in issue_form.id_labels + issue_form.labels:
            labels.setdefault(label.category.value, []).append(label)
        status_label = self._manager.label.status_label(IssueStatus.TRIAGE)
        return labels, status_label

    def _add_labels_env_var(self, labels: dict[LabelType, list[Label]]):
        labels_out = {k.value: v for k, v in labels.items() if k is not LabelType.STATUS}
        self._env_vars["labels"] = labels_out
        self._env_vars["status_label"] = labels.get(LabelType.STATUS, [None])[0]
        return

    def _extract_marker_wrapped(self, text: str, marker: dict):
        pattern = rf"{re.escape(marker['start'].lstrip())}(.*?){re.escape(marker['end'].rstrip())}"
        match = re.search(pattern, text, flags=re.DOTALL)
        data = match.group(1) if match else ""
        logger.info(
            f"{self._type} Protocol Data Extraction",
            mdit.element.code_block(data, caption="Match") if data else "No Match found.",
            mdit.element.code_block(pattern, caption="RegEx Pattern"),
        )
        return data

    @staticmethod
    def _wrap_in_markers(entry: str, marker: dict[str, str]):
        return f"{marker['start']}{entry}{marker['end']}"

    @staticmethod
    def _extract_issue_ticket_inputs(body: str, body_elems: list[dict]) -> dict[str, str | list]:
        def create_pattern(parts_):
            pattern_sections = []
            for idx, part in enumerate(parts_):
                pattern_content = f"(?P<{part['id']}>.*)" if part["id"] else "(?:.*)"
                pattern_section = rf"### {re.escape(part['title'])}\n{pattern_content}"
                if idx != 0:
                    pattern_section = f"\n{pattern_section}"
                # if part["optional"]:
                #     pattern_section = f"(?:{pattern_section})?"
                pattern_sections.append(pattern_section)
            return "".join(pattern_sections)

        def extract_value(raw_value: str, elem_settings):
            raw_value = raw_value.strip()
            elem_type = elem_settings["type"]
            if elem_type == "textarea":
                render = elem_settings.get("attributes", {}).get("render")
                if render:
                    return raw_value.removeprefix(f"```{render}").removesuffix("```")
                return raw_value
            if elem_type == "dropdown":
                multiple = elem_settings.get("attributes", {}).get("multiple")
                if multiple:
                    return raw_value.split(", ")
                return raw_value
            if elem_type == "checkboxes":
                out = []
                for line in raw_value.splitlines():
                    if line.startswith("- [X] "):
                        out.append(True)
                    elif line.startswith("- [ ] "):
                        out.append(False)
                return out
            return raw_value

        parts = []
        settings = {}
        for elem in body_elems:
            if elem["type"] == "markdown" or not elem.get("active", True):
                continue
            elem_id = elem.get("id")
            parts.append({"id": elem_id, "title": elem["attributes"]["label"]})
            if elem_id:
                settings[elem_id] = elem
        pattern = create_pattern(parts)
        compiled_pattern = re.compile(pattern, re.DOTALL)
        # Search for the pattern in the markdown
        logger.debug("Issue body", mdit.element.code_block(body))
        match = re.search(compiled_pattern, body)
        if not match:
            logger.critical(
                "Issue Body Pattern Matching",
                "Could not match the issue body to pattern defined in control center settings.",
            )
            raise ProManException()
        # Create a dictionary with titles as keys and matched content as values
        sections = {
            section_id: extract_value(content, settings[section_id]) if content else None
            for section_id, content in match.groupdict().items()
        }
        logger.debug("Matched sections", str(sections))
        return sections

    # @staticmethod
    # def _toggle_checkbox(checkbox: str, check: bool) -> str:
    #     """Toggle the checkbox in a markdown tasklist entry."""
    #
    #     def replacer(match):
    #         checkmark = "X" if check else " "
    #         return f"{match.group(1)}{checkmark}{match.group(3)}"
    #
    #     pattern = re.compile(r"(^[\s\n]*-\s*\[)([ ]|X)(]\s*)", re.MULTILINE)
    #     matches = re.findall(pattern, checkbox)
    #     if len(matches) == 0 or len(matches) > 1:
    #         logger.warning(
    #             "Checkbox Toggle",
    #             f"Found {len(matches)} checkboxes in the input string:",
    #             mdit.element.code_block(checkbox, language="markdown", caption="Input String"),
    #         )
    #         return checkbox
    #     return re.sub(pattern, replacer, checkbox, count=1)

    # def add_data(
    #     self,
    #     id: str,
    #     spec: dict,
    #     data: str,
    #     replace: bool = False
    # ) -> str:
    #     marker_start, marker_end = self._make_text_marker(id=id, data=spec)
    #     pattern = rf"({re.escape(marker_start)})(.*?)({re.escape(marker_end)})"
    #     replacement = r"\1" + data + r"\3" if replace else r"\1\2" + data + r"\3"
    #     self.protocol = re.sub(pattern, replacement, self.protocol, flags=re.DOTALL)
    #     return self.protocol
