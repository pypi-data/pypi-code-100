#__init__

#Imports
import sys

from .exception import *

if not str(sys.version).startswith("3"):
    #HOW DARE YOU USE PYTHON2 IDIOT. or python4, if that ever exists
    raise VersionError("Python version is not supported.")

from .metadata import *
from .beetroot import *