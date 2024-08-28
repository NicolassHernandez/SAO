# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information


import os
import sys


# Add the path to your Python modules
sys.path.insert(0, os.path.abspath('../../'))



#sys.path.insert(0, os.path.abspath('..'))

#sys.path.insert(0, os.path.abspath('.'))

import sphinx_rtd_theme

html_theme = "sphinx_rtd_theme"
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

project = 'Simulated Adaptive Optics'
copyright = '2024, Nicolas et al'
author = 'Nicolas et al'
release = '2025'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx_copybutton',
    'sphinx_togglebutton',
    'sphinx.ext.graphviz', 

    'nbsphinx',
    'sphinx.ext.mathjax',
]
nbsphinx_execute = 'auto'

html_theme = 'sphinx_rtd_theme'  # or another theme of your choice
html_theme_options = {
    'navigation_depth': 4,  # Adjust to control how many levels deep you want in the sidebar
    'collapse_navigation': True,  # Collapse navigation by default
    'titles_only': False,  # Show all sections and subsections

}
html_context = {
    "display_github": True,  # Integrate GitHub
    "github_user": "NicolassHernandez",  # Username of your GitHub account
    "github_repo": "AOS",  # Repository name
    "github_version": "main",  # The branch
    "conf_py_path": "/docs/source/",  # Path in the repository to the source folder
}
html_show_sourcelink = False

templates_path = ['_templates']
exclude_patterns = []

numfig = True

#html_theme = 'alabaster'
html_static_path = ['_static']


# Configure sphinx-copybutton options
copybutton_prompt_text = ">>> "  # If you have a specific prompt, like in a Python REPL
copybutton_only_copy_prompt_lines = True
pygments_style = 'friendly'