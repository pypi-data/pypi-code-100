def CustomProperty(atr, types):
    if isinstance(atr, types):
        return atr
    else:
        raise AttributeError(f"Use only {types}")

def StrProperty(atr):
    return CustomProperty(atr, str)

def IntProperty(atr):
    return CustomProperty(atr, int)

def FloatProperty(atr):
    return CustomProperty(atr, float)

def ListProperty(atr):
    return CustomProperty(atr, list)

def BoolProperty(atr):
    return CustomProperty(atr, bool)

def DictProperty(atr):
    return CustomProperty(atr, dict)

def TupleProperty(atr):
    return CustomProperty(atr, tuple)
