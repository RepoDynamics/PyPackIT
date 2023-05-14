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

copyright: str = f"{_about.first_release_date}, {_about.owner_name}"

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

templates_path = ['../templates']




# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['../static']
