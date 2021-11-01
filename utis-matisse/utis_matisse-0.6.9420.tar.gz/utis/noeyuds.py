import random

import ast
class Node():
    
    def __init__(self,name="Root",parent=None):
        self.parent=parent
        if type(self.parent)==Node:
            self.parent.childs.append(self)
        self.name=name
        self.childs=list()
        self.n=self.name[0]
        self.x,self.y=250,0
        
    @property
    def dist(self):
        nb=0
        lieu=self
        while lieu.parent!=None:
            nb+=1
            lieu=lieu.parent
        return nb+1
    
    @property
    def ancetre(self):
        if self.parent==None:
            return self.name
        else:
            return self.parent.ancetre+'/'+self.name
        return nb

    def copy(self,paent=None):
        r=self.__class__(self.name,paent)

        for child in self.childs:
            child.copy(paent=r)
        
        return r
    
    def __repr__(self):
        return self.name
    
    def tree(self,nb=0):
        t=self.name
        for child in self.childs:
            t+="\n"+" | "*(nb+1)+child.tree(nb+1)
        if nb==0:print(t)
        else: return t

    
    def deepest(self):
        if self.childs==[]:
            return 1
        else:
            return max([child.deepest() for child in self.childs])+1
            
    def __getitem__(self,nb):return self.childs[nb]

    def __setitem__(self,nb,val):self.childs[nb]=val


r=Node('Racine')
a=Node('Abba',r)
b=Node('Beu',a)
c=Node('Clo',a)
d=Node('Damien',b)
e=Node('Eloi',d)
f=Node('Fr',e)
g=Node('gontrand',a)
names=open("rambouillet.csv","r").read().split("\n")

"""
from urllib import request
import json
T = json.load(request.urlopen(
    "https://raw.githubusercontent.com/dataaddict/prenoms/master/src/data/raw.json"))
years={}
for elem in T:
    name=elem['forename']
    if elem['year'] in years:
        freres=years[elem['year']]
        if not (name in freres):
            years[elem['year']].append(name)
    else:
        years[elem['year']]=[name]
"""

years= ast.literal_eval(open('years','r').read())

def random_tree(begin_year=1900):
    main=Node(random.choice(['Adam','Eve']))
    gen=[main]
    for i in range(5):
        nextgen=[]
        for elem in gen:
            for j in range(random.randint(1,5)):
                anne=begin_year+random.randrange(12,45)*i
                if anne<2016:
                    age_de_vie=random.randrange(50,80)
                    new=Node(random.choice(years[anne])+f' ({anne}-{anne+age_de_vie}, {age_de_vie}ans)',
                                        elem)
                    nextgen.append(new)
        gen=nextgen[:]
    return main
            
        
def lenght():
    todo,taille=[(r,1)],0
    while todo:
        nextdo=[]
        for elem,niv in todo:
            for subelem in elem.childs:
                nextdo.append((subelem,niv+1))
                if niv+1>taille:taille=niv+1
        todo=nextdo[:]
    return taille

def allchilds(r):
    todo=[r]
    alls=[r]
    while todo:
        nextdo=[]
        for elem in todo:
            for subelem in elem.childs:
                nextdo.append(subelem)
        todo=nextdo[:]
        alls+=nextdo[:]
    return alls

def fil(n):
    nv=racine=Node()
    for i in range(n):
        nv=Node("X",nv)
    return racine

def binarytree(n):
    racine=Node()
    leafs=[racine]
    for i in range(n):
        nextleafs=[]
        for node in leafs:
            nextleafs.append(Node("g",node))
            nextleafs.append(Node("d",node))
        leafs=nextleafs[:]
    return racine

def generation(k,racine):
    leafs=[racine]
    for _ in range(k):
        nxt=[]
        for i in leafs:
            for child in i:
                nxt.append(child)
        leafs=nxt[:]
    return leafs

def recur_generation(racines:list,nb):
    if nb<0:
        return [racines]
    else:
        l=[]
        for i in racines:
            l+=recur_generation(i,nb-1)
        return l

    
def tree(racine):
    geners=[racine]
    while True: #danger
        toappend=[]
        for elem in geners[-1]:
            for child in elem.childs:
                toappend.append(child)
        if len(toappend):
            geners.append(toappend)
        else:
            break
    for gen in geners:
        for i in gen:
            print(i.n,end="\t")
        print()



def nearest_ancestor(a,b):
    tocheck_a=[a.parent]
    tocheck_b=[b.parent]
    while True:
        next_a,next_b=[],[]
        
        for parent in tocheck_a:
            if parent in tocheck_b:
                return parent
            next_a+=[parent.parent]
            
        for parent in tocheck_b:
            if parent in tocheck_a:
                return parent
            next_b+=[parent.parent]
        print(tocheck_a,tocheck_b)
        tocheck_a,to_check_b=next_a[:],next_b[:]

"""def nearest_ancestor(a,b):
    tocheck=[[a.parent],[b.parent]]
    while True:
        next_=[[],[]]
        
        for i in range(2):
            for parent in tocheck[i]:
                if parent in tocheck[1-i]:
                    return parent
                next_[i]+=[parent.parent]
        print(tocheck)   
        tocheck[0],tocheck[1]=next_[0][:],next_[1][:]"""
        



def pygame():
    import pygame as pg
    pg.init()
    f=pg.display.set_mode((500,500),pg.RESIZABLE)
    fps=pg.time.Clock()
    B=1
    font=pg.font.SysFont('consolas Bold',20)
    #r=binarytree(4)

    while B:
        pg.display.update()
        f.fill(0)
        
        fps.tick(60)
        for node in allchilds(r):
            if node.parent:
                node.y=node.parent.y+100
                nbbros=len(node.parent.childs)
                index=node.parent.childs.index(node)
                node.x=node.parent.x+(nbbros-(4*index))*(5-node.dist)*50
                pg.draw.line(f,0xffffff,(node.x,node.y),(node.parent.x,node.parent.y))
                
                
            fo=font.render(node.name,True,(255,255,255))
            f.blit(fo,(node.x,node.y))
        for event in pg.event.get():
            if event.type==pg.QUIT:
                pg.quit()
                B=0
            elif event.type==pg.VIDEORESIZE:
                r.x=event.w/2
        

    
