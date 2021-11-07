import sys
from optparse import OptionParser
import src.sheng.compile as compile


def default(str):
    return str + ' [Default: %default]'

def read_command(argv):
    usage_str = 'sheng [option] [file]'
    parser = OptionParser(usage_str)

    parser.add_option('-d', '--debug', action='store_true', dest='debug',
                      help=default('debug mode'), default=False)
    
    options, other = parser.parse_args(argv[1:])
    if (len(other) == 0):
        parser.error('no input file')
    if (len(other) > 1):
        parser.error('Command line input not understood: ' + str(other[1:]))

    args = dict()
    args['file'] = other[0]
    args['debug'] = options.debug

    return args

def read_file(file, debug):
    f = open(file, "r", encoding='utf-8')
    data = f.read()
    f.close()
    return data, debug

def main():
    args = read_command(sys.argv)
    data, debug = read_file(**args)
    compile.exec(data, debug)
