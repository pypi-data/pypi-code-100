#!/usr/bin/env python
# coding: utf-8

from __future__ import print_function

import sys
import os
import errno
import subprocess
import json
import glob
import datetime


_default_minwin = 3
_default_keep = 10

_default_config = f"""\
[global]
keep = {_default_keep}
[save]
minwin = {_default_minwin}
[br-firefox]
basenamestart = firefox-trunk, firefox
[br-chrome]
basenamestart = chromium-browser, chrome
"""


class BrowserWorkspace(object):
    """"""

    # names of the fields returned by wmctrl -l -G -p
    _names = 'wid workspace pid x y w h hostname title'.split()

    def __init__(self, args, config):
        self._args = args
        self._config = config
        self._browsers = {}
        self._nr_windows = 0
        self._format_version = 1
        # self._path_pattern = os.path.join(
        #     os.path.dirname(self._config.get_file_name()), '{}.bws'
        # )
        if not self._config._path.exists():
            self._config._path.parent.mkdir(parents=True, exist_ok=True)
            self._config._path.write_text(_default_config)
            self._config._data = None
        self._path_pattern = str(self._config._path.parent / '{}.bws')

    def ewmh(self):
        NR_PARTS = 8
        start = []
        data = self._config.data
        for key in data:
            if not key.startswith('br-'):
                continue
            val = data[key].get('basenamestart')
            if val is None:
                print(
                    "your config file ({}) doesn't have basenamestart\n"
                    '    defintions for key: {}'.format(self._config._path, key)
                )
                continue
            if not isinstance(val, list):
                val = [v.strip() for v in val.split(',')]
                # val = [val]
            start.extend(val)
        if not start:
            print(
                "your config file ({}) doesn't have any\n   "
                'br-*/basenamestart defintions'.format(self._config._path)
            )
            sys.exit()
        res = subprocess.check_output('wmctrl -l -G -p'.split()).decode('utf-8')
        self._browsers = {}
        self._nr_windows = 0
        for line in res.splitlines():
            parts = line.split(None, NR_PARTS)
            pids = parts[2]
            parts = (
                [parts[0]]
                + [int(x) for x in parts[1 : NR_PARTS - 1]]
                + [z for z in parts[NR_PARTS - 1 :]]
            )
            # pid = parts[2]
            exe = '/proc/' + pids + '/exe'
            try:
                full_path = os.path.realpath(exe)
            except OSError as e:
                if e.errno == errno.EACCES:
                    continue
                raise
            binary = os.path.basename(full_path)
            for s in start:
                if not binary.startswith(s):
                    continue
                # print(parts, pids)
                # print(full_path, len(parts))
                if len(parts) == NR_PARTS - 1:
                    parts.append('')  # not very helpful for identifying
                self._browsers.setdefault(s, []).append(dict(zip(self._names, parts)))
                self._nr_windows += 1

    def save(self):
        if self._args.check and not os.path.exists(self._args.unlock_file):
            if self._args.verbose > 0:
                print('no unlock file ({}) found'.format(self._args.unlock_file))
            return
        if not self._browsers:
            self.ewmh()
        if self._nr_windows < self._args.minwin and not self._args.force:
            if self._args.verbose > 0:
                print(
                    'not saving number of windows: {} < {}'.format(
                        self._nr_windows, self._args.minwin
                    )
                )
            return 1
        _p = self._path_pattern.format('{:%Y%m%d-%H%M%S}')
        file_name = _p.format(datetime.datetime.now())
        # print(json.dumps(self._browsers, indent=2))
        with open(file_name, 'w') as fp:
            json.dump(
                [self._format_version, self._nr_windows, self._browsers],
                fp,
                indent=2,
                separators=(',', ': '),
            )
        self.read(keep=self._args.keep)

    def read(self, spec=None, show=False, keep=None):
        """
        file names are date-time-stamps which are lexicographically ordered
        if spec is None, 0: read back the lastest file if spec is None or 0
        if spec is a simple integer: offset in reversed list (based 0)
        else assume the spec is a date-time-stamp, use that
        """
        list_of_saves = sorted(glob.glob(self._path_pattern.format('*')), reverse=True)
        nlos = []
        for file_name in list_of_saves:
            if os.path.getsize(file_name) == 0:
                os.remove(file_name)
            else:
                nlos.append(file_name)
            list_of_saves = nlos
        if keep is not None:
            for file_name in list_of_saves[keep:]:
                os.remove(file_name)
        if show:
            default = ' (default)'
            print('index | date-time-stamp | nr windows')
            for i, saved in enumerate(list_of_saves):
                num_windows = ''
                with open(saved) as fp:
                    data = fp.read(20)
                    if data[0] == '[':
                        # second number, the one before dict
                        num_windows = ' ' + data.split('{', 1)[0].rsplit(',', 2)[1].strip()
                print(
                    ' {:>4s}   {} {:>4}{}'.format(
                        '[{}]'.format(i),
                        os.path.basename(saved).rsplit('.')[0],
                        num_windows,
                        default,
                    )
                )
                default = ""
            print('\nYou can specify an older saved workspace by index')
            return
        if spec is None:
            spec = 0
        if spec >= len(list_of_saves):
            print(
                'You have not enough saved browser workspace data sets to restore by ' 'index',
                spec,
            )
            sys.exit(1)
        return list_of_saves[spec]

    def restore(self, position=None):
        position = self._args.position if position is None else None
        if not self._args.unlock and os.path.exists(self._args.unlock_file):
            if self._args.verbose > 0:
                print('removing unlock file ({})'.format(self._args.unlock_file))
            os.remove(self._args.unlock_file)
            return
        if not self._browsers:
            self.ewmh()
        file_name = self.read(position)
        # print ('filename', file_name)
        with open(file_name, 'r') as fp:
            data = fp.read()
            # if data[0] == '[':
            data = json.loads(data)
            if data[0] == 1:
                data = data[2]
        # some desktops (like Mate) will only add one workspace if the previous
        # one is not empty therefor restore in order of workspaces
        to_restore = {}
        for browser in data:
            instances = data[browser]
            for instance in instances:
                for k in self._browsers.get(browser, []):
                    if k['title'] != instance['title']:
                        # if the title differs never restore
                        continue
                    ws = instance['workspace']
                    if k['pid'] == instance['pid'] and k['wid'] == instance['wid']:
                        # if the process id and window id is the same
                        # this instance was probably never away
                        # but maybe workspace was edited by hand for testing
                        if k['workspace'] == ws:
                            continue
                    if k['workspace'] == ws:
                        print('not moving', k['title'])
                        continue
                    # now move new window id to old workspace
                    cmd = ['wmctrl', '-i', '-r', k['wid'], '-t', str(ws)]
                    to_restore.setdefault(ws, []).append(cmd)
                    k['title'] = None  # don't move it again
        for ws in sorted(to_restore):
            for cmd in to_restore[ws]:
                if self._args.verbose > 0:
                    print(self.cmdlst_as_string(cmd))
                print(subprocess.check_output(cmd).decode('utf-8'))
        if self._args.unlock:
            with open(self._args.unlock_file, 'w') as fp:
                pass

    @staticmethod
    def cmdlst_as_string(cmd):
        """return cmd list as cut-and-pasteable string with quotes"""
        return ' '.join([c if ' ' not in c else '"' + c + '"' for c in cmd])

    def list(self):
        return self.read(show=True)
