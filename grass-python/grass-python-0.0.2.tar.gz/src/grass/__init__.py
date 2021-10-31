from forbiddenfruit import curse

from grass.function import flip, applyFlipped, const, apply, applyN, id, on, compose

from grass.functor import Functor, map, mapFlipped

# 修改内置类型的实现

def list_fmap(self, f):
    res = []
    for x in self:
        res.append(f(x))
    return res

curse(list, "fmap", list_fmap)

Functor.register(list)