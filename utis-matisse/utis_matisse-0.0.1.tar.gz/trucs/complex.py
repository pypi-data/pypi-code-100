class Complex:
    def __new__(cls,a,b):
        if b==0:
            return type(a).__new__(type(a),a)
        else:
            return super(Complex,cls).__new__(cls)
    def __init__(self, Re, Im):
        if Im:
            self.re = Re
            self.im = Im
        else:
            self.__class__=int

    def __add__(self, other):
        return Complex(self.re+other.re, self.im+other.im)

    def __repr__(self):
        return f"{self.re}{'+' if self.im>=0 else ''}{self.im}i"

    @property
    def bar(self):
        return Complex(self.re, -self.im)

    def set_im(self, val):
        if val == 0:
            del self.im
        else:
            self._im = val

    def del_im(self):
        self._im=0
        self.__init__(self.re,0)
    def intoger(int):pass
    im = property(lambda self: self._im, set_im, del_im)

if __name__=="__main__":
    a = Complex(1, 2)
