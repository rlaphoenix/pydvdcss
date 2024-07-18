# Configuration file for the Sphinx documentation builder.
# https://www.sphinx-doc.org/en/master/usage/configuration.html

from datetime import datetime

from dunamai import Style, Version

# -- Project information -----------------------------------------------------

project = "pydvdcss"
copyright = f"2021-{datetime.now().year}, rlaphoenix"
author = "rlaphoenix"
version = Version.from_git().serialize(style=Style.SemVer)
release = Version.from_git().base

# -- General configuration ---------------------------------------------------

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.napoleon",
    "myst_parser",
]
exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
]
root_doc = "index"
templates_path = [
    "_templates",
]

# -- Builder options ---------------------------------------------------------

html_theme = "furo"
html_css_files = [
    "styles/custom.css",
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.1/css/fontawesome.min.css",
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.1/css/solid.min.css",
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.1/css/brands.min.css",
]
html_static_path = [
    "_static",
]
html_sidebars = {
    "**": [
        "sidebar/scroll-start.html",
        "sidebar/brand.html",
        "sidebar/search.html",
        "sidebar/navigation.html",
        "sidebar/scroll-end.html",
    ],
}

# -- MyST configuration ------------------------------------------------------

myst_enable_extensions = [
    "smartquotes",
    "replacements",
]
