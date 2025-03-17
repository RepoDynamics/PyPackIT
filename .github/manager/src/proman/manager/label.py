from __future__ import annotations as _annotations

from typing import TYPE_CHECKING as _TYPE_CHECKING

import pyserials as _ps
from loggerman import logger
from pylinks.exception.api import WebAPIError as _WebAPIError

from proman.dtype import LabelType
from proman.dstruct import Label

if _TYPE_CHECKING:
    from proman.dtype import IssueStatus
    from proman.manager import Manager


class LabelManager:

    def __init__(self, manager: Manager):
        self._manager = manager
        self._label_name_to_obj: dict[str, Label] = {}
        self._label_id_to_obj: dict[tuple[str, str], Label] = {}
        return

    def from_id(self, group_id: str, label_id: str) -> Label:
        return self.id_to_obj_map[(group_id, label_id)]

    @property
    def name_to_obj_map(self) -> dict[str, Label]:
        """All repository labels, as a dictionary mapping full label names to Label objects."""
        if not self._label_name_to_obj:
            self._label_name_to_obj, self._label_id_to_obj = self._initialize_label_data()
        return self._label_name_to_obj

    @property
    def id_to_obj_map(self) -> dict[tuple[str, str], Label]:
        """All repository labels, as a dictionary mapping full label IDs to Label objects."""
        if not self._label_id_to_obj:
            self._label_name_to_obj, self._label_id_to_obj = self._initialize_label_data()
        return self._label_id_to_obj

    def update_status_label_on_github(
        self, issue_nr: int, old_status_labels: list[Label], new_status_label: Label
    ) -> None:
        for old_status_label in old_status_labels:
            if old_status_label.name != new_status_label.name:
                try:
                    self._manager.gh_api_actions.issue_labels_remove(
                        number=issue_nr, label=old_status_label.name
                    )
                except _WebAPIError as e:
                    logger.warning(
                        "Status Label Updated",
                        f"Failed to remove label '{old_status_label.name}' from issue #{issue_nr}.",
                        e.report.body,
                    )
        return

    def status_label(self, status: str | IssueStatus) -> Label:
        if not isinstance(status, str):
            status = status.value
        return self.from_id("status", status)

    def label_version(self, version: str) -> Label:
        return self.from_id("version", version)

    def label_branch(self, branch: str) -> Label:
        return self.from_id("branch", branch)

    def label_version_to_branch(self, version_label: Label) -> Label:
        branch = self._manager.branch.from_version(version=version_label.suffix)
        return self.label_branch(branch=branch.name)

    def resolve_labels(self, names: list[str]) -> dict[LabelType, list[Label]]:
        """
        Resolve a list of label names to label objects.

        Parameters
        ----------
        names : list[str]
            List of label names.
        """
        labels = {}
        for name in names:
            label = self.resolve_label(name)
            labels.setdefault(label.category, []).append(label)
        return labels

    def resolve_label(self, name: str) -> Label:
        """
        Resolve a label name to a label object.

        Parameters
        ----------
        name : str
            Name of the label.
        """
        label = self.name_to_obj_map.get(name)
        if label:
            return label
        logger.warning(
            "Label Resolution",
            f"Could not find label '{name}' in label data.",
        )
        return Label(category=LabelType.UNKNOWN, name=name)

    def _initialize_label_data(self) -> tuple[dict[str, Label], dict[tuple[str, str], Label]]:
        name_to_obj = {}
        id_to_obj = {}
        for group_id, group_data in self._manager.data.get("label", {}).items():
            if group_id == "single":
                for label_id, label_data in group_data.items():
                    label = Label(
                        category=LabelType.CUSTOM_SINGLE,
                        name=label_data["name"],
                        group_id=group_id,
                        id=label_id,
                        description=label_data.get("description", ""),
                        color=label_data.get("color", ""),
                    )
                    name_to_obj[label_data["name"]] = id_to_obj[(group_id, label_id)] = label
            else:
                for label_id, label_data in group_data.get("label", {}).items():
                    label = Label(
                        category=LabelType(group_id) if group_id in (
                            "status", "version", "branch"
                        ) else LabelType.CUSTOM_GROUP,
                        name=label_data["name"],
                        group_id=group_id,
                        id=label_id,
                        prefix=group_data["prefix"],
                        suffix=label_data["suffix"],
                        description=label_data.get("description", group_data.get("description", "")),
                        color=label_data.get("color") or group_data.get("color", ""),
                    )
                    name_to_obj[label_data["name"]] = id_to_obj[(group_id, label_id)] = label
        return name_to_obj, id_to_obj

