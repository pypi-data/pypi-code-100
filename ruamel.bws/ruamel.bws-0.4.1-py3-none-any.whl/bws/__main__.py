# coding: utf-8
# flake8: noqa
# cligen: 0.1.6, dd: 2021-11-05

import argparse
import configparser
import importlib
import os
import pathlib
import sys

from . import __version__


class ConfigBase:
    def __init__(self, path=None, parser=None):
        self._parser = parser
        self._data = None
        tmp_path = self.get_config_parm()
        if tmp_path:
            self._path = tmp_path
        elif isinstance(path, pathlib.Path):
            self._path = path
        elif path is not None:
            if path[0] in '~/':
                self._path = pathlib.Path(path).expanduser()
            elif '/' in path:  # assume '!Config config_dir/config_name'
                self._path = self.config_dir / path
            else:
                self._path = self.config_dir / path / (path.rsplit('.')[-1] + self.suffix)
        else:
            # could use sys.argv[0]
            raise NotImplementedError

    @property
    def data(self):
        if self._data is None:
            self.set_defaults()
        return self._data

    def set_defaults(self):
        self._data = self.load()  # NOQA
        self._set_section_defaults(self._parser, self._data.get('global', {}))
        if self._parser._subparsers is None:
            return
        assert isinstance(self._parser._subparsers, argparse._ArgumentGroup)
        progs = set()
        for sp in self._parser._subparsers._group_actions:
            if not isinstance(sp, argparse._SubParsersAction):
                continue
            for k in sp.choices:
                subp_action = sp.choices[k]
                if 'global' in self._data:
                    self._set_section_defaults(subp_action, self._data['global'], glbl=False)
                if k not in self._data:
                    continue
                if subp_action.prog not in progs:
                    progs.add(subp_action.prog)
                    self._set_section_defaults(subp_action, self._data[k], glbl=False)
        # if self._save_defaults:
        #     self.parse_args()

    def _set_section_defaults(self, parser, section, glbl=True):
        assert isinstance(section, dict)
        defaults = {}
        for action in parser._get_optional_actions():
            if isinstance(action,
                          (argparse._HelpAction,
                           argparse._VersionAction,
                           # SubParsersAction._AliasesChoicesPseudoAction,
                           )):
                continue
            for x in action.option_strings:
                if not x.startswith('-'):
                    continue
                try:
                    # get value based on long-option (without --)
                    # store in .dest
                    v = section[x.lstrip('-')]
                    defaults[action.dest] = v
                except KeyError:  # not in config file
                    if glbl:
                        if x == '--config':
                            defaults[action.dest] = self._path
                    else:
                        try:
                            if self._data[glbl] is None:
                                raise KeyError
                            defaults[action.dest] = self[glbl][x.lstrip('-')]
                        except KeyError:  # not in config file
                            pass
                break  # only first --option
        parser.set_defaults(**defaults)

    def get_config_parm(self):
        # check if --config was given on commandline
        for idx, arg in enumerate(sys.argv[1:]):
            if arg.startswith('--config'):
                if len(arg) > 8 and arg[8] == '=':
                    return pathlib.Path(arg[9:])
                else:
                    try:
                        return pathlib.Path(sys.argv[idx + 2])
                    except IndexError:
                        print('--config needs an argument')
                        sys.exit(1)
        return None

    @property
    def config_dir(self):
        # https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html
        attr = '_' + sys._getframe().f_code.co_name
        if not hasattr(self, attr):
            if sys.platform.startswith('win32'):
                d = os.environ['APPDATA']
            else:
                d = os.environ.get(
                    'XDG_CONFIG_HOME', os.path.join(os.environ['HOME'], '.config')
                )
            pd = pathlib.Path(d)
            setattr(self, attr, pd)
            return pd
        return getattr(self, attr)


class ConfigINI(ConfigBase):
    suffix = '.ini'

    def load(self):
        config = configparser.ConfigParser()
        config.read(self._path)
        data = {section.lower(): dict(config.items(section)) for section in config.sections()}
        defaults = dict(config.defaults())
        if defaults:
            data['default'] = defaults
        return data


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
    parsers[-1].add_argument('--keep', default=None, dest='_gl_keep', metavar='KEEP', help='max number of old saves to keep (default: %(default)s)', type=int)
    parsers[-1].add_argument('--version', action='store_true', help='show program\'s version number and exit')
    subp = parsers[-1].add_subparsers()
    px = subp.add_parser('save', help='save the current setup, purging old versions\n                     (based on --keep)')
    px.set_defaults(subparser_func='save')
    parsers.append(px)
    parsers[-1].add_argument('--minwin', '-m', default=3, type=int, metavar='N', help='minimum number of windows that needs to be open to create a new save file (default: %(default)s)')
    parsers[-1].add_argument('--force', action='store_true', help='override (configured) minwin setting')
    parsers[-1].add_argument('--unlock-file', default='/tmp/bws.restored', metavar='FILE', help='file that has to exist when doing bws save --check (default: %(default)s)')
    parsers[-1].add_argument('--check', action='store_true', help="exit if file specified with --unlock-file doesn't exist")
    parsers[-1].add_argument('--verbose', '-v', nargs=0, default=0, help='increase verbosity level', action=CountAction, const=1)
    parsers[-1].add_argument('--keep', help='max number of old saves to keep (default: %(default)s)', type=int)
    px = subp.add_parser('list', help='list availabel workspace setups')
    px.set_defaults(subparser_func='list')
    parsers.append(px)
    parsers[-1].add_argument('--verbose', '-v', nargs=0, default=0, help='increase verbosity level', action=CountAction, const=1)
    parsers[-1].add_argument('--keep', help='max number of old saves to keep (default: %(default)s)', type=int)
    px = subp.add_parser('restore', help='restore workspace setup (defaults to most recent)')
    px.set_defaults(subparser_func='restore')
    parsers.append(px)
    parsers[-1].add_argument('position', nargs='?', type=int, default=0)
    parsers[-1].add_argument('--unlock', action='store_true', help='create file specified by --unlock-file')
    parsers[-1].add_argument('--unlock-file', default='/tmp/bws.restored', metavar='FILE', help='file that has to exist when doing bws save --check (default: %(default)s)')
    parsers[-1].add_argument('--verbose', '-v', nargs=0, default=0, help='increase verbosity level', action=CountAction, const=1)
    parsers[-1].add_argument('--keep', help='max number of old saves to keep (default: %(default)s)', type=int)
    parsers.pop()
    config = ConfigINI(path='~/.config/bws/bws.ini', parser=parsers[0])
    config.set_defaults()
    if '--version' in cmdarg[1:]:
        if '-v' in cmdarg[1:] or '--verbose' in cmdarg[1:]:
            return list_versions(pkg_name='ruamel.bws', version=None, pkgs=[])
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
    for gl in ['verbose', 'keep']:
        glv = getattr(args, '_gl_' + gl, None)
        if glv is not None:
            setattr(args, gl, glv)
        delattr(args, '_gl_' + gl)
    cls = getattr(importlib.import_module('ruamel.bws.browserworkspace'), 'BrowserWorkspace')
    obj = cls(args, config=config)
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
