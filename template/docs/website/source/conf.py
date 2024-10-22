"""Configuration file for the Sphinx website builder."""

from __future__ import annotations as _annotations

import ast as _ast
import copy as _copy
import json as _json
from pathlib import Path as _Path
from typing import TYPE_CHECKING as _TYPE_CHECKING
import os as _os

import gittidy as _git
from loggerman import logger as _logger
from sphinx.builders.dirhtml import DirectoryHTMLBuilder as _DirectoryHTMLBuilder
from versionman import pep440_semver as _semver

try:
    from intersphinx_registry import get_intersphinx_mapping as _get_intersphinx_mapping
except (ImportError, ModuleNotFoundError):
    _get_intersphinx_mapping = None

if _TYPE_CHECKING:
    from typing import Any

    from sphinx.application import Sphinx


_METADATA_FILEPATH: str = ".github/.control/.metadata.json"
_globals: dict = {}


class _CustomDirectoryHTMLBuilder(_DirectoryHTMLBuilder):
    """Customized DirectoryHTMLBuilder to exclude the 404 file."""

    name = 'dirhtml'

    def get_target_uri(self, docname: str, typ: str | None = None) -> str:
        if docname == "404":
            return ""
        return super().get_target_uri(docname=docname, typ=typ)

    def get_outfilename(self, pagename: str) -> str:
        if pagename == "404":
            return _os.path.join(self.outdir, '404.html')
        return super().get_outfilename(pagename=pagename)


def setup(app: Sphinx):
    """Add custom configurations to the Sphinx application."""
    app.add_builder(_CustomDirectoryHTMLBuilder, override=True)
    app.connect("source-read", _source_jinja_template)
    return


def linkcode_resolve(domain: str, info: dict[str, str]) -> str | None:
    """Resolve the source code links for the `sphinx.ext.linkcode` extension.

    References
    ----------
    - https://www.sphinx-doc.org/en/master/usage/extensions/linkcode.html
    """

    def get_obj_def_lines(filepath: _Path, object_name: str) -> tuple[int, int | None] | None:
        """Get the line numbers of an object definition in the source file.

        Parameters
        ----------
        filepath
            Path to the source file.
        object_name
            Name of the object to find in the source file.

        Returns
        -------
        Start and end line numbers of the object definition.
        End line number is `None` if the object definition is a single line.
        If the object is not found, `None` is returned.
        """
        source = filepath.read_text()
        tree = _ast.parse(source, filename=filepath)
        for node in _ast.walk(tree):
            # Check for class or function definitions
            if isinstance(
                node,
                (_ast.ClassDef, _ast.FunctionDef, _ast.AsyncFunctionDef)
            ) and node.name == object_name:
                return node.lineno, getattr(node, 'end_lineno', None)
            # Check for variable assignments (without type annotations)
            if isinstance(node, _ast.Assign):
                for target in node.targets:
                    if isinstance(target, _ast.Name) and target.id == object_name:
                        return node.lineno, getattr(node, 'end_lineno', None)
            # Check for variable assignments (with type annotations)
            if isinstance(node, _ast.AnnAssign):
                target = node.target
                if isinstance(target, _ast.Name) and target.id == object_name:
                    return node.lineno, getattr(node, 'end_lineno', None)
        return

    def add_obj_line_number_to_url(
        url: str,
        filepath: _Path,
        object_name: str,
    ) -> str:
        """Add line numbers of the object definition to the URL.

        Parameters
        ----------
        url
            URL to the source file.
        filepath
            Local path to the source file.
        object_name
            Name of the object to find in the source file.

        Returns
        -------
        URL to the source file with added line numbers of the object definition, if found.
        """
        log_intro = f"Resolved source-code filepath of module `{info["module"]}` to `{module_path_abs}`"
        lines = get_obj_def_lines(filepath=filepath, object_name=object_name)
        if not lines:
            _logger.warning(
                logger_title,
                f"{log_intro}, but could not find object `{object_name}` in the file.",
                f"Generated URL (without line numbers): {url}"
            )
            return url
        start_line, end_line = lines
        if end_line and end_line != start_line:
            url_fragment = f"L{start_line}-L{end_line}"
            log_segment = f"lines {start_line}-{end_line}"
        else:
            url_fragment = f"L{start_line}"
            log_segment = f"line {start_line}"
        final_url = f"{url}#{url_fragment}"
        _logger.success(
            logger_title,
            f"{log_intro} and found object `{object_name}` at {log_segment}.",
            f"Generated URL: {final_url}"
        )
        return final_url

    logger_title = "LinkCode Resolve"
    if domain != 'py' or not info['module']:
        _logger.warning(
            logger_title,
            "Invalid domain or module information:",
            _logger.pretty({"domain": domain, "info": info}),
        )
        return
    source_path = _Path(_meta["pkg"]["path"]["source"])
    module_path = source_path / info['module'].replace('.', '/')
    module_path_abs = _path_root / module_path
    if module_path_abs.is_dir() and module_path_abs.joinpath("__init__.py").is_file():
        filepath = module_path.joinpath("__init__.py")
    elif module_path_abs.with_suffix(".py").is_file():
        filepath = module_path.with_suffix(".py")
    else:
        _logger.warning(
            logger_title,
            f"Python module {info["module"]} not found at {module_path_abs}.",
        )
        return
    url = f"https://github.dev/{_meta["repo"]["full_name"]}/blob/{_current_hash}/{filepath}"
    return add_obj_line_number_to_url(url=url, filepath=_path_root/filepath, object_name=info["fullname"])


