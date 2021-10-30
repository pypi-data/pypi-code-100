try:
    import discord
    import DiscordUtils
    from Cybernator import Paginator
    from PIL import *
    import asyncio
    import random
    import sys
    import os
    import re
except:
    print()
    print(' -----|[IMPORTED LIBS]|-----')
    print()
    print(' "pip install infpath" or "from infpath import *" ')
    print()
    print(' "pip install discord.py" or "import discord" ')
    print()
    print(' "pip install DiscordUtils" or "import DiscordUtils" ')
    print()
    print(' "pip install Cybernator" or "from Cybernator *" ')
    print()
    print(' "pip install Pillow" or "from PIL import *" ')
    print()
    print(' "pip install random" or "import random" ')
    print()
    print(' "pip install sys" or "import sys" ')
    print()
    print(' "pip install os" or "import os" ')
    print()
    print(' -----|[IMPORTED LIBS]|-----')
    print()


class infpath(object):
    def __init__(self, path, option):
        """
        `The MIT License (MIT)`

        `Copyright (c) 2021-present. "adamsonScripts"`

        Permission is hereby granted, free of charge, to any person obtaining a
        copy of this software and associated documentation files (the "Software"),
        to deal in the Software without restriction, including without limitation
        the rights to use, copy, modify, merge, publish, distribute, sublicense,
        and/or sell copies of the Software, and to permit persons to whom the
        Software is furnished to do so, subject to the following conditions:

        The above copyright notice and this permission notice shall be included in
        all copies or substantial portions of the Software.

        THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
        OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
        FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
        AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
        LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
        FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
        DEALINGS IN THE SOFTWARE.
        """
        self.path = path
        self.option = option

        if self.path and self.option:
            if self.path == self.path and self.option == "LEN":
                imgs = os.listdir(self.path)
                return print(len(imgs))
            elif self.path == self.path and self.option == "RND":
                imgs = os.listdir(self.path)
                random_photo = (lambda x: random.choice(x))(imgs)
                return print(random_photo)
            elif self.path == self.path and self.option == "IMG":
                imgs = os.listdir(self.path)
                print()
                print(' -----|[VALUES]|-----')
                print()
                for photo in imgs:
                    print(f'{photo}')
                print()
                print(' -----|[VALUES]|-----')
                print()
            else:
                print()
                print(f' [ERROR] >>> infpath("{self.path}", "{self.option}") > This Option "{self.option}" Has Not Found ! ')
                print()

                print()
                print(' -----|[HELPOP OF OPTIONS]|-----')
                print()
                print(' "LEN" > Has Imported Limits Values in Path. ')
                print()
                print(' "RND" > Has Imported Random Values in Path. ')
                print()
                print(' "IMG" > Has Imported List Values on Tree in Path.  ')
                print()
                print(' -----|[HELPOP OF OPTIONS]|-----')
                print()
        else:
            print()
            print(' [USING] >>> infpath("PATH", "OPTION") ')
            print()

            print()
            print(f' [EXAMPLE] >>> infpath("C:\\Users\\Username\\Desktop\\Bot\\Images\\Fun\\", "IMG") ')
            print()

            print()
            print(f' [ERROR] >>> infpath("{self.path}", "{self.option}") > This Option "{self.option}" Has Not Found ! ')
            print()