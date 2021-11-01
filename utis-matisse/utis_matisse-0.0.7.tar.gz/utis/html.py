class Balise:
    def __init__(self, name, parent=None, arguments=dict()):
        self.name=name
        self.childs = dict()
        self.args = arguments
        self.parent=parent
        if parent:
            parent.childs[self.name]=self

    def __repr__(self):
        indent=self.nbancestors*'\t'
        return indent+f"<{self.name} {self.repr_args()}>\n"+\
                '\n'.join([str(self.childs[child])+"\n" for child in self.childs])+\
                indent+f"</{self.name}>"

    def repr_args(self):
        t=""
        for key in self.args:
            t+=f"{key}={self.args[key]} "
        return t
    @property
    def nbancestors(self):
        nb = 0
        lieu = self
        while lieu.parent != None:
            nb += 1
            lieu = lieu.parent
        return nb
if __name__=="__main__":
    a=Balise('main',None)
    Balise('test',a)
