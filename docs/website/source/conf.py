"""Configuration file for the Sphinx website builder.

References
----------
- [ReadTheDocs environment variables](https://docs.readthedocs.io/en/stable/reference/environment-variables.html)
"""

from __future__ import annotations as _annotations

import copy as _copy
import json as _json
import shutil as _shutil
from pathlib import Path as _Path
from typing import TYPE_CHECKING as _TYPE_CHECKING

import pysyntax as _pysyntax
from loggerman import logger as _logger
from sphinx.builders.dirhtml import DirectoryHTMLBuilder as _DirectoryHTMLBuilder

import proman


try:
    from intersphinx_registry import get_intersphinx_mapping as _get_intersphinx_mapping
except (ImportError, ModuleNotFoundError):
    _get_intersphinx_mapping = None

if _TYPE_CHECKING:
    from sphinx.application import Sphinx


class _CustomDirectoryHTMLBuilder(_DirectoryHTMLBuilder):
    """Customized DirectoryHTMLBuilder to exclude the 404 file."""

    name = "dirhtml"

    def get_target_uri(self, docname: str, typ: str | None = None) -> str:
        if docname == "404":
            return ""
        return super().get_target_uri(docname=docname, typ=typ)

    def get_outfilename(self, pagename: str) -> str:
        if pagename == "404":
            return str(_Path(self.outdir) / "404.html")
        return super().get_outfilename(pagename=pagename)


def setup(app: Sphinx):
    """Add custom configurations to the Sphinx application."""
    app.add_builder(_CustomDirectoryHTMLBuilder, override=True)
    app.connect("source-read", _source_jinja_template)
    return


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
    # Change Jinja environment markers to avoid clashes with the MyST Attributes extension
    # as well as templating syntax in control center configurations.
    # Refs:
    # - Jinja: https://jinja.palletsprojects.com/en/stable/api/#jinja2.Environment
    # - MyST: https://myst-parser.readthedocs.io/en/latest/syntax/optional.html#attributes
    attrs_default = {}
    for attr, attr_new_val in (
        ("block_start_string", "|{%"),
        ("block_end_string", "%}|"),
        ("variable_start_string", "|{{"),
        ("variable_end_string", "}}|"),
        ("comment_start_string", "|{#"),
        ("comment_end_string", "#}|"),
    ):
        attr_val = getattr(app.builder.templates.environment, attr)
        attrs_default[attr] = attr_val
        setattr(app.builder.templates.environment, attr, attr_new_val)
    # Run page through Jinja
    try:
        content[0] = app.builder.templates.render_string(
            content[0],
            app.config.html_context | {"docname": app.env.docname},
        )
    except Exception as e:
        raise RuntimeError(error_msg) from e
    # Revert Jinja environment markers to their defaults
    # so that other templates and tools have the default markers.
    for attr, attr_val in attrs_default.items():
        setattr(app.builder.templates.environment, attr, attr_val)
    return


def linkcode_resolve(domain: str, info: dict[str, str]) -> str | None:
    """Resolve the source code links for the `sphinx.ext.linkcode` extension.

    References
    ----------
    - https://www.sphinx-doc.org/en/master/usage/extensions/linkcode.html
    """

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
        log_intro = (
            f"Resolved source-code filepath of module `{info['module']}` to `{module_path_abs}`"
        )
        lines = _pysyntax.parse.object_definition_lines(
            code=filepath.read_text(),
            object_name=object_name
        )
        if not lines:
            _logger.warning(
                logger_title,
                f"{log_intro}, but could not find object `{object_name}` in the file.",
                f"Generated URL (without line numbers): {url}",
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
            f"Generated URL: {final_url}",
        )
        return final_url

    logger_title = "LinkCode Resolve"
    if domain != "py" or not info["module"]:
        _logger.warning(
            logger_title,
            "Invalid domain or module information:",
            _logger.pretty({"domain": domain, "info": info}),
        )
        return None
    source_path = _Path(_manager.data["pypkg_main.path.source"])
    module_path = source_path / info["module"].replace(".", "/")
    module_path_abs = _manager.git.repo_path / module_path
    if module_path_abs.is_dir() and module_path_abs.joinpath("__init__.py").is_file():
        filepath = module_path.joinpath("__init__.py")
    elif module_path_abs.with_suffix(".py").is_file():
        filepath = module_path.with_suffix(".py")
    else:
        _logger.warning(
            logger_title,
            f"Python module {info['module']} not found at {module_path_abs}.",
        )
        return None
    url = f"https://github.dev/{_manager.data['repo.full_name']}/blob/{_current_hash}/{filepath}"
    return add_obj_line_number_to_url(
        url=url, filepath=_manager.git.repo_path / filepath, object_name=info["fullname"]
    )


