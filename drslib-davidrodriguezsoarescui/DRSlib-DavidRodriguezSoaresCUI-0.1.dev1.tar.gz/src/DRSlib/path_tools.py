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
import logging
log = logging.getLogger( __file__ )


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
        