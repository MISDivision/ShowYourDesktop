#!/usr/bin/env python
##
##  setup.py - ShowYourDesktop
##
 
# This module is used to compile ShowYourDesktop to a Windows executable.
# Py2exe is required to be installed in order to compile.
#
# To compile, run "python setup.py install"
#                 "python setup.py py2exe"

from distutils.core import setup
import py2exe

setup(windows=['main.py'])