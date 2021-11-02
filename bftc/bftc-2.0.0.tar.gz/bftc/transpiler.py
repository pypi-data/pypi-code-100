from .tokens import (DecrementCellValueToken, GetCellValueToken,
                     IncrementCellValueToken, LoopEndToken, LoopStartToken,
                     NextCellToken, PreviousCellToken, PutCellValueToken,
                     Token)


def transpile(token: Token) -> str:
    """Transpile given token to C

    Args:
        token (Token): BF token

    Returns:
        str: C code
    """
    match token:
        case NextCellToken():
            return "i++;"
        case PreviousCellToken():
            return "i--;"
        case PutCellValueToken():
            return "putchar(arr[i]);"
        case GetCellValueToken():
            return "arr[i] = getchar();"
        case LoopStartToken():
            return "while(arr[i]) {"
        case LoopEndToken():
            return "}"
        case IncrementCellValueToken():
            return "arr[i]++;"
        case DecrementCellValueToken():
            return "arr[i]--;"
        case _:
            return ""


__all__ = ["transpile"]
