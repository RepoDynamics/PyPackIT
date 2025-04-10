from __future__ import annotations

import re
from pathlib import Path
from typing import TYPE_CHECKING

import htmp
import mdit
from proman import const

from proman.dtype import FileChangeType, RepoFileType

if TYPE_CHECKING:
    from pyserials import NestedDict

    from proman.report import Reporter


def run(data: NestedDict, changes: dict, reporter: Reporter) -> dict[str, bool]:
    change_type_map = {
        "added": FileChangeType.ADDED,
        "deleted": FileChangeType.REMOVED,
        "modified": FileChangeType.MODIFIED,
        "unmerged": FileChangeType.UNMERGED,
        "unknown": FileChangeType.UNKNOWN,
        "broken": FileChangeType.BROKEN,
        "copied_to": FileChangeType.ADDED,
        "renamed_from": FileChangeType.REMOVED,
        "renamed_to": FileChangeType.ADDED,
        "copied_modified_to": FileChangeType.ADDED,
        "renamed_modified_from": FileChangeType.REMOVED,
        "renamed_modified_to": FileChangeType.ADDED,
    }
    full_info: list = []
    paths_abs, paths_start, paths_regex = _make_filetype_patterns(data)
    dynamic_files = _get_dynamic_file_paths(data)
    for change_type, changed_paths in changes.items():
        if change_type.startswith("copied") and change_type.endswith("from"):
            continue
        for path in changed_paths:
            typ, subtype = _determine_filetype(path, paths_abs, paths_start, paths_regex)
            is_dynamic = path in dynamic_files
            full_info.append((typ, subtype, change_type_map[change_type], is_dynamic, path))
    changed_filetypes, oneliner, body = _generate_report(full_info)
    reporter.add(
        name="file_change",
        status="pass",
        summary=oneliner,
        body=body,
    )
    return _get_changed_project_components(full_info)


def _make_filetype_patterns(data: NestedDict):
    paths_abs = [
        (RepoFileType.CONFIG, "Metadata", const.FILEPATH_METADATA),
        (RepoFileType.CONFIG, "Git Ignore", const.FILEPATH_GITIGNORE),
        (RepoFileType.CONFIG, "Git Attributes", const.FILEPATH_GIT_ATTRIBUTES),
        (RepoFileType.CONFIG, "Citation", const.FILEPATH_CITATION_CONFIG),
    ]
    paths_start = [
        (RepoFileType.CC, "Custom Hook", f"{data['control.path']}/{const.DIRNAME_CC_HOOK}/"),
    ]
    for key in ("pkg", "test"):
        key_data = data[key]
        if not key_data:
            continue
        path_root = key_data["path"]["root"]
        path_import = key_data["path"]["import"]
        filetype = RepoFileType.PKG_CONFIG if key == "pkg" else RepoFileType.TEST_CONFIG
        paths_abs.extend(
            [
                (
                    filetype,
                    "Typing Marker",
                    f"{path_import}/{const.FILENAME_PACKAGE_TYPING_MARKER}",
                ),
                (filetype, "Manifest", f"{path_root}/{const.FILENAME_PACKAGE_MANIFEST}"),
                (filetype, "PyProject", f"{path_root}/{const.FILENAME_PKG_PYPROJECT}"),
            ]
        )
    for key in ("pkg", "test", "web"):
        key_data = data[key]
        if not key_data:
            continue
        path_root = key_data["path"]["root"]
        path_source = key_data["path"]["source"]
        # Order matters; first add the subdirectories and then the root directory
        paths_start.extend(
            [
                (RepoFileType[f"{key.upper()}_SOURCE"], None, f"{path_root}/{path_source}/"),
                (RepoFileType[f"{key.upper()}_CONFIG"], None, f"{path_root}/"),
            ]
        )
    if data["theme.path"]:
        paths_start.append((RepoFileType.THEME, "–", f"{data['theme.path']}/"))
    paths_regex = [
        (
            RepoFileType.CC,
            "Source",
            re.compile(rf"^{re.escape(data['control.path'])}/[^/]+\.(?i:y?aml)$"),
        ),
        (
            RepoFileType.ISSUE_FORM,
            None,
            re.compile(r"^\.github/ISSUE_TEMPLATE/(?!config\.ya?ml$)[^/]+\.(?i:y?aml)$"),
        ),
        (
            RepoFileType.ISSUE_TEMPLATE,
            None,
            re.compile(r"^\.github/ISSUE_TEMPLATE/[^/]+\.(?i:md)$"),
        ),
        (
            RepoFileType.CONFIG,
            "Issue Template Chooser",
            re.compile(r"^\.github/ISSUE_TEMPLATE/config\.(?i:y?aml)$"),
        ),
        (
            RepoFileType.PULL_TEMPLATE,
            None,
            re.compile(r"^(?:|\.github/|docs/)PULL_REQUEST_TEMPLATE/[^/]+(?:\.(txt|md|rst))?$"),
        ),
        (
            RepoFileType.PULL_TEMPLATE,
            "default",
            re.compile(r"^(?:|\.github/|docs/)pull_request_template(?:\.(txt|md|rst))?$"),
        ),
        (
            RepoFileType.DISCUSSION_FORM,
            None,
            re.compile(r"^\.github/DISCUSSION_TEMPLATE/[^/]+\.(?i:y?aml)$"),
        ),
        (RepoFileType.CONFIG, "Code Owners", re.compile(r"^(?:|\.github/|docs/)CODEOWNERS$")),
        (RepoFileType.CONFIG, "License", re.compile(r"^LICENSE(?:\.(txt|md|rst))?$")),
        (RepoFileType.CONFIG, "Funding", re.compile(r"^\.github/FUNDING\.(?i:y?aml)$")),
        (
            RepoFileType.README,
            "main",
            re.compile(r"^(?:|\.github/|docs/)README(?:\.(txt|md|rst|html))?$"),
        ),
        (RepoFileType.README, "–", re.compile(r"/README(?i:\.(txt|md|rst|html))?$")),
        (
            RepoFileType.HEALTH,
            None,
            re.compile(
                r"^(?:|\.github/|docs/)(?:(?i:CONTRIBUTING)|GOVERNANCE|SECURITY|SUPPORT|CODE_OF_CONDUCT)(?i:\.(txt|md|rst))?$"
            ),
        ),
        (RepoFileType.WORKFLOW, None, re.compile(r"^\.github/workflows/[^/]+\.(?i:y?aml)$")),
    ]
    return paths_abs, paths_start, paths_regex


