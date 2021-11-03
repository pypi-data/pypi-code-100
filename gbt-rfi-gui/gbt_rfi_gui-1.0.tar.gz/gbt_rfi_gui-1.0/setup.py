######################################################################
#  setup.py - Installs data_pub to the local python installation.
#
#  Copyright (C) 2017 Associated Universities, Inc. Washington DC, USA.
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful, but
#  WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
#  General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#
#  Correspondence concerning GBT software should be addressed as follows:
#  GBT Operations
#  Green Bank Observatory
#  P. O. Box 2
#  Green Bank, WV 24944-0002 USA
#
######################################################################

# Needed to build wheels
import setuptools
from distutils.core import setup
from setuptools import find_packages

# this will make a package of only the GUI directory 
#  as specified by the 'packages' keyword
setup(name='gbt_rfi_gui',
      version='1.0',
      description='GBT RFI Webpage is the public-facing webpage containing access to the Green Bank Observatory Radio Frequency Interference database for the Green Bank Telescope.',
      author='Aaron Lovato, and Brenne Gregory',
      author_email='alovato@nrao.edu, bgregory@nrao.edu',
      url='https://www.greenbankobservatory.org',
      keywords="singledish, gridder, gridding",
      package_dir={"": "src"},
      packages=find_packages(where="src"),
      install_requires=[
            "numpy",
            "pandas",
            "matplotlib",
            "PyQt5"],
      python_requires=">=3.6, <3.9",
      entry_points={  # Optional
          "console_scripts": [
              "gbt_rfi_gui=RFI_Gui:main",
          ],
    },
      )

