

# Standard libraries
import importlib
import json
from pathlib import Path
from typing import Any, Literal, Union




"""
Project information

References
----------
* https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
"""



author: str = ", ".join(
    [_author["name"] for _author in meta["author"]["entries"] if _author["name"]],
)
"""Authors' names"""



release: str = importlib.import_module(meta["package"]["import_name"]).__version__
"""Full version, including alpha/beta/rc tags"""

version: str = ".".join(release.split(".")[:3])
"""SemVer version in format X.Y.Z"""


"""
General configuration

References
----------
* https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration
"""


# source_suffix: Union[str, List[str], Dict[str, str]] = {
#   '.rst': 'restructuredtext',
#   '.txt': 'restructuredtext',
#   '.md': 'markdown',
# }
# source_encoding: str = 'utf-8-sig'
root_doc: str = "index"
"""Name of the root (homepage) document"""

exclude_patterns: list[str] = [
    "**Thumbs.db",
    "**.DS_Store",
    "**.ipynb_checkpoints",
    "**README.md",
]
"""A list of glob-style patterns to exclude from source files"""
# include_patterns: List[str] = ['**']
"""A list of glob-style patterns to include in source files"""

templates_path: list[str] = [
    "_templates",
]  # Ref: https://www.sphinx-doc.org/en/master/development/templating.html
"""A list of directories containing extra templates"""
# template_bridge: str = ''
# rst_epilog: str = ''
# rst_prolog: str = ''
# primary_domain: Union[str, None] = 'py'
# default_role: Union[str, None] = None
# keep_warnings: bool = False
# suppress_warnings: List[str] = []
needs_sphinx: str = "7.2.6"

needs_extensions: dict[str, str] = {"sphinx_design": "0.5", "myst_parser": "2.0"}
# manpages_url: str = ""
nitpicky: bool = True
"""Warn about all references where the target cannot be found"""
# nitpick_ignore: List[Tuple[str, str]] = [('py:func', 'int'), ('envvar', 'LD_LIBRARY_PATH')]
# nitpick_ignore_regex: List[Tuple[str, str]] =[(r'py:.*', r'foo.*bar\.B.*')]
numfig: bool = True
"""Automatically number figures, tables and code-blocks that have a caption"""

numfig_format: dict[str, str] = {
    "figure": "Fig. %s",
    "table": "Table %s",
    "code-block": "Snippet %s",
    "section": "Section %s",
}

numfig_secnum_depth: int = 2

smartquotes: bool = True
# smartquotes_action: str = "qDe"
# smartquotes_excludes: Dict[str, List[str]] = {'languages': ['ja'], 'builders': ['man', 'text']}
# user_agent: str = "Sphinx/X.Y.Z requests/X.Y.Z python/X.Y.Z"
tls_verify: bool = True
# tls_cacerts: str = ''
# today: str = ''
# today_fmt: str = '%b %d, %Y'
highlight_language: str = "python3"
# highlight_options: Union[Dict[str, Any], Dict[str, Dict[str, Any]]]
pygments_style: str = "default"

maximum_signature_line_length: Union[int, None] = 80

add_function_parentheses: bool = True

add_module_names: bool = True

toc_object_entries: bool = True

toc_object_entries_show_parents: Literal["domain", "hide", "all"] = "all"  # New in version 5.2

show_authors: bool = True
# modindex_common_prefix: List[str] = []
trim_footnote_reference_space: bool = True

trim_doctest_flags: bool = True

strip_signature_backslash: bool = False

option_emphasise_placeholders: bool = True


"""
Options for internationalization

References
----------
* https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-internationalization
"""
language = "en"
# locale_dirs: List[str] = ['locales']
# gettext_allow_fuzzy_translations: bool = False
# gettext_compact: Union[bool, str]
# gettext_uuid: bool = False
# gettext_location: bool = True
# gettext_auto_build: bool = True
# gettext_additional_targets: List[str] = []
# figure_language_filename: str = '{root}.{language}{ext}'
"""
Options for math

References
----------
* https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-math
"""
math_number_all: bool = True

math_eqref_format: str = "Eq. {number}"

math_numfig: bool = True


"""
Options for HTML output

References
----------
* https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output
"""
html_theme: str = "pydata_sphinx_theme"

