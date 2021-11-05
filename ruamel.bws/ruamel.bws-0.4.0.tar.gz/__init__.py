# coding: utf-8

_package_data = dict(
    full_package_name='ruamel.bws',
    version_info=(0, 4, 0),
    __version__='0.4.0',
    version_timestamp='2021-11-05 12:19:57',
    author='Anthon van der Neut',
    description='browser restore to workspace',
    keywords='browser multiple workspace restore',
    author_email='a.van.der.neut@ruamel.eu',
    # install_requires=[],
    since=2014,
    print_allowed=True,
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Internet :: WWW/HTTP :: Browsers',
    ],
)


version_info = _package_data['version_info']
__version__ = _package_data['__version__']


_cligen_data = """\
# all tags start with an uppercase char and can often be shortened to three and/or one
# characters. If a tag has multiple uppercase letter, only using the uppercase letters is a
# valid shortening
# Tags used:
# !Commandlineinterface, !Cli,
# !Option, !Opt, !O
# !PreSubparserOption, !PSO
# !Help, !H
# !Argument, !Arg
# !Module   # make subparser function calls imported from module
# !Instance # module.Class: assume subparser method calls on instance of Class imported from module
# !Action # either one of the actions in subdir _action (by stem of the file) or e.g. "store_action"
# !Config YAML/INI/PON  read defaults from config file
# !AddDefaults
# !Epilog epilog text (for multiline use | )
# !NQS used on arguments, makes sure the scalar is non-quoted e.g for instance/method/function
#      call arguments, when cligen knows about what argument a keyword takes, this is not needed
!Cli 0:
- !Opt [verbose, v, !Help increase verbosity level, !Action count, const: 1, nargs: 0, default: 0]
- !Opt [keep, !Help 'max number of old saves to keep (default: %(default)s)', type: int, default: 10]
- !Instance ruamel.bws.browserworkspace.BrowserWorkspace
- !Config [INI, ~/.config/bws/bws.ini]   # path for backwards compatibility
- save:
  - !Opt [minwin, m, default: 3, type: int, metavar: N, !Help 'minimum number of windows that needs to be open to create a new save file (default: %(default)s)']
  - !Opt [force, !Action store_true, !Help override (configured) minwin setting]
  - !Opt [unlock-file, default: '/tmp/bws.restored', metavar: FILE, !Help 'file that has to exist when doing bws save --check (default: %(default)s)']
  - !Opt [check, !Action store_true, !Help exit if file specified with --unlock-file doesn't exist]
  - !Help "save the current setup, purging old versions\n                     (based on --keep)"
- list:
  - !Help list availabel workspace setups
- restore:
  - !Arg [position, nargs: '?', type: int, default: 0]
  - !Opt [unlock, !Action store_true, !Help create file specified by --unlock-file]
  - !Opt [unlock-file, default: '/tmp/bws.restored', metavar: FILE, !Help 'file that has to exist when doing bws save --check (default: %(default)s)']
  - !Help restore workspace setup (defaults to most recent)
"""  # NOQA
