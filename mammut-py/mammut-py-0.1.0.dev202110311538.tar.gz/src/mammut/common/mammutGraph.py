# coding=utf-8
import mammut.common.google_api as ga
import os
import configparser
from graphviz import *
from IPython.display import *
from mammut.common.storage.storage_manager import StorageManager


class MammutGraph:

    storage_manager = StorageManager()
    DEFAULT_VERTEX_SHEET_TITTLE = "vertices"
    DEFAULT_VERTEX_BEGIN_RANGE = "A2"
    DEFAULT_VERTEX_BEGIN_COLUMN = "A"
    DEFAULT_VERTEX_BEGIN_ROW = "2"
    DEFAULT_VERTEX_END_RANGE = "G"

    DEFAULT_PROPERTIES_SHEET_TITTLE = "properties"
    DEFAULT_PROPERTIES_BEGIN_RANGE = "A2"
    DEFAULT_PROPERTIES_BEGIN_COLUMN = "A"
    DEFAULT_PROPERTIES_BEGIN_ROW = "2"
    DEFAULT_PROPERTIES_END_RANGE = "F"

    VERTEX_NAME = "name"
    VERTEX_ELEMENT_TYPE = "element_type"
    VERTEX_PROPERTY_PREDICATE = "property_predicate"
    VERTEX_ELEMENT_NAME = "element_name"
    VERTEX_EDGE_HEAD = "edge_head"
    VERTEX_OPTIONAL = "optional"
    VERTEX_ENTRY_POINT = "entry_point"

    PROPERTY_NAME = "name"
    PROPERTY_PROPERTY_TYPE = "property_type"
    PROPERTY_CARDINALITY = "cardinality"
    PROPERTY_PROPERTIES = "properties"
    PROPERTY_RANGE = "range"
    PROPERTY_LAMBDA_LEXICAL_FORM = "lambda_lexical_form"

    def __init__(self, spreadsheet_id, package_name):
        self.package_name = package_name
        self.vertex_data_frame = None
        self.vertex_group_by_object = None
        self.properties_data_frame = None
        self.properties_dict = {}
        self.graph = Graph("G", filename="MammutGraph.gv", format="png")
        self.load_graph(spreadsheet_id)

    def load_graph(self, spreadsheet_id):
        self.vertex_data_frame = self.storage_manager.get_spreadsheet_as_dataframe(
            spreadsheet_id,
            MammutGraph.DEFAULT_VERTEX_SHEET_TITTLE,
            MammutGraph.DEFAULT_VERTEX_BEGIN_COLUMN,
            MammutGraph.DEFAULT_VERTEX_BEGIN_ROW,
            MammutGraph.DEFAULT_VERTEX_END_RANGE,
        )

        self.properties_data_frame = self.storage_manager.get_spreadsheet_as_dataframe(
            spreadsheet_id,
            MammutGraph.DEFAULT_PROPERTIES_SHEET_TITTLE,
            MammutGraph.DEFAULT_PROPERTIES_BEGIN_COLUMN,
            MammutGraph.DEFAULT_PROPERTIES_BEGIN_ROW,
            MammutGraph.DEFAULT_PROPERTIES_END_RANGE,
        )

        self.graph.attr("node", shape="doublecircle")
        for vertex in self.vertex_data_frame.groupby([MammutGraph.VERTEX_NAME]):
            self.graph.node(vertex[0], vertex[0])

        self.graph.attr("node", style="filled", shape="square")
        for i, property in enumerate(
            self.properties_data_frame[MammutGraph.PROPERTY_NAME]
        ):
            self.graph.node(property, property)
            self.properties_dict[property] = []
            if (
                self.properties_data_frame[MammutGraph.PROPERTY_PROPERTIES][i].__len__()
                != 0
            ):
                properties_list = self.properties_data_frame[
                    MammutGraph.PROPERTY_PROPERTIES
                ][i].split(",")
                for prop in properties_list:
                    aux = prop.split(".")
                    self.graph.edge(property, aux[1], label=aux[0])
                    self.properties_dict[property].append(aux)

        for i, name in enumerate(self.vertex_data_frame[MammutGraph.VERTEX_NAME]):
            if self.vertex_data_frame[MammutGraph.VERTEX_ELEMENT_TYPE][i] == "PROPERTY":
                self.graph.edge(
                    self.vertex_data_frame[MammutGraph.VERTEX_NAME][i],
                    self.vertex_data_frame[MammutGraph.VERTEX_ELEMENT_NAME][i],
                    label=self.vertex_data_frame[MammutGraph.VERTEX_PROPERTY_PREDICATE][
                        i
                    ],
                )
            elif self.vertex_data_frame[MammutGraph.VERTEX_ELEMENT_TYPE][i] == "EDGE":
                self.graph.edge(
                    self.vertex_data_frame[MammutGraph.VERTEX_NAME][i],
                    self.vertex_data_frame[MammutGraph.VERTEX_EDGE_HEAD][i],
                    label=self.vertex_data_frame[MammutGraph.VERTEX_ELEMENT_NAME][i],
                )

        self.graph.render("MammutGraph.gv")
        os.system("mkdir -p ~/temp")
        os.system("mv MammutGraph.gv.png ~/temp")
        os.system("mv MammutGraph.gv ~/temp")

    def view(self):
        display(Image(os.path.expanduser("~") + "/temp/MammutGraph.gv.png"))

    def view_filtered(self, vertex_list):
        graph_filtered = Graph("G", filename="MammutGraphF.gv", format="png")
        graph_filtered.attr("node", shape="doublecircle")
        for vertex in vertex_list:
            graph_filtered.node(vertex, vertex)

        graph_filtered.attr("node", style="filled", shape="square")

        for i, name in enumerate(self.vertex_data_frame[MammutGraph.VERTEX_NAME]):
            if self.vertex_data_frame[MammutGraph.VERTEX_NAME][i] in vertex_list:
                if (
                    self.vertex_data_frame[MammutGraph.VERTEX_ELEMENT_TYPE][i]
                    == "PROPERTY"
                ):
                    property = self.vertex_data_frame[MammutGraph.VERTEX_ELEMENT_NAME][
                        i
                    ]
                    graph_filtered.node(property, property)
                    graph_filtered.edge(
                        self.vertex_data_frame[MammutGraph.VERTEX_NAME][i],
                        property,
                        label=self.vertex_data_frame[
                            MammutGraph.VERTEX_PROPERTY_PREDICATE
                        ][i],
                    )
                    for tuple in self.properties_dict[property]:
                        graph_filtered.edge(property, tuple[1], label=tuple[0])

                elif (
                    self.vertex_data_frame[MammutGraph.VERTEX_ELEMENT_TYPE][i] == "EDGE"
                ):
                    graph_filtered.edge(
                        self.vertex_data_frame[MammutGraph.VERTEX_NAME][i],
                        self.vertex_data_frame[MammutGraph.VERTEX_EDGE_HEAD][i],
                        label=self.vertex_data_frame[MammutGraph.VERTEX_ELEMENT_NAME][
                            i
                        ],
                    )

        graph_filtered.render("MammutGraphF.gv")
        os.system("mv MammutGraphF.gv.png ~/temp")
        os.system("mv MammutGraphF.gv ~/temp")
        clear_output()
        display(Image(os.path.expanduser("~") + "/temp/MammutGraphF.gv.png"))
