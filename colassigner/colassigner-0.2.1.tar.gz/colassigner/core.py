from typing import Type, Union

from .constants import PREFIX_SEP
from .meta_base import ColMeta
from .util import camel_to_snake


class ColAccessor(metaclass=ColMeta):
    """describe and access raw columns

    useful for
    - getting column names from static analysis
    - documenting types
    - dry describing nested structures

    e. g.

    class LocationCols(ColAccessor):
        lon = float
        lat = float

    class TableCols(ColAccessor):
        col1 = int
        col2 = str
        foreign_key1 = "name_of_key"

        class NestedCols(ColAccessor):
            s = str
            x = float

        start_loc = LocationCols
        end_loc = LocationCols

    >>> TableCols.start_loc.lat
    'start_loc__lat'

    """


class ColAssigner(ColAccessor):
    """define functions that create columns in a dataframe

    later the class attributes can be used to access the column
    can be used to created nested structures of columns

    either by assigning or inheriting within:

    class MyStaticChildAssigner(ColAssigner):

        pass

    class MyAssigner(ColAssigner):

        class MySubAssigner(ColAssigner):
            pass

        chass1 = MyStaticChildAssigner
    """

    def __call__(self, df, carried_prefixes=()):
        # dir() is alphabetised object.__dir__ is not
        # important here if assigned cols rely on each other
        for attid in self.__dir__():
            if attid.startswith("_"):
                continue
            att = getattr(self, attid)
            new_pref_arr = (*carried_prefixes, camel_to_snake(attid))
            if isinstance(att, ColMeta):
                if ChildColAssigner in att.mro():
                    inst = att(df, self)
                else:
                    inst = att()
                df = inst(df, carried_prefixes=new_pref_arr)
            elif callable(att):
                colname = PREFIX_SEP.join(new_pref_arr)
                df = df.assign(**{colname: self._call_att(att, df)})
        return df

    @staticmethod
    def _call_att(att, df):
        return att(df)


class ChildColAssigner(ColAssigner):
    """assigner specifically for nested structures

    methods of these are not called with parameters

    the dataframe and the parent assigner are passed
    to the __init__ method as parameters
    """

    def __init__(self, df, parent_assigner: ColAssigner) -> None:
        pass

    @staticmethod
    def _call_att(att, _):
        return att()


def get_all_cols(cls: Union[Type[ColAccessor], Type[ColAssigner]]):
    """returns a list of strings of all columns given by the type

    can also be used for nested structues of columns
    """
    out = []
    for attid in dir(cls):
        if attid.startswith("_"):
            continue
        attval = getattr(cls, attid)
        if isinstance(attval, type) and any(
            [kls in attval.mro() for kls in [ColAccessor, ColAssigner]]
        ):
            out += get_all_cols(attval)
            continue
        if ColAccessor in cls.mro():
            out.append(attval)
    return out


def get_att_value(accessor: Type[ColAccessor], attname: str):
    """get the true assigned value for the class attribute"""
    return accessor.__getcoltype__(attname)
