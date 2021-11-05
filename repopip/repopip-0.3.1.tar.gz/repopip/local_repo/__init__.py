from pathlib import Path
import os

try:
    SIMPLE_PATH = Path(os.environ['HOMEPATH']).resolve().joinpath('.static', 'simple')
    if(not SIMPLE_PATH.exists()):
        os.makedirs(SIMPLE_PATH)
except OSError:
    pass

