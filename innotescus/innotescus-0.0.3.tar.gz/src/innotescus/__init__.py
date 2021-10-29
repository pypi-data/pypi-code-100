import sys
import os

# grpcio-tools generated files must be on the python path (code doesn't assume it's in a package)
# we're still placing it in a package anyway for better editor support from our code.
sys.path.append(os.path.join(os.path.dirname(__file__), '_grpc'))

from .innotescus import *  # noqa

__version__ = '0.0.3'
