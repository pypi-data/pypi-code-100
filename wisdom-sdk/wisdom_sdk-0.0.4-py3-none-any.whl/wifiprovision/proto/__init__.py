import os
import sys
def _load_source(name, path):
    try:
        from importlib.machinery import SourceFileLoader
        return SourceFileLoader(name, path).load_module()
    except ImportError:
        # importlib.machinery doesn't exists in Python 2 so we will use imp (deprecated in Python 3)
        import imp
        return imp.load_source(name, path)

dirpath = os.path.dirname(__file__) + "/"
# protocomm component related python files generated from .proto files
constants_pb2 = _load_source('constants_pb2', dirpath+'constants_pb2.py')
sec0_pb2      = _load_source('sec0_pb2',     dirpath+'sec0_pb2.py')
sec1_pb2      = _load_source('sec1_pb2',       dirpath+'sec1_pb2.py')
session_pb2   = _load_source('session_pb2',    dirpath+'session_pb2.py')

# wifi_provisioning component related python files generated from .proto files
wifi_constants_pb2 = _load_source('wifi_constants_pb2',dirpath+'wifi_constants_pb2.py')
wifi_config_pb2    = _load_source('wifi_config_pb2',     dirpath+'wifi_config_pb2.py')
wifi_scan_pb2      = _load_source('wifi_scan_pb2',     dirpath+'wifi_scan_pb2.py')

# custom_provisioning component related python files generated from .proto files
custom_config_pb2  = _load_source('custom_config_pb2', 
                                  dirpath+'custom_config_pb2.py')
