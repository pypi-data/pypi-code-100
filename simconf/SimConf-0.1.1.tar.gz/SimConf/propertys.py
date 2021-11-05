def CustomProperty(atr, types):
    if isinstance(atr, types):
        return atr
    else:
        raise AttributeError(f"Use only {types}")

def StrProperty(atr):
    CustomProperty(atr, str)

def IntProperty(atr):
    CustomProperty(atr, int)

def FloatProperty(atr):
    CustomProperty(atr, float)

def ListProperty(atr):
    CustomProperty(atr, list)

def BoolProperty(atr):
    CustomProperty(atr, bool)

def DictProperty(atr):
    CustomProperty(atr, dict)

def TupleProperty(atr):
    CustomProperty(atr, tuple)
