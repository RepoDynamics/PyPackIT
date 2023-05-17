"""Configuration file for the Sphinx documentation builder.

References
----------
* Full list of built-in configuration values:
    https://www.sphinx-doc.org/en/master/usage/configuration.html
"""


from typing import Any, Dict, Union, List, Literal, Tuple, NoReturn
import json
import datetime


# Open and read the metadata file
with open("../../metadata.json") as f:
    _data = json.load(f)
# Generate recurring variables from the metadata to use in several places
_github_link = f"https://github.com/{_data['github']['user_name']}/{_data['github']['repo_name']}"
_author_names_in_order = [
    _author['name'] for _author in (_data['contact']['authors'] + _data['contact']['corresponding_authors'])
]

"""
Project information

References
----------
* https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
"""
project: str = _data["project"]["name"]

author: str = ', '.join(
    [_author['name'] for _author in _data['contact']['authors']]
    + [_author['name'] for _author in _data['contact']['corresponding_authors']]
)

copyright: str = (
    (
        f"{_data['copyright']['start_year']}--{datetime.date.today().year}, "
        if _data['copyright']['start_year'] != datetime.date.today().year else
        f"{_data['copyright']['start_year']}, "
    ) +
    (
        _orgname if (_orgname := _data['contact']['organization']['name']) != ''
        else _data['contact']['corresponding_authors'][0]['name']
     )
)

project_copyright: Union[str, List[str]] = copyright

version: str = _data['package']['short_version']

release: str = _data['package']['long_version']


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
    'ablog',
    # For displaying a copy button next to code blocks;
    #   Ref: https://sphinx-copybutton.readthedocs.io/en/latest/
    'sphinx_copybutton',
    'sphinx_last_updated_by_git'
]

# source_suffix: Union[str, List[str], Dict[str, str]] = {
#   '.rst': 'restructuredtext',
#   '.txt': 'restructuredtext',
#   '.md': 'markdown',
# }

# source_encoding: str = 'utf-8-sig'

root_doc: str = 'index'

exclude_patterns: List[str] = ['Thumbs.db', '.DS_Store', '**.ipynb_checkpoints', 'README.md']

# include_patterns: List[str] = ['**']

templates_path: List[str] = ['_templates']

# template_bridge: str = ''

# rst_epilog: str = ''

# rst_prolog: str = ''

# primary_domain: Union[str, None] = 'py'

# default_role: Union[str, None] = None

# keep_warnings: bool = False

# suppress_warnings: List[str] = []

needs_sphinx: str = '5.3'

# TODO: Fill me
# needs_extensions: Dict[str, str] = {'sphinxcontrib.something': '1.5'}

# manpages_url: str = ""

# nitpicky: bool = False

# nitpick_ignore: List[Tuple[str, str]] = [('py:func', 'int'), ('envvar', 'LD_LIBRARY_PATH')]

# nitpick_ignore_regex: List[Tuple[str, str]] =[(r'py:.*', r'foo.*bar\.B.*')]

numfig: bool = True

# numfig_format: Dict[str, str] = {
#     'figure': 'Fig. %s',
#     'table': 'Table %s',
#     'code-block': 'Listing %s',
#     'section': 'Section %s'
# }

# numfig_secnum_depth: int = 1

# smartquotes: bool = True

# smartquotes_action: str = "qDe"

# smartquotes_excludes: Dict[str, List[str]] = {'languages': ['ja'], 'builders': ['man', 'text']}

# user_agent: str = "Sphinx/X.Y.Z requests/X.Y.Z python/X.Y.Z"

# tls_verify: bool = True

# tls_cacerts: str = ''

# today: str = ''

# today_fmt: str = '%b %d, %Y'

# highlight_language: str = 'default'

# highlight_options: Union[Dict[str, Any], Dict[str, Dict[str, Any]]]

pygments_style: str = 'default'

maximum_signature_line_length: Union[int, None] = 99

