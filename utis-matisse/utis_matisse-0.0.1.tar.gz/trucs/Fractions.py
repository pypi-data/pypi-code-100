class Frac(float):
    
    def __init__(self,a:int,b:int):
        super().__init__()
        self.a=a
        self.b=b
        if self.b==0: raise ZeroDivisionError
        
    def __add__(self,other):
        if type(other)==Frac:return Frac(self.a*other.b+other.a*self.b,self.b*other.b)
        elif type(other)== int or type(other)==float:return Frac(self.a*other,self.b)
        else:raise TypeError
        
    def __mul__(self,other):
        return Frac(self.a*other.a,self.b*other.b)

    def __div__(self,other):
        if type(other)==Frac:return Frac(self.a*other.b,self.b*other.a)
        elif type(other)==int:return Frac(self.a*other.b,other)
        else:raise TypeError

    def simp(self):
        '''Euclide divison'''
        a,b,r=self.a,self.b,1
        while b:b,a,r=r,b,a%b
        self.a//=a
        self.b//=a
    
    def __repr__(self):
        up,down=str(self.a),str(self.b)
        long=max(len(up),len(down))+2
        upsace,downsace=" "*((long-len(up))//2)," "*((long-len(down))//2)
        return upsace+up+upsace+"\n"+"-"*long+"\n"+downsace+down+downsace
if __name__=="__main__":
    a=Frac(1,2)
