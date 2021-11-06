def cipher(text, shift, encrypt=True):
    
    """
    Encipher the information.
    
    Each letter is replaced by a letter some fixed number of positions down the 
    alphabet

    Parameters
    ----------
    text : a sequence of string.
    shift : integer.
    encrypt : boolean.

    Returns
    -------
    String

    Examples
    --------
    >>> from cipher_xh2503 import cipher_xh2503
    >>> text = "C'est la vie."
    >>> shift = 1
    >>> cipher_xh2503.cipher(a, b)
    "D'ftu mb wjf."
    """

    alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    new_text = ''
    for c in text:
        index = alphabet.find(c)
        if index == -1:
            new_text += c
        else:
            new_index = index + shift if encrypt == True else index - shift
            new_index %= len(alphabet)
            new_text += alphabet[new_index:new_index+1]
    return new_text
