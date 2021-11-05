from typing import Dict, Optional, TypedDict
from IPython.display import Javascript
from custom_typings import Vector


class YAxisParams(TypedDict):
    min: Optional[int]
    max: Optional[int]


class TimeseriesParams(TypedDict):
    title: Optional[str]
    palette: Optional[str]
    theme: Optional[str]
    customHeight: Optional[int]
    customWidth: Optional[int]
    yAxis: Optional[YAxisParams]


def draw_timeseries_graph(timestamps: Vector, series: Dict[str, Vector], params: TimeseriesParams):
    return Javascript("""(function(element){DDGraphs.drawTimeseriesGraph(element.get(0), %s, %s, 
    %s);})(element);""" % (timestamps, series, params))
