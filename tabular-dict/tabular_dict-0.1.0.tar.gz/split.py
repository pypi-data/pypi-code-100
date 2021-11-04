from flatten_json import split_path, escape_type, inflate


def check(arg, exp):
    print(str(arg).rjust(30), arg == exp)


# check(split_path('\\.', '.', escape_type.SLASH, False), ['.'])
# check(split_path('\\.\\.', '.', escape_type.SLASH, False), ['..'])
# check(split_path('\\.a', '.', escape_type.SLASH, False), ['.a'])
# check(split_path('a\\.', '.', escape_type.SLASH, False), ['a.'])
# check(split_path('key\\.test', '.', escape_type.SLASH, False), ['key.test'])
# check(split_path('[123]', '.', escape_type.SLASH, False), [123])

print(inflate({
    'a.b': 'b',
    'a.c.[0]': 99,
    'a.c.[1]': 98,
    'c': 'c',
}))