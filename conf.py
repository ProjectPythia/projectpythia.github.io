#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join('sphinxext')))
project = 'Pythia Portal'
copyright = f'2020-{datetime.datetime.now().year}'
author = 'Project Pythia Developers & Contributors'
html_last_updated_fmt = '%b %d, %Y'


extensions = ['myst_nb', 'sphinx_panels', 'gallery_generator']


# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = [
    '_build',
    'Thumbs.db',
    '.DS_Store',
    '*import_posts*',
    '**/pandoc_ipynb/inputs/*',
    '**.ipynb_checkpoints',
]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.

html_theme = 'sphinx_book_theme'
html_theme_options = {
    'path_to_docs': './',
    'search_bar_text': 'Search this site...',
    'repository_url': 'https://github.com/NCAR/pythia-portal',
    # "repository_branch": "gh-pages",  # For testing
    'launch_buttons': {
        'binderhub_url': 'https://mybinder.org',
        # "jupyterhub_url": "https://datahub.berkeley.edu",  # For testing
        'colab_url': 'https://colab.research.google.com/',
        'notebook_interface': 'jupyterlab',
        'thebe': True,
    },
    'use_edit_page_button': True,
    'use_issues_button': True,
    'use_repository_button': True,
}
copybutton_selector = 'div:not(.output) > div.highlight pre'

# html_favicon = '_static/favicon.ico'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
# html_extra_path = ['feed.xml']


# Panels config
panels_add_bootstrap_css = False

# MyST config
myst_admonition_enable = True
myst_deflist_enable = True
jupyter_execute_notebooks = 'off'


# -- Custom scripts ----------------------------------------------------------
