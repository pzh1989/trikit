#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# trikit documentation build configuration file, created by
# sphinx-quickstart on Mon Sep  3 10:45:51 2018.
#
# This file is execfile()d with the current directory set to its
# containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
import sphinx_rtd_theme


sys.path.insert(0, os.path.abspath("../.."))

# -- General configuration ------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
	'sphinx.ext.autodoc',
	'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.imgmath',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages',
	'sphinxcontrib.napoleon'
	]


# Napoleon settings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = False
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_use_keyword = True
napoleon_custom_sections = None



# Specify date format.
today_fmt = "%Y-%m-%d"

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = 'trikit'
copyright = '2018, James D. Triveri'
author = 'James D. Triveri'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = '0.3'
# The full version, including alpha/beta/rc tags.
release = '0.3.1'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = ['_build', '**tests**', '**spi**']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True


add_module_names = False


# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"
#html_theme_path = sphinx_bootstrap_theme.get_html_theme_path()

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
# html_theme_options = {}
#~ html_theme_options = {
    #~ # Navigation bar title. (Default: ``project`` value)
    #~ #'navbar_title': "Demo",

    #~ # Tab name for entire site. (Default: "Site")
    #~ 'navbar_site_name': "",

    #~ # A list of tuples containing pages or urls to link to.
    #~ # Valid tuples should be in the following forms:
    #~ #    (name, page)                 # a link to a page
    #~ #    (name, "/aa/bb", 1)          # a link to an arbitrary relative url
    #~ #    (name, "http://example.com", True) # arbitrary absolute url
    #~ # Note the "1" or "True" value above as the third argument to indicate
    #~ # an arbitrary url.
    #~ 'navbar_links': [
        #~ ("Examples", "examples"),
        #~ ("Link", "http://example.com", True),
    #~ ],

    #~ # Render the next and previous page links in navbar. (Default: true)
    #~ 'navbar_sidebarrel': True,

    #~ # Render the current pages TOC in the navbar. (Default: true)
    #~ 'navbar_pagenav': True,

    #~ # Tab name for the current pages TOC. (Default: "Page")
    #~ 'navbar_pagenav_name': "Page",

    #~ # Global TOC depth for "site" navbar tab. (Default: 1)
    #~ # Switching to -1 shows all levels.
    #~ 'globaltoc_depth': 1,

    #~ # Include hidden TOCs in Site navbar?
    #~ #
    #~ # Note: If this is "false", you cannot have mixed ``:hidden:`` and
    #~ # non-hidden ``toctree`` directives in the same page, or else the build
    #~ # will break.
    #~ #
    #~ # Values: "true" (default) or "false"
    #~ 'globaltoc_includehidden': "true",

    #~ # HTML navbar class (Default: "navbar") to attach to <div> element.
    #~ # For black navbar, do "navbar navbar-inverse"
    #~ 'navbar_class': "navbar",

    #~ # Fix navigation bar to top of page?
    #~ # Values: "true" (default) or "false"
    #~ 'navbar_fixed_top': "true",

    #~ # Location of link to source.
    #~ # Options are "nav" (default), "footer" or anything else to exclude.
    #~ 'source_link_position': "none",

    #~ # Bootswatch (http://bootswatch.com/) theme.
    #~ #
    #~ # Options are nothing (default) or the name of a valid theme
    #~ # such as "cosmo" or "sandstone".
    #~ #
    #~ # The set of valid themes depend on the version of Bootstrap
    #~ # that's used (the next config option).
    #~ #
    #~ # Currently, the supported themes are:
    #~ # - Bootstrap 2: https://bootswatch.com/2
    #~ # - Bootstrap 3: https://bootswatch.com/3
	#~ # BOOTSTRAP_THEME  = 'cyborg'  # black background
	#~ # BOOTSTRAP_THEME   = 'darkly' # black background
	#~ # BOOTSTRAP_THEME  = 'flatly'  # Green 
	#~ # BOOTSTRAP_THEME  = 'journal'
	#~ # BOOTSTRAP_THEME  = 'lumen' # white
	#~ # BOOTSTRAP_THEME  = 'paper'
	#~ # BOOTSTRAP_THEME  = 'readable' # white
	#~ # BOOTSTRAP_THEME  = 'sandstone'
	#~ # BOOTSTRAP_THEME  = 'simplex' # red
	#~ # BOOTSTRAP_THEME  = 'united'
	#~ # BOOTSTRAP_THEME  = 'slate'
	#~ # BOOTSTRAP_THEME  = 'superhero'
	#~ # BOOTSTRAP_THEME  = 'spacelab'
	#~ # BOOTSTRAP_THEME  = 'yeti'
	#~ # BOOTSTRAP_THEME  = 'cosmo' # Blue
    #~ 'bootswatch_theme': "sandstone",
    #~ # Choose Bootstrap version.
    #~ # Values: "3" (default) or "2" (in quotes)
    #~ 'bootstrap_version': "3",
#~ }

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# This is required for the alabaster theme
# refs: http://alabaster.readthedocs.io/en/latest/installation.html#sidebars
#~ html_sidebars = {
    #~ '**': [
        #~ 'about.html',
        #~ 'navigation.html',
        #~ 'relations.html',  # needs 'show_related': True theme option to display
        #~ 'searchbox.html',
        #~ 'donate.html',
    #~ ]
#~ }

#~ html_sidebars = {
   #~ '**': ['globaltoc.html'],
   #~ 'using/windows': ['windowssidebar.html', 'searchbox.html'],
#~ }


# -- Options for HTMLHelp output ------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = 'trikitdoc'


# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',

    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, 'trikit.tex', 'trikit Documentation',
     'James D. Triveri', 'manual'),
]


# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'trikit', 'trikit Documentation',
     [author], 1)
]


# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'trikit', 'trikit Documentation',
     author, 'trikit', 'One line description of project.',
     'Miscellaneous'),
]




# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {'https://docs.python.org/': None}
