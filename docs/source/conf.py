"""Configuration file for the Sphinx documentation builder.

References
----------
* Full list of built-in configuration values:
    https://www.sphinx-doc.org/en/master/usage/configuration.html
"""


from typing import Any, Dict, Union, List, Literal, Tuple


# -- Project information -----------------------------------------------------
# Reference: https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = '_!Project Name!_'
copyright = '2023, _!Armin Ariamajd, Armin Ariamajd_!'
author = '_!Armin Ariamajd, Armin Ariamajd_!'
release = '1.2.3'
version = '1.2'



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
