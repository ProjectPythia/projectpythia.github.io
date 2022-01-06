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
import os
import shutil
import sys

sys.path.insert(0, os.path.abspath('_extensions'))


# -- Project information -----------------------------------------------------

project = 'Project Pythia'
author = 'the <a href="https://projectpythia.org/">Project Pythia</a> Community'
copyright = '2022'

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
html_last_updated_fmt = '%-d %B %Y'

# Logo & Title
html_logo = '_static/images/logos/pythia_logo-white-rtext.svg'
html_title = ''

# Favicon
html_favicon = '_static/images/icons/favicon.ico'

# Permalinks Icon
html_permalinks_icon = '<i class="fas fa-link"></i>'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
html_css_files = ['custom.css']
# html_js_files = ['custom.js']

# Disable Sidebars on special pages
html_sidebars = {
    'index': [],
    'gallery': [],
}

# HTML Theme-specific Options
html_theme_options = {
    'github_url': 'https://github.com/ProjectPythia',
    'twitter_url': 'https://twitter.com/project_pythia',
    'google_analytics_id': 'G-T9KGMX7VHZ',
    'logo_only': True,
    'logo_link': 'https://projectpythia.org',
    'navbar_links': [
        {'name': 'Home', 'url': '/'},
        {'name': 'Foundations', 'url': 'https://foundations.projectpythia.org'},
        {'name': 'Gallery', 'url': 'https://projectpythia.org/gallery.html'},
        {'name': 'Community', 'url': 'https://projectpythia.org/index.html#join-us'},
    ],
    'navbar_align': 'left',
    'page_layouts': {'index': 'page-banner.html', 'gallery': 'page-standalone.html'},
    'footer_menu': [
        {
            'title': 'Column A',
            'class': 'col-8 col-sm-4 col-md-3 col-lg-2',
            'items': [
                {
                    'name': 'Link 1',
                    'url': 'https://google.com',
                },
                {
                    'name': 'Link 2',
                    'url': 'https://google.com',
                },
                {
                    'name': 'Link 3',
                    'url': 'https://google.com',
                },
                {
                    'name': 'Link 4',
                    'url': 'https://google.com',
                },
            ],
        },
        {
            'title': 'Column B',
            'class': 'col-8 col-sm-4 col-md-3 col-lg-2',
            'items': [
                {
                    'name': 'Link 1',
                    'url': 'https://google.com',
                },
                {
                    'name': 'Link 2',
                    'url': 'https://google.com',
                },
                {
                    'name': 'Link 3',
                    'url': 'https://google.com',
                },
                {
                    'name': 'Link 4',
                    'url': 'https://google.com',
                },
            ],
        },
        {
            'title': 'Column C',
            'class': 'col-8 col-sm-4 col-md-3 col-lg-2',
            'items': [
                {'name': 'Just some text!'},
                {
                    'name': (
                        'Another paragraph of text. This has '
                        'a lot more information in it than '
                        'the previous paragraph.'
                    )
                },
                {
                    'name': 'And finally a link',
                    'url': 'https://google.com',
                },
            ],
        },
    ],
    'footer_logos': {
        'NCAR': '_static/images/logos/NCAR-contemp-logo-blue.svg',
        'Unidata': '_static/images/logos/Unidata_logo_horizontal_1200x300.svg',
        'UAlbany': '_static/images/logos/UAlbany-A2-logo-purple-gold.svg',
    },
    'footer_items': [
        'footer-logos.html',
        'footer-menu.html',
        'footer-info.html',
        'footer-nsf.html',
    ],
    'extra_navbar': ('Theme by <a href="https://projectpythia.org">Project Pythia</a>'),
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
