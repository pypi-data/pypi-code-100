from .lex import lexer
from .parse import parser
from .symtable import SymbolTable


def exec(data, debug=False):
    if (debug):
        print('[DEBUG] input data as raw string:')
        print(repr(data))
        print('[DEBUG] input data as string:')
        print(data)

    lexer.input(data)

    if (debug):
        print('[DEBUG] tokens:')
        while (True):
            tok = lexer.token()
            if (not tok): break
            print(tok)
    
    if (debug):
        print('[DEBUG] program output:')
    
    symtable = SymbolTable()
    ast = parser.parse(data)
    ast.evaluate(symtable)
