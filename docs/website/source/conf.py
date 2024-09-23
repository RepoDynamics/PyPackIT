"""Configuration file for the Sphinx website builder.

"""

import json as _json
from pathlib import Path as _Path

import gittidy as _git
from versionman import pep440_semver as _semver


_METADATA_FILEPATH = ".github/.control/.metadata.json"


def setup(app):
    # register custom config values
    # app.add_config_value(name='rd_meta', default=dict(), rebuild='html', types=[dict])
    app.connect("source-read", _rstjinja)
    # app.add_css_file("css/theme/custom.css")
    return


def _rstjinja(app, docname, source) -> None:
    """Render pages as jinja template for templating inside source files.

    References
    ----------
    - https://www.ericholscher.com/blog/2016/jul/25/integrating-jinja-rst-sphinx/
    """
    # Make sure we're outputting HTML
    # if app.builder.format != 'html':
    #     return
    try:
        source[0] = app.builder.templates.render_string(
            source[0],
            app.config.html_context | {"docname": app.env.docname},
        )
    except Exception as e:
        raise RuntimeError(
            f"Could not render page '{docname}' as Jinja template. "
            "Please ensure that the page content is valid.",
        ) from e
    return


def _add_version() -> None:
    """Add the version to the Sphinx configuration."""
    if all(key in global_vars for key in ("version", "release")):
        return
    ver_tag_prefix = meta["tag"]["version"]["prefix"]
    tags = _git.Git(path=_path_root).get_tags()
    ver = _semver.latest_version_from_tags(tags=tags, version_tag_prefix=ver_tag_prefix)
    if ver:
        global_vars["version"] = global_vars.get("version") or f"{ver.major}.{ver.minor}"
        global_vars["release"] = global_vars.get("release") or str(ver)
    return


def _add_css_and_js_files() -> None:
    """Add all CSS and JS files from the static directory to the
    `html_css_files` and `html_js_files` configuration variables.

    This function takes the first static path defined in `html_static_path`
    (this should be the '_static' directory in the Sphinx project) and looks
    for all CSS and JS files in the 'css' and 'js' subdirectories, respectively.
    It then adds these files to the Sphinx configuration in the `html_css_files`
    and `html_js_files` lists.
    Therefore, you can add new CSS and JS files to the 'css' and 'js'
    directories in the '_static' directory, and they will be automatically
    added to the Sphinx configuration.
    """
    static_paths = global_vars.get(f"html_static_path", [])
    if not static_paths:
        return
    static_path = _Path(static_paths[0])
    for file_type in ("css", "js"):
        _to_add = []
        target_files = global_vars.setdefault(f"html_{file_type}_files", [])
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
    num_up: int = -1
    for parent_dir in _Path(__file__).parents:
        num_up += 1
        for path in parent_dir.iterdir():
            if path.is_dir() and path.name == ".github" and (parent_dir / _METADATA_FILEPATH).is_file():
                return parent_dir, '../' * num_up
    raise RuntimeError(
        "Could not find the repository root. "
        "The repository root must have a `.github` directory, "
        f"and must contain the control center metadata file at '{_METADATA_FILEPATH}'.",
    )


def _add_sphinx():
    # Set sphinx main configurations
    for key, value in meta["web"]["sphinx"].items():
        global_vars[key] = value

    html_favicon = global_vars.get("html_favicon", "")
    if html_favicon and "://" not in html_favicon:
        global_vars["html_favicon"] = f"{_path_to_root}{html_favicon}"

    global_vars["html_static_path"] = [
        static_path if not static_path.startswith("/") else f"{_path_to_root}{static_path[1:]}"
        for static_path in global_vars.get("html_static_path", [])
    ]


def _add_theme():
    theme = meta["web"].get("theme")
    if not theme:
        print("No theme specified in control center metadata at `web.theme`.")
        return
    if "html_theme" in global_vars:
        raise RuntimeError(
            "The key `html_theme` is already defined in the Sphinx configuration at `web.sphinx`, "
            "but a theme is specified in the control center metadata at `web.theme`. "
            "Please remove one of the theme configurations.",
        )
    global_vars["html_theme"] = meta["web"]["theme"]["dependency"]["import_name"]
    for _conf_key, _conf_value in meta["web"]["theme"].get("config", {}).items():
        if _conf_key not in global_vars:
            global_vars[_conf_key] = _conf_value
            continue
        _existing_val = global_vars[_conf_key]
        if isinstance(_existing_val, list):
            if isinstance(_conf_value, list):
                _existing_val.extend(_conf_value)
                continue
            raise RuntimeError(
                f"Sphinx configuration key '{_conf_key}' is already set to a list, "
                f"but theme configuration key `web.theme.config.{_conf_key}` is a trying to add "
                f"a value of type '{type(_conf_value)}': {_conf_value}."
            )
        if isinstance(_existing_val, dict):
            if isinstance(_conf_value, dict):
                for _sub_key, _sub_value in _conf_value.items():
                    if _sub_key in _existing_val:
                        raise RuntimeError(
                            f"Duplicate configuration key '{_sub_key}' for theme "
                            f"defined at `web.theme.config.{_conf_key}`. "
                            "Please ensure that no configuration key is defined more than once.",
                        )
                    _existing_val[_sub_key] = _sub_value
                continue
            raise RuntimeError(
                f"Sphinx configuration key '{_conf_key}' is already set to a dictionary, "
                f"but theme configuration key `web.theme.config.{_conf_key}` is a trying to add "
                f"a value of type '{type(_conf_value)}': {_conf_value}."
            )
        raise RuntimeError(
            f"Duplicate configuration key '{_conf_key}' for theme "
            f"defined at `web.theme.config`. "
            "Please ensure that no configuration key is defined more than once.",
        )


