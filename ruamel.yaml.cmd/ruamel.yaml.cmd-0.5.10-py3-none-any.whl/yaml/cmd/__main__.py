# coding: utf-8
# flake8: noqa
# cligen: 0.1.6, dd: 2021-10-31

import argparse
import importlib
import sys

from . import __version__


class CountAction(argparse.Action):
    """argparse action for counting up and down

    standard argparse action='count', only increments with +1, this action uses
    the value of self.const if provided, and +1 if not provided

    parser = argparse.ArgumentParser()
    parser.add_argument('--verbose', '-v', action=CountAction, const=1,
            nargs=0)
    parser.add_argument('--quiet', '-q', action=CountAction, dest='verbose',
            const=-1, nargs=0)
    """

    def __call__(self, parser, namespace, values, option_string=None):
        if self.const is None:
            self.const = 1
        try:
            val = getattr(namespace, self.dest) + self.const
        except TypeError:  # probably None
            val = self.const
        setattr(namespace, self.dest, val)


def main(cmdarg=None):
    cmdarg = sys.argv if cmdarg is None else cmdarg
    parsers = []
    parsers.append(argparse.ArgumentParser())
    parsers[-1].add_argument('--verbose', '-v', default=None, dest='_gl_verbose', metavar='VERBOSE', nargs=0, help='increase verbosity level', action=CountAction, const=1)
    parsers[-1].add_argument('--indent', metavar='IND', type=int, help='set indent level (default: auto)')
    parsers[-1].add_argument('--bsi', dest='block_seq_indent', metavar='BLOCK_SEQ_IND', type=int, help='set block sequence indent level (default: auto)')
    parsers[-1].add_argument('--smart-string', default=None, dest='_gl_smartstring', action='store_true', help='set literal block style on strings with \\n otherwise plain if possible')
    parsers[-1].add_argument('--version', action='store_true', help='show program\'s version number and exit')
    subp = parsers[-1].add_subparsers()
    px = subp.add_parser('rt', aliases=['round-trip'], description='round trip on YAML document, test if first or second round stabilizes document', help='test round trip on YAML document')
    px.set_defaults(subparser_func='rt')
    parsers.append(px)
    parsers[-1].add_argument('--save', action='store_true', help="save the rewritten data back\n    to the input file (if it doesn't exist a '.orig' backup will be made)\n    ")
    parsers[-1].add_argument('--width', metavar='W', default=80, type=int, help='set width of output (default: %(default)s')
    parsers[-1].add_argument('file', nargs='+')
    parsers[-1].add_argument('--verbose', '-v', nargs=0, default=0, help='increase verbosity level', action=CountAction, const=1)
    parsers[-1].add_argument('--indent', metavar='IND', type=int, help='set indent level (default: auto)')
    parsers[-1].add_argument('--bsi', dest='block_seq_indent', metavar='BLOCK_SEQ_IND', type=int, help='set block sequence indent level (default: auto)')
    parsers[-1].add_argument('--smart-string', action='store_true', help='set literal block style on strings with \\n otherwise plain if possible')
    px = subp.add_parser('me', aliases=['merge-expand'], description='expand merges in input file to output file', help='expand merges in input file to output file')
    px.set_defaults(subparser_func='me')
    parsers.append(px)
    parsers[-1].add_argument('--allow-anchors', action='store_true', help='allow "normal" anchors/aliases in output')
    parsers[-1].add_argument('file', nargs=2)
    parsers[-1].add_argument('--verbose', '-v', nargs=0, default=0, help='increase verbosity level', action=CountAction, const=1)
    parsers[-1].add_argument('--indent', metavar='IND', type=int, help='set indent level (default: auto)')
    parsers[-1].add_argument('--bsi', dest='block_seq_indent', metavar='BLOCK_SEQ_IND', type=int, help='set block sequence indent level (default: auto)')
    parsers[-1].add_argument('--smart-string', action='store_true', help='set literal block style on strings with \\n otherwise plain if possible')
    px = subp.add_parser('json', aliases=['from-json'], description='convert JSON to block-style YAML', help='convert JSON to block-style YAML')
    px.set_defaults(subparser_func='json')
    parsers.append(px)
    parsers[-1].add_argument('--flow', action='store_true', help='use flow-style instead of block style')
    parsers[-1].add_argument('--semi', action='store_true', help='write block style except for "leaf" mapping/dict')
    parsers[-1].add_argument('--literal', action='store_true', help='convert scalars with newlines to literal block style')
    parsers[-1].add_argument('--write', '-w', action='store_true', help='write a  .yaml file, instead of stdout')
    parsers[-1].add_argument('file', nargs='+')
    parsers[-1].add_argument('--verbose', '-v', nargs=0, default=0, help='increase verbosity level', action=CountAction, const=1)
    parsers[-1].add_argument('--indent', metavar='IND', type=int, help='set indent level (default: auto)')
    parsers[-1].add_argument('--bsi', dest='block_seq_indent', metavar='BLOCK_SEQ_IND', type=int, help='set block sequence indent level (default: auto)')
    parsers[-1].add_argument('--smart-string', action='store_true', help='set literal block style on strings with \\n otherwise plain if possible')
    px = subp.add_parser('ini', aliases=['from-ini'], description='convert .ini/config file to block YAML', help='convert .ini/config to block YAML')
    px.set_defaults(subparser_func='ini')
    parsers.append(px)
    parsers[-1].add_argument('--basename', '-b', action='store_true', help='re-use basename of .ini file for .yaml file, instead of writing to stdout')
    parsers[-1].add_argument('--test', action='store_true')
    parsers[-1].add_argument('file')
    parsers[-1].add_argument('--verbose', '-v', nargs=0, default=0, help='increase verbosity level', action=CountAction, const=1)
    parsers[-1].add_argument('--indent', metavar='IND', type=int, help='set indent level (default: auto)')
    parsers[-1].add_argument('--bsi', dest='block_seq_indent', metavar='BLOCK_SEQ_IND', type=int, help='set block sequence indent level (default: auto)')
    parsers[-1].add_argument('--smart-string', action='store_true', help='set literal block style on strings with \\n otherwise plain if possible')
    px = subp.add_parser('htmltable', description='convert YAML to html tables. If hierarchy is two levels deep (\nsequence/mapping over sequence/mapping) this is mapped to one table\nIf the hierarchy is three deep, a list of 2 deep tables is assumed, but\nany non-list/mapp second level items are considered text.\nRow level keys are inserted in first column (unless --no-row-key),\nitem level keys are used as classes for the TD. \n', help='convert YAML to HTML tables')
    px.set_defaults(subparser_func='htmltable')
    parsers.append(px)
    parsers[-1].add_argument('--level', action='store_true', help='print # levels and exit')
    parsers[-1].add_argument('--check')
    parsers[-1].add_argument('file')
    parsers[-1].add_argument('--verbose', '-v', nargs=0, default=0, help='increase verbosity level', action=CountAction, const=1)
    parsers[-1].add_argument('--indent', metavar='IND', type=int, help='set indent level (default: auto)')
    parsers[-1].add_argument('--bsi', dest='block_seq_indent', metavar='BLOCK_SEQ_IND', type=int, help='set block sequence indent level (default: auto)')
    parsers[-1].add_argument('--smart-string', action='store_true', help='set literal block style on strings with \\n otherwise plain if possible')
    px = subp.add_parser('from-html', description='convert HTML to YAML. Tags become keys with as\nvalue a list. The first item in the list is a key value pair with\nkey ".attribute" if attributes are available followed by tag and string\nsegment items. Lists with one item are by default flattened.\n', help='convert HTML to YAML')
    px.set_defaults(subparser_func='from-html')
    parsers.append(px)
    parsers[-1].add_argument('--no-body', action='store_true', help='drop top level html and body from HTML code segments')
    parsers[-1].add_argument('--strip', action='store_true', help='strip whitespace surrounding strings')
    parsers[-1].add_argument('file')
    parsers[-1].add_argument('--verbose', '-v', nargs=0, default=0, help='increase verbosity level', action=CountAction, const=1)
    parsers[-1].add_argument('--indent', metavar='IND', type=int, help='set indent level (default: auto)')
    parsers[-1].add_argument('--bsi', dest='block_seq_indent', metavar='BLOCK_SEQ_IND', type=int, help='set block sequence indent level (default: auto)')
    parsers[-1].add_argument('--smart-string', action='store_true', help='set literal block style on strings with \\n otherwise plain if possible')
    px = subp.add_parser('from-csv', aliases=['csv'], description='convert CSV to YAML.\nBy default generates a sequence of rows, with the items in a 2nd level\nsequence.\n', help='convert CSV to YAML')
    px.set_defaults(subparser_func='from-csv')
    parsers.append(px)
    parsers[-1].add_argument('--mapping', '-m', action='store_true', help='generate sequence of mappings with first line as keys')
    parsers[-1].add_argument('--delimeter', metavar='DELIM', default=',', help='field delimiter (default %(default)s)')
    parsers[-1].add_argument('--strip', action='store_true', help='strip leading & trailing spaces from strings')
    parsers[-1].add_argument('--no-process', dest='process', action='store_false', help='do not try to convert elements into int/float/bool/datetime')
    parsers[-1].add_argument('file')
    parsers[-1].add_argument('--verbose', '-v', nargs=0, default=0, help='increase verbosity level', action=CountAction, const=1)
    parsers[-1].add_argument('--indent', metavar='IND', type=int, help='set indent level (default: auto)')
    parsers[-1].add_argument('--bsi', dest='block_seq_indent', metavar='BLOCK_SEQ_IND', type=int, help='set block sequence indent level (default: auto)')
    parsers[-1].add_argument('--smart-string', action='store_true', help='set literal block style on strings with \\n otherwise plain if possible')
    px = subp.add_parser('from-dirs', aliases=['fromdirs'], description='Combine multiple YAML files into one.\nPath chunks (directories) are converted to mapping entries, the YAML contents\nthe value of the (last) key. If there are multiple files in one directory, the\nfilenames are used as well (or specify --use-file-name).\n', help='combine multiple YAML files into one')
    px.set_defaults(subparser_func='from-dirs')
    parsers.append(px)
    parsers[-1].add_argument('--output', '-o', help='write to file OUTPUT instead of stdout')
    parsers[-1].add_argument('--use-file-names', action='store_true')
    parsers[-1].add_argument('--sequence', action='store_true', help='no paths, each YAML content is made an element of a root level sequence')
    parsers[-1].add_argument('file', nargs='+', help='full path names (a/b/data.yaml)')
    parsers[-1].add_argument('--verbose', '-v', nargs=0, default=0, help='increase verbosity level', action=CountAction, const=1)
    parsers[-1].add_argument('--indent', metavar='IND', type=int, help='set indent level (default: auto)')
    parsers[-1].add_argument('--bsi', dest='block_seq_indent', metavar='BLOCK_SEQ_IND', type=int, help='set block sequence indent level (default: auto)')
    parsers[-1].add_argument('--smart-string', action='store_true', help='set literal block style on strings with \\n otherwise plain if possible')
    px = subp.add_parser('mapping', aliases=['map'], help='create new YAML file with at root a mapping with key and file content')
    px.set_defaults(subparser_func='mapping')
    parsers.append(px)
    parsers[-1].add_argument('--output', '-o', help='write to file OUTPUT instead of stdout')
    parsers[-1].add_argument('key', help='key of the new root-level mapping')
    parsers[-1].add_argument('file', help='file with YAML content that will be value for key')
    parsers[-1].add_argument('--verbose', '-v', nargs=0, default=0, help='increase verbosity level', action=CountAction, const=1)
    parsers[-1].add_argument('--indent', metavar='IND', type=int, help='set indent level (default: auto)')
    parsers[-1].add_argument('--bsi', dest='block_seq_indent', metavar='BLOCK_SEQ_IND', type=int, help='set block sequence indent level (default: auto)')
    parsers[-1].add_argument('--smart-string', action='store_true', help='set literal block style on strings with \\n otherwise plain if possible')
    px = subp.add_parser('add', help='add a value to a path in the data structure loaded from YAML', description='Add a value to a path in the data structure loaded from YAML.\nUse value are resolved like in YAML, use --str if necessary\nThe value is the last args token.\nThe "path" in the data structure is taken from all other args,\ninterpreting numerical values as indices in list/seq.\nE.g.:\n    yaml add --parents --value Windows test.yaml computers os type\n    yaml add --file test.yaml computers os secure false\n    yaml add --str test.yaml computers.os.year 2019\n')
    px.set_defaults(subparser_func='add')
    parsers.append(px)
    parsers[-1].add_argument('--parents', action='store_true', help='create parents if necessary')
    parsers[-1].add_argument('--item', action='store_true', help='create item')
    parsers[-1].add_argument('--key', action='store_true', help='create key, even if not found in siblings of item')
    parsers[-1].add_argument('--str', action='store_true', help='store value as string')
    parsers[-1].add_argument('--file', help='use FILE instead of first argument as YAML file')
    parsers[-1].add_argument('--value', help='use FILE instead of first argument as YAML file')
    parsers[-1].add_argument('--sep', help='set separator for splitting single element path')
    parsers[-1].add_argument('args', nargs='*', help='path in yaml/path.in.yaml [value]')
    parsers[-1].add_argument('--verbose', '-v', nargs=0, default=0, help='increase verbosity level', action=CountAction, const=1)
    parsers[-1].add_argument('--indent', metavar='IND', type=int, help='set indent level (default: auto)')
    parsers[-1].add_argument('--bsi', dest='block_seq_indent', metavar='BLOCK_SEQ_IND', type=int, help='set block sequence indent level (default: auto)')
    parsers[-1].add_argument('--smart-string', action='store_true', help='set literal block style on strings with \\n otherwise plain if possible')
    parsers.pop()
    if '--version' in cmdarg[1:]:
        if '-v' in cmdarg[1:] or '--verbose' in cmdarg[1:]:
            return list_versions(pkg_name='ruamel.yaml.cmd', version=None, pkgs=['configobj', 'ruamel.yaml.convert', 'ruamel.yaml', 'ruamel.yaml.base'])
        print(__version__)
        return
    if '--help-all' in cmdarg[1:]:
        try:
            parsers[0].parse_args(['--help'])
        except SystemExit:
            pass
        for sc in parsers[1:]:
            print('-' * 72)
            try:
                parsers[0].parse_args([sc.prog.split()[1], '--help'])
            except SystemExit:
                pass
        sys.exit(0)
    args = parsers[0].parse_args(args=cmdarg[1:])
    for gl in ['verbose', 'smartstring']:
        glv = getattr(args, '_gl_' + gl, None)
        if glv is not None:
            setattr(args, gl, glv)
        delattr(args, '_gl_' + gl)
    cls = getattr(importlib.import_module('ruamel.yaml.cmd.yaml_cmd'), 'YAMLCommand')
    obj = cls(args)
    funcname = getattr(args, 'subparser_func', None)
    if funcname is None:
        parsers[0].parse_args('--help')
    fun = getattr(obj, args.subparser_func)
    return fun()

def list_versions(pkg_name, version, pkgs):
    version_data = [
        ('Python', '{v.major}.{v.minor}.{v.micro}'.format(v=sys.version_info)),
        (pkg_name, __version__ if version is None else version),
    ]
    for pkg in pkgs:
        try:
            version_data.append(
                (pkg,  getattr(importlib.import_module(pkg), '__version__', '--'))
            )
        except ModuleNotFoundError:
            version_data.append((pkg, 'NA'))
        except KeyError:
            pass
    longest = max([len(x[0]) for x in version_data]) + 1
    for pkg, ver in version_data:
        print('{:{}s} {}'.format(pkg + ':', longest, ver))


if __name__ == '__main__':
    sys.exit(main())
