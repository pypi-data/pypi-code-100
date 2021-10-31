# pylint: disable=broad-except, eval-used

# module-level docstring
__doc__='''
FileSystemDataBase
==================

A collection of tools for having a cached representation of
a file system.

API:
    - FSindex
    - CachedFS
    - 
    - 

See elements' docstrings for further explanations.
'''

from pathlib import Path
import re
import json
from typing import Callable, Union, List, Dict
from .decorators import timer


def FSindex( root: Path, condition: Callable = lambda x: True ) -> Dict[str,dict]:
    ''' Returns a dictionnary such as
    - Contains <root_path:str> as only key
    - Recursively represents contained files and subdirectories, with each their subdirectories, etc
    '''
    assert root.is_dir()
    _root = root.resolve()

    def recursive_collection( _dir: Path ):
        def try_recursion( location: Path ):
            try:
                return recursive_collection( location ) if location.is_dir() else None
            except Exception as e:
                print(f"FSindex: something went wrong at '{root}'. Error:\n{e}")
                return None

        return {
            str(child.name): try_recursion( child )
            for child in _dir.iterdir()
            if condition( child )
        }

    root_s = root.as_posix()
    if root_s[-1] == '/':
        root_s = root_s[:-1]

    return {
        root_s: recursive_collection( root )
    }


class CachedFS:
    ''' Caching a filesystem tree can be useful for applications
    with frequent file system lookups.
    
    Features :
     - Possiblity to backup to/load from JSON file
     - cache directories, files, or both
    '''

    def __init__( self, root: Path, directories: bool = True, files: bool = True, backup_fs: dict = None ) -> None:

        if backup_fs:
            self.root = Path( backup_fs['root'] )
            assert root.samefile(self.root), f"ERROR: given root path '{root}' is different from backup root path '{self.root}' !"
            assert self.root.is_dir(), f"It seems root='{self.root}' is no longer a valid directory !"
            self.filter_text = backup_fs['filter']
            self.filter = eval( backup_fs['filter'] )
            self.fs = backup_fs['fs']

        else:
            assert files or directories, "CachedFS cannot be instantiated with directories=files=False."
            assert root.is_dir(), f"root='{root}' is not a valid directory"
            self.root = root.resolve()
            condition = ' or '.join( [
                x
                for x in [
                    'x.is_dir()' if directories else None,
                    'x.is_file()' if files else None
                ]
                if x is not None 
            ] )
            self.filter_text = f'lambda x: {condition}'
            self.filter = eval( self.filter_text )
            self.update()
        
        
    @timer
    def update( self ) -> None:
        ''' Updates internal DB '''
        self.fs = FSindex( self.root, self.filter )


    def __contains__( self, pattern: str ) -> bool:
        ''' Implements `<pattern:str> in <_:CachedFS>` operation
        '''
        _pattern = re.compile(pattern, flags=re.IGNORECASE )

        return 0 < len( self.search( 
            search_for=_pattern,
            stop_at_first=True
        ) )


    @timer
    def search( self, search_for: Union[str,re.Pattern,Callable], stop_at_first: bool = False ) -> List[str]:
        ''' Performs a search on internal FileSystem representation.

        `search_for`: Match criterion. Can be a string (matches file/directory name; case insensitive),
        a re.Pattern (matches with re.Pattern.match()) or a callable (must return boolean values; match
        on True).

        `stop_at_first`: returns at most one matching item.
        '''

        if callable(search_for):
            _search_for = search_for
        if isinstance(search_for, re.Pattern):
            _search_for = lambda x: bool(search_for.match(x))
        if isinstance(search_for, str):
            search_for_lower = search_for.lower()
            _search_for = lambda x: search_for_lower in x.lower()

        combine_paths = lambda x,y: f"{x}/{y}" if x else y

        def search_recursive( FSDB: dict, path_prefix: str = '' ):
            matches = list()
            #print(f"search_recursive: from '{path_prefix}'")
            try:
                for item, children in FSDB.items():
                    if _search_for( item ):
                        #print(f"Positive: '{item}'")
                        matches.append( combine_paths( path_prefix, item ) )
                        if stop_at_first:
                            return matches
                    if children:
                        matches.extend( 
                            search_recursive( children, combine_paths( path_prefix, item ) )
                        )
                    if stop_at_first and matches:
                        return matches
            except Exception as e:
                print(f"search_recursive: something went wrong at '{path_prefix}'. Error:\n{e}")
                raise
            
            return matches
        
        return search_recursive( self.fs )


    def as_json( self ) -> str:
        ''' Dumps CachedFS as json-formatted string '''
        data = {
            'root': str(self.root),
            'fs': self.fs,
            'filter': self.filter_text
        }
        return json.dumps( data, indent=2 )

    
    def backup_to_file( self, backup_file: Path ) -> None:
        ''' Dumps CachedFS to json-formatted file '''
        assert backup_file.suffix.lower() == '.json'
        backup_file.write_text( self.as_json(), encoding='utf8' )


    @classmethod
    def from_file( cls, backup_file: Path, root: Path ):
        ''' Loads CachedFS from json-formatted string produced by CachedFS.backup_to_file() function.
        Note: `root` is required to verify the intended root matches root in cache file.
        '''
        assert backup_file.suffix.lower() == '.json'
        backup = json.loads( backup_file.read_text( encoding='utf8' ) )
        return CachedFS( root=root, backup_fs=backup )
    