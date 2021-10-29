from pickle import dumps, loads
from lzma import compress, decompress

def dump(variable, path):
    open(path, 'wb').write(compress(dumps(variable)))
    
def load(path):
    return loads(decompress(open(path, 'rb').read()))