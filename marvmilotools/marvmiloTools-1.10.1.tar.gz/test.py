import marvmiloTools as mm
import pandas as pd
import sys

mm.timer.start()
print = mm.ScriptPrint("TEST", block = False).print

d = {'a': 1, 'b': {'c': 2}, 'd': ["hi", {'foo': "bar", "dict": {"hello": "world"}}]}
l = [1, {'a': 2}, ["hi", {'foo': "bar"}]]
df = pd.DataFrame({1: [10], 2: [20]})
string = "hello world"
number = 10.7

settings = mm.json.load("test.json")
settings_copy = settings.copy()
print(type(settings_copy))
settings_copy.test = "hello world"

print(settings)
print(settings_copy)

print(mm.get_variable_name(df, locals()))
print(mm.__version__)
print("test")

mm.json.write("hello", "test.json", ["glossary", "GlossDiv", "GlossList", "val"])

mm.json.save(settings, "test_save.json")