__all__ = ['Colors', 'bool2symbol']

# True => Green checkmark, False => Big red X
bool2symbol = {True: u'\u2705', False: u'\N{CROSS MARK}'}


class Colors:
    RED = '\033[31m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    BOLD = '\033[1m'
    ITALIC = '\033[3m'
    RESET = '\033[0m'

    @staticmethod
    def html_color(text, color):
        return f'<font color="{color}">{text}</font>'
