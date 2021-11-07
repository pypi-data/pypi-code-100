class SyntaxException(Exception):
    
    def __init__(self, token):
        super().__init__(f'{token.value}, line {token.lineno}')


class RuntimeException(Exception):
    
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
