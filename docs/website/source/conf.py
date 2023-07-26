"""Configuration file for the Sphinx documentation builder.

References
----------
* Full list of built-in configuration values:
    https://www.sphinx-doc.org/en/master/usage/configuration.html
"""


from typing import Any, Dict, Union, List, Literal, Tuple, NoReturn
import importlib
from pathlib import Path

import pypackit


def setup(app):
    # register custom config values
    # app.add_config_value(name='rd_meta', default=dict(), rebuild='html', types=[dict])
    return


meta = pypackit.metadata(path_root=Path(__file__).parents[3])


"""
Project information

References
----------
* https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
"""

project: str = meta['project']['name']
"""Name of the project"""

author: str = ', '.join([_author['name'] for _author in meta['project']['authors']])
"""Authors' names"""

project_copyright: Union[str, List[str]] = (
    f"{meta['project']['copyright_year']} {meta['project']['owner']['name']}"
)
"""Copyright statement(s)"""

release: str = getattr(importlib.import_module(meta['package']['name']), '__version__')
"""Full version, including alpha/beta/rc tags"""

version: str = '.'.join(release.split('.')[:3])
"""SemVer version in format X.Y.Z"""


"""
General configuration

References
----------
* https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration
"""

extensions: List[str] = [
    'sphinx.ext.autosummary',
    'sphinx.ext.autodoc',
    'sphinx.ext.mathjax',
    'sphinx.ext.viewcode',
    'sphinx.ext.intersphinx',
    'sphinx.ext.extlinks',
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    # --- 3rd-party extensions ---
    'myst_parser',
    'sphinx_design',
    # For adding blog to website;
    #   Ref: https://ablog.readthedocs.io/en/stable/index.html
    'ablog',
    # For displaying a copy button next to code blocks;
    #   Ref: https://sphinx-copybutton.readthedocs.io/en/latest/
    'sphinx_copybutton',
    'sphinx_last_updated_by_git',
    # For including SVG files in LaTeX
    #   Ref: https://github.com/missinglinkelectronics/sphinxcontrib-svg2pdfconverter
    #        https://nbsphinx.readthedocs.io/en/latest/markdown-cells.html
    #   Note: Doesn't work on `latex_logo`.
    'sphinxcontrib.rsvgconverter',
    # For adding Open Graph meta tags to HTML output files:
    'sphinxext.opengraph',
]
"""List of required Sphinx extensions"""

# source_suffix: Union[str, List[str], Dict[str, str]] = {
#   '.rst': 'restructuredtext',
#   '.txt': 'restructuredtext',
#   '.md': 'markdown',
# }

# source_encoding: str = 'utf-8-sig'

root_doc: str = 'index'
"""Name of the root (homepage) document"""

exclude_patterns: List[str] = ['**Thumbs.db', '**.DS_Store', '**.ipynb_checkpoints', '**README.md']
"""A list of glob-style patterns to exclude from source files"""

# include_patterns: List[str] = ['**']
"""A list of glob-style patterns to include in source files"""

templates_path: List[str] = ['_templates']  # Ref: https://www.sphinx-doc.org/en/master/development/templating.html
"""A list of directories containing extra templates"""

# template_bridge: str = ''

# rst_epilog: str = ''

# rst_prolog: str = ''

# primary_domain: Union[str, None] = 'py'

# default_role: Union[str, None] = None

# keep_warnings: bool = False

# suppress_warnings: List[str] = []

needs_sphinx: str = '6.2.1'

needs_extensions: Dict[str, str] = {
    'sphinx_design': '0.4.1',
    'myst_parser': '2.0.0'
}

# manpages_url: str = ""

nitpicky: bool = True
"""Warn about all references where the target cannot be found"""

# nitpick_ignore: List[Tuple[str, str]] = [('py:func', 'int'), ('envvar', 'LD_LIBRARY_PATH')]

# nitpick_ignore_regex: List[Tuple[str, str]] =[(r'py:.*', r'foo.*bar\.B.*')]

numfig: bool = True
"""Automatically number figures, tables and code-blocks that have a caption"""