# add_function_parentheses: bool = True

# add_module_names: bool = True

# toc_object_entries: bool = True

toc_object_entries_show_parents: Literal['domain', 'hide', 'all'] = 'all'  # New in version 5.2

show_authors: bool = True

# modindex_common_prefix: List[str] = []

trim_footnote_reference_space: bool = True

# trim_doctest_flags: bool = True

# strip_signature_backslash: bool = False

# option_emphasise_placeholders: bool = False


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
        # "text": "an open-source Python library for computer-aided drug design",
        "image_light": "_static/logo/logo.svg",
        "image_dark": "_static/logo/logo.svg",
    },

    "announcement": (
        f"https://raw.githubusercontent.com/{_data['github']['user_name']}/"
        f"{_data['github']['repo_name']}/{_data['github']['branch_name']}/"
        f"{_data['docs']['path']}/_templates/announcement.html"
    ),

    # --- Header / Navigation Bar ---
    # Left section
    "navbar_start": ["navbar-logo"],
    # Middle menu
    "navbar_center": ["navbar-nav"],
    # Right section
    "navbar_end": ["theme-switcher", "navbar-icon-links"],
    # Persistent right section
    "navbar_persistent": ["search-button"],
    # Alignment of `navbar_center`
    "navbar_align": "content",  # {"left", "right", "content"}

    "search_bar_text": f"Search {_data['project']['name']} ...",
    "primary_sidebar_end": ["indices"],
    "secondary_sidebar_items": ["page-toc", "edit-this-page", "sourcelink"],
    "show_prev_next": True,
    "footer_start": ["copyright", "sphinx-version", "theme-version"],
    "footer_end": [],

    "show_nav_level": 1,
    "navigation_depth": 3,

    "show_toc_level": 2,

    "header_links_before_dropdown": 5,

    "icon_links": [
        {
            "name": "Source Repository",
            "url": _github_link,
            "icon": "fa-brands fa-github",
        },
        {
            "name": "Issues",
            "url": f"{_github_link}/issues",
            "icon": "fa-regular fa-circle-dot",
        },
        {
            "name": "Pull Requests",
            "url": f"{_github_link}/pulls",
            "icon": "fa-solid fa-code-pull-request",
        },
        {
            "name": "Discussions",
            "url": f"{_github_link}/discussions",
            "icon": "fa-solid fa-comments",
        },
        {
            "name": "Email",
            "url": f"mailto:{_data['project']['email']}",
            "icon": "fa-regular fa-envelope",
        },
        {
            "name": "Copyright/License",
            "url": f"{_github_link}/blob/{_data['github']['branch_name']}/{_data['copyright']['path']}",
            "icon": "fa-solid fa-copyright",

        },
        {
            "name": "PyPi Package",
            "url": f"https://pypi.org/project/{_data['package']['name']}/",
            "icon": "fa-brands fa-python",
        },
    ],
    "icon_links_label": "External links",

    "use_edit_page_button": True,
}


# -------------------------------------------------------------------------
# The following part dynamically reads header icon flags from the metadata,
# and adds the corresponding icons to `html_theme_options['icon_links']`.
_contact_platform = {
    "twitter": {"name": "Twitter", "icon": "fa-brands fa-twitter"},
    "linkedin": {"name": "LinkedIn", "icon": "fa-brands fa-linkedin"},
    "researchgate": {"name": "ResearchGate", "icon": "fa-brands fa-researchgate"},
    "orcid": {"name": "ORCiD", "icon": "fa-brands fa-orcid"},
}


def _add_icon_link(
        name: str,
        url: str,
        icon: str,
        type: Literal['fontawesome', 'url', 'local'] = 'fontawesome'
) -> NoReturn:
    """Add an icon link to `html_theme_options['icon_links']`."""
    html_theme_options['icon_links'].append(
        {
            "name": name,
            "url": url,
            "icon": icon,
            "type": type,
        }
    )
    return


