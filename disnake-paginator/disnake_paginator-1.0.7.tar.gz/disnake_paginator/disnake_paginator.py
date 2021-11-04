def split(text, length=2000):
    return [text[i: i + length] for i in range(0, len(text), length)] 

