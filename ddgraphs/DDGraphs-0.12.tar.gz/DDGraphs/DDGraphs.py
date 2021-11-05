from IPython.display import Javascript, HTML
from typing import Dict, List, Optional, TypedDict

Vector = List[float]
StringVector = List[str]


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


class PieChartParams(TypedDict):
    title: Optional[str]
    palette: Optional[str]
    theme: Optional[str]
    customHeight: Optional[int]
    customWidth: Optional[int]


class TopListParams(TypedDict):
    title: Optional[str]
    theme: Optional[str]
    customHeight: Optional[int]
    customWidth: Optional[int]


# Init Function
def init():
    return HTML("""The lib was successfully loaded 👍<script src='dd-graphs.js'/>""")


def draw_timeseries_graph(timestamps: Vector, series: Dict[str, Vector], params: TimeseriesParams):
    return Javascript("""(function(element){DDGraphs.drawTimeseriesGraph(element.get(0), %s, %s, 
    %s);})(element);""" % (timestamps, series, params))


def draw_pie_chart(keys: StringVector, values: Vector, params: PieChartParams):
    return Javascript("""(function(element){DDGraphs.drawPieChart(element.get(0), %s, %s, 
    %s);})(element);""" % (keys, values, params))


def draw_top_list(keys: StringVector, values: Vector, params: TopListParams):
    return Javascript("""(function(element){DDGraphs.drawTopList(element.get(0), %s, %s, 
    %s);})(element);""" % (keys, values, params))
