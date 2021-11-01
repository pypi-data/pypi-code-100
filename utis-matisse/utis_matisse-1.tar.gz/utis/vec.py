"""Stuufs utils pour momo, je sais même pas si je vais m'en serveir"""
import math

class Pos:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def dist(self, autrui):
        return math.sqrt((self.x-autrui.x)**2+(self.y-autrui.y)**2)

    def angle(self, autrui):
        return math.atan2(self.y-autrui.y, self.x-autrui.x)

    def tup(self):
        return (self.x, self.y)

    def __add__(self, other):
        return Pos(self.x+other.x, self.y+other.y)

    __sub__ = dist

    def __repr__(self):
        return str(vars(self))


class Vec:
    def __init__(self, x=None, y=None, angle=None, long=None, a=None, b=None):
        self.x = 0
        self.y = 0
        if x != None and y != None:
            self.x = x
            self.y = y
        elif angle != None and long != None:
            self.angle = angle
            self.long = long

        elif type(a) == Pos and type(b) == Pos:
            self.x = a.x-b.x
            self.y = a.y-b.y
        else:
            raise TypeError("No good pair of keywords")

    def __set_angle(self, val):
        long = self.long
        self.x = round(math.cos(val)*long, 9)
        self.y = round(math.sin(val)*long, 9)

    def __set_long(self, val):
        angle = self.angle
        self.x = round(math.cos(angle)*val, 9)
        self.y = round(math.sin(angle)*val, 9)

    angle = property(lambda self: 0 if self.long ==
                     0 else math.atan2(self.y, self.x)+math.pi, __set_angle)
    long = property(lambda self: math.sqrt(self.x**2+self.y**2), __set_long)

    def pointtoo(self, form: Pos, to: Pos):
        self.angle = form.angle(to)

    def __getitem__(self, ind):
        return [self.x, self.y][ind]

    def __add__(self, other):
        return Vec(x=self.x+other.x, y=self.y+other.y)

    def __sub__(self, other):
        return Vec(x=self.x-other.x, y=self.y-other.y)

    def __mul__(self, num):
        return self.x*num.x+self.y*num.y if type(num) == Vec else Vec(x=self.x*num, y=self.y*num)

    def __truediv__(self, num):
        return Vec(x=self.x/num, y=self.y/num)

    def __floordiv__(self, num):
        return Vec(x=int(self.x/num), y=int(self.y/num))

    def __repr__(self):
        return f"{self.x=} {self.y=}"
    __rmul__ = __mul__
    __radd__ = __add__








if __name__ == "__main__":
    a = Vec(x=1, y=1)
    b = Vec(long=1, angle=math.tau)
    c = Pos(0, 10)
    d = Pos(20, 20)
    
    ...
else:
    print('Services offerts par votre bien aimé capitaine µ uwu')
