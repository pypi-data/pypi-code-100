NBSP = '\u00A0'
NNBSP = '\u202F'
WHSP = ' '
ANYSP = fr'[{WHSP}{NBSP}{NNBSP}]'

NDASH = '–'  # Ctrl + "minus" on keyboard \u2013
MDASH = '—'
MDASH_PAIR = NBSP + MDASH + WHSP

MINUS = '−'  # mathematical operator \u2212
HYPHEN_MINUS = '-'  # "minus" on keyboard \u002D
HYPHEN = '‐'  # \u2010
NBHYPHEN = '‑'  # \u2011

TIMES = '×'

LSQUO = '‘'  # left curly quote mark
RSQUO = '’'  # right curly quote mark/apostrophe
LDQUO = '“'  # left curly quote marks
RDQUO = '”'  # right curly quote marks
DLQUO = '„'  # double low curly quote mark
LAQUO = '«'  # left angle quote marks
RAQUO = '»'  # right angle quote marks

SPRIME = '′'
DPRIME = '″'