def _source_jinja_template(app: Sphinx, docname: str, content: list[str]) -> None:
    """Render pages as jinja template for templating inside source files.

    References
    ----------
    - https://www.ericholscher.com/blog/2016/jul/25/integrating-jinja-rst-sphinx/
    - https://www.sphinx-doc.org/en/master/extdev/event_callbacks.html#event-source-read
    """
    error_msg = (
        f"Could not render page '{docname}' as Jinja template. "
        "Please ensure that the page content is valid."
    )
    try:
        content[0] = app.builder.templates.render_string(
            content[0],
            app.config.html_context | {"docname": app.env.docname},
        )
    except Exception as e:
        raise RuntimeError(error_msg) from e
    return


def _add_version() -> None:
    """Add the version to the Sphinx configuration."""
    if all(key in _globals for key in ("version", "release")):
        return
    ver_tag_prefix = _meta["tag"]["version"]["prefix"]
    tags = _git_api.get_tags()
    ver = _semver.latest_version_from_tags(tags=tags, version_tag_prefix=ver_tag_prefix)
    if ver:
        _globals["version"] = _globals.get("version") or f"{ver.major}.{ver.minor}"
        _globals["release"] = _globals.get("release") or str(ver)
    return


def _add_css_and_js_files() -> None:
    """Add CSS and JS files from the static directory.

    This function takes the first static path defined in `html_static_path`
    (this should be the '_static' directory in the Sphinx project) and looks
    for all CSS and JS files in the 'css' and 'js' subdirectories, respectively.
    It then adds these files to the Sphinx configuration in the `html_css_files`
    and `html_js_files` lists.
    Therefore, you can add new CSS and JS files to the 'css' and 'js'
    directories in the '_static' directory, and they will be automatically
    added to the Sphinx configuration.
    """
    static_paths = _globals.get("html_static_path", [])
    if not static_paths:
        return
    static_path = _Path(static_paths[0])
    for file_type in ("css", "js"):
        _to_add = []
        target_files = _globals.setdefault(f"html_{file_type}_files", [])
        for _glob in [f"**/*.{file_type}", f"**/*.{file_type}_t"]:
            for _path in (static_path / file_type).glob(_glob):
                _filename = str(_path).removeprefix(f"{static_path}/").removesuffix("_t")
                for file in target_files:
                    if isinstance(file, tuple):
                        if file[0] == _filename:
                            break
                    elif file == _filename:
                        break
                else:
                    _to_add.append(_filename)
        target_files.extend(_to_add)
    return


