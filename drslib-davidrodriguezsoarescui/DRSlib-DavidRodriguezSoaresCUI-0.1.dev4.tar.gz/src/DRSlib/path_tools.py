# pylint: disable=too-few-public-methods

# module-level docstring
__doc__='''
FileSystemDataBase
==================

Easy to use tool to collect files matching a pattern.

Note: both class and function versions should be euivalent, both kept
just in case. Class may be usefull for repeated calls to `collect` method.

API:
    - FileCollector
    - file_collector

See elements' docstrings for further explanations.
'''

from typing import Union, Iterable, List
from pathlib import Path
import re
import logging
log = logging.getLogger( __file__ )

MAKE_FS_SAFE_PATTERN = re.compile( pattern=r'[\\/*?:"<>|]' )


class FileCollector:
    ''' Easy to use tool to collect files matching a pattern (recursive or not), using pathlib.glob. 
    Reasoning for making it a class: Making cohexist an initial check/processing on root with a recursive
    main function was not straightforward. I did it anyway, so feel free to use the function alternative. '''

    def __init__( self, root: Path ) -> None:
        assert root.is_dir()
        root.resolve()
        self.root = root
        self.log = logging.getLogger( __file__ )
        self.log.debug( "root=%s", root )

    def collect( self, pattern: Union[str,Iterable[str]] = '**/*.*' ) -> List[Path]:
        ''' Collect files matching given pattern(s) '''
        files = []
        
        if isinstance( pattern, str ):
            # 11/11/2020 BUGFIX : was collecting files in trash like a cyber racoon
            files = [
                item.resolve() 
                for item in self.root.glob( pattern )
                if item.is_file() and (not '$RECYCLE.BIN' in item.parts)
            ]

            self.log.debug( "\t'%s': Found %s files in %s", pattern, len(files), self.root )
        elif isinstance( pattern, Iterable ):
            patterns = pattern
            assert 0 < len(patterns)
            for p in patterns:
                files.extend( self.collect(p) )
        else:
            raise ValueError(f"FileCollector: 'pattern' ({pattern}) must be an Iterable or a string, but is a {type(pattern)}")

        return files
        

def file_collector( root: Path, pattern: Union[str,Iterable[str]] = '**/*.*' ) -> List[Path]:
    ''' Easy to use tool to collect files matching a pattern (recursive or not), using pathlib.glob.
    Collect files matching given pattern(s) '''
    assert root.is_dir()
    root.resolve()
    log.debug( "root=%s", root )

    def collect( _pattern: str ) -> List[Path]:
        # 11/11/2020 BUGFIX : was collecting files in trash like a cyber racoon
        _files = [
            item.resolve() 
            for item in root.glob( pattern )
            if item.is_file() and (not '$RECYCLE.BIN' in item.parts)
        ]
        log.debug( "\t'%s': Found %s files in %s", pattern, len(_files), root )
        return _files

    files = []
    if isinstance( pattern, str ):
        files = collect( pattern )
    elif isinstance( pattern, Iterable ):
        patterns = pattern
        assert 0 < len(patterns)
        for p in patterns:
            files.extend( collect(p) )
    else:
        raise ValueError(f"FileCollector: 'pattern' ({pattern}) must be an Iterable or a string, but is a {type(pattern)}")

    return files


def make_FS_safe( s: str ) -> str:
    ''' File Systems don't accept all characters on file/directory names.
    Return s with illegal characters stripped
    Note: OS/FS agnostic, applies a simple filter on characters: backslash, /, *, ?, :, ", <, >, |
    '''
    return re.sub(
        pattern=MAKE_FS_SAFE_PATTERN,
        repl="",
        string=s
    )

def find_available_path( root: Path, base_name, file: bool ) -> Path:
    ''' Returns a path to a file/directory that DOESN'T already exist.
    The file/dir the user wishes to make a path for is referred as X.

    `root`: where X must be created. Can be a list of path parts
    `base_name`: the base name for X. May be completed with '(index)' if name already exists.
    `file`: True if X is a file, False if it is a directory
    '''
    # Helper function: makes suffixes for already existing files/directories
    def suffixes():
        yield ''
        idx=0
        while True:
            idx+=1
            yield f" ({idx})"
    
    # Iterate over candidate paths until an unused one is found
    safe_base_name = make_FS_safe( base_name )
    if file:
        # name formatting has to keep the extension at the end of the name !
        ext_idx = safe_base_name.rfind('.')
        assert ext_idx!=-1
        f_name, f_ext = safe_base_name[:ext_idx], safe_base_name[ext_idx:]
        for suffix in suffixes():
            _object = root / ( f_name + suffix + f_ext )
            if not _object.is_file():
                return _object
    else:
        for suffix in suffixes():
            _object = root / ( safe_base_name + suffix )
            if not _object.is_dir():
                return _object


def make_valid_path( 
    root: Union[Path, List],
    base_name: str,
    file: bool = True,
    create: bool = False ) -> Path:
    ''' Returns a path to a file/directory that DOESN'T already exist.
    The file/dir the user wishes to make a path for is referred as X.

    `root`: where X must be created. Can be a list of path parts
    `base_name`: the base name for X. May be completed with '(index)' if name already exists.
    `file`: True if X is a file, False if it is a directory
    `create`: True instantiates X (empty file or dir), False doesn't

    Build upon `find_available_path`, adding:
    - root path construction
    - root mkdir
    - ability to initialize returned file/dir
    '''

    # make root path
    if isinstance(root, List):
        if isinstance(root[0], str):
            _root = Path(make_FS_safe(root[0]))
        elif isinstance(root[0], Path):
            _root = root[0]
        else:
            raise TypeError(f"root[0]={root[0]} is of unexpected type {type(root[0])}, not str or Path !")
        
        for path_part in root[1:]:
            assert isinstance(path_part, str), f"path part in root '{path_part}' is of unexpected type {type(path_part)}, not str !"
            safe_path_part = make_FS_safe(path_part)
            assert safe_path_part
            _root = _root / safe_path_part
    elif isinstance(root, Path):
        _root = root
    else:
        raise TypeError(f"root={root} is of unexpected type {type(root)}, not str or Path !")
            
    # make root directory
    if not _root.is_dir():
        _root.mkdir( parents=True )

    # Find valid path
    valid_path = find_available_path(
        _root,
        base_name,
        file
    )

    # Optionally create file/dir
    if create:
        if file:
            valid_path.touch()
        else:
            valid_path.mkdir()

    return valid_path