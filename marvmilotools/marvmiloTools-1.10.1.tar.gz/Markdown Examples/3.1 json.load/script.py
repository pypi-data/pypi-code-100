import marvmiloTools as mmt

dictionary = mmt.json.load("example.json", object=False)
DictObj = mmt.json.load("example.json")

print("Dictionary:")
print(dictionary)
print(type(dictionary))
print()
print("DictObject:")
print(DictObj)
print(type(DictObj))