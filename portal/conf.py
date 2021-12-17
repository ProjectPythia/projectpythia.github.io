#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import datetime
import os
import shutil
import sys

sys.path.insert(0, os.path.abspath('_extensions'))


# -- Project information -----------------------------------------------------

project = 'Project Pythia'
author = 'Project Pythia Developers & Contributors'
copyright = f'2021-{datetime.datetime.now().year}, {author}'

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'myst_nb',
    'sphinx_panels',
    'yaml_gallery_generator',
]

# Define what extensions will parse which kind of source file
source_suffix = {
    '.ipynb': 'myst-nb',
    '.myst': 'myst-nb',
}

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_pythia_theme'
html_last_updated_fmt = '%d %B %Y'

# Logo & Title
html_logo = '_static/images/logos/pythia_logo-white-rtext.svg'
html_title = ''

# Favicon
html_favicon = '_static/images/icons/favicon.ico'

# Permalinks Icon
html_permalinks_icon = '<i class="bi bi-link"></i>'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
html_css_files = ['custom.css']
# html_js_files = ['custom.js']

# HTML Theme-specific Options
html_theme_options = {
    'page_layouts': {'index': 'banner', 'gallery': 'standalone'},
    'domnav': [
        {
            'content': 'Start Learning',
            'url': '/index.html#start-learning',
        },
        {
            'content': 'Join us!',
            'url': '/index.html#join-us',
        },
        {
            'content': 'Team',
            'url': '/index.html#the-project-pythia-team',
        },
        {
            'content': 'About',
            'url': 'about',
        },
    ],
    'footer': {
        'logos': {
            'NCAR': '_static/images/logos/NCAR-contemp-logo-blue.svg',
            'Unidata': '_static/images/logos/Unidata_logo_horizontal_1200x300.svg',
            'UAlbany': '_static/images/logos/UAlbany-A2-logo-purple-gold.svg',
        },
        'acknowledgement': {
            'content': (
                'This material is based upon work supported by the National '
                'Science Foundation under Grant Nos. 2026863 and 2026899. Any '
                'opinions, findings, and conclusions or recommendations expressed '
                'in this material are those of the author(s) and do not necessarily '
                'reflect the views of the National Science Foundation.'
            ),
            'image': '_static/images/logos/footer-logo-nsf.png',
        },
    },
}

# Panels config
panels_add_bootstrap_css = False

# MyST config
myst_enable_extensions = ['amsmath', 'colon_fence', 'deflist', 'html_image']
myst_url_schemes = ['http', 'https', 'mailto']
jupyter_execute_notebooks = 'off'

# CUSTOM SCRIPTS ==============================================================

# Copy root files into content pages ------------------------------------------

shutil.copyfile('../CODEOFCONDUCT.md', 'code_of_conduct.md')
