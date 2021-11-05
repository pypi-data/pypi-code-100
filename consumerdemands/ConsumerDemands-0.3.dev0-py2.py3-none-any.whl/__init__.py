from . import _core
from . import marshallian
from . import frischian
from . import hicksian
from . import _utils
from .demands import utility, marginal_utilities
from ._core import lambdavalue, derivative
from . import engel_curves

try:
    from .demands_class import OracleDemands
except ModuleNotFoundError:
    print("Missing dependencies for OracleDemands.")

__version__ = '0.3dev'

