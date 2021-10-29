# pylint: disable = no-member
import marvmiloTools as mmt

dictionary = {"hello": "world", "list": ["string", 10, {"a": "b"}]}
#convert dictionary to Object
DictObj = mmt.dictionary.toObj(dictionary)

print(type(DictObj))
print(DictObj)
print(DictObj.hello)
print(DictObj.list[2].a)