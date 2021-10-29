elements = []
class Console:
    def log(self, x):
        print(x)
    def error(self, x):
        __import__("os").system("color 4")
        print("ERROR: " + x, file=__import__("sys").stderr)
class Document:
    def getElementById(self, id):
        try:
            return next(filter(lambda x: x["id"] == id, elements))
        except:
            print("Error")
    def getElementByClass(self, id):
        try:
            return next(filter(lambda x: x["class"] == id, elements))
        except:
            print("Error")
    def createElement(self, id):
        try:
            if id[:1] == "#":
                elements.append({'id': id.replace('#', ''), 'class': ''})
            elif id[:1] == ".":
                elements.append({'class': id.replace('.', ''), 'id': ''})
        except:
            print("Error")

