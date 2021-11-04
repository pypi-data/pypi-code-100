'''
Custom Exception Classes to assist in debugging and error handling
'''
class ShapeError(Exception):
    def __init__(self, a,b, mult=False):
        '''
        Thrown on shape mismatch during operation
        '''
        self.a = a
        self.b = b
        self.mult = mult
    def __str__(self):
        if not self.mult:  return f'Matrix must be of same dimension but got {self.a.shape[0]} x {self.a.shape[1]} and {self.b.shape[0]} x {self.b.shape[1]} instead' 
        else: f'ShapeError: A.shape[1] must equal B.shape[0] but got A.shape[1] = {self.a.shape[1]} and B.shape[0] = {self.b.shape[0]} instead'

class TypeOperandError(Exception):
    '''
    Thrown when type mismatch between operands
    other = type(Incorrect Var)
    '''
    def __init__(self,other,op):
        self.other = other
        self.op = op
    def __str__(self):
        return f'TypeError: unsupported operand type(s) for "{self.op}": "Matrix" and "{self.other}"'

class ArgError(Exception):
    '''
    Thrown when arguments length is not valid
    '''
    def __init__(self, args):
        self.args = args
    def __str__(self):
        return f'Expected 1 or 2 arguments but got {len(self.args)} instead'

class RectError(Exception):
    '''
    Thrown when input data is not rectangular
    '''
    def __str__(self):
        return f'Matrix must be rectangular'

class TypeArgError(Exception):
    '''
    Thrown when constructor faces type mismatch from input data
    val = len(args)
    '''
    def __init__(self, args, val):
        self.args = args
        self.val = val
    def __str__(self):
        if self.val == 1: return f'Arguments must be of type <int> or <list> but got <{type(self.args[0]).__name__}>'
        else: return f'Arguments must be of type <int, int> but got <{type(self.args[0]).__name__}, {type(self.args[1]).__name__}>'

class DetException(Exception):
    def __str__(self):
        return 'Determinant Error: Matrix is not square'