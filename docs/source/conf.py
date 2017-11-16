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
import io
import copy
sys.path.insert(0, os.path.abspath('../..'))

#Save the documentation directory path
initialpath = os.getcwd()

#List with all the models with a batch_example
models = []
dictionary = []

#Class definition
class Model:
	fileName = ""
	title = ""
	label = ""
class Word:
	file = ""
	title = ""
	label = ""

with io.open("conf_param.py", "r") as m:
	count = 2
	curWord = Word()
	for line in m:
		if not line.startswith("#") and not line == "\n" and line.find(":") == (-1):
			if (count == 2):
				curWord.file = line.rstrip("\n\r")

			if (count == 1):
				curWord.title = line[1:].rstrip("\n\r")

			if (count == 0):
				curWord.label = line[1:].rstrip("\n\r")
				copyWord = copy.deepcopy(curWord)
				dictionary.append(copyWord)

			if count == 0:
				count = 2
			elif count == 2:
				count = 1
			elif count == 1:
				count = 0

with io.open("conf_param.py", "r") as m:
	inModels = False
	count = -1
	curModel = Model()
	for line in m:
		if not line.startswith("#") and not line == "\n":
			if line.find("Dictionary") != (-1):
				inModels = False
				count = -1

			if (count == 2) and inModels:
				curModel.fileName = line.rstrip("\n\r")

			if (count == 1) and inModels:
				curModel.title = line[1:].rstrip("\n\r")

			if (count == 0):
				curModel.label = line[1:].rstrip("\n\r")
				copyModel = copy.deepcopy(curModel)
				models.append(copyModel)

			if count == 0:
				count = 2
			elif count == 2:
				count = 1
			elif count == 1:
				count = 0

			if line.find("Models list") != (-1):
				inModels = True
				count = 2

#Go to the correct directory to check all the batch_examples
os.chdir("../../Data")
#Loop in every batch_example directory
#for root, dirs, files in os.walk("."):
	#for name in files:
		#if name.endswith(".m"):
			#root_check = os.getcwd() + root[1:]
			#dir_check = os.path.join(root_check, "html")
			#name_check = name[:-1] + "html"
			#filepath_check = os.path.join(dir_check, name_check)
			#if not(os.path.isfile(filepath_check)):
				#os.system('matlab -nodesktop -nosplash -wait -r "publish(\'' + os.path.join(root,name) + '\'); quit"')

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

            #Set the name of the file
            base = os.path.splitext(os.path.basename(filepath))[0]
            modelIndex = base.find("_batch")
            model = base[:modelIndex]
            if model == "IR":
            	model = "InversionRecovery"

            #Create a ".rst" file and transcript
            with io.open(base +".rst", "wb") as f:
                #body = xml.etree.ElementTree.tostring(tree[0][1])
                t = base+"_example"
                #Write the good title
                titleCount = base.find("_batch")
                title = base[:titleCount]
                if title == "IR":
                	title = "Inversion Recovery"

                f.write(title.encode())
                f.write(b"\n")
                f.write(b"=" * len(title))
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
                        count = 0
                        #The while loop help to find every png if there are mutliple ones in the same line
                        while index !=(-1):
                        	#Remove links in the html file
                        	#Check if there's a link in the help header
                        	linkIndex = line.find("&lt;a href")
                        	if linkIndex != (-1):
                        		#If it's for the command line, replace it by the batch example path
                        		if line.find("command line usage")!= (-1):
                        			absolutePath = os.path.abspath(filepath)
                        			line = line[:linkIndex]+"qMRLab\\Data\\"+os.path.dirname(os.path.dirname(filepath))+"\\"+model+"_batch.m):\n"
                        		#If it's for the command line, replace it by qMRusage
                        		elif line.find("qMRusage") != (-1):
                        			line = line[:linkIndex] + "qMRusage(" + model + ")"

                        	#Change the png paths in the file
                        	if line.find(".png", index) != (-1):
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

#Return to the initial documentation directory
os.chdir(initialpath)

