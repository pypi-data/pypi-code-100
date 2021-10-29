BASE_62 = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
BASE_64 = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ+/'

def encode(n: int, base: str=BASE_62) -> str: 
    base_size = len(base)

    if n == 0:
        return base[0]

    remainder: int = 0
    encoded_string: list = []
    encoded_string_append = encoded_string.append

    while n > 0:
        n, remainder = divmod(n, base_size)
        
        encoded_string_append(base[remainder])
    
    encoded_string.reverse()
    
    return ''.join(encoded_string)
    

def decode(s: str, base: str=BASE_62) -> int: 
    result = 0
    for i, v in enumerate(s, start=1):
        power = len(s) - i
        index = base.index(v)
        result += index * len(base)**power

    return result