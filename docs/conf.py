# Configuration file for the Sphinx documentation builder.
# https://www.sphinx-doc.org/en/master/usage/configuration.html
from datetime import datetime

from dunamai import Version, Style

# -- Project information -----------------------------------------------------

project = 'pydvdcss'
copyright = f'2021-{datetime.now().year}, rlaphoenix'
author = 'rlaphoenix'

version = Version.from_git().serialize(style=Style.SemVer)
release = Version.from_git().base

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.autosectionlabel',
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'myst_parser'
]

master_doc = 'index'

exclude_patterns = [
    '_build',
    'Thumbs.db',
    '.DS_Store',
]

templates_path = ['_templates']

# -- Options for internationalization ----------------------------------------

language = 'en'

# -- Options for HTML output -------------------------------------------------

html_theme = 'furo'
html_static_path = ['_static']

html_css_files = [
    'styles/custom.css',
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.1/css/fontawesome.min.css',
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.1/css/solid.min.css',
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.1/css/brands.min.css',
]

html_sidebars = {
    '**': [
        'sidebar/scroll-start.html',
        'sidebar/brand.html',
        'sidebar/search.html',
        'sidebar/navigation.html',
        'sidebar/scroll-end.html',
    ]
}
