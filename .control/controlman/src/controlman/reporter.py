import mdit as _mdit
import htmp as _htmp
from controlman.datatype import (
    DynamicFileChangeType,
    DynamicDirType,
    DynamicFile as _GeneratedFile,
    DynamicDir as _DynamicDir,
)


class ControlCenterReporter:

    def __init__(
        self,
        metadata: list[tuple[str, DynamicFileChangeType]],
        files: list[_GeneratedFile],
        dirs: list[_DynamicDir],
    ):
        self.metadata = metadata
        self.files = files
        self.dirs = dirs
        self.has_changed_metadata = bool(self.metadata)
        self.changed_files = [
            file for file in self.files if file.change not in (
                DynamicFileChangeType.DISABLED, DynamicFileChangeType.UNCHANGED, DynamicFileChangeType.INACTIVE
            )
        ]
        self.changed_dirs = [
            dir_ for dir_ in self.dirs if dir_.change not in (
                DynamicFileChangeType.DISABLED, DynamicFileChangeType.UNCHANGED, DynamicFileChangeType.INACTIVE
            )
        ]
        self.has_changed_files = bool(self.changed_files)
        self.has_changed_dirs = bool(self.changed_dirs)
        self.has_changes = self.has_changed_metadata or self.has_changed_files or self.has_changed_dirs
        return

    def report(self) -> _mdit.Document:
        if not self.has_changes:
            content = (
                "All dynamic content were in sync with control center configurations. No changes were made."
            )
            return self._create_document(content=content)
        changed_categories = []
        section = {}
        for category_name, category_changed, category_reporter in (
            ("metadata", self.has_changed_metadata, self._report_metadata),
            ("files", self.has_changed_files, self._report_files),
            ("directories", self.has_changed_dirs, self._report_dirs),
        ):
            if category_changed:
                changed_categories.append(category_name)
                section[category_name] = category_reporter()
        changed_categories_str = self._comma_list(changed_categories)
        verb = "was" if len(changed_categories) == 1 else "were"
        content = f"Project's {changed_categories_str} {verb} out of sync with control center configurations."
        return self._create_document(content=content, section=section)

    def _create_document(self, content, section: dict | None = None) -> _mdit.Document:
        details_section = _mdit.document(
            heading="Changes",
            section=section,
        )
        return _mdit.document(
            heading="Control Center Report",
            body={"summary": content},
            section={"changes": details_section} if section else None,
        )

    def _report_metadata(self):
        rows = [["Path", "Change"]]
        for changed_key, change_type in sorted(self.metadata, key=lambda elem: elem[0]):
            change = change_type.value
            rows.append(
                [
                    _mdit.element.code_span(changed_key),
                    _htmp.element.span(change.emoji, {"title": change.title})
                ]
            )
        table = _mdit.element.table(
            rows,
            caption=f"ℹ️ Changes in the project's metadata.",
            align_table="center",
            align_columns=["left", "center"],
            num_rows_header=1,
            width_columns="auto",
        )
        page = _mdit.document(
            heading="Metadata",
            body={"table": table},
        )
        return page

    def _report_files(self) -> _mdit.Document | None:
        rows = [["Type", "Subtype", "Change", "Path", "Old Path"]]
        for file in sorted(
            self.files,
            key=lambda elem: (elem.type.value[1], elem.subtype[1]),
        ):
            if file.change in (DynamicFileChangeType.DISABLED, DynamicFileChangeType.UNCHANGED):
                continue
            change = file.change.value
            rows.append(
                [
                    file.type.value[1],
                    file.subtype[1],
                    _htmp.element.span(change.emoji, {"title": change.title}),
                    _mdit.element.code_span(file.path),
                    _mdit.element.code_span(file.path_before) if file.path_before else "—"
                ]
            )
        if not rows:
            return
        table = _mdit.element.table(
            rows,
            caption=f"📝 Changes in the project's dynamic files.",
            align_table="center",
            align_columns=["left", "left", "center", "left", "left"],
            num_rows_header=1,
            width_columns="auto",
        )
        page = _mdit.document(
            heading="Files",
            body={"table": table},
        )
        return page

    def _report_dirs(self) -> _mdit.Document | None:
        rows = [["Type", "Change", "Path", "Old Path"]]
        for dir_ in sorted(self.dirs, key=lambda elem: elem.type.value):
            if dir_.change in (DynamicFileChangeType.DISABLED, DynamicFileChangeType.UNCHANGED):
                continue
            change = dir_.change.value
            rows.append(
                [
                    dir_.type.value,
                    _htmp.element.span(change.emoji, {"title": change.title}),
                    _mdit.element.code_span(dir_.path),
                    _mdit.element.code_span(dir_.path_before) if dir_.path_before else "—",
                ]
            )
        if not rows:
            return
        table = _mdit.element.table(
            rows,
            caption=f"🗂 Changes in the project's dynamic directories.",
            align_table="center",
            align_columns=["left", "left", "center", "left", "left"],
            num_rows_header=1,
            width_columns="auto",
        )
        page = _mdit.document(
            heading="Directories",
            body={"table": table},
        )
        return page

    @staticmethod
    def _comma_list(l):
        if len(l) == 1:
            return l[0]
        if len(l) == 2:
            return f"{l[0]} and {l[1]}"
        return f"{", ".join(l[:-1])}, and {l[-1]}"