#Loops in the elements (models) to add them to their toctrees
for element in models:

	#create a directory t=list to save the models category list
    directories = []
    nbdir = -1

    #Loop in the model directory to find the correct document related to the model
    for root, dirs, files in os.walk("../../Models"):
        for name in files:

            #if the model is found
            search = element.fileName
            if search == "IR":
            	search = "InversionRecovery"
            if name.find(search+".m") != (-1) and name.find("~") == (-1):
            	file = os.path.join(root,name)
            	currentDir = ""

            	#Save the directories in order in the list to have the category list (and the caracterization)
            	while (currentDir != "Models"):
            		file = os.path.split(file)[0]
            		currentDir = os.path.split(file)[1]

            		directories.append(currentDir)
            		#if file.endswith("/") or file.endswith("\\"):
            			#file = file[:(file.len()-1)]
            		nbdir = nbdir + 1
    toOpen = directories[nbdir - 1]
    #Open a temporary file to transfer the toctree
    with io.open(element.fileName +"temp.rst", "wb") as fd:
        #If you find the class for your model in .rst file
        if directories[nbdir - 1] != "UnderDevelopment":

        	#Open the file
        	included = False
        	try:
        		with io.open(directories[nbdir - 1].lower()+".rst", "rb") as fw:
        			print('YES')
        	except IOError:
        		with io.open(directories[nbdir - 1].lower()+".rst", "w") as fw:
        			print('NO')
        		fw.close()

        	with io.open(directories[nbdir - 1].lower()+".rst", "rb") as fw:
        		for line in fw:
        			if line.find(element.title) != (-1) and line.find("_batch") == (-1):
        				included = True

        	with io.open(directories[nbdir - 1].lower()+".rst", "rb") as fw:
        	    j = nbdir - 1
        	    while j != (-1):
        	    	for word in dictionary:
        	    		if word.file == directories[j]:
        	    			directories[j] = word.title
        	    	j = j - 1
        	    #Declare counting and validation variables
        	    nbTitle = nbdir - 2
        	    i = -1
        	    found = False
        	    count = -1
        	    k = -1

        	    if not included:
        	    	written = False
        	    	nbTitle = nbTitle + 1
        	    	for line in fw:
        	    		#If you find the category of the last unchecked directory
        	    		if line.find(directories[nbTitle]) != (-1):
        	    			nbTitle = nbTitle - 1

        	    		if nbTitle == (-1):
        	    			#Set the counter to 2 to pass 2 lines
        	        		i = 2

        	        	if i == 0:
        	        		fd.write(b"\n")
        	    			fd.write(element.title)
        	    			fd.write("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
        	    			fd.write(element.label+"\n")
        	    			fd.write("\n")
        	    			fd.write(b".. toctree::\n")
        	    			fd.write(b"\t:maxdepth: 1\n")
        	    			fd.write(b"\n")
        	    			fd.write("\t" + element.fileName+"_batch")
        	    			fd.write(b"\n\n")

        	    		i = i - 1

        	        	fd.write(line)

        	    	if not written:
        	    		if nbTitle == nbdir - 1:
        	    			fd.write(directories[nbTitle])
        	    			fd.write("\n")
        	    			fd.write("==========================================================\n")
        	    			label = ""
        	    			for word in dictionary:
        	    				if word.title == directories[nbTitle]:
        	    					label = word.label
        	    			fd.write(label+"\n")
        	    			fd.write("\n")
        	    			nbTitle = nbTitle - 1
        	    		while nbTitle != (-1):
        	    			fd.write(b"\n")
        	    			fd.write(directories[nbTitle])
        	    			fd.write("\n")
        	    			fd.write("----------------------------------------------------------\n")
        	    			for word in dictionary:
        	    				if word.title == directories[nbTitle]:
        	    					label = word.label
        	    			fd.write(label+"\n")
        	    			fd.write("\n")
        	    			nbTitle = nbTitle - 1

        	        	fd.write(b"\n")
        	    		fd.write(element.title)
        	    		fd.write("\n")
        	    		fd.write("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
        	    		fd.write(element.label+"\n")
        	    		fd.write("\n")
        	    		fd.write(b".. toctree::\n")
        	    		fd.write(b"\t:maxdepth: 1\n")
        	    		fd.write(b"\n")
        	    		fd.write("\t" + element.fileName+"_batch")
        	    		fd.write(b"\n\n")

        	    if included:
        	    	#Loop accross every line of the .rst file with the toctree
        	    	for line in fw:
        	    	#If you find the model and not the batch_example (as a title)
        	        	if line.find(element.title) != (-1) and line.find("_batch") == (-1) and line.find("label") == (-1):
        	        		#Set the counter to 2 to pass 2 lines
        	        		i = 4
        	        		k = 2
        	        		found = True

        	        	#When the two lines are passed, write the toctree (with modification for known models having issues)
        	        	if i == 0:
        	        		fd.write(b".. toctree::\n")
        	        		fd.write(b"\t:maxdepth: 1\n")
        	        		fd.write(b"\n")
        	        		fd.write("\t" + element.fileName+"_batch")
        	        		count = 2

        	        	if k == 0:
        	        		line = element.label + "\n"
        	        	#Decrement counting
        	        	i = i - 1
        	        	k = k - 1

        	        	#Rewrite all the lines in the temporary file (without any toctree and maxdepth already there
        	        	#removing duplicates)
        	        	if (line.find("toctree") == (-1) and line.find("maxdepth") == (-1)) or found == False:
        	        		count = count - 1
        	        		fd.write(line)
        	        		#Remove the found validation to enable other models to be written in the same document
        	        		if count == 0:
        	        			found = False

    #Open the temporary file in reading mode
    with io.open(element.fileName +"temp.rst", "r") as fd:
    	#Open the original file in write mode
    	with io.open(toOpen+".rst", "w") as fw:
    		#Create a list of the lines seen
    		line_seen = []
    		#For every line in the temp file, check if it was already seen (remove duplicates)
    		for line in fd:
    			duplicate = False
    			#Put the duplicate tag
    			for seen in line_seen:
    				if line == seen:
    					duplicate = True
    			#If it is a duplicate and a batch file (no mistakes of getting rid of important lines)
    			#Check only for batch_example files
    			if duplicate == True and line.find("batch") != (-1):
    				#Don't do anything
    				dummy=0
    			#If not a duplicate, write the line in the original file
    			else:
    				fw.write(line)
    				line_seen.append(line)
    #close the files
    fd.close()
    fw.close()
    #Remove the temp file
    os.remove(element.fileName +"temp.rst")



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
project = u'qMRLab'
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
#html_logo = '_static/logo-neuropoly.png'
html_logo = '_static/neuropoly_logo-try.png'
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
htmlhelp_basename = 'qMRLabdoc'


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
    (master_doc, 'qMRLab.tex', u'qMRLab Documentation',
     u'Ilana Leppert', 'manual'),
]


# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'qmrLab', u'qMRLab Documentation',
     [author], 1)
]


# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'qMRLab', u'qMRLab Documentation',
     author, 'qMRLab', 'One line description of project.',
     'Miscellaneous'),
]