html_theme_options: dict[str, Any] = {
    # `logo` is added due to this issue:
    #  https://github.com/pydata/pydata-sphinx-theme/issues/1094#issuecomment-1368264928
    "logo": {
        # "text": "This will appear just after the logo image",
        # "link": "URL or path that logo links to"
        "image_light": "_static/logo_simple_light.svg",
        "image_dark": "_static/logo_simple_dark.svg",
        "alt_text": meta["name"],
    },
    "announcement": meta["url"]["website"]["announcement"],
    # --- Header / Navigation Bar ---
    # Left section
    "navbar_start": ["navbar-logo"],
    # Middle menu
    "navbar_center": ["navbar-nav"],
    # Right section
    "navbar_end": ["navbar-icon-links", "theme-switcher"],
    # Persistent right section
    "navbar_persistent": ["search-button"],
    # Alignment of `navbar_center`
    "navbar_align": "left",  # {"left", "right", "content"}
    "search_bar_text": f"Search {meta['name']} ...",
    # "primary_sidebar_end": ["indices"],
    "secondary_sidebar_items": [
        "page-toc",
        "last-updated",
        "edit-this-page",
        "sourcelink",
    ],
    "show_prev_next": True,
    "footer_start": ["version", "copyright", "pypackit_ver"],
    "footer_end": ["quicklinks"],  # "sphinx-version", "theme-version"
    "show_nav_level": 1,
    "navigation_depth": 5,
    "show_toc_level": 2,
    "header_links_before_dropdown": 7,
    "icon_links": meta["web"]["navbar_icons"],
    "icon_links_label": "External links",
    "use_edit_page_button": True,
    # Code highlighting color themes
    # Refs:
    #  https://pygments.org/styles/
    #  https://pydata-sphinx-theme.readthedocs.io/en/stable/user_guide/styling.html#configure-pygments-theme
    "pygment_light_style": "default",
    "pygment_dark_style": "monokai",
}
# ----------------------------- Dynamically fill html_theme_options ---------------------------------------
# The following part dynamically reads analytics options from the metadata, and sets them up.
# Ref: https://pydata-sphinx-theme.readthedocs.io/en/stable/user_guide/analytics.html
_analytics = meta["web"].get("analytics")
if _analytics:
    _plausible_analytics = _analytics.get("plausible")
    if (
        _plausible_analytics
        and _plausible_analytics.get("domain")
        and _plausible_analytics.get("url")
    ):
        html_theme_options["analytics"] = {
            "plausible_analytics_domain": _plausible_analytics["domain"],
            "plausible_analytics_url": _plausible_analytics["url"],
        }
    _google_analytics = _analytics.get("google")
    if _google_analytics and _google_analytics.get("id"):
        html_theme_options["analytics"] = {
            "google_analytics_id": _google_analytics["id"],
        }
# -------------------------------------------------------------------------
# -------------------------------------------------------------------------
# html_theme_path: List[str] = []
# html_style: str
html_title: str = meta["name"]

html_short_title: str = meta["name"]
# html_baseurl: str = ''
html_secnumber_suffix: str = ". "
html_context = {
    # PyData variables
    "github_user": meta["owner"]["username"],
    "github_repo": meta["repo"]["name"],
    "github_version": meta["repo"]["default_branch"],
    "doc_path": f'{meta["path"]["dir"]["website"]}/source',
    "default_mode": "auto",  # Default theme mode: {'light', 'dark', 'auto'}
    # PyPackIT variables
    "pp_meta": meta,
    "pp_title_sep": html_secnumber_suffix,
}
# html_logo: Union[str, None] = ''
html_favicon: str | None = (
    f"{'../'*_num_up}{meta['path']['dir']['control']}/ui/branding/favicon.png"
)

html_static_path: list[str] = [
    "_static",
    f"{'../'*_num_up}{meta['path']['dir']['control']}/ui/branding",
    # Due to an issue with the PyData Sphinx Theme, the logo files used in the navbar are explicitly
    # added to the root of static path, since PyData always looks there, regardless of the set path.
    # Ref:
    #  https://github.com/pydata/pydata-sphinx-theme/issues/1325
    #  https://github.com/pydata/pydata-sphinx-theme/issues/1328
    #  https://github.com/pydata/pydata-sphinx-theme/issues/1385
    # "../../../.meta/ui/logo/simple_dark.svg",
    # "../../../.meta/ui/logo/simple_light.svg",
]
html_extra_path: list[str] = ["404.html"]
html_css_files: list[Union[str, tuple[str, dict[str, str]]]] = [
    str(path).removeprefix(f"{html_static_path[0]}/").removesuffix("_t")
    for glob in ["**/*.css", "**/*.css_t"]
    for path in (Path(html_static_path[0]) / "css").glob(glob)
]
"""A list of CSS files.

Automatically include all CSS files in the `_static/css` directory.
"""
# html_js_files: List[Union[str, Tuple[str, Dict[str, str]]]]
html_last_updated_fmt: Union[str, None] = "%b %d, %Y"
"""Inserte a ‘Last updated on:’ timestamp at every page bottom, using the given strftime() format."""

html_permalinks: bool = True

html_permalinks_icon: str = "¶"


# html_additional_pages: Dict[str, str]
# html_domain_indices: Union[bool, List[str]] = True
# html_use_index: bool = True
# html_split_index: bool = False
# html_copy_source: bool = True
html_show_sourcelink: bool = False

html_sourcelink_suffix: str = ".txt"

html_use_opensearch: str = meta["url"]["website"]["base"]
# html_file_suffix: str = '.html'
# html_link_suffix: str = '.html'
html_show_copyright: bool = True

html_show_search_summary: bool = True

html_show_sphinx: bool = False
# html_output_encoding: str = 'utf-8'
# html_compact_lists: bool = True
html_search_language: str = "en"
# html_search_options: Dict[str, Any]
# html_search_scorer: str
# html_scaled_image_link: bool = True
# html_math_renderer: str = 'mathjax'
# html4_writer: bool = False



latex_documents: list[tuple[str, str, str, str, str, bool]] = [
    (
        root_doc,
        f"{meta['package']['name']}_docs.tex",
        f"{meta['name']} Documentation",
        " \\and ".join(
            [_author["name"] for _author in meta["author"]["entries"] if _author["name"]],
        ),
        "manual",
        False,
    ),
]

latex_logo: str = f"{'../'*_num_up}{meta['path']['dir']['control']}/ui/branding/logo_full_light.png"  # Doesn't work with SVG files


