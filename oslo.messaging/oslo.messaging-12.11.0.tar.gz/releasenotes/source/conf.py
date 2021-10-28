# -*- coding: utf-8 -*-
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# oslo.log Release Notes documentation build configuration file, created by
# sphinx-quickstart on Tue Nov  3 17:40:50 2015.
#
# This file is execfile()d with the current directory set to its
# containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# This file does only contain a selection of the most common options. For a
# full list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Project information --------------------------------------------------
# General information about the project.
copyright = '2016, oslo.messaging Developers'

# Release notes do not need a version in the title, they span
# multiple versions.
# The full version, including alpha/beta/rc tags.
release = ''
# The short X.Y version.
version = ''

# -- General configuration ------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = [
    'openstackdocstheme',
    'reno.sphinxext',
]

# openstackdocstheme options
openstackdocs_repo_name = 'openstack/oslo.messaging'
openstackdocs_bug_project = 'oslo.messaging'
openstackdocs_bug_tag = ''

# The master toctree document.
master_doc = 'index'

# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = 'openstackdocs'

# -- Options for Internationalization output ------------------------------
locale_dirs = ['locale/']
