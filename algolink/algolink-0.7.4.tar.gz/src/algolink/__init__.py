from . import config
from .client import AlgoLink, create_model
from .ext.ext_loader import ExtensionLoader, load_extensions
from .runtime.command_line import start_runtime

EBONITE_DEBUG = config.Core.DEBUG
if config.Core.AUTO_IMPORT_EXTENSIONS:
    ExtensionLoader.load_all()

__all__ = ['load_extensions', 'AlgoLink', 'ALGOLINK_DEBUG', 'start_runtime', 'create_model']
__version__ = '0.7.3'

if __name__ == '__main__':
    pass