numfig_format: Dict[str, str] = {
    'figure': 'Fig. %s',
    'table': 'Table %s',
    'code-block': 'Snippet %s',
    'section': 'Section %s'
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

highlight_language: str = 'python3'

# highlight_options: Union[Dict[str, Any], Dict[str, Dict[str, Any]]]

pygments_style: str = 'default'

maximum_signature_line_length: Union[int, None] = 80

add_function_parentheses: bool = True

add_module_names: bool = True

toc_object_entries: bool = True

toc_object_entries_show_parents: Literal['domain', 'hide', 'all'] = 'all'  # New in version 5.2

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

math_eqref_format: str = 'Eq. {number}'

math_numfig: bool = True


"""
Options for HTML output

References
----------
* https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output
"""
html_theme: str = 'pydata_sphinx_theme'

html_theme_options: Dict[str, Any] = {
    # `logo` is added due to this issue:
    #  https://github.com/pydata/pydata-sphinx-theme/issues/1094#issuecomment-1368264928
    "logo": {
        # "text": "This will appear just after the logo image",
        # "link": "URL or path that logo links to"
        "image_light": "_static/img/logo/logo_light.svg",
        "image_dark": "_static/img/logo/logo_dark.svg",
        "alt_text": meta['project']['name'],
    },
    "announcement": meta['url']['announcement'],

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
    "navbar_align": "content",  # {"left", "right", "content"}

    "search_bar_text": f"Search {meta['project']['name']} ...",
    # "primary_sidebar_end": ["indices"],
    "secondary_sidebar_items": ["page-toc", "last-updated", "edit-this-page", "sourcelink", ],
    "show_prev_next": True,
    "footer_start": ["version", "copyright", "pypackit_ver"],
    "footer_end": ["quicklinks"],  # "sphinx-version", "theme-version"

    "show_nav_level": 1,
    "navigation_depth": 3,

    "show_toc_level": 2,

    "header_links_before_dropdown": 7,

    "icon_links": [],  # set dynamically below
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
# The following part dynamically reads header icon flags from the metadata,
# and adds the corresponding icons to `html_theme_options['icon_links']`.
_navbar_defaults = {
    "repo": {
        "name": "Source Repository",
        "icon": "fa-brands fa-github",
        "url": meta['url']['github']['home']
    },
    "issues": {
        "name": "Issues",
        "icon": "fa-regular fa-circle-dot",
        "url": meta['url']['github']['issues']['home']
    },
    "pull_requests": {
        "name": "Pull Requests",
        "icon": "fa-solid fa-code-pull-request",
        "url": meta['url']['github']['pulls']['home']
    },
    "discussions": {
        "name": "Discussions",
        "icon": "fa-solid fa-comments",
        "url": meta['url']['github']['discussions']['home']
    },
    "email": {
        "name": "Email",
        "icon": "fa-regular fa-envelope",
        "url": f"mailto:{meta['maintainer']['email']['main']}"
    },
    "license": {
        "name": "License",
        "icon": "fa-solid fa-copyright",
        "url": meta['url']['license']
    },
    "pypi": {
        "name": "PyPI Distribution",
        "icon": "fa-brands fa-python",
        "url": meta['url']['pypi']
    },
    "twitter": {
        "name": "Twitter",
        "icon": "fa-brands fa-twitter",
        "url": meta['project']['owner']['external_urls'].get('twitter', '')
    },
    "linkedin": {
        "name": "LinkedIn",
        "icon": "fa-brands fa-linkedin",
        "url": meta['project']['owner']['external_urls'].get('linkedin', '')
    },
    "researchgate": {
        "name": "ResearchGate",
        "icon": "fa-brands fa-researchgate",
        "url": meta['project']['owner']['external_urls'].get('researchgate', '')
    },
    "orcid": {
        "name": "ORCiD",
        "icon": "fa-brands fa-orcid",
        "url": meta['project']['owner']['external_urls'].get('orcid', '')
    },
}


def _add_icon_link(
        name: str,
        url: str,
        icon: str,
        type: Literal['fontawesome', 'url', 'local'] = 'fontawesome'
) -> NoReturn:
    """Add an icon link to `html_theme_options['icon_links']`."""
    html_theme_options['icon_links'].append({"name": name, "url": url, "icon": icon, "type": type})
    return


for _icon in meta['website']['navbar_icons']:
    _icon_id = _icon.pop('id', None)
    if _icon_id:
        _def = _navbar_defaults[_icon_id]
        _icon.setdefault('name', _def['name'])
        _icon.setdefault('url', _def['url'])
        _icon.setdefault('icon', _def['icon'])
        if _icon.get('icon'):
            _icon.setdefault('type', 'fontawesome')
        else:
            _icon['type'] = _def.get('type') or 'fontawesome'
        _add_icon_link(**_icon)
    else:
        _add_icon_link(**_icon)
# -------------------------------------------------------------------------
# -------------------------------------------------------------------------
# -------------------------------------------------------------------------
# The following part dynamically reads analytics options from the metadata, and sets them up.
# Ref: https://pydata-sphinx-theme.readthedocs.io/en/stable/user_guide/analytics.html
_analytics = meta['website'].get('analytics')
if _analytics:
    _plausible_analytics = _analytics.get('plausible')
    if _plausible_analytics and _plausible_analytics.get('domain') and _plausible_analytics.get('url'):
        html_theme_options['analytics'] = {
            "plausible_analytics_domain": _plausible_analytics['domain'],
            "plausible_analytics_url": _plausible_analytics['url'],
        }
    _google_analytics = _analytics.get('google')
    if _google_analytics and _google_analytics.get('id'):
        html_theme_options['analytics'] = {
            "google_analytics_id": _google_analytics['id'],
        }
# -------------------------------------------------------------------------
# -------------------------------------------------------------------------


# html_theme_path: List[str] = []

# html_style: str

html_title: str = meta['project']['name']

html_short_title: str = meta['project']['name']

# html_baseurl: str = ''

html_context = {

    # PyData variables
    "github_user": meta['project']['owner']['login'],
    "github_repo": meta['project']['repo']['name'],
    "github_version": meta['project']['repo']['default_branch'],
    "doc_path": meta['path']['docs']['website']['source'],
    "default_mode": "auto",  # Default theme mode: {'light', 'dark', 'auto'}

    # PyPackIT variables
    "pp_meta": meta,
}

# html_logo: Union[str, None] = '_static/logo/logo_light.svg'

html_favicon: Union[str, None] = '_static/img/logo/icon.png'

html_static_path: List[str] = ['_static']

# html_extra_path: List[str] = []

html_css_files: List[Union[str, Tuple[str, Dict[str, str]]]] = [
    str(path).removeprefix(f"{html_static_path[0]}/")
    for path in (Path(html_static_path[0]) / 'css').glob('**/*.css')
]
"""A list of CSS files.

Automatically include all CSS files in the `_static/css` directory.
"""

# html_js_files: List[Union[str, Tuple[str, Dict[str, str]]]]

html_last_updated_fmt: Union[str, None] = '%b %d, %Y'
"""Inserte a ‘Last updated on:’ timestamp at every page bottom, using the given strftime() format."""

html_permalinks: bool = True

html_permalinks_icon: str = '¶'

html_sidebars: Dict[str, Union[List[str], str]] = {
    # "**": ["sidebar-nav-bs"],
    "news/**": [
        'ablog/postcard.html',
        'ablog/recentposts.html',
        'ablog/tagcloud.html',
        'ablog/categories.html',
        'ablog/archives.html',
    ]
}

# html_additional_pages: Dict[str, str]

# html_domain_indices: Union[bool, List[str]] = True

# html_use_index: bool = True

# html_split_index: bool = False

# html_copy_source: bool = True

html_show_sourcelink: bool = True

html_sourcelink_suffix: str = ".txt"

html_use_opensearch: str = meta['url']['website']['base']

# html_file_suffix: str = '.html'

# html_link_suffix: str = '.html'

html_show_copyright: bool = True

html_show_search_summary: bool = True

html_show_sphinx: bool = False

# html_output_encoding: str = 'utf-8'

# html_compact_lists: bool = True

html_secnumber_suffix: str = '. '

html_search_language: str = 'en'

# html_search_options: Dict[str, Any]

# html_search_scorer: str

# html_scaled_image_link: bool = True

# html_math_renderer: str = 'mathjax'

# html4_writer: bool = False


"""
Options for single HTML output

References
----------
* https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-single-html-output
"""

# singlehtml_sidebars: Dict[str, str]


"""
Options for HTML help output

References
----------
* https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-help-output
"""
htmlhelp_basename: str = f"{meta['project']['name']} Docs"

# htmlhelp_file_suffix: str = '.html'

# htmlhelp_link_suffix: str = '.html'


"""
Options for epub output

Notes
-----
Options are only partially implemented.
See reference for a full list.

References
----------
* https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-epub-output
"""
epub_show_urls: Literal['inline', 'footnote', 'no'] = 'footnote'


"""
Options for LaTeX output

Notes
-----
Options are only partially implemented.
See reference for a full list.

References
----------
* https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-latex-output
* https://www.sphinx-doc.org/en/master/latex.html
"""

latex_engine: Literal['pdflatex', 'xelatex', 'lualatex', 'platex', 'uplatex'] = 'lualatex'

latex_documents: List[Tuple[str, str, str, str, str, bool]] = [
    (
        root_doc,
        f"{meta['package']['name']}_docs.tex",
        f"{meta['project']['name']} Documentation",
        ' \\and '.join([_author['name'] for _author in meta['project']['authors']]),
        'manual',
        False
    ),
]

# latex_logo: str = "_static/img/logo/logo_light.svg" # TODO: Doesn't work with SVG files

latex_show_pagerefs: bool = True

latex_show_urls: Literal['inline', 'footnote', 'no'] = 'footnote'

latex_elements: Dict[str, str] = {
    'papersize': 'a4paper',  # {'letterpaper', 'a4paper'}
    'pointsize': '11pt',
    'figure_align': 'htbp',
    'fontpkg': r'''
\setmainfont{DejaVu Serif}
\setsansfont{DejaVu Sans}
\setmonofont{DejaVu Sans Mono}
''',
    'preamble': r'''
\usepackage[titles]{tocloft}
\usepackage{fontspec}
\usepackage{fontawesome}
\cftsetpnumwidth {1.25cm}\cftsetrmarg{1.5cm}
\setlength{\cftchapnumwidth}{0.75cm}
\setlength{\cftsecindent}{\cftchapnumwidth}
\setlength{\cftsecnumwidth}{1.25cm}
''',
    'fncychap': r'\usepackage[Bjornstrup]{fncychap}',
    'printindex': r'\footnotesize\raggedright\printindex',
    'passoptionstopackages': '\\PassOptionsToPackage{warn}{textcomp}',
}

# latex_additional_files: List[str] = []

latex_theme: Literal['manual', 'howto'] = 'manual'

# latex_theme_options: Dict[str, Any] = {}

# latex_theme_path: List[str] = []


"""
Options for manual page output

Notes
-----
Options are only partially implemented.
See reference for a full list.

References
----------
* https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-manual-page-output
"""
man_pages: List[Tuple[str, str, str, Union[str, List[str]], str]] = [
    (
        root_doc,
        meta['package']['name'],
        f"{meta['project']['name']} Documentation",
        [_author['name'] for _author in meta['project']['authors']],
        "1"
    )
]


"""
Options for Texinfo output

Notes
-----
Options are only partially implemented.
See reference for a full list.

References
----------
* https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-texinfo-output
"""
texinfo_documents: List[Tuple[str, str, str, str, str, str, str, bool]] = [
    (
        root_doc,
        f"{meta['package']['name']}_docs",
        f"{meta['project']['name']} Documentation",
        '@*'.join([_author['name'] for _author in meta['project']['authors']]),
        meta['package']['name'],
        meta['project']['tagline'],
        'Documentation',
        False,
    ),
]


"""
Options for Python domain

References
----------
* https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-the-python-domain
"""
python_display_short_literal_types: bool = True

python_use_unqualified_type_names: bool = False

python_maximum_signature_line_length: int = 80


# ----------------------------------- End of Sphinx Config ----------------------------------------
# *************************************************************************************************
# ----------------------------------- Start of Extensions Config ----------------------------------


"""
Options for `myst_parser`

Notes
-----
Options are only partially implemented.
See reference for a full list.

References
----------
* https://myst-parser.readthedocs.io/en/latest/configuration.html
"""

# --- Extensions ----
#  Ref: https://myst-parser.readthedocs.io/en/latest/syntax/optional.html
myst_enable_extensions: List[str] = [
    "substitution",
    "smartquotes",
    "replacements",
    "dollarmath",
    "amsmath",
    "colon_fence",
    "deflist",
    "tasklist",
    "attrs_inline",
    "attrs_block",
]

myst_heading_anchors: int = 6

# myst_html_meta: dict[str, str] = {}

# ------ MyST Extensions Settings ------
# Ref: https://myst-parser.readthedocs.io/en/latest/configuration.html#extensions
myst_substitutions = {"meta": meta}


"""
Options for `sphinx_design`

"""
sd_fontawesome_latex = True


"""
Options for `sphinx.ext.autosummary`

References
----------
* https://www.sphinx-doc.org/en/master/usage/extensions/autosummary.html#generating-stub-pages-automatically
"""
# autosummary_context: Dict

autosummary_generate: bool = True

autosummary_generate_overwrite: bool = True

autosummary_imported_members: bool = False

autosummary_ignore_module_all: bool = False


"""
Options for `ablog`

Notes
-----
Options are only partially implemented.
See reference for a full list.

References
----------
* https://ablog.readthedocs.io/en/stable/manual/ablog-configuration-options.html
"""

blog_path: str = meta['website']['blog_dir_name']
blog_baseurl: str = meta['url']['website']['base']

blog_post_pattern: list[str] = [
    f"{meta['website']['blog_dir_name']}/posts/*.rst",
    f"{meta['website']['blog_dir_name']}/posts/*.md"
]
post_auto_image: int = 1
blog_feed_archives: bool = True
fontawesome_included: bool = True

if meta['website']['disqus_shortname']:
    disqus_shortname: str = meta['website']['disqus_shortname']


"""
Options for `sphinx.ext.intersphinx`

Notes
-----
Options are only partially implemented.
See reference for a full list.

References
----------
* https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html
"""
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'numpy': ('https://numpy.org/doc/stable', None),
    'matplotlib': ('https://matplotlib.org/stable', None),
}


"""
sphinxext.opengraph

Options for `sphinxext.opengraph` extension.

References
----------
* https://sphinxext-opengraph.readthedocs.io/en/latest/
* https://github.com/wpilibsuite/sphinxext-opengraph
"""
# TODO: Fill me