def _determine_filetype(
    path: str,
    paths_abs: list[tuple[RepoFileType, str, str]],
    paths_start: list[tuple[RepoFileType, str, str]],
    paths_regex: list[tuple[RepoFileType, str, re.Pattern]],
) -> tuple[RepoFileType, str | None]:
    for filetype, subtype, abs_path in paths_abs:
        if path == abs_path:
            return filetype, subtype
    for filetype, subtype, pattern in paths_regex:
        if pattern.search(path):
            return filetype, subtype
    for filetype, subtype, start_path in paths_start:
        if path.startswith(start_path):
            return filetype, subtype
    return RepoFileType.OTHER, "–"


def _get_dynamic_file_paths(data: NestedDict) -> list[str]:
    dynamic_files = []
    for file_group in data.get("project.file", {}).values():
        dynamic_files.extend(list(file_group.values()))
    return dynamic_files


def _generate_report(full_info: list):
    changed_filetypes = {}
    rows = [["Type", "Subtype", "Change", "Dynamic", "Path"]]
    for typ, subtype, change_type, is_dynamic, path in sorted(
        full_info, key=lambda x: (x[0].value, x[1] or "")
    ):
        changed_filetypes.setdefault(typ, []).append(change_type)
        if is_dynamic:
            changed_filetypes.setdefault(RepoFileType.DYNAMIC, []).append(change_type)
        dynamic = htmp.element.span(
            "✅" if is_dynamic else "❌", title="Dynamic" if is_dynamic else "Static"
        )
        change_sig = change_type.value
        change = htmp.element.span(change_sig.emoji, title=change_sig.title)
        subtype = subtype or Path(path).stem
        rows.append([typ.value, subtype, change, dynamic, mdit.element.code_span(path)])
    if not changed_filetypes:
        oneliner = "No files were changed in this event."
        body = None
    else:
        changed_types = ", ".join(sorted([typ.value for typ in changed_filetypes]))
        oneliner = f"Following filetypes were changed: {changed_types}"
        body = mdit.element.unordered_list()
        intro_table_rows = [["Type", "Changes"]]
        has_broken_changes = False
        if RepoFileType.DYNAMIC in changed_filetypes:
            warning = "⚠️ Dynamic files were changed; make sure to double-check that everything is correct."
            body.append(warning)
        for file_type, change_list in changed_filetypes.items():
            change_list = sorted(set(change_list), key=lambda x: x.value.title)
            changes = []
            for change_type in change_list:
                if change_type in (FileChangeType.BROKEN, FileChangeType.UNKNOWN):
                    has_broken_changes = True
                changes.append(
                    f'<span title="{change_type.value.title}">{change_type.value.emoji}</span>'
                )
            changes_cell = "&nbsp;".join(changes)
            intro_table_rows.append([file_type.value, changes_cell])
        if has_broken_changes:
            warning = "⚠️ Some changes were marked as 'broken' or 'unknown'; please investigate."
            body.append(warning)
        intro_table = mdit.element.table(intro_table_rows, num_rows_header=1)
        body.append(["Following filetypes were changed:", intro_table])
        body.append(["Following files were changed:", mdit.element.table(rows, num_rows_header=1)])
    return changed_filetypes, oneliner, body


def _get_changed_project_components(changed_filetypes):
    def decide(filetypes: list[RepoFileType]):
        return any(filetype in changed_filetypes for filetype in filetypes)

    return {
        "dynamic": any(
            filetype in changed_filetypes for filetype in (RepoFileType.CC, RepoFileType.DYNAMIC)
        ),
        "pkg": decide([RepoFileType.PKG_SOURCE, RepoFileType.PKG_CONFIG]),
        "test": decide([RepoFileType.TEST_SOURCE, RepoFileType.TEST_CONFIG]),
        "web": decide(
            [
                RepoFileType.CC,
                RepoFileType.WEB_CONFIG,
                RepoFileType.WEB_SOURCE,
                RepoFileType.THEME,
                RepoFileType.PKG_SOURCE,
            ]
        ),
    }
