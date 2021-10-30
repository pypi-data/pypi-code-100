import a9a
import sys
import pathlib

source, target = map(pathlib.Path, sys.argv[1:3])
if source.is_file():
    with open(source, "rb") as f:
        bts = f.read()
    a9a.Archive.from_bytes(bts).to_directory(target)
else:
    with open(target, "wb") as f:
        f.write(a9a.Archive.from_directory(source).to_bytes())
