# -*- coding: utf-8 -*-
#
# qMRlab documentation build configuration file, created by
# sphinx-quickstart on Thu Sep  7 15:04:50 2017.
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
import shutil
import xml.etree.ElementTree
sys.path.insert(0, os.path.abspath('../..'))

#Save the documentation directory path
initialpath = os.getcwd()

#List with all the models qith a batch_example
models = []

#Go to the correct directory to check all the batch_examples
os.chdir("../../Data")
#Loop in every batch_example directory
for root, dirs, files in os.walk("."):
	for name in files:
		if name.endswith(".m"):
			root_check = os.getcwd() + root[1:]
			dir_check = os.path.join(root_check, "html")
			name_check = name[:-1] + "html"
			filepath_check = os.path.join(dir_check, name_check)
			if not(os.path.isfile(filepath_check)):
				os.system('matlab -nodesktop -nosplash -wait -r "publish(\'' + os.path.join(root,name) + '\'); quit"')


for root, dirs, files in os.walk("."):
    #Check for every files in each directory if there's an ".html" file (generated by MATLAB)
    for name in files:
        #If there is a ".html" file begin transcription script
        if name.endswith("html"):

            #Save the path of the ".html" file 
            filepath = os.path.join(root, name)

            #Remove the "." at the begining if there is one
            if filepath.startswith("."):
                filepath = filepath[2:]

            #Save the absolute path of the file to transcript
            fn = os.path.join(os.getcwd(),filepath)

            #Return to the original directory for the documentation
            #tree = xml.etree.ElementTree.parse(
            os.chdir(initialpath)
            import io

            #Set the name of the file
            base = os.path.splitext(os.path.basename(filepath))[0]
            modelIndex = base.find("_batch")
            models.append(base[:modelIndex])

            #Create a ".rst" file and transcript
            with io.open(base +".rst", "wb") as f:
                #body = xml.etree.ElementTree.tostring(tree[0][1])
                t = base+"_example"
                f.write(t.encode())
                f.write(b"\n")
                f.write(b"=" * len(t))
                f.write(b"\n")
                f.write(b"\n")
                f.write(b".. raw:: html\n")
                f.write(b"\n   \n")
                #f.write(("  %s" % body).encode("utf-8"))
                #f.write(b"   oihokh")

                #Copy the html code of the file
                with io.open(fn, "rb") as fi:
                    for line in fi:
                        f.write(b"   ")

                        #If the line contains a ".png" sub-string (indicating a path to an image)
                        index = 0

                        #The while loop help to find every png if there are mutliple ones in the same line
                        while index !=(-1):
                            if line.find(".png", index)!=(-1):

                                #Save the index of the image path (after the pervious occurrences of the path)
                                a = line.find("src", index)
                                b = line.find("png", index)

                                #Save the index at where we have to search for the next png
                                index = b+3+len("_static")

                                #Save the initial path and the "_images" directory in the new path
                                initialstr = line[a+5:b+3]
                                replacement = os.path.join("_static/",initialstr)

                                #Replace sub-string with the new path
                                line = line.replace(initialstr, replacement)
                            else:
                                index = (-1)
                        f.write(line)


            #Return to the batch_example directory
            os.chdir("../../Data")

        elif name.endswith(".png"):
            #Save the path of the ".png" file 
            filepath = os.path.join(root, name)

            #Remove the "." at the begining if there is one
            if filepath.startswith("."):
                filepath = filepath[2:]

            #Save the absolute path of the file to move
            fn = os.path.join(os.getcwd(),filepath)

            #Copy the ".png" file to the new location
            shutil.copy(fn, os.path.join(initialpath,"../source/_static"))

os.chdir(initialpath)
#for element in models:
#    for file in os.walk("."):
#        for name in files:
#            if name.find(element) and not(name.find("batch")):
#                with io.open(element +"temp.rst", "wb") as fd:
#                    with io.open(element+".rst", "rb") as fw:
#                        i = -1
#                        for line in fw:
#                            if line.find("USAGE") != (-1):
#                                i=2
#                            elif i == 0 and line.find("toctree") == (-1):
#                                fd.write(".. toctree::\n")
#                                fd.write("\t:maxdepth: 1")
#                                fd.write(element+"_batch")
#                            if i > -1:
#                                i=i-1
#                            fd.write(line)
#    with io.open(element+".rst", "wb") as f:
#        with io.open(element +"temp.rst", "rb") as fd:
#            for line in fd:
#                f.write(line)
#	os.remove(element +"temp.rst")



# -- General configuration ------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['sphinx.ext.autodoc',
    'sphinx.ext.imgmath',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages',
    'sphinx.ext.autosectionlabel']
    #'sphinxcontrib.matlab']

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# Primary domain
primary_domain = 'mat'
# Matlab source dir
matlab_src_dir = os.path.abspath('../..')
autodoc_member_order = 'groupwise'

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = u'qMRlab'
copyright = u'2017, NeuroPoly'
author = u'NeuroPoly'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = u'0.1'
# The full version, including alpha/beta/rc tags.
release = u'0.1'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = []

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = False


# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
#html_theme = 'alabaster'
html_theme = "sphinx_rtd_theme"
# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
# html_theme_options = {}
html_theme_options = {
#   'logo': 'logo-neuropoly.png',
    'github_user': 'neuropoly',
    'github_repo': 'qMRLab',
    'github_button': True,
    'github_banner': True,
}
html_theme_options = {
    'collapse_navigation': False,
    'display_version': False,
    'navigation_depth': 4,
}
html_logo = '_static/logo-neuropoly.png'
# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# This is required for the alabaster theme
# refs: http://alabaster.readthedocs.io/en/latest/installation.html#sidebars
html_sidebars = {
    '**': [
        'about.html',
        'navigation.html',
        'relations.html',  # needs 'show_related': True theme option to display
        'searchbox.html',
        'donate.html',
    ]
}


# -- Options for HTMLHelp output ------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = 'qMRlabdoc'


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
    (master_doc, 'qMRlab.tex', u'qMRlab Documentation',
     u'Ilana Leppert', 'manual'),
]


# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'qmrlab', u'qMRlab Documentation',
     [author], 1)
]


# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'qMRlab', u'qMRlab Documentation',
     author, 'qMRlab', 'One line description of project.',
     'Miscellaneous'),
]
