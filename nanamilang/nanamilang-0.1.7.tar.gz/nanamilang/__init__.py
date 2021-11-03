"""NanamiLang Package"""

# This file is a part of NanamiLang Project
# This project licensed under GNU GPL version 2
# Initially made by @jedi2light (aka Stoian Minaiev)

from nanamilang.ast import AST
from nanamilang.token import Token
from nanamilang.program import Program
from nanamilang.builtin import Builtin
from nanamilang.formatter import Formatter
from nanamilang.tokenizer import Tokenizer

__pkg_name__ = 'nanamilang'
__pkg_desc__ = 'NanamiLang - Chiaki Nanami Language'
__project_url__ = 'https://nanamilang.jedi2light.moe/'
__project_license__ = 'GNU GPL v2'
__author__ = '@jedi2light'
__author_email__ = 'stoyan.minaev@gmail.com'
__maintainer__ = __author__
__maintainer_email__ = __author_email__
__major_version__ = 0
__minor_version__ = 1
__patch_version__ = 7
__version_tuple__ = (__major_version__,
                     __minor_version__,
                     __patch_version__)
__version_string__ = '.'.join(list(map(str, __version_tuple__)))