def _get_path_repo_root() -> tuple[_Path, str]:
    """Get the path to the root of the repository."""
    error_msg = (
        "Could not find the repository root. "
        "The repository root must have a `.github` directory, "
        f"and must contain the control center metadata file at '{_METADATA_FILEPATH}'."
    )
    num_up: int = -1
    for parent_dir in _Path(__file__).parents:
        num_up += 1
        for path in parent_dir.iterdir():
            if (
                path.is_dir()
                and path.name == ".github"
                and (parent_dir / _METADATA_FILEPATH).is_file()
            ):
                return parent_dir, "../" * num_up
    raise RuntimeError(error_msg)


def _add_sphinx() -> None:
    """Set sphinx main configurations."""
    _globals.update(_meta["web"]["sphinx"]["config"])
    return


def _merge_extra_config(
    config: dict[str, Any],
    config_key: str,
    config_name: str,
) -> None:
    """Merge theme or extension configurations with the Sphinx configuration."""

    def raise_unmatched_type(original_type: str) -> None:
        """Raise an error for unmatched configuration types."""
        error_msg = (
            f"Sphinx configuration key '{_conf_key}' is already set to a {original_type}, "
            f"but {config_name} configuration key '{config_key}.{_conf_key}' is a trying to add "
            f"a value of type '{type(_conf_value)}': {_conf_value}."
        )
        raise RuntimeError(error_msg)

    def raise_duplicate_key(key: str, path: str) -> None:
        """Raise an error for duplicate configuration keys."""
        error_msg = (
            f"Duplicate configuration key '{key}' for {config_name} defined at '{path}'. "
            "Please ensure that no configuration key is defined more than once."
        )
        raise RuntimeError(error_msg)

    for _conf_key, _conf_value in config.items():
        if _conf_key not in _globals:
            _globals[_conf_key] = _conf_value
            continue
        _existing_val = _globals[_conf_key]
        if isinstance(_existing_val, list):
            if not isinstance(_conf_value, list):
                raise_unmatched_type("list")
            _existing_val.extend(_conf_value)
        elif isinstance(_existing_val, dict):
            if not isinstance(_conf_value, dict):
                raise_unmatched_type("dictionary")
            for _sub_key, _sub_value in _conf_value.items():
                if _sub_key in _existing_val:
                    raise_duplicate_key(key=_sub_key, path=f"{config_key}.{_conf_key}")
                _existing_val[_sub_key] = _sub_value
        else:
            raise_duplicate_key(key=_conf_key, path=config_key)
    return


def _add_theme() -> None:
    """Add theme configurations."""
    theme = _meta["web"].get("theme")
    if not theme:
        print("No theme specified in control center metadata at 'web.theme'.")  # noqa: T201
        return
    error_msg_html_theme = (
        "The key `html_theme` is already defined in the Sphinx configuration at `web.sphinx`, "
        "but a theme is specified in the control center metadata at `web.theme`. "
        "Please remove one of the theme configurations.",
    )
    if "html_theme" in _globals:
        raise RuntimeError(error_msg_html_theme)
    _globals["html_theme"] = _meta["web"]["theme"]["dependency"]["import_name"]
    _merge_extra_config(
        config=_meta["web"]["theme"].get("config", {}),
        config_key="web.theme.config",
        config_name="theme",
    )
    return


