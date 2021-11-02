from .tokens import (DecrementCellValueToken, GetCellValueToken,
                     IncrementCellValueToken, InvalidSyntaxToken, LoopEndToken,
                     LoopStartToken, NextCellToken, PreviousCellToken,
                     PutCellValueToken, Token)


def tokenize(char: str) -> Token:
    """Tokenize given Brainfuck command

    Args:
        char (str): Brainfuck command

    Returns:
        Token: token
    """
    match char:
        case "+":
            return IncrementCellValueToken()
        case "-":
            return DecrementCellValueToken()
        case ".":
            return PutCellValueToken()
        case ",":
            return GetCellValueToken()
        case "[":
            return LoopStartToken()
        case "]":
            return LoopEndToken()
        case ">":
            return NextCellToken()
        case "<":
            return PreviousCellToken()
        case _:
            return InvalidSyntaxToken()


__all__ = ["tokenize"]