def _add_extensions():
    if "extensions" in global_vars:
        raise RuntimeError(
            "The key `extensions` is already defined in the Sphinx configuration at `web.sphinx`. "
            "Please remove the key from the configuration.",
        )
    extensions = []
    global_vars["extensions"] = extensions
    for _ext_type, _ext_path, _exts in (
        ("internal", "web.sphinx.extension", meta["web"]["sphinx"].get("extension", {})),
        ("external", "web.extension", meta["web"].get("extension", {})),
    ):
        for _ext_id, _ext in _exts.items():
            # Add extension name to `extensions`
            _ext_import_name = _ext["dependency"]["import_name"]
            if _ext_import_name in extensions:
                raise RuntimeError(
                    f"Duplicate extension name '{_ext_import_name}' for Sphinx "
                    f"{_ext_type} extension defined at "
                    f"`{_ext_path}.{_ext_id}.dependency.import_name`. "
                    "Please ensure that no two extensions have the same import name.",
                )
            # Add extension configurations to global variables
            extensions.append(_ext_import_name)
            for _conf_key, _conf_value in _ext.get("config", {}).items():
                if _conf_key not in global_vars:
                    global_vars[_conf_key] = _conf_value
                    continue
                _existing_val = global_vars[_conf_key]
                if isinstance(_existing_val, list):
                    if isinstance(_conf_value, list):
                        _existing_val.extend(_conf_value)
                        continue
                    raise RuntimeError(
                        f"Sphinx configuration key '{_conf_key}' is already set to a list, "
                        f"but Sphinx {_ext_type} extension "
                        f"defined at `{_ext_path}.{_ext_id}.config` is a trying to add "
                        f"a value of type '{type(_conf_value)}': {_conf_value}."
                    )
                if isinstance(_existing_val, dict):
                    if isinstance(_conf_value, dict):
                        for _sub_key, _sub_value in _conf_value.items():
                            if _sub_key in _existing_val:
                                raise RuntimeError(
                                    f"Duplicate configuration key '{_sub_key}' for Sphinx {_ext_type} "
                                    f"extension defined at `{_ext_path}.{_ext_id}.config.{_conf_key}`. "
                                    "Please ensure that no configuration key is defined more than once.",
                                )
                            _existing_val[_sub_key] = _sub_value
                        continue
                    raise RuntimeError(
                        f"Sphinx configuration key '{_conf_key}' is already set to a dictionary, "
                        f"but Sphinx {_ext_type} extension "
                        f"defined at `{_ext_path}.{_ext_id}.config` is a trying to add "
                        f"a value of type '{type(_conf_value)}': {_conf_value}."
                    )
                raise RuntimeError(
                    f"Duplicate configuration key '{_conf_key}' for Sphinx {_ext_type} extension "
                    f"defined at `{_ext_path}.{_ext_id}.config`. "
                    "Please ensure that no configuration key is defined more than once.",
                )
    return


def _add_extension_ablog():
    if "blog_authors" in global_vars:
        return
    blog_authors = {}
    global_vars["blog_authors"] = blog_authors
    for person_id, person in meta["team"].items():
        for contact_type in ("website", "github", "twitter", "linkedin", "researchgate", "orcid", "email"):
            if contact_type in person:
                url = person[contact_type]["url"]
                break
        else:
            url = meta["web"]["url"]["home"]
        blog_authors[person_id] = (person["name"]["full"], url)
    return




_path_root, _path_to_root = _get_path_repo_root()

# Read control center configurations
try:
    with open(_path_root / _METADATA_FILEPATH) as f:
        meta = _json.load(f)
except _json.JSONDecodeError as e:
    raise RuntimeError(
        f"Could not read control center metadata file at {_METADATA_FILEPATH}."
        "Please ensure that the file is a valid JSON file.",
    ) from e

global_vars = globals()


_add_sphinx()
_add_version()
_add_css_and_js_files()
_add_theme()
_add_extensions()
_add_extension_ablog()

html_context = global_vars.get("html_context", dict()) | {
    "pp_meta": meta,
    "pp_title_sep": global_vars.get("html_secnumber_suffix"),
}






# TODO: KEEP?
def _maintainers(self) -> list[dict]:
    def sort_key(val):
        return val[1]["issue"] + val[1]["pull"] + val[1]["discussion"]

    maintainers = dict()
    for role in ["issue", "discussion"]:
        if not self._data["maintainer"].get(role):
            continue
        for assignees in self._data["maintainer"][role].values():
            for assignee in assignees:
                entry = maintainers.setdefault(assignee, {"issue": 0, "pull": 0, "discussion": 0})
                entry[role] += 1
    codeowners_entries = self._data["maintainer"].get("pull", {}).get("reviewer", {}).get("by_path")
    if codeowners_entries:
        for codeowners_entry in codeowners_entries:
            for reviewer in codeowners_entry[list(codeowners_entry.keys())[0]]:
                entry = maintainers.setdefault(reviewer, {"issue": 0, "pull": 0, "discussion": 0})
                entry["pull"] += 1
    maintainers_list = [
        {**self._get_github_user(username.lower()), "roles": roles}
        for username, roles in sorted(maintainers.items(), key=sort_key, reverse=True)
    ]
    _logger.info("Successfully generated all maintainers data")
    _logger.debug("Generated data:", code=str(maintainers_list))
    return maintainers_list
