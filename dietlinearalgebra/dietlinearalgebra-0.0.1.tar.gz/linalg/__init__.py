from __exception_handler__ import *
class Matrix:
    def __init__(self,*args):
        self.m = None
        self.shape = [None,None]
        '''
        Constructor
        ===========
        args = {
            int n : n x n matrix created or
            int m,n: m x n matrix created or
            list mat: matrix set to mat 
        }
        '''
        if 2 < len(args) or len(args) < 1: 
            raise ArgError(len(args))
        if len(args) == 1:
            if type(args[0]).__name__ == 'int':
                # self.m := nxn matrix where n = args[0]
                self.m = [[0]*args[0] for i in range(args[0])]
                self.shape = [args[0],args[0]]
            elif type(args[0]).__name__ == 'list':
                if type(args[0][0]).__name__ == 'int':
                    # self.m := 1xn matrix where n = len(args[0])
                    self.m = [args[0]]
                    self.shape = [1,len(args[0])]
                elif type(args[0][0]).__name__ == 'list':
                    if len({len(row) for row in args[0]}) > 1:
                        raise RectError()
                    else:
                        # self.m := m x n matrix where m,n = len(args[0]),len(args[0][0])
                        self.m = args[0]
                        self.shape = [len(args[0]),len(args[0][0])]
            else:
                raise TypeArgError(args,1)
        elif len(args) == 2:
            # m x n matrix
            if type(args[0]).__name__ == 'int' and type(args[0]).__name__ == 'int':
                self.m = [[0]*args[1] for i in range(args[0])]
                self.shape = [args[0],args[1]]
            else:
                raise TypeArgError(args,2)
               
    def __str__(self):
        '''
        Pretty prints matrix
        '''
        s = '[\n'
        for i in range(self.shape[0]):
            s+= '    ['
            for j in range(self.shape[1]):
                if j < self.shape[1]-1: s+= f'{self.m[i][j]}, '
                else: s += f'{self.m[i][j]}'
            if i < self.shape[0]-1: s +='],\n'
            else: s+=']'
        s+='\n]\n'
        return s   

    def __add__(self,other):
        '''
        returns self.m + other.m
        '''
        if type(other).__name__ == 'Matrix':
            if self.shape == other.shape:
                return Matrix([[self.m[i][j]+other.m[i][j] for j in range(self.shape[1])] for i in range(self.shape[0])])
            else:
                raise ShapeError(self,other)
        else:
            raise  TypeOperandError(type(other).__name__, "+")    

    def __sub__(self,other):
        '''
        return self.m - other.m
        '''
        if type(other).__name__ == 'Matrix':
            if self.shape == other.shape:
                return Matrix([[self.m[i][j]-other.m[i][j] for j in range(self.shape[1])] for i in range(self.shape[0])])
            else:
                raise ShapeError(self,other)
        else:
            raise  TypeOperandError(type(other).__name__, "-")    

    def __mul__(self, other):
        '''
        returns self.m * other.m 
        '''
        if type(other).__name__ == 'Matrix':
            if self.shape[1] == other.shape[0]:
                ret = [[0]*self.shape[0] for i in range(other.shape[1])]
                for i in range(self.shape[0]):
                    for j in range(other.shape[1]):
                        for k in range(self.shape[1]):
                            ret[i][j] += self.m[i][k] * other.m[k][j]
                return Matrix(ret)

            else:
                raise ShapeError(self,other,True)
        else:
            raise TypeOperandError(type(other).__name__, "*")    

    @property
    def T(self):
        '''
        Returns Transpose of itself
        '''
        r = [[0]*self.shape[0] for i in range(self.shape[1])]
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
               r[j][i] = self.m[i][j]
        return Matrix(r)

    def is_square(self):
        '''
        Returns true if self.m is square matrix
        '''
        return self.shape[0] == self.shape[1]

    def determinant(self,A):
        '''
        Fast determinant calc for matrix A
        '''
        n = len(A)
        ac = [row[:] for row in A]

        for d in range(n):
            if ac[d][d] == 0: ac[d][d] = 1.0e-18
            for i in range(d+1,n):
                scl = ac[i][d] / ac[d][d]
                for j in range(n):
                    ac[i][j] = ac[i][j] - scl*ac[d][j]
        p = 1.0
        for i in range(n):
            p*=ac[i][i]
        return 0.0 if round(p,10) == -0.0 or 0.0 else round(p,10)

    @property
    def det(self):
        '''
        Determinant wrapper for error checking and passing value of self.m
        '''
        if self.is_square():
            return self.determinant(self.m)
        else: 
            raise DetException()

class IdentityMatrix(Matrix):
    def __init__(self, n):
        id = [[0 if i != j else 1 for j in range(n)] for i in range(n)]
        super().__init__(id)


class ZerosMatrix(Matrix):
    def __init__(self, m,n):
        id = [[0 for j in range(n)] for i in range(m)]
        super().__init__(id)

class OnesMatrix(Matrix):
    def __init__(self, m,n):
        id = [[1 for j in range(n)] for i in range(m)]
        super().__init__(id)