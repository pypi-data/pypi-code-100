from typing import Optional, TypedDict
from IPython.display import Javascript

from custom_typings import StringVector, Vector


class TopListParams(TypedDict):
    title: Optional[str]
    theme: Optional[str]
    customHeight: Optional[int]
    customWidth: Optional[int]


def draw_top_list(keys: StringVector, values: Vector, params: TopListParams):
    return Javascript("""(function(element){DDGraphs.drawTopList(element.get(0), %s, %s, 
    %s);})(element);""" % (keys, values, params))
