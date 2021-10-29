import marvmiloTools as mmt

dictionary = {"hello": "world"}
DictObj = mmt.dictionary.toObj(dictionary)

#save to json
mmt.json.save(dictionary, filename = "dictionary.json")
mmt.json.save(DictObj, filename = "DictObj.json")