class Test:
    def __init__(self):
        self.name = ''
        self.age = 0

    @property
    def Name(self):
        return self.name

    @Name.setter
    def Name(self, value):
        self.name = value

