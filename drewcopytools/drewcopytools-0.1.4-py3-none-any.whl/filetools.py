# Some utiltiy functions for helping us with file type things...
from pathlib import Path


def get_sequential_file_path(dir:Path, basename:str, extension:str) ->Path:
    """Generates a sequential file name <basename>_<0, 1,2,3, etc.> in the given directory.
    The directory will be created if it doesn't already exist."""
    if not dir.exists():
        dir.mkdir()

    SANITY_COUNT = 1024    # We will give up attempting to create a sequential file after this many tries.

    # We will grab the oldest file with the given base name as check its number.
    # https://stackoverflow.com/questions/39909655/listing-of-all-files-in-directory
    # see answer by prasastoadi (list comprehension)
    entries = dir.glob("**/*")
    files = [x for x in entries if x.is_file() and x.name.startswith(basename) ]
    maxTime = 0

    newest: Path = None
    for f in files:
        time = f.stat().st_mtime
        if time > maxTime:
            maxTime = time
            newest = f

    fNumber = 0
    if newest != None:
        fNumberStr = newest.name.replace(basename + "_", '').replace(extension, '')
        if fNumberStr == '':
            fNumber = 0
        else:
            fNumber = int(fNumberStr)

    newName = basename + "_" + str(fNumber + 1) + extension
    res =  dir / newName
    return res