for _contact_type, _show_icon in _data['docs']['header_icon'].items():
    if _show_icon:
        for _contact_person in [_data['contact']['organization']] + _data['contact']['corresponding_authors']:
            _contact_url = _contact_person[_contact_type]
            if _contact_url != "":
                _add_icon_link(
                    name=_contact_platform[_contact_type]['name'],
                    url=_contact_url,
                    icon=_contact_platform[_contact_type]['icon']
                )
                break
        else:
            raise ValueError(
                f"Displaying the header icon for {_contact_type} is active, "
                f"but no contact person has a URL."
            )
# -------------------------------------------------------------------------
# -------------------------------------------------------------------------


# html_theme_path: List[str] = []

# html_style: str

# html_title: str = ''

# html_short_title: str = ''

# html_baseurl: str = ''

html_context = {
    "github_user": _data['github']['user_name'],
    "github_repo": _data['github']['repo_name'],
    "github_version": _data['github']['branch_name'],
    "doc_path": _data['docs']['path'],
}

html_logo: Union[str, None] = '_static/logo/logo.svg'

html_favicon: Union[str, None] = '_static/logo/logo.ico'

html_css_files: List[Union[str, Tuple[str, Dict[str, str]]]] = ['css/base.css', 'css/custom.css', 'css/color.css']

# html_js_files: List[Union[str, Tuple[str, Dict[str, str]]]]

html_static_path: List[str] = ['_static']

# html_extra_path: List[str] = []

html_last_updated_fmt: Union[str, None] = '%b %d, %Y'

# html_permalinks: bool = True

# html_permalinks_icon: str = '¶'

html_sidebars: Dict[str, Union[List[str], str]] = {
    # "**": ["sidebar-nav-bs"],
    "blog/**": [
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

# html_show_sourcelink: bool = True

# html_sourcelink_suffix: str = ".txt"

# html_use_opensearch: str = ''

# html_file_suffix: str = '.html'

# html_link_suffix: str = '.html'

# html_show_copyright: bool = True

# html_show_search_summary: bool = True

# html_show_sphinx: bool = True

# html_output_encoding: str = 'utf-8'

# html_compact_lists: bool = True

# html_secnumber_suffix: str = '. '

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
htmlhelp_basename: str = f"{_data['project']['name']} Docs"

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
"""
latex_documents: List[Tuple[str, str, str, str, str, bool]] = [
    (
        root_doc,
        f"{_data['package']['name']}_docs.tex",
        f"{_data['project']['name']} Documentation",
        ' \\and '.join(_author_names_in_order),
        'manual',
        False
    ),
]

latex_elements: Dict[str, str] = {
    'papersize': 'a4paper',  # {'letterpaper', 'a4paper'}
    'pointsize': '11pt',
    'figure_align': 'htbp',
}


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
        _data['package']['name'],
        f"{_data['project']['name']} Documentation",
        _author_names_in_order,
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
        f"{_data['package']['name']}_docs",
        f"{_data['project']['name']} Documentation",
        '@*'.join(_author_names_in_order),
        _data['package']['name'],
        _data['project']['short_description'],
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

python_maximum_signature_line_length: int = 99


"""
Options for `sphinx.ext.autosummary`

References
----------
* https://www.sphinx-doc.org/en/master/usage/extensions/autosummary.html#generating-stub-pages-automatically
"""
# autosummary_context: Dict

autosummary_generate: bool = True

autosummary_generate_overwrite: bool = True

autosummary_imported_members:bool = False

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
blog_path: str = "blog"
blog_baseurl: str = f"https://{_data['docs']['readthedocs_name']}.readthedocs.io/"

blog_post_pattern: list[str] = ["blog/posts/*.rst", "blog/posts/*.md"]
post_auto_image: int = 1
blog_feed_archives: bool = True
fontawesome_included: bool = True

if _data['docs']['disqus_shortname'] != "":
    disqus_shortname: str = _data['docs']['disqus_shortname']