def _add_version() -> None:
    """Add project version info to Sphinx configurations."""
    version = _manager.release.latest_version()
    if version:
        _globals["version"] = _globals.get("version") or str(version.public)
        _globals["release"] = _globals.get("release") or str(version.full)
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


def _add_api_files():
    schemas = [
        {
            "id": f"https://controlman.repodynamics.com/schema/{schema[0]}",
            "name": schema[1],
            "filepath": f"api/{schema[0]}",
        }
        for schema in (
            ("metadata", "ccc"),
            ("local", "cc-local"),
            ("cache", "cc-cache"),
            ("variables", "cc-vars"),
            ("changelog", "cc-changelog"),
            ("contributors", "cc-contrib"),
        )
    ]
    _globals["jsonschema_autodoc"] = {
        "schemas": schemas,
        "registry": sorted(
            (schema_id, resource.contents)
            for schema_id, resource in proman.data_validator.get_registry().items()
        ),
        "badge_permissive": {"color": "#00802B"},
        "badge_restrictive": {"color": "#AF1F10"},
        "badges": {"separator": 2, "style": "flat-square", "color": "#0B3C75"},
        "ref_doc_filepath": "api/refs",
    }
    return


def _add_license():
    for license_id, component in _manager.data.get("license.component", {}).items():
        copyright_path = component["path"].get("header_plain")
        if copyright_path:
            copyright_abs_path = _manager.git.repo_path / copyright_path
            component["header_plain"] = copyright_abs_path.read_text()
        license_path = _manager.git.repo_path / component["path"]["text_plain"]
        dest_path = _manager.data["web.page.license.path"]
        if not dest_path:
            continue
        dest_dir = _Path(dest_path) / license_id.lower()
        dest_dir.mkdir(parents=True, exist_ok=True)
        _shutil.copy2(license_path, dest_dir / "index.md")
    return


def _read_json_data(name: str, path: str | _Path, *, required: bool) -> dict | None:
    """Read a JSON data file."""
    try:
        with (_manager.git.repo_path / path).open() as f:
            return _json.load(f)
    except (_json.JSONDecodeError, FileNotFoundError) as e:
        if not required:
            return None
        error_msg = (
            f"Could not read project {name} file at '{path}'. "
            "Please ensure that the file is a valid JSON file."
        )
        raise RuntimeError(error_msg) from e


_logger.initialize(realtime_levels=list(range(1, 7)))
_manager = proman.manager.create()
_globals: dict = _read_json_data(name="Sphinx config", path=_manager.data["file_sphinx_conf.path"], required=True)
_current_hash = _manager.git.commit_hash_normal()
_add_version()
_add_css_and_js_files()
_add_intersphinx_mapping()
_add_license()
_logger.info("Configurations", _logger.pretty(_globals))
_globals.setdefault("html_context", {}).update(
        {"ccc": _copy.deepcopy(_manager.data()), "manager": _manager}
    )
_logger.info("HTML context", _logger.pretty(_globals["html_context"]))
# _add_api_files()  # noqa: ERA001
globals().update(_globals)
