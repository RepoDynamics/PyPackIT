"""Inline Hooks."""

from __future__ import annotations

from typing import TYPE_CHECKING

from controlman.changelog_manager import ChangelogManager
from loggerman import logger
import mdit
import pylinks as pl
import pyserials as ps

if TYPE_CHECKING:
    from typing import Callable, Any
    from pathlib import Path
    from pyserials import NestedDict


class InlineHooks:
    """Inline Hooks.

    Parameters
    ----------
    repo_path
        Path to the root of the repository.
    ccc
        Control center configurations from the existing `metadata.json` file.
    """

    def __init__(self, repo_path: Path, ccc: NestedDict):
        self.repo_path = repo_path
        self.ccc = ccc
        self.get = None
        self.changelog = ChangelogManager(repo_path=self.repo_path)
        return

    def __call__(self, get_metadata: Callable[[str, Any, bool], Any]) -> InlineHooks:
        """Prime with metadata getter function.

        Parameters
        ----------
        get_metadata
            A function to retrieve current control center configurations.
        """
        self.get = get_metadata
        self.changelog(get_metadata=get_metadata)
        return self

    def commit_labels(self) -> dict:
        out = {}
        release_commits = self.get("commit.release")
        commit_config = self.get("commit.config")
        label_prefix = self.get("label.commit.prefix")
        label_sep = self.get("label.commit.separator")
        scope_start = commit_config["scope_start"]
        scope_end = commit_config["scope_end"]
        scope_sep = commit_config["scope_separator"]
        for commit_id, commit_data in release_commits.items():
            scopes = commit_data.get("scope")
            if isinstance(scopes, str):
                scopes = [scopes]
            scope = f"{scope_start}{scope_sep.join(scopes)}{scope_end}" if scopes else ""
            label_suffix = f"{commit_data["type"]}{scope}"
            out[commit_id] = {
                "suffix": label_suffix,
                "description": commit_data.get("type_description", ""),
                "name": f"{label_prefix}{label_sep}{label_suffix}"
            }
        return out

    def trove_classifiers(self) -> list[str]:
        """Create trove classifiers for the package/test-suite."""

        def programming_language():
            base = "Programming Language :: Python"
            return [base] + [
                f"{base} :: {version}" for version in self.get("..python.version.minors") + ["3 :: Only"]
            ]

        def operating_system():
            base = "Operating System :: {}"
            trove = {
                "ubuntu": "POSIX :: Linux",
                "macos": "MacOS",
                "windows": "Microsoft :: Windows",
            }
            out = [
                base.format(trove[runner_type]) for runner_type in set(
                    [os["runner"].split("-")[0] for os in self.get("..os").values()]
                )
            ]
            if self.get("..python.pure"):
                out.append(base.format("OS Independent"))
            return out

        def development_phase():
            log = self.changelog.current_public
            ver = log.version
            phase = log.get("phase")
            if ver == "0.0.0":
                code = 1
            elif phase == "dev":
                code = 2
            elif phase == "alpha":
                code = 3
            elif phase in ("beta", "rc") or ver.startswith("0"):
                code = 4
            else:
                highest_major = max(int(version[0]) for version in self.get("project.versions"))
                if int(ver[0]) == highest_major:
                    code = 5
                else:
                    code = 6
            code_name = {
                1: "Planning",
                2: "Pre-Alpha",
                3: "Alpha",
                4: "Beta",
                5: "Production/Stable",
                6: "Mature",
                7: "Inactive",
            }
            return f"Development Status :: {code} - {code_name[code]}"

        out = programming_language() + operating_system() + [development_phase()]
        if self.get("..typed"):
            out.append("Typing :: Typed")
        return out

    def web_page(self) -> dict[str, dict[str, str]]:
        """Create `$.web.page` data."""
        path = self.repo_path / (self.ccc["web.path.source"] or self.get("web.path.source"))
        url_home = self.get("web.url.home")
        pages = {}
        blog = {}
        for md_filepath in path.rglob("*.md", case_sensitive=False):
            if not md_filepath.is_file():
                continue
            rel_path = md_filepath.relative_to(path)
            dirhtml_path = str(rel_path.with_suffix("")).removesuffix("/index")
            text = md_filepath.read_text()
            frontmatter = mdit.parse.frontmatter(text) or {}
            if "ccid" in frontmatter:
                pages[pl.string.to_slug(frontmatter["ccid"])] = {
                    "title": mdit.parse.title(text),
                    "path": dirhtml_path,
                    "url": f"{url_home}/{dirhtml_path}",
                }
            for key in ["category", "tags"]:
                val = frontmatter.get(key)
                if not val:
                    continue
                if isinstance(val, str):
                    val = [item.strip() for item in val.split(",")]
                if not isinstance(val, list):
                    logger.warning(
                        mdit.inline_container(
                            "Invalid webpage frontmatter: ",
                            mdit.element.code_span(str(rel_path)),
                        ),
                        mdit.inline_container(
                            "Invalid frontmatter value for ",
                            mdit.element.code_span(key),
                            " :"),
                        mdit.element.code_block(
                            ps.write.to_yaml_string(val, end_of_file_newline=False),
                            language="yaml",
                        ),
                    )
                blog.setdefault(key, []).extend(val)
        if "blog" not in pages:
            return pages
        for key, values in blog.items():
            for value in set(values):
                value_slug = pl.string.to_slug(value)
                key_singular = key.removesuffix('s')
                final_key = f"blog_{key_singular}_{value_slug}"
                if final_key in pages:
                    logger.error(
                        mdit.inline_container(
                            "Duplicate webpage ID ",
                            mdit.element.code_span(final_key)
                        ),
                        f"Generated ID '{final_key}' already exists "
                        f"for page '{pages[final_key]['path']}'. "
                        "Please do not use `ccid` values that start with 'blog_'."
                    )
                blog_group_path = f"{pages["blog"]["path"]}/{key_singular}/{value_slug}"
                pages[final_key] = {
                    "title": value,
                    "path": blog_group_path,
                    "url": f"{url_home}/{blog_group_path}",
                }
        return pages
