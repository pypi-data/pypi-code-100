from pybrary.main import parse_argv

from pybrary import *

_, f, a, k = parse_argv()
fct = globals()[f]
res = fct(*a, **k)
print(res)