def _add_extensions() -> None:
    """Add extensions and their configurations."""
    if "extensions" in _globals:
        error_msg = (
            "The key `extensions` is already defined in the Sphinx configuration at `web.sphinx`. "
            "Please remove the key from the configuration.",
        )
        raise RuntimeError(error_msg)
    extensions = []
    _globals["extensions"] = extensions
    for _ext_type, _ext_path, _exts in (
        ("internal", "web.sphinx.extension", _meta["web"]["sphinx"].get("extension", {})),
        ("external", "web.extension", _meta["web"].get("extension", {})),
    ):
        for _ext_id, _ext in _exts.items():
            # Add extension name to `extensions`
            _ext_import_name = _ext["dependency"]["import_name"]
            if _ext_import_name in extensions:
                error_msg = (
                    f"Duplicate extension name '{_ext_import_name}' for Sphinx "
                    f"{_ext_type} extension defined at "
                    f"`{_ext_path}.{_ext_id}.dependency.import_name`. "
                    "Please ensure that no two extensions have the same import name.",
                )
                raise RuntimeError(error_msg)
            # Add extension configurations to global variables
            extensions.append(_ext_import_name)
            _merge_extra_config(
                config=_ext.get("config", {}),
                config_key=f"{_ext_path}.{_ext_id}.config",
                config_name=f"{_ext_type} extension",
            )
    return


def _add_ablog_blog_authors() -> None:
    """Add ablog `blog_authors` extension configuration.

    This function looks for the `blog_authors` key in the Sphinx configuration;
    if not found, it adds the `blog_authors` key with the authors from the control center metadata.

    References
    ----------
    - [ABlog Configuration Options](https://ablog.readthedocs.io/en/stable/manual/ablog-configuration-options.html#confval-blog_authors)
    """
    if "blog_authors" in _globals:
        return
    blog_authors = {}
    _globals["blog_authors"] = blog_authors
    for person_id, person in _meta["team"].items():
        if "website" in person:
            url = person["website"]
        else:
            for contact_type in ("github", "twitter", "linkedin", "researchgate", "orcid", "email"):
                if contact_type in person:
                    url = person[contact_type]["url"]
                    break
            else:
                url = _meta["web"]["url"]["home"]
        blog_authors[person_id] = (person["name"]["full"], url)
    return


def _read_metadata() -> dict[str, Any]:
    """Read control center metadata."""
    error_msg = (
        f"Could not read control center metadata file at '{_METADATA_FILEPATH}'. "
        "Please ensure that the file is a valid JSON file."
    )
    try:
        with (_path_root / _METADATA_FILEPATH).open() as f:
            return _json.load(f)
    except _json.JSONDecodeError as e:
        raise RuntimeError(error_msg) from e


def _add_html_context():
    """Add the HTML context to the Sphinx configuration."""
    _globals.setdefault("html_context", {}).update({"ccc": _copy.deepcopy(_meta)})
    return


def _add_intersphinx_mapping():
    """Add intersphinx mappings to the Sphinx configuration."""
    mapping = _globals.get("intersphinx_mapping", {})
    if not mapping:
        return
    error_msg = (
        "Intersphinx mapping value for key '{key}' is not set. "
        "Mapping values can only be omitted if `intersphinx_registry` is installed."
    )
    to_get = []
    for key, val in mapping.items():
        if not val:
            if not _get_intersphinx_mapping:
                raise RuntimeError(error_msg.format(key=key))
            to_get.append(key)
    if not to_get:
        return
    mapping_addon = _get_intersphinx_mapping(packages=set(to_get))
    mapping.update(mapping_addon)
    return


_logger.initialize(realtime_levels=list(range(1, 7)))
_path_root, _path_to_root = _get_path_repo_root()
_git_api = _git.Git(path=_path_root)
_current_hash = _git_api.commit_hash_normal()
_meta = _read_metadata()
_add_sphinx()
_add_version()
_add_css_and_js_files()
_add_theme()
_add_extensions()
_add_ablog_blog_authors()
_add_intersphinx_mapping()
_logger.info("Configurations", _logger.pretty(_globals))
_add_html_context()
_logger.info("HTML context", _logger.pretty(_globals["html_context"]))
globals().update(_globals)
