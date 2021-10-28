import re 
import math

def str2int(a:str)->int:
    if a[0] == 'b':
        return int(re.sub(r'[^01]', '', a),2)
    


def width_infer(a)->int:
    if type(a) is int:
        if a >= 0:
            return 1 if a < 2 else math.floor(math.log2(a)) + 1

