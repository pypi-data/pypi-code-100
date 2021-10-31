
class Node():

    def __init__(self, name="Root", parent=None):
        self.parent = parent
        if type(self.parent) == Node:
            self.parent.childs.append(self)
        self.childs = list()
        self.name = name.upper()
        self.n = self.name[0]
        self.x, self.y = 250, 0

    @property
    def dist(self):
        nb = 0
        lieu = self
        while lieu.parent != None:
            nb += 1
            lieu = lieu.parent
        return nb+1

    @property
    def ancetre(self):
        if self.parent == None:
            return self.name
        else:
            return self.parent.ancetre+'/'+self.name

    def __repr__(self):
        return self.name

    def tree(self, nb=0):
        t = self.name
        for child in self.childs:
            t += "\n"+" | "*(nb+1)+child.tree(nb+1)
        if nb == 0:
            print(t)
        else:
            return t

    def deepest(self):
        if self.childs == []:
            return 1
        else:
            return max([child.deepest() for child in self.childs])+1

    def __getitem__(self, nb): return self.childs[nb]

    def __setitem__(self, nb, val): self.childs[nb] = val


def lenght():
    todo, taille = [(r, 1)], 0
    while todo:
        nextdo = []
        for elem, niv in todo:
            for subelem in elem.childs:
                nextdo.append((subelem, niv+1))
                if niv+1 > taille:
                    taille = niv+1
        todo = nextdo[:]
    return taille

def allchilds(r):
    todo = [r]
    alls = [r]
    while todo:
        nextdo = []
        for elem in todo:
            for subelem in elem.childs:
                nextdo.append(subelem)
        todo = nextdo[:]
        alls += nextdo[:]
    return alls

def fil(n):
    nv = racine = Node()
    for i in range(n):
        nv = Node("X", nv)
    return racine

def binarytree(n):
    racine = Node()
    leafs = [racine]
    for i in range(n):
        nextleafs = []
        for node in leafs:
            nextleafs.append(Node("g", node))
            nextleafs.append(Node("d", node))
        leafs = nextleafs[:]
    return racine

def generation(k, racine):
    leafs = [racine]
    for _ in range(k):
        nxt = []
        for i in leafs:
            for child in i:
                nxt.append(child)
        leafs = nxt[:]
    return leafs

def recur_generation(racines: list, nb):
    if nb < 0:
        return [racines]
    else:
        l = []
        for i in racines:
            l += recur_generation(i, nb-1)
        return l

def tree(racine):
    geners = [racine]
    while True:  # danger
        toappend = []
        for elem in geners[-1]:
            for child in elem.childs:
                toappend.append(child)
        if len(toappend):
            geners.append(toappend)
        else:
            break
    for gen in geners:
        for i in gen:
            print(i.n, end="\t")
        print()

def commun_ancestor(a, b):
    for i in a.ancetre:
        for y in b.ancetre:
            if y == i:
                return y, i

def node_visualisation(r=binarytree(4)):
    import pygame as pg
    pg.init()
    f = pg.display.set_mode((500, 500), pg.RESIZABLE)
    fps = pg.time.Clock()
    B = 1
    font = pg.font.SysFont('consolas Bold', 20)

    while B:
        pg.display.update()
        f.fill(0)

        fps.tick(60)
        for node in allchilds(r):
            if node.parent:
                node.y = node.parent.y+100
                nbbros = len(node.parent.childs)
                index = node.parent.childs.index(node)
                node.x = node.parent.x+(nbbros-(4*index))*(5-node.dist)*50
                pg.draw.line(f, 0xffffff, (node.x, node.y),
                             (node.parent.x, node.parent.y))

            fo = font.render(node.name, True, (255, 255, 255))
            f.blit(fo, (node.x, node.y))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                B = 0
            elif event.type == pg.VIDEORESIZE:
                r.x = event.w/2

if __name__=="__main__":
    r = Node('Racine')
    a = Node('Abba', r)
    b = Node('Beu', a)
    c = Node('Clo', a)
    d = Node('Damien', b)
    e = Node('Eloi', d)
    f = Node('Fr', e)
    g = Node('gontrand', a)