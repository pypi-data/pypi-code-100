class Table:
    def __init__(self, size=(0, 0), default=lambda x, y: (x, y)):
        self.list = [[]]
        self.default = default
        self.addcolumn(size[0])
        self.addline(size[1]-1)

    def __getitem__(self, val):
        try:
            return self.list[val[1]][val[0]]
        except TypeError:
            if type(val) == int:
                return self.list[val]
            else:
                raise

    def __setitem__(self, pos, value):
        if pos[0] >= self.xmax:
            self.addcolumn(pos[0]-self.xmax+1)
        if pos[1] >= self.ymax:
            self.addline(pos[1]-self.ymax)
        self.list[pos[1]][pos[0]] = value

    def addcolumn(self, nb=1):
        for y in range(self.ymax+1):  # For each line
            self.list[y] += [self.default(x, y)
                             for x in range(nb)]  # Ajouter nb colone(s)

    def addline(self, nb=1):
        for y in range(self.ymax+1, self.ymax+nb+1):  # Pour each nouvelle line
            self.list.append([self.default(x, y)
                             for x in range(self.xmax+1)])  # en créer une

    def __repr__(self):
        t = ""
        for y in self.list:
            for x in y:
                t += str(x)+"\t"
        #t+=f"{self.xmax= } {self.ymax= }"
        return t[:-1]

    def __iter__(self):
        self.av = [0, 0]
        return self

    def __next__(self):
        res = self.av[:]
        if self.av == "ended":
            raise StopIteration
        self.av[0] += 1
        if self.av[0] > self.xmax:
            self.av[0] = 0
            self.av[1] += 1
            if self.av[1] > self.ymax:
                self.av = "ended"
                return self[-1, -1], res
        return self[res[0], res[1]], res

    @property
    def xmax(self):
        try:
            val = len(self.list[0])
            return val-1 if val > 0 else 0
        except IndexError:
            return 0

    @property
    def ymax(self):
        val = len(self.list)
        return val-1 if val > 0 else 0


class Plan:

    def __init__(self, inter=(-5, -5, 5, 5), default=lambda x, y: (x, y)):
        self.default = default
        self.list = []

        self.ouest, self.nord, self.est, self.sud = 0, 0, 0, 0

        self.addlineDown(abs(inter[3]))
        self.addlineUp(abs(inter[1]))
        self.addcolumnLeft(abs(inter[0]))
        self.addcolumnRight(abs(inter[2]))

    def __getitem__(self, val):
        if type(val) == tuple:
            return self.list[val[1]][abs(self.ouest)+val[0]]
        else:
            print(f"Bad index for type Plan: {val}")

    def addcolumnRight(self, nb=1):
        for index, y in enumerate(range(self.nord, self.sud)):
            self.list[index] = self.list[index] + \
                [self.default(x, y) for x in range(self.est, self.est+nb)]
        self.est += nb

    def addcolumnLeft(self, nb=1):
        for index, y in enumerate(range(self.nord, self.sud)):
            self.list[index] = [self.default(x, y) for x in range(
                self.ouest-nb, self.ouest)]+self.list[index]
        self.ouest -= nb

    def addlineUp(self, nb=1):
        self.list = [[self.default(x, y) for x in range(
            self.ouest, self.est)] for y in range(self.nord-nb, self.nord)]+self.list
        self.nord -= nb

    def addlineDown(self, nb):
        self.list = self.list+[[self.default(x, y) for x in range(
            self.ouest, self.est)] for y in range(self.sud, self.sud+nb)]
        self.sud += nb

    def __setitem__(self, pos, value):
        x, y = pos
        if not self.ouest < x < self.est:
            if x < self.ouest:
                self.addcolumnLeft(abs(x-self.ouest))
            if self.est < x:
                self.addcolumnRight(abs(x-self.est))

        if not self.nord < y < self.sud:
            if y < self.nord:
                self.addlineUp(abs(y-self.nord))
            if self.sud < y:
                self.addlineDown(abs(y-self.sud))
        self.list[abs(self.nord)+y][abs(self.ouest)+x] = value

    def __repr__(self):
        t = ""
        for y in self.list:
            t += str(y)+"\n"
        return t

    def __iter__(self):
        self.av = [self.ouest, self.nord]
        return self

    def __next__(self):
        if self.av == "end":
            raise StopIteration
        else:
            res = self[self.av[0], self.av[1]], self.av[:]
            self.av[0] += 1
            if self.av[0] > self.est:
                self.av[1] += 1
                if self.av[1] > self.sud:
                    self.av = 'end'
        return res
if __name__=="__main__":
    S = Plan()
    T = Table(default=lambda x, y: 0)
    D = Table(size=(10, 10), default=lambda x, y: x*y)
