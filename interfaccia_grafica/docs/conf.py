# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import sys
import os
import sphinx_pdj_theme

sys.path.insert(0,os.path.abspath(".."))

project = 'TrainTrack Manager'
copyright = '2024, Alessio Cammarata'
author = 'Alessio Cammarata'
release = '1.2.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["sphinx.ext.todo",
              "sphinx.ext.viewcode",
              "sphinx.ext.autodoc"]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_pdj_theme'
html_theme_path = [sphinx_pdj_theme.get_html_theme_path()]

html_logo = '../assets/window_logo.ico'
html_favicon = '../assets/window_logo.ico'

html_theme_options = {
    'logo_width': '200px',
    'logo_height': '150px',
    'search': 'show',   # o 'hide' per nascondere la barra di ricerca
    'home_link': 'show' # o 'hide' per nascondere il link alla home
}
html_static_path = ['_static']
