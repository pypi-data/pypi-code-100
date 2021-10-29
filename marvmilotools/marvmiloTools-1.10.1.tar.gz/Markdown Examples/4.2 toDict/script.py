import marvmiloTools as mmt

DictObj = mmt.dictionary.toObj({"hello": "world"})

#convert to dictionary
dictionary = mmt.dictionary.toDict(DictObj)
print(dictionary)
print(type(dictionary))