# Configuration file for the Sphinx documentation builder.  # noqa: D100
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'WhatXtract'
copyright = '2025, Hasan Rasel'
author = 'Hasan Rasel'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

# Extensions
extensions = [
    'sphinx.ext.autodoc',  # pulls in docstrings
    'sphinx.ext.napoleon',  # parses Google/NumPy style
    'sphinx.ext.viewcode',  # adds [source] links
    'sphinx.ext.autosummary',  # optional: for summary tables
]

templates_path = ['_templates']
exclude_patterns = []

# Napoleon config (optional)
napoleon_google_docstring = True
napoleon_numpy_docstring = False


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'  # 'sphinx_rtd_theme'
html_static_path = ['_static']
