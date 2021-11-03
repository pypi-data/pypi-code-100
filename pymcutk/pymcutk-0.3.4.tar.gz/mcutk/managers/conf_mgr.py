#
# MIT License
# 
# Copyright 2021 NXP
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

import os
import yaml

class ConfMgr(object):

    CONFIG_FILE = os.path.join(os.path.expanduser('~'), '.mcutk')

    @classmethod
    def load(cls):
        return cls(cls.CONFIG_FILE)

    def __init__(self, path):
        self._path = path
        self.is_empty = True

        if not os.path.exists(path):
            self._data = dict()
        else:
            with open(path, 'r') as stream:
                self._data = yaml.safe_load(stream)
            self.is_empty = False

        if 'apps' not in self._data:
            self._data['apps'] = dict()

        if not isinstance(self._data['apps'], dict):
            self._data['apps'] = dict()

    def apps(self):
        return self._data['apps']

    def get_app(self, name):
        return self._data['apps'].get(name)

    def get_apps(self):
        return self._data['apps']

    def set_app(self, app):
        assert app.name
        info = {
            'path': str(app.path),
            'version': str(app.version)
        }
        self._data['apps'][app.name] = info

    def __str__(self):
        return str(self._data)

    def save(self):
        with open(self._path, 'w') as file:
            yaml.dump(self._data, file, default_flow_style=False)

    def show(self):
        print(yaml.dump(self._data, default_flow_style=False))
