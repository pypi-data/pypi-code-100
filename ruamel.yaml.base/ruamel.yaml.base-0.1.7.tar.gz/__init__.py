# coding: utf-8

from __future__ import print_function, absolute_import, division, unicode_literals

_package_data = dict(
    full_package_name='ruamel.yaml.base',
    version_info=(0, 1, 7),
    __version__='0.1.7',
    author='Anthon van der Neut',
    author_email='a.van.der.neut@ruamel.eu',
    description='YAMLBase class with saving loading and version support',
    # keywords="",
    entry_points='base=ruamel.yaml.base.__main__:main',
    # entry_points=None,
    license='Copyright Ruamel bvba 2007-2021',
    since=2016,
    # status="α|β|stable",  # the package status on PyPI
    # data_files="",
    universal=True,
    nested=True,
    install_requires=['ruamel.yaml'],
    tox=dict(env='23', deps=['python-dateutil', 'beautifulsoup4']),
)

version_info = _package_data['version_info']
__version__ = _package_data['__version__']

#################################

import sys  # NOQA
from pathlib import Path  # NOQA
import ruamel.yaml  # NOQA


class YAMLBase:
    """
    top level should be a mapping (for version, creating)
    """

    def __init__(self, path=None, verbose=0, create_ok=None):
        if not isinstance(path, Path):
            path = Path(path)
        self._path = path
        self._data = None
        self._changed = False

        # if not getattr(self, '_create_ok', False):
        #     if not self._path.exists():
        #         print('cannot open', self._path)
        #         sys.exit(1)

        # newer version allows for create_ok argument to instantiation
        if not self._path.exists():
            create_ok = getattr(self, '_create_ok', create_ok)
            if create_ok in [None, False]:
                print('cannot open', self._path)
                sys.exit(1)
            if create_ok is True:
                self._data = ruamel.yaml.comments.CommentedMap()
            else:
                self._data = create_ok
            self._changed = True
        self._verbose = verbose
        self._last_read = None
        self._yaml = ruamel.yaml.YAML()
        self._yaml.preserve_quotes = True

    @property
    def data(self):
        """access the data, reread if changed on disc and not changed in memory"""
        if self._data is not None and self._changed:  # if changed don't re-read
            return self._data
        if not self._last_read or self._last_read < self._path.stat().st_mtime:
            if self._verbose > 0:
                # you can read None from a YAML document, so the following is not
                # entirly correct
                sys.stdout.write(
                    'data {}reading {}\n'.format(
                        're-' if self._data is not None else '', self._path
                    )
                )
            self._data = None
        if self._data is None:
            try:
                self._data = self._yaml.load(self._path)
            except FileNotFoundError:  # NOQA
                if not self._create_ok:
                    raise
                self._data = ruamel.yaml.comments.CommentedMap()
                self._changed = True
            self.check_version()
            self._last_read = -1 if not self._path.exists() else self._path.stat().st_mtime
        return self._data

    @property
    def fast_data(self):
        import ruamel.yaml.cyaml  # NOQA

        if self._data is not None:
            return self._data
        yaml = ruamel.yaml.YAML(typ='safe')
        return yaml.load(self._path)

    def save(self, force=False, out=None):
        # should check if file changed on disc and warn
        if not force and not self._changed:
            return
        assert self._data is not None
        # if out is None:
        #     with self._path.open('wb') as out:
        #         ruamel.yaml.main.round_trip_dump(self._data, out)
        # else:
        #     ruamel.yaml.main.round_trip_dump(self._data, out)
        if out is None:
            out = self._path
            self._changed = False
        if self._verbose > 0:
            sys.stdout.write(f'writing: {self._path}\n')
        self._yaml.dump(self._data, out)
        return True

    def check_version(self):
        """this should be specified by subclass if needed"""
        pass


if __name__ == '__main__':
    for x in sys.argv[1:]:
        yb = YAMLBase(x)
        print(yb.fast_data)
