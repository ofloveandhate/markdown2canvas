# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'markdown2canvas'
copyright = '2024, silviana amethyst, Mckenzie West, Allison Beemer'
author = 'silviana amethyst, Mckenzie West, Allison Beemer'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc','sphinx.ext.autosectionlabel'
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'bizstyle'
html_static_path = ['_static']

import os
import sys

_HERE = os.path.dirname(__file__)
_ROOT_DIR = os.path.abspath(os.path.join(_HERE, '..'))
_PACKAGE_DIR = os.path.abspath(os.path.join(_HERE, '../markdown2canvas'))

sys.path.insert(0, _ROOT_DIR)
sys.path.insert(0, _PACKAGE_DIR)

# test the path; not strictly needed
import markdown2canvas


rst_prolog = """
.. |markdowndefaults| replace:: :attr:`markdown2canvas.translation_functions.default_markdown_extensions`
"""
