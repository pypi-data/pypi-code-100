#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
#
#    Copyright (C) 2017, Kai Raphahn <kai.raphahn@laburec.de>
#


import sys
import bbutil.lang.parser
import bbutil.lang.parser.pyfile

from bbutil.logging import Logging
from bbutil.lang.parser import Parser, Command

log: Logging = Logging()


if __name__ == '__main__':

    bbutil.lang.parser.set_log(log)
    bbutil.lang.parser.pyfile.set_log(log)
    log.setup(app="make-lang.py", level=0)

    console = log.get_writer("console")
    console.setup(text_space=12, error_index=["ERROR", "EXCEPTION"])
    log.register(console)
    _check = log.open()
    if _check is False:
        sys.exit(1)

    main = Parser()

    _check = main.init(sys.argv[1:])
    if _check is False:
        sys.exit(1)

    _check = main.parse()
    if _check is False:
        sys.exit(1)

    _check = main.store(command=Command.generate)
    if _check is False:
        sys.exit(1)

    _check = main.store(command=Command.update)
    if _check is False:
        sys.exit(1)

    _check = main.store(command=Command.copy)
    if _check is False:
        sys.exit(1)

    _check = main.store(command=Command.compile)
    if _check is False:
        sys.exit(1)
