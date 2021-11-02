import shutil
import os

try:
    import ujson as json
    
except (ModuleNotFoundError, ImportError):
    try:
        import simplejson as json
        
    except (ModuleNotFoundError, ImportError):
        import json

from .exception import *
from .objtype import objtype

from pathlib import Path as p

class fil:
    """File Manipulation"""
    def move(self, start, end):
        """Moves files"""
        shutil.move(start, end)
        return 0

    def rename(self, orig, new):
        """Renames files, also kinda works to move files, and vice versa"""
        os.rename(p(orig), p(new))
        return 0

    def delete(self, fi, force=False):
        """Deletes files/folders"""
        fi = str(p(fi))
        if os.path.isdir(fi):
            shutil.rmtree(fi)
            
        elif os.path.isfile(fi):
            os.remove(fi)
            
        else:
            if force:
                try:
                    shutil.rmtree(fi)
                    
                except:
                    os.remove(fi)
                    
            else:
                return 1
            
        return 0
    
    def dump(self, fi, data):
        """Dumps data to a file"""
        with open(p(fi), "w", encoding="iso-8859-1") as f:
            f.write(data)
            f.close()
            
        return 0

    def bdump(self, fi, data):
        """Dumps binary (non-text) data to a file"""
        with open(p(fi), "wb", encoding="iso-8859-1") as f:
            try:
                inp = data.encode("iso-8859-1")
                f.write(inp)
                
            except AttributeError:
                try:
                    inp = data.decode("iso-8859-1")
                    inp = data.encode("iso-8859-1")
                    f.write(inp)
                    
                except AttributeError:
                    f.write(str(data).encode("iso-8859-1"))
                
            f.close()
            
        return 0
    
    def jdump(self, fi, data, pp=True):
        """Dumps a dict into a .json file in JSON format
        with or without pretty print."""
        with open(p(fi), "w", encoding="iso-8859-1") as f:
            if objtype(pp) != "bool":
                f.close()
                raise InvalidPPBool("Argument \"pp\" must be bool")
            
            if pp:
                json.dump(data, f, indent=4)
                
            elif not pp:
                json.dump(data, f)
                
            else:
                raise UnknownError("¯\_(ツ)_/¯")
            
        return 0

    def load(self, fi):
        """Reads data from text files."""
        with open(p(fi), "r", encoding="iso-8859-1") as f:
            return f.read()
        
    def bload(self, fi):
        """Reads data from binary (non-text) files."""
        with open(p(fi), "rb", encoding="iso-8859-1") as f:
            return f.read()
        
    def jload(self, fi):
        """Reads data from JSON files."""
        with open(p(fi), "r", encoding="iso-8859-1") as f:
            return json.loads(f.read())

file = fil()
del fil