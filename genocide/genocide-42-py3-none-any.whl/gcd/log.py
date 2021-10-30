# This file is in the Public Domain.


from .obj import Object
from .ofn import save


class Log(Object):
    def __init__(self):
        super().__init__()
        self.txt = ""


def log(event):
    if not event.prs.rest:
        event.reply("log <txt>")
        return
    o = Log()
    o.txt = event.prs.rest
    save(o)
    event.reply("ok")
