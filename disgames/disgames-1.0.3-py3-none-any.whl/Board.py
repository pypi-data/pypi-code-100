class Board:
    """A board class that gives a nested which is the board"""

    def __init__(
        self, x, y, seperator="", coordinates=[], replacment=" ", test=[]
    ):
        self.x = x
        self.y = y
        self._seperator = seperator
        self.coors = coordinates
        self.replacment = replacment
        self.test = test

    def __str__(self):
        lst = []
        g = [f"{self._seperator}{i}" for i in range(self.x + 1)]
        lst.append(g)
        for i in range(self.x):
            lst.append([f"{self._seperator}{i+1}"])
            for _ in range(self.y):
                lst[i + 1].append(f"{self._seperator}")
        if self.coors:
            for x, i in enumerate(self.test):
                for y, j in enumerate(i):
                    if self.test[x][y] != f"{self._seperator} ":
                        lst[x][y] = self.test[x][y]
            for x, y in self.coors:
                lst[int(x)][int(y)] = f"{self._seperator}{self.replacment}"
        return str(lst)

    @property
    def dimensions(self):
        """Give the dimensions of the board"""
        return self.x, self.y

    @property
    def seperator(self):
        """Returns the seperator of the board"""

        return self._seperator
