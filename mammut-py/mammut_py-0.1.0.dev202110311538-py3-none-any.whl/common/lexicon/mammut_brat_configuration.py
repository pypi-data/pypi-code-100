# coding=utf-8
import re
from collections import namedtuple, defaultdict, UserList, UserDict

import sys

from mammut.common.basic_tokenizer import BasicTokenizer
import mammut
import logging

from brat_widget.configuration import CollectionConfiguration

from mammut.common.constants import DictionaryTable
from mammut.common.indexer import DefinitionIndexer
from mammut.common.lexicon.inflection_rule import InflectionRule
from mammut.common.util import StringEnum
import pandas as pd
from mammut.common.storage.storage_manager import StorageManager
from mammut.common.lexicon.pos import POSType

log = logging.getLogger(__name__)


class MammutBratConfiguration(CollectionConfiguration):
    DIMENSION_CLASS_GROUP_COLUMN_NAME = "dimension-class-group"
    DIMENSION_CLASS_COLUMN_NAME = "dimension-class"
    DIMENSION_COLUMN_NAME = "dimension"

    def __init__(
        self, dimension_class_group: str, dimension_class: str, dimension: str, standard
    ):
        CollectionConfiguration.__init__(self)
        self.dimension_class_group = dimension_class_group
        self.dimension_class = dimension_class
        self.dimension = dimension
        self.standard = standard
        self.pos_classes = [s.strip() for s in self.dimension.split(",") if s.strip()]
        self._arcs_for_event_types = []
        self.ui_names = {
            "entities": "pos",
            "events": "pos-arcs",
            "relations": "relations",
            "attributes": "features",
        }
        self._has_been_initialized = False

    def initialize(self):
        if not self._has_been_initialized:
            self._populate_entity_types()
            self._populate_event_types()
            CollectionConfiguration.initialize(self)
            self._has_been_initialized = True

    def _populate_event_types(self):
        for c_id in self.pos_classes:
            for pos in self.standard.pos_descriptor_classes[c_id]:
                if pos.pos_type == POSType.Event:
                    pos_fets = []
                    fet_by_class = defaultdict(list)
                    for f in self.standard.all_feature_descriptor_by_pos_tag[pos.id]:
                        fet_by_class[f.feature_class].append(f)
                    for fc, fs in fet_by_class.items():
                        att_type = f"{pos.id}-{fc}"
                        pos_fets.append(att_type)
                        a_vals = []
                        if len(fs) == 1:
                            a_vals = [{"box": "crossed", "name": fs[0].feature_id}]
                        else:
                            a_vals = []
                            for f in fs:
                                a_vals.append(
                                    {
                                        "dashArray": ",",
                                        "name": f.feature_id,
                                        "glyph": "\u2191",
                                    }
                                )
                        a_d = {
                            "unused": False,
                            "values": a_vals,
                            "labels": None,
                            "type": att_type,
                            "name": fc,
                        }
                        self.event_attribute_types.append(a_d)
                    p_d = {
                        "borderColor": "darken",
                        "normalizations": [],
                        "name": pos.name,
                        "arcs": self._arcs_for_event_types,
                        "labels": [pos.name, pos.pos_abbreviation],
                        "children": [],
                        "unused": False,
                        "bgColor": "lightgreen",
                        "attributes": pos_fets,
                        "type": pos.id,
                        "fgColor": "black",
                    }
                    p_d_arc = {
                        "labelArrow": "none",
                        "arrowHead": "triangle,5",
                        "color": "black",
                        "name": pos.name,
                        "labels": [pos.name, pos.name],
                        "dashArray": ",",
                        "type": f"{pos.id}-Arg",
                        "count": "*",  # '{1-5}', '{2}', '', '?', '*', '+'
                        "targets": [pos.id],
                    }
                    self.event_types.append(p_d)
                    self._arcs_for_event_types.append(p_d_arc)
        if self.dimension_class == "functionals":  # TODO:puede quedar hardcode??
            for key, functional in self.standard.functionals.items():
                pos_fets = []
                for definition in functional.definitions:
                    att_type = functional.lemma + "-" + definition.index  # f'elieser'
                    pos_fets.append(att_type)
                    attributes = [i.index for i in functional.definitions]
                    a_vals = []
                    for f in attributes:
                        a_vals.append({"dashArray": ",", "name": f, "glyph": "\u2191"})
                    a_d = {
                        "unused": False,
                        "values": a_vals,
                        "labels": None,
                        "type": att_type,
                        "name": "index",
                    }
                    self.event_attribute_types.append(a_d)
                p_d = {
                    "borderColor": "darken",
                    "normalizations": [],
                    "name": functional.lemma,
                    "arcs": self._arcs_for_event_types,
                    "labels": [
                        functional.lemma,
                        functional.lemma,
                    ],  # conviene que tenga abreviatura, implica agregarla al sheet
                    "children": [],
                    "unused": False,
                    "bgColor": "lightgreen",
                    "attributes": pos_fets,
                    "type": functional.id,
                    "fgColor": "black",
                }
                p_d_arc = {
                    "labelArrow": "none",
                    "arrowHead": "triangle,5",
                    "color": "black",
                    "name": functional.lemma,
                    "labels": [functional.lemma, functional.lemma],
                    "dashArray": ",",
                    "type": f"{functional.id}-Arg",
                    "count": "*",  # '{1-5}', '{2}', '', '?', '*', '+'
                    "targets": [functional.id],
                }
                self.event_types.append(p_d)
                self._arcs_for_event_types.append(p_d_arc)

    def _populate_entity_types(self):
        for c_id in self.pos_classes:
            for pos in self.standard.pos_descriptor_classes[c_id]:
                if pos.pos_type == POSType.Entity:
                    pos_fets = []
                    fet_by_class = defaultdict(list)
                    for f in self.standard.all_feature_descriptor_by_pos_tag[pos.id]:
                        fet_by_class[f.feature_class].append(f)
                    for fc, fs in fet_by_class.items():
                        att_type = f"{pos.id}-{fc}"
                        pos_fets.append(att_type)
                        a_vals = []
                        if len(fs) == 1:
                            a_vals = [{"box": "crossed", "name": fs[0].feature_id}]
                        else:
                            a_vals = []
                            for f in fs:
                                a_vals.append(
                                    {
                                        "dashArray": ",",
                                        "name": f.feature_id,
                                        "glyph": "\u2191",
                                    }
                                )
                        a_d = {
                            "unused": False,
                            "values": a_vals,
                            "labels": None,
                            "type": att_type,
                            "name": fc,
                        }
                        self.entity_attribute_types.append(a_d)
                    p_d = {
                        "borderColor": "darken",
                        "normalizations": [],
                        "name": pos.name,
                        "arcs": [],
                        "labels": [pos.name, pos.pos_abbreviation],
                        "children": [],
                        "unused": False,
                        "bgColor": "#FF821C",
                        "attributes": pos_fets,
                        "type": pos.id,
                        "fgColor": "black",
                    }
                    p_d_arc = {
                        "labelArrow": "none",
                        "arrowHead": "triangle,5",
                        "color": "black",
                        "name": pos.name,
                        "labels": [pos.arc_name, pos.arc_name],
                        "dashArray": ",",
                        "type": f"{pos.id}-Arg",
                        "count": "*",  # '{1-5}', '{2}', '', '?', '*', '+'
                        "targets": [pos.id],
                    }
                    self.entity_types.append(p_d)
                    self._arcs_for_event_types.append(p_d_arc)
