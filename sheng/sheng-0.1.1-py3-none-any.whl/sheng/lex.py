from .ply import lex
import itertools as _itertools


STATE_KEYWORDS = [
    '字符串'
]

RESERVED_KEYWORDS = {
    '赋值': 'EQUAL',
    '开始': 'BEGIN',
    '结束': 'END',
    '打印': 'PRINT',
    '定义': 'FUNCTIONDEF',
    '返回': 'RETURN',
    '呼叫': 'CALL',
    '如果': 'IF',
    '则': 'THEN',
    '否则如果': 'ELIF',
    '否则': 'ELSE',
    '对': 'TRUE',
    '错': 'FALSE',
    '与': 'AND',
    '或': 'OR',
    '非': 'NOT',
    '列表': 'LIST_TYPE',
    '索引': 'INDEX',
    '迭代': 'ITERATE',
    '循环': 'LOOP',
    '继续': 'CONTINUE',
    '停止': 'BREAK',
    '字符串': 'STRING_TYPE'
}

EXACT_TOKEN_TYPES = RESERVED_KEYWORDS | {
    '(': 'LPAR',
    ')': 'RPAR',
    '+': 'PLUS',
    '-': 'MINUS',
    '*': 'STAR',
    '/': 'SLASH',
    '**': 'DOUBLESTAR',
    '//': 'DOUBLESLASH',
    '%': 'PERCENT',
    '==': 'EQEQUAL',
    '!=': 'NOTEQUAL',
    '<': 'LESS',
    '<=': 'LESSEQUAL',
    '>': 'GREATER',
    '>=': 'GREATEREQUAL',
    '!': 'NOT'
}

# List of token names.   This is always required
tokens = tuple(set(EXACT_TOKEN_TYPES.values())) + (
    'INTEGER', 'FLOAT', 'COMPLEX', 'STRING', 'NAME'
)

# States
states = (
    ('string', 'inclusive'),
)

# Regular expression rules for tokens
t_LPAR = r'\('
t_RPAR = r'\)'
t_PLUS = r'\+'
t_MINUS = r'-'
t_STAR = r'\*'
t_SLASH = r'/'
t_DOUBLESTAR = r'\*\*'
t_DOUBLESLASH = r'//'
t_PERCENT = r'%'
t_EQEQUAL = r'=='
t_NOTEQUAL = r'!='
t_LESS = r'<'
t_LESSEQUAL = r'<='
t_GREATER = r'>'
t_GREATEREQUAL = r'>='
t_TRUE = r'对'
t_FALSE = r'错'
t_AND = r'与'
t_OR = r'或'
t_NOT = r'(非)|\!'
t_EQUAL = r'赋值'
t_BEGIN = r'开始'
t_END = r'结束'
t_PRINT = r'打印'
t_FUNCTIONDEF = r'定义'
t_RETURN = r'返回'
t_CALL = r'呼叫'
t_IF = r'如果'
t_THEN = r'则'
t_ELIF = r'否则如果'
t_ELSE = r'否则'
t_LIST_TYPE = r'列表'
t_INDEX = r'索引'
t_ITERATE = r'迭代'
t_LOOP = r'循环'
t_CONTINUE = r'继续'
t_BREAK = r'停止'

# Define identifier rule that can only allow chinese characters
def t_NAME(t):
    r'[^\x00-\xff]+'
    if (t.value in RESERVED_KEYWORDS):
        t.type = RESERVED_KEYWORDS[t.value]
    if (t.value == '字符串'):
        return t_begin_STRING_TYPE(t)
    return t

# Define a rule so we can track line numbers
def t_NEWLINE(t):
    r'\n'
    t.lexer.lineno += 1
    # return t

def group(*choices): return '(' + '|'.join(choices) + ')'
def any(*choices): return group(*choices) + '*'
def maybe(*choices): return group(*choices) + '?'

# Ignore
Whitespace = r'[ \f\t]*'
Comment = r'\#[^\r\n]*'
Ignore = Whitespace + any(r'\\\r?\n' + Whitespace) + maybe(Comment)

t_ignore_COMMENT = Comment
t_ignore = ' \t'

# Number
Hexnumber = r'0[xX](?:_?[0-9a-fA-F])+'
Binnumber = r'0[bB](?:_?[01])+'
Octnumber = r'0[oO](?:_?[0-7])+'
Decnumber = r'(?:0(?:_?0)*|[1-9](?:_?[0-9])*)'
Intnumber = group(Hexnumber, Binnumber, Octnumber, Decnumber)
Exponent = r'[eE][-+]?[0-9](?:_?[0-9])*'
Pointfloat = group(r'[0-9](?:_?[0-9])*\.(?:[0-9](?:_?[0-9])*)?',
                   r'\.[0-9](?:_?[0-9])*') + maybe(Exponent)
Expfloat = r'[0-9](?:_?[0-9])*' + Exponent
Floatnumber = group(Pointfloat, Expfloat)
Imagnumber = group(r'[0-9](?:_?[0-9])*[jJ]', Floatnumber + r'[jJ]')
Number = group(Imagnumber, Floatnumber, Intnumber)

t_INTEGER = Intnumber
t_FLOAT = Floatnumber
t_COMPLEX = Imagnumber

# String
def t_begin_STRING_TYPE(t):
    r'字符串'
    t.lexer.begin('string')
    return t

def t_string_BEGIN(t):
    r'开始'
    return t

def t_string_STRING(t):
    r'([^(结束)\\]+|(\\(结束))|\\.)+'
    t.value = t.value.strip() \
        .replace('\结束', '结束') \
        .replace('\开始', '开始')
    return t

def t_string_END(t):
    r'结束'
    t.lexer.begin('INITIAL')
    return t

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()
