import numpy.polynomial as npp
import scipy.spatial as ss
import scipy.ndimage as si

class mytest():
    x:int
    y:float
    z:list

    def __init__(self) -> None:
        self.x=10
        self.y=20.
        self.z=[20,30]

        self.test=[]
        self.test.append((self.x,self.y))
        self.test.append(self.z)

        self.x=2
        self.z[0]=50
        print(self.test[0][0])
        print(self.test[1][0])
        pass


m=mytest()
