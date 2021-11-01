import random,math
class Ant():
    def __init__(self,nbpattes=6,nbantennes=2,mandibulles=2):
        self.legs,self.antennes,self.mandi=nbpattes,nbantennes,mandibulles
        
    def __add__(self,other):
        return Ant((self.legs+other.legs)//2,
                   (self.antennes+other.antennes)//2,
                   (self.mandi+other.mandi)//2)
    
    @property
    def score(self):return self.legs+self.mandi+self.antennes
    
    def __mul__(self,other):
        win,loose= (self,other) if self.score>other.score else (other,self)
        if random.random()<1/100: win,loose=loose,win
        trophe=random.choice(list(win.__dict__.keys()))
        setattr(win,trophe,getattr(win,trophe)+1)
        setattr(loose,trophe,getattr(loose,trophe)-1)
        return trophe
    
    def __repr__(self):
        return f'''{"|"*(self.legs//2)}\n{"0"*max(self.legs//2,self.legs-self.legs//2)}{"."*self.mandi}{"-"*self.antennes}\n{"|"*(self.legs-self.legs//2)}'''
if __name__=="__main__":
    mimi=Ant()
    stephane=Ant(4,2,5)
