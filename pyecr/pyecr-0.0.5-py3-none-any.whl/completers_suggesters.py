import re
from arnparse import arnparse
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.validation import Validator, ValidationError
from prompt_toolkit.auto_suggest import AutoSuggest, Suggestion
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.styles import Style as Prompt_Style
from typing import Optional
from prompt_toolkit.document import Document
from prompt_toolkit.buffer import Buffer
from pygments.lexer import RegexLexer
from pygments.token import *
from pyecr.emoticons import Emoticons
from prompt_toolkit import PromptSession
from prompt_toolkit.formatted_text import HTML as Prompt_HTML

Prompt_Style = Prompt_Style.from_dict({
                   '':      '#ffffff',
                   'white2'  : '#DE3163 bg:#ffffff',
                   'green'  : '#00c300',
                   'green2' : '#5CD95C',
                   #'bottom-toolbar': '#0000FF bg:#FFFFFF',
                   'bottom-toolbar': '#DE3163 bg:#DFFF00',
                   'rprompt': 'bg:#ff0066 #ffffff',
               })


#toolbar_key_style_open  = "<b><style bg=\"white\">"
toolbar_key_style_open  = "<b><style bg=\"white\">"
toolbar_key_style_close = "</style></b>"
toolbar_margin          = "      "
toolbar_separator       = "     |    " 
toolbar_default         = f"&#9001;{toolbar_key_style_open}RIGHT ARROW{toolbar_key_style_close} or {toolbar_key_style_open}ALT+F{toolbar_key_style_close}&#9002;<i>Complete with suggestion (Start typing)</i>{toolbar_separator}&#9001;{toolbar_key_style_open}CTRL+U{toolbar_key_style_close}&#9002;<i>Clean input</i>{toolbar_separator}&#9001;{toolbar_key_style_open}ENTER{toolbar_key_style_close}&#9002;<i>Confirm or Exit</i>"

class GenericLexer(RegexLexer):
    name      = 'Generic'
    aliases   = ['generic']
    filenames = ['*.gen']
    flags     = re.MULTILINE | re.DOTALL

    tokens = {
        'root': [
            (r'\b(\w{3,})\s*\b', Keyword),
        ]
    }

class AwsArnLexer(RegexLexer):
    name      = 'AwsArn'
    aliases   = ['awsarn']
    filenames = ['*.arn']
    flags     = re.MULTILINE | re.DOTALL

    tokens = {
        'root': [
            (r'\b(arn|aws|iam|mfa|\/)\s*\b', Keyword),
            (r'\b(:{1,})\s*\b', Generic.Output),
            (r'\b(\d{12})\s*\b', Generic.Traceback),
        ]
    }

general_bindings = KeyBindings()
@general_bindings.add('c-space')
def _(event):
    " Initialize autocompletion, or select the next completion. "
    buff = event.app.current_buffer
    if buff.complete_state:
        buff.complete_next()
    else:
        buff.start_completion(select_first=False)

@general_bindings.add('c-x')
def _(event):
    " Initialize autocompletion, or select the next completion. "
    print(event.app.current_buffer.delete(2))


class MyCustomCompleter(Completer):
    def __init__(self, lines):
        self._lines     = lines
        self._data_dict = {}
        for idx, c in enumerate(self._lines):
            self._data_dict[c] = str(idx+1)

    def get_completions(self, document, complete_event):
        matches = [name for name in self._data_dict.keys() if document.text in name]
        for m in matches:
            yield Completion(m,
                             start_position=-len(document.text_before_cursor),
                             display = m, 
                             #display_meta = self._data_dict[m]
                             )

class MySuggestion(AutoSuggest):
    def __init__(self, lines):
        self._lines     = lines
        self._data_dict = {}
        
        for idx, c in enumerate(lines):
            self._data_dict[c] = str(idx+1)

    def get_suggestion(self, buffer: "Buffer", document: Document) -> Optional[Suggestion]:
        text = document.text.rsplit("\n", 1)[-1]
        if text.strip():
            # Find first matching line in history.
            for line in self._lines:
                if line.startswith(text):
                    return Suggestion(line[len(text):])
        return None

class MyValidator(Validator):
    def __init__(self, lines, message):
        self._lines   = lines
        self._message = message
    def is_valid(self, text):
        return text in self._lines
    def validate(self, document: Document) -> None:
        text = document.text
        if not self.is_valid(document.text) and len(text) > 0:
            raise ValidationError(message=f'{text} {self._message}', cursor_position=len(document.text))

class DockerImageValidator(Validator):
    def __init__(self, lines, message):
        self._lines   = lines
        self._message = message
    def is_valid(self, text):
        return ":" in text
    def validate(self, document: Document) -> None:
        text = document.text
        if not self.is_valid(document.text) and len(text) > 0:
            raise ValidationError(message=f'{text} {self._message}', cursor_position=len(document.text))

class RepositoryNameValidator(Validator):
    def __init__(self, message):
        self._message = message
    def is_valid(self, text):
        if " " in text:
            return False
        if ":" in text:
            return False
        if text.strip() == "":
            return False
        return True
    def validate(self, document: Document) -> None:
        text = document.text
        if not self.is_valid(document.text) and len(text) > 0:
            raise ValidationError(message=f'{text} {self._message}', cursor_position=len(document.text))

class TagValidator(Validator):
    def __init__(self, message):
        self._message = message
    def is_valid(self, text):
        if " " in text:
            return False
        if ":" in text:
            return False
        if text.strip() == "":
            return False
        return True
    def validate(self, document: Document) -> None:
        text = document.text
        if not self.is_valid(document.text) and len(text) > 0:
            raise ValidationError(message=f'{text} {self._message}', cursor_position=len(document.text))

class MyNegativeValidator(Validator):
    def __init__(self, lines, message):
        self._lines   = lines
        self._message = message
    def is_valid(self, text):
        for l in self._lines:
            if l in text:
                return False
        return True
    def validate(self, document: Document) -> None:
        text = document.text
        if not self.is_valid(document.text) and len(text) > 0:
            raise ValidationError(message=f'\"{text}\" {self._message}', cursor_position=len(document.text))

class AwsArnValidator(Validator):
    def __init__(self):
        pass
    def is_valid(self, text):
        spacesFound = re.search(" ", text)
        if spacesFound:
            return False
        try:
            arnparse(text)
        except:
            return False
        return True
    def validate(self, document: Document) -> None:
        text = document.text
        if not self.is_valid(document.text) and len(text) > 0:
            raise ValidationError(message=f'{text} is not valid!', cursor_position=len(document.text))

def _request_confirm_y_n():
    message = [
               ('class:green', f' {Emoticons.pin()} Confirm ['),
               ('class:green2', f'y'),
               ('class:green', f'/'),
               ('class:green2', f'n'),
               ('class:green', f']: ')
              ]
    session = PromptSession()
    toolbar = Prompt_HTML(f'{toolbar_margin}{toolbar_default}')
    yes_no  = session.prompt(message,style=Prompt_Style,complete_while_typing=True,validate_while_typing=False,
                               completer=MyCustomCompleter(["Y","N"]),
                               validator=MyValidator(["Y","N","y","n"],"not valid answer, must be \"y\" or \"n\"..."),
                               key_bindings=general_bindings,bottom_toolbar=toolbar,
                               auto_suggest=MySuggestion(["Y","N"]),rprompt='<<<  Yes/No ')
    if yes_no.strip() == "":
       return None                        
    return yes_no
