#!/usr/bin/python3

# imports

from .__init__ import __doc__ as description, __version__ as version
from argparse import ArgumentParser as Parser, RawDescriptionHelpFormatter as Formatter
from warnings import simplefilter
from os import popen
from sys import argv

# globals

class args: pass # container for arguments

def pypido(argv):
    '...'

    # get arguments
    parser = Parser(prog='pypido', formatter_class=Formatter, description=description)
    parser.add_argument('-H', '--user-guide', action='store_true', help='open User Guide in PDF format and exit')
    parser.add_argument('-V', '--version', action='version', version='pypido ' + version)
    parser.add_argument('-v', '--verbose', action='store_true',    help='show what happens')
    parser.add_argument('-n', '--new', action='store_true',        help='package # create a new unexisting package')
    parser.add_argument('-e', '--edit', action='store_true',       help='package # edit an existing package')
    parser.add_argument('-d', '--delete', action='store_true',     help='package # delete (i.e. remove) an existing package')
    parser.add_argument('-p', '--publish', action='store_true',    help='package # publish an existing package')
    parser.add_argument('-c', '--copy', action='store_true',       help='package package2 # copy an existing package into unexisting package2')
    parser.add_argument('-m', '--move', action='store_true',       help='package package2 # move (i.e. rename) an existing package into unexisting package2')
    parser.add_argument('-l', '--list', action='store_true',       help='# list all existing packages, published or not')
    parser.add_argument('package', nargs='*',                      help='package(s) to process')
    parser.parse_args(argv[1:], args)
    if args.user_guide:
        popen(f'xdg-open docs/pypido.pdf')
        exit()
    if args.new + args.edit + args.delete + args.publish + args.copy + args.move + args.list != 1:
        exit('ERROR: you must give exactly one and only one argument between -n -e -d -p -c -m or -l')
    arg = '-' + ('n' if args.new else 'e' if args.edit else 'd' if args.delete else 'p' if args.publish else 'c' if args.copy else 'm' if args.move else 'l')
    npackage = 0 if args.list else 2 if args.copy or args.move else 1
    if len(args.package) != npackage:
        exit(f'ERROR: with the {arg!r} argument you must give exactly {npackage} package names, not {len(args.package)}')

    def do_new(package): print(f'This is only an empty stub for the {arg!r} action')

    def do_edit(package): print(f'This is only an empty stub for the {arg!r} action')
        
    def do_delete(package): print(f'This is only an empty stub for the {arg!r} action')
        
    def do_publish(package): print(f'This is only an empty stub for the {arg!r} action')
        
    def do_copy(package, package2): print(f'This is only an empty stub for the {arg!r} action')
        
    def do_move(package, package2): print(f'This is only an empty stub for the {arg!r} action')
        
    def do_list(): print(f'This is only an empty stub for the {arg!r} action')
        
    if args.new: do_new(args.package[0])
    elif args.edit: do_edit(args.package[0])
    elif args.delete: do_edit(args.package[0])
    elif args.publish: do_publish(args.package[0])
    elif args.copy: do_copy(args.package[0], args.package[1])
    elif args.move: do_move(args.package[0], args.package[1])
    else: do_list()

def main():
    try:
        simplefilter('ignore')
        pypido(argv)
    except KeyboardInterrupt:
        print()

if __name__ == '__main__':
    main()

