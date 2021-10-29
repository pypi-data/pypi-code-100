from configparser import ConfigParser
import pygments.lexers


class Handler:
    def __init__(self, ini: ConfigParser, suffix: str):
        self.suffix = suffix
        self.command = ini.get(suffix, "command")
        self.comment = ini.get(suffix, "comment", fallback="#")
        self.display = ini.get(suffix, "display", fallback=self.command)
        self.options = ini.get(suffix, "options", fallback="").split()
        self.pygment = ini.get(suffix, "pygment", fallback=self.command)

        if self.pygment is None:
            lexer = pygments.lexers.get_lexer_for_filename(suffix)
            self.pygment = lexer and lexer.name

    def __eq__(self, other: str):
        return other in {self.suffix, self.command, self.display, self.pygment}

    def __str__(self):
        return self.command

    @classmethod
    def create_handlers(cls, ini: ConfigParser):
        handlers = {}

        for suffix in ini.keys():
            if suffix.startswith("."):
                handler = Handler(ini, suffix)
                handlers[handler.suffix] = handler
                handlers[handler.command] = handler
                handlers[handler.display] = handler

        return handlers
