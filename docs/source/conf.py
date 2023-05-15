"""Configuration file for the Sphinx documentation builder.

References
----------
* Full list of built-in configuration values:
    https://www.sphinx-doc.org/en/master/usage/configuration.html
"""


from typing import Any, Dict, Union, List, Literal, Tuple
from template_package import _about


"""
Project information

References
----------
* https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
"""
project: str = _about.app_name

author: str = _about.owner_name

copyright: str = f"{_about.first_release_date.year}, {_about.owner_name}"

project_copyright: Union[str, List[str]] = copyright

version: str = _about.version

release: str = _about.release


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

templates_path: List[str] = ['../templates']

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

maximum_signature_line_length: Union[int, None] = 99  # New in version 7.1.

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
html_theme = 'alabaster'

# html_theme_path: List[str] = []

# html_style: str

# html_title: str = ''

# html_short_title: str = ''

# html_baseurl: str = ''

# html_context: Dict

html_logo: Union[str, None] = '../static/logo/logo.svg'

html_favicon: Union[str, None] = '../static/logo/logo.ico'

# html_css_files: List[Union[str, Tuple[str, Dict[str, str]]]] = ['css/custom.css']

# html_js_files: List[Union[str, Tuple[str, Dict[str, str]]]]

html_static_path: List[str] = ['../static']

# html_extra_path: List[str] = []

html_last_updated_fmt: Union[str, None] = '%b %d, %Y'

# html_permalinks: bool = True

# html_permalinks_icon: str = '¶'

# html_sidebars: Dict[str, Union[List[str], str]] = {
#     "**": ["search-field", "sidebar-nav-bs"]
# }

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
htmlhelp_basename: str = f"{_about.app_name} Docs"

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
        f'{_about.package_name}_docs.tex',
        f'{_about.app_name} Documentation',
        ' \\and '.join([name for name, _ in _about.authors]),
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
        _about.package_name,
        f'{_about.app_name} Documentation',
        [name for name, _ in _about.authors],
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
        f'{_about.package_name}_docs',
        f'{_about.app_name} Documentation',
        '@*'.join([name for name, _ in _about.authors]),
        _about.package_name,
        _about.short_description,
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
