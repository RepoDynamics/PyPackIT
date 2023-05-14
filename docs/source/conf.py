"""Configuration file for the Sphinx documentation builder.

References
----------
* Full list of built-in configuration values:
    https://www.sphinx-doc.org/en/master/usage/configuration.html
"""


from typing import Any, Dict, Union, List, Literal, Tuple
from template_package import _about


# -- Project information -----------------------------------------------------
# Reference: https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = _about.app_name
copyright = _about.copyright_notice
author = _about.owner_name
release = _about.release
version = _about.version



# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = []

templates_path = ['../templates']
exclude_patterns = []


root_doc: str = 'index'


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['../static']
