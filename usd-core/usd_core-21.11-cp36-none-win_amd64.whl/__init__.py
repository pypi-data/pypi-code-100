__all__ = ['Tf', 'Gf', 'Trace', 'Work', 'Plug', 'Vt', 'Ar', 'Kind', 'Sdf', 'Ndr', 'Sdr', 'Pcp', 'Usd', 'UsdGeom', 'UsdVol', 'UsdMedia', 'UsdShade', 'UsdLux', 'UsdRender', 'UsdHydra', 'UsdRi', 'UsdSkel', 'UsdUI', 'UsdUtils', 'UsdPhysics']


# appended to this file for the windows PyPI package
import os, sys
dllPath = os.path.split(os.path.realpath(__file__))[0]
if sys.version_info >= (3, 8, 0):
    os.environ['PXR_USD_WINDOWS_DLL_PATH'] = dllPath
else:
    os.environ['PATH'] = dllPath + os.pathsep + os.environ['PATH']
