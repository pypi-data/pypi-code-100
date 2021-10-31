# coding=utf-8
import datetime

import django
from django.conf import settings
from ipywidgets import *
import mammut.common.universal_dependencies as ud
import os
from mammut.linguistics.concordance import Concordance
from functools import reduce
from collections import namedtuple
from mammut.common.lexicon.linguistic_standard import LinguisticStandard
from mammut.common.lexicon.dictionary import (
    DictionaryDefinitionEntry,
    DictionaryDefinitionSetEntry,
    DictionaryPosTagEntry,
    DictionaryLemmaEntry
)

MODULE_PATH = os.path.realpath(os.path.dirname(__file__))

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [MODULE_PATH + """/templates"""],
    }
]
settings.configure(TEMPLATES=TEMPLATES, DEBUG=True)
django.setup()

from django.template import Template, Context
from django.template.loader import get_template
from .widgets_utilities import show_paradigm_application

pending_words_template = get_template("pending_words.html")
concordance_template = get_template("concordance.html")
external_dict_links_template = Template(
    """<html>
<body>
{% for edl in ext_dict_links %}
    <p><a href="{{ edl.link }}" target="_blank">{{ edl.id }}: {{ lemma }}</a></p>
{% endfor %}
</body>
</html>"""
)

PendingWordDesc = namedtuple("PendingWordDesc", ["text", "strike"])
ConcordanceDesc = namedtuple("ConcordanceDesc", ["morpheme", "text", "source"])
ParadigmAppWordDesc = namedtuple("ParadigmAppWordDesc", ["morpheme", "features"])
ExternalDictionaryLinksDesc = namedtuple("ExternalDictionaryLinksDesc", ["id", "link"])

DEFAULT_STANDARD = None


def create_dictionary_definition_section(
    standard: LinguisticStandard,
    def_entry: DictionaryDefinitionEntry,
    delete_callback,
    regional_settings,
):
    out_vocabulary_ratio = widgets.ToggleButton(
        value=True,
        description="OVR: 0/0",
        disabled=True,
        button_style="success",
        tooltip="Out of vocabulary ratio",
        icon="check",
        layout=Layout(width="100px"),
    )
    primes_ratio = widgets.ToggleButton(
        value=True,
        description="SPR: 0/0",
        disabled=True,
        button_style="success",
        tooltip="Semantic Primes Exponent Ratio",
        icon="check",
        layout=Layout(width="100px"),
    )
    in_vocabulary = widgets.VBox([out_vocabulary_ratio, primes_ratio])
    # entry object where to store the values selected
    if def_entry is None:
        def_entry = DictionaryDefinitionEntry(
            "",
            "",
            "",
            standard.regional_settings_definition_list[0],
            datetime.date.today().strftime("%Y/%m/%d"),
        )
        # TODO: hay que cambar esto para que use common.LOCAL_DATE_FORMATTER. Pero hacer esto implica ir a todos los diccionarios ya existentes y actualizarlos.
    # definition widget to show to the user
    definition = widgets.Textarea(
        value=def_entry.definition,
        placeholder="Definición",
        description="",
        layout=Layout(width="350px", height="70px"),
    )
    # details about the out of vocabulary words
    out_vocabulary_details = widgets.Textarea(
        value="",
        placeholder="",
        description="",
        disabled=True,
        layout=Layout(width="270px", height="35px"),
    )

    def change_vocabulary_info():
        inv = standard.is_in_vocabulary(def_entry.definition, regional_settings)
        if inv.value:
            out_vocabulary_ratio.description = inv.description
            out_vocabulary_ratio.value = True
            out_vocabulary_ratio.button_style = "success"
        else:
            out_vocabulary_ratio.description = inv.description
            out_vocabulary_ratio.value = False
            out_vocabulary_ratio.button_style = "danger"
        if inv.base_value:
            primes_ratio.description = inv.base_description
            primes_ratio.value = True
            primes_ratio.button_style = "success"
        else:
            primes_ratio.description = inv.base_description
            primes_ratio.value = False
            primes_ratio.button_style = "danger"
        out_vocabulary_details.value = inv.details

    def on_definition_value_change(change):
        def_entry.definition = change["new"]
        change_vocabulary_info()

    change_vocabulary_info()
    definition.observe(on_definition_value_change, names="value")
    # source widget to show to the user
    ext_dic_list = [
        ed.source_id for ed in standard.external_dictionary_sources.values()
    ]
    if def_entry.source == "":
        source_value = ext_dic_list[0]
    else:
        source_value = def_entry.source

    source = widgets.Dropdown(
        options=ext_dic_list,
        value=source_value,
        description="",
        layout=Layout(width="110px"),
    )
    def_entry.source = ext_dic_list[0]

    def on_source_value_change(change):
        def_entry.source = change["new"]

    source.observe(on_source_value_change, names="value")
    # topic widget to show to the user
    topic = widgets.Text(
        value=def_entry.topic,
        placeholder="",
        description="",
        layout=Layout(width="80px"),
    )

    def on_topic_value_change(change):
        def_entry.topic = change["new"]

    topic.observe(on_topic_value_change, names="value")
    # regional settings definition widget to show to the user
    if def_entry.regional_settings_definition == "":
        regional_settings_definition_value = standard.regional_settings_definition_list[
            0
        ]
    else:
        regional_settings_definition_value = def_entry.regional_settings_definition

    regional_settings_definition = widgets.Dropdown(
        options=standard.regional_settings_definition_list,
        value=regional_settings_definition_value,
        description="",
        layout=Layout(width="60px"),
    )

    def on_regional_settings_definition_value_change(change):
        def_entry.regional_settings_definition = change["new"]

    regional_settings_definition.observe(
        on_regional_settings_definition_value_change, names="value"
    )
    # delete button widget to show to the user
    delete = widgets.Button(
        description="-",
        button_style="",
        tooltip="Eliminar",
        layout=Layout(width="20px"),
    )
    pre_box1 = widgets.HBox([source, topic, regional_settings_definition, delete])
    pre_box2 = widgets.VBox([pre_box1, out_vocabulary_details])
    # the box control that group all the control that form the definition
    box = widgets.HBox([in_vocabulary, definition, pre_box2])

    def delete_on_click(sender):
        delete_callback(box, def_entry)

    delete.on_click(delete_on_click)
    return [box, def_entry]


def create_dictionary_definition_set_section(
    postag_value,
    definition_index: int,
    standard: LinguisticStandard,
    delete_callback,
    definition_set_entry_param: DictionaryDefinitionSetEntry,
    dictionary,
    lemma,
    regional_settings,
):
    if definition_set_entry_param is None:
        definition_set_entry = DictionaryDefinitionSetEntry(definition_index, None)
    else:
        definition_set_entry = definition_set_entry_param

    def get_features_list():
        res = []
        for f in definition_set_entry.features_list:
            res.append(standard.feature_descriptor_list[f])
        return res

    features = widgets.SelectMultiple(
        options=standard.feature_descriptor_by_pos_tag[postag_value.id],
        value=([] if definition_set_entry_param is None else get_features_list()),
        description="Adicionales:",
        rows=3,
        layout=Layout(width="350px"),
    )

    def on_features_change(change):
        definition_set_entry.set_features_list(change["new"])

    features.observe(on_features_change, names="value")
    add_definition = widgets.Button(
        description="Agregar Parafrasis",
        button_style="",
        tooltip="Agregar Parafrasis",
        icon="check",
    )
    features_box = widgets.HBox([features, add_definition])
    dummy_label = widgets.Label(
        value="->", placeholder="", description="", layout=Layout(width="100px")
    )
    definition_label = widgets.Label(
        value="Definición",
        placeholder="Definición",
        description="Definición",
        layout=Layout(width="350px"),
    )
    source_label = widgets.Label(
        value="Fuente",
        placeholder="Fuente",
        description="Fuente",
        layout=Layout(width="110px"),
    )
    topic_label = widgets.Label(
        value="Topico",
        placeholder="Topico",
        description="Topico",
        layout=Layout(width="80px"),
    )
    regional_settings_def_label = widgets.Label(
        value="Idioma",
        placeholder="Idioma",
        description="Idioma",
        layout=Layout(width="60px"),
    )
    box_definition_label = widgets.HBox(
        [
            dummy_label,
            definition_label,
            source_label,
            topic_label,
            regional_settings_def_label,
        ]
    )
    definitions_box = widgets.VBox([box_definition_label])
    box = widgets.VBox([features_box, definitions_box])

    def delete_definition_callback(definition_box, def_entry):
        definitions_box.children = list(
            filter(lambda db: db != definition_box, definitions_box.children)
        )
        definition_set_entry.definitions_entries.remove(def_entry)
        dictionary.delete_definition_lemma(lemma, def_entry.definition)
        if len(definitions_box.children) == 1:
            delete_callback(box, definition_set_entry)

    def add_defition():
        definition_box, def_entry = create_dictionary_definition_section(
            standard, None, delete_definition_callback, regional_settings
        )
        definitions_box.children = [c for c in definitions_box.children] + [
            definition_box
        ]
        definition_set_entry.definitions_entries.append(def_entry)

    if definition_set_entry_param is None:
        add_defition()

    def add_definition_if_exist():
        if len(definition_set_entry.definitions_entries) > 0:
            for i in definition_set_entry.definitions_entries:
                definition_box, def_entry = create_dictionary_definition_section(
                    standard, i, delete_definition_callback, regional_settings
                )
                definitions_box.children = [c for c in definitions_box.children] + [
                    definition_box
                ]
                # definition_set_entry.definitions_entries.append(def_entry)

    if definition_set_entry_param is not None:
        add_definition_if_exist()

    def handle_add_definition(sender):
        add_defition()

    add_definition.on_click(handle_add_definition)
    return [box, definition_set_entry]


def create_dictionary_pos_tag_section(
    lemma: str,
    postag_value,
    postag_change_callback,
    delete_callback,
    standard: LinguisticStandard,
    index_name: str,
    pos_tag_entry_param: DictionaryPosTagEntry,
    regional_settings,
    dictionary,
):
    if pos_tag_entry_param is None:
        pos_tag_entry = DictionaryPosTagEntry(postag_value.id, None)
        morph_parad_value = ""
    else:
        pos_tag_entry = pos_tag_entry_param
        morph_parad_value = pos_tag_entry.morpheme_paradigm
    pos_tag = widgets.Dropdown(
        options=list(standard.pos_descriptor_list.values()),
        value=postag_value,
        description="PoS:",
        layout=Layout(width="260px"),
    )
    morph_parad_vals, morph_paradigms = standard.get_morpheme_paradigms(
        postag_value.id, regional_settings
    )
    if morph_parad_vals.__len__() == 0:
        options_value = {"": ""}
    else:
        options_value = {}
        for i, morph in enumerate(morph_paradigms):
            if morph_parad_value == "":
                morph_parad_value = morph.word_model
            morph_parad_key = (
                morph_parad_vals[i]
                + "        "
                + reduce(
                    lambda a, b: a + " | " + b
                    if b is not ""
                    else a + " | " + "sin descripcion",
                    list(morph.descriptions.values()),
                    "",
                )
            )
            options_value[morph_parad_key] = morph.word_model

    morph_parad = widgets.Dropdown(
        options=options_value,
        value=morph_parad_value,
        description="Parad. Morfema:",
        layout=Layout(width="320px"),
    )
    pos_tag_entry.morpheme_paradigm = morph_parad_value

    def morph_parad_change(change):
        pos_tag_entry.morpheme_paradigm = change["new"]

    morph_parad.observe(morph_parad_change, names="value")
    morph_parad_apply = widgets.Button(
        description="",
        button_style="",
        tooltip="Aplicar Paridigma de Morfema",
        icon="check",
        disabled=(len(morph_parad_vals) == 0),
        layout=Layout(width="20px"),
    )
    morph_parad_box = widgets.HBox([morph_parad, morph_parad_apply])
    miss_parad_vals = standard.get_misspelling_paradigms(
        postag_value.id, regional_settings
    )
    miss_parad = widgets.Dropdown(
        options=miss_parad_vals,
        description="Parad. Errores:",
        layout=Layout(width="320px"),
    )
    pos_tag_entry.misspellings_paradigm = ""

    def miss_parad_change(change):
        pos_tag_entry.misspellings_paradigm = change["new"]

    miss_parad.observe(miss_parad_change, names="value")
    miss_parad_apply = widgets.Button(
        description="",
        button_style="",
        tooltip="Aplicar Paridigma de Errores",
        icon="check",
        disabled=(len(miss_parad_vals) == 0),
        layout=Layout(width="20px"),
    )
    miss_parad_box = widgets.HBox([miss_parad, miss_parad_apply])
    fet_parad_vals = standard.get_feature_paradigms(postag_value.id, regional_settings)
    fet_parad = widgets.Dropdown(
        options=fet_parad_vals,
        description="Otros Parad.:",
        layout=Layout(width="320px"),
    )
    pos_tag_entry.features_paradigm = ""

    def fet_parad_change(change):
        pos_tag_entry.features_paradigm = change["new"]

    fet_parad.observe(fet_parad_change, names="value")
    fet_parad_apply = widgets.Button(
        description="",
        button_style="",
        tooltip="Aplicar Paridigma Adicionales",
        icon="check",
        disabled=(len(fet_parad_vals) == 0),
        layout=Layout(width="20px"),
    )
    fet_parad_box = widgets.HBox([fet_parad, fet_parad_apply])
    show_concordance = widgets.Button(
        description="Concordancia",
        button_style="",
        tooltip="Ver Concordancia",
        icon="check",
        layout=Layout(width="100px"),
    )
    add_definition_set = widgets.Button(
        description="Agregar Def.",
        button_style="",
        tooltip="Agregar Definicion",
        icon="check",
        layout=Layout(width="100px"),
    )
    delete = widgets.Button(
        description="Borrar",
        button_style="",
        tooltip="Borrar",
        icon="",
        layout=Layout(width="60px"),
    )
    show_add_delete_box = widgets.HBox([show_concordance, add_definition_set, delete])
    pos_tag_parads_box = widgets.VBox(
        [pos_tag, morph_parad_box, miss_parad_box, fet_parad_box, show_add_delete_box]
    )
    parad_application = widgets.HTML(value="")

    def morph_parad_apply_click(sender):
        morph_value = morph_parad.value.split(" ")[0]
        morpheme_res = standard.get_morphemes(
            pos_tag.value.id, morph_value, lemma, regional_settings
        )
        word_rows = [
            ParadigmAppWordDesc(
                m.text, ", ".join(map(lambda f: f.feature_name, m.features))
            )
            for m in morpheme_res
        ]
        show_paradigm_application(
            "Paradigma Morfema Aplicado", word_rows, parad_application
        )
        return word_rows

    morph_parad_apply.on_click(morph_parad_apply_click)

    def miss_parad_apply_click(sender):
        morpheme_res = standard.get_misspelling(
            pos_tag.value.id, miss_parad.value, lemma, regional_settings
        )
        word_rows = [
            ParadigmAppWordDesc(
                m.text, ", ".join(map(lambda f: f.feature_name, m.features))
            )
            for m in morpheme_res
        ]
        show_paradigm_application(
            "Paradigma Errores Aplicado", word_rows, parad_application
        )

    miss_parad_apply.on_click(miss_parad_apply_click)

    def fet_parad_apply_click(sender):
        morpheme_res = standard.get_other_inflections(
            pos_tag.value.id, fet_parad.value, lemma, regional_settings
        )
        word_rows = [
            ParadigmAppWordDesc(
                m.text, ", ".join(map(lambda f: f.feature_name, m.features))
            )
            for m in morpheme_res
        ]
        show_paradigm_application(
            "Paradigma Adicionales Aplicado", word_rows, parad_application
        )

    fet_parad_apply.on_click(fet_parad_apply_click)

    show_paradigm_application("Ningun paradigma aplicado", [], parad_application)
    pos_tag_parads_app_box = widgets.HBox([pos_tag_parads_box, parad_application])
    context_dict = {"concordance_rows": []}
    concordance_html = concordance_template.render(context_dict)
    concordance = widgets.HTML(value=concordance_html)
    definitions_box = widgets.VBox([])
    accordion = widgets.Accordion(children=[concordance, definitions_box])
    accordion.set_title(0, "Concordancia")
    accordion.set_title(1, "Definiciones")

    def show_concordance_click(sender):
        concordance_rows = [
            ConcordanceDesc("Implementar", "Falta implementar esto.", "Mammut"),
            ConcordanceDesc(
                "Implementare", "Lo implementare con un Web Scrapper.", "Mammut"
            ),
            ConcordanceDesc(
                "Implementado", "Tan pronto este implementado, lo subire.", "Mammut"
            ),
        ]
        context_dict = {"concordance_rows": concordance_rows}
        # TODO: revisar bien para eliminar data dummy
        concordance_results = []
        concordance_lib = Concordance()
        words_list = morph_parad_apply_click(
            sender
        )  # TODO:deberia ser con todos las aplicaiones de paradigmas, incluyendo errores y otros
        for i in words_list:
            word_result = concordance_lib.get_data_from_index(index_name, i.morpheme)
            if len(word_result):
                concordance_results.append(word_result)
        concordance_html = concordance_template.render(
            {"concordance_results": concordance_results}
        )
        concordance.value = concordance_html

    show_concordance.on_click(show_concordance_click)

    def delete_definition_callback(definition_set_box, def_set_entry):
        definitions_box.children = list(
            filter(lambda db: db != definition_set_box, definitions_box.children)
        )
        pos_tag_entry.definitions_set_entries.remove(def_set_entry)

    def add_definition_set_click(sender):
        definition_box, definition_set_entry = create_dictionary_definition_set_section(
            postag_value,
            len(definitions_box.children),
            standard,
            delete_definition_callback,
            None,
            dictionary,
            lemma,
            regional_settings,
        )
        definitions_box.children = [c for c in definitions_box.children] + [
            definition_box
        ]
        pos_tag_entry.definitions_set_entries.append(definition_set_entry)

    add_definition_set.on_click(add_definition_set_click)

    def add_definition_set_if_exist():
        if len(pos_tag_entry.definitions_set_entries) > 0:
            for i in pos_tag_entry.definitions_set_entries:
                (
                    definition_box,
                    definition_set_entry,
                ) = create_dictionary_definition_set_section(
                    postag_value,
                    len(definitions_box.children),
                    standard,
                    delete_definition_callback,
                    i,
                    dictionary,
                    lemma,
                    regional_settings,
                )

                definitions_box.children = [c for c in definitions_box.children] + [
                    definition_box
                ]
                # pos_tag_entry.definitions_set_entries.append(definition_set_entry)

    if pos_tag_entry_param is not None:
        add_definition_set_if_exist()

    def postag_change(change):
        pos_tag_entry.pos_tag = change["new"].id
        ##morph_parad_vals = list(standard.morpheme_paradigms[pos_tag.value.id][regional_settings].producers.keys())
        morph_parad_vals, morph_paradigms = standard.get_morpheme_paradigms(
            pos_tag.value.id, regional_settings
        )
        morph_parad_value = ""
        if morph_parad_vals.__len__() == 0:
            options_value = {"": ""}
        else:
            options_value = {}
            for i, morph in enumerate(morph_paradigms):
                if morph_parad_value == "":
                    morph_parad_value = morph.word_model
                morph_parad_key = (
                    morph_parad_vals[i]
                    + "        "
                    + reduce(
                        lambda a, b: a + " | " + b
                        if b is not ""
                        else a + " | " + "sin descripcion",
                        list(morph.descriptions.values()),
                        "",
                    )
                )
                options_value[morph_parad_key] = morph.word_model
        morph_parad.options = options_value
        morph_parad.value = morph_parad_value
        miss_parad_vals = list(
            standard.misspelling_paradigms[pos_tag.value.id][""].producers.keys()
        )
        miss_parad.options = miss_parad_vals
        fet_parad_vals = list(standard.feature_paradigms[pos_tag.value.id].keys())
        fet_parad.options = fet_parad_vals
        postag_change_callback(change)

    pos_tag.observe(postag_change, names="value")
    box = widgets.VBox([pos_tag_parads_app_box, accordion])

    def delete_click(sender):
        delete_callback(box, pos_tag_entry)

    delete.on_click(delete_click)

    return [box, pos_tag_entry]


def create_external_dictionaries_section(
    lemma: str, standard: LinguisticStandard, regional_settings
):
    ext_dict_html = []
    ext_dict_desc = []
    for ed in standard.external_dictionary_sources.values():
        if ed.source_url_pattern:
            if regional_settings in ed.regional_settings.split(","):
                ext_dict_html.append(widgets.HTML(value=ed.get_iframe(lemma)))
                ext_dict_desc.append(
                    ExternalDictionaryLinksDesc(ed.source_id, ed.get_url(lemma))
                )
    context_dict = {"lemma": lemma, "ext_dict_links": ext_dict_desc}
    ext_dict_html.append(
        widgets.HTML(value=external_dict_links_template.render(Context(context_dict)))
    )

    accordion = widgets.Accordion(children=ext_dict_html, tooltip="accordion")
    for i in range(0, len(ext_dict_desc)):
        accordion.set_title(i, ext_dict_desc[i].id)
    accordion.set_title(len(ext_dict_desc), "LINKS")
    return accordion


def create_lemma_section(dictionary, index_name: str):
    default_lemma = "mammut"
    lemma_entry = DictionaryLemmaEntry(default_lemma, None)
    # creamos el control donde se debe introducir el Lemma
    lemma_text = widgets.Text(
        value="",
        placeholder="Forma canonica de la palabra",
        description="Lemma:",
        layout=Layout(width="250px"),
    )

    def on_lemma_text_value_change(change):
        lemma_entry.lemma = change["new"].lower()

    lemma_text.observe(on_lemma_text_value_change, names="value")
    # creamos el control donde se debe introducir el AFI
    afi_text = widgets.Text(
        value="",
        placeholder="AFI de la forma canonica del lema",
        description="AFI:",
        layout=Layout(width="250px"),
    )

    def on_afi_text_value_change(change):
        lemma_entry.afi = change["new"].lower()

    afi_text.observe(on_afi_text_value_change, names="value")
    # creamos el dropdown para el tipo de palabra
    word_type = widgets.Dropdown(
        options=dictionary.standard.word_type_list,
        value=dictionary.standard.word_type_list[0],
        description="Tipo:",
        layout=Layout(width="220px"),
    )
    lemma_entry.word_type = dictionary.standard.word_type_list[0]

    def word_type_change(change):
        lemma_entry.word_type = change["new"]

    word_type.observe(word_type_change, names="value")
    # creamos el dropdown para el idioma del lemma
    reg_set_lemma = widgets.Dropdown(
        options=dictionary.standard.regional_settings_lemma_list,
        value=dictionary.standard.regional_settings_lemma_list[0],
        description="",
        layout=Layout(width="60px"),
        tooltip="regional_settings",
    )
    lemma_entry.regional_settings_lemma = dictionary.standard.regional_settings_lemma_list[
        0
    ]

    def reg_set_lemma_change(change):
        lemma_entry.regional_settings_lemma = change["new"]

    reg_set_lemma.observe(reg_set_lemma_change, names="value")
    # creamos la ayuda de los diccionarios en linea
    accordion = create_external_dictionaries_section(
        default_lemma, dictionary.standard, reg_set_lemma.value
    )
    search_lemma = widgets.Button(
        description="Buscar Lemma",
        button_style="",
        tooltip="Buscar Lemma",
        icon="",
        layout=Layout(width="100px"),
    )

    add_pos = widgets.Button(
        description="Agregar POS",
        button_style="",
        tooltip="Agregar POS",
        icon="",
        layout=Layout(width="100px"),
    )
    box_lemma_search_add = widgets.HBox(
        [lemma_text, afi_text, word_type, reg_set_lemma, search_lemma, add_pos]
    )
    # creamos el tab donde estaran los distintos morphemes
    pos_tab = widgets.Tab([])
    pos_values = list(dictionary.standard.pos_descriptor_list.values())
    pos_values_used = {}

    def on_pos_change_partial(index):
        def on_pos_change_complete(change):
            pos_tab.set_title(index, change["new"].name)
            pos_values.remove(change["new"])
            pos_values.append(pos_values_used[index])
            pos_values_used[index] = change["new"]

        return on_pos_change_complete

    def delete_pos_tab(pos_box, pos_tag_entry):
        pos_tab.children = list(filter(lambda pb: pb != pos_box, pos_tab.children))
        lemma_entry.remove_pos_tag_entry(pos_tag_entry)
        pos_values.append(
            dictionary.standard.pos_descriptor_list[pos_tag_entry.pos_tag]
        )
        add_pos.disabled = False

    def add_pos_tab(
        lemma,
        pos_tab_index,
        append_pos_entry,
        pos_tag_entry_param: DictionaryPosTagEntry,
    ):

        if pos_tag_entry_param is not None:
            in_postag_entry_param = True
            for index, i in enumerate(pos_values):
                if (
                    i.id == pos_tag_entry_param.pos_tag
                    and i not in pos_values_used.values()
                ):
                    pos_value = pos_values.pop(index)
                    pos_values_used[pos_tab_index] = pos_value
                    in_postag_entry_param = False
                    break
            if in_postag_entry_param:
                for index, i in enumerate(pos_values):
                    if i not in pos_values_used.values():
                        pos_value = pos_values.pop(index)
                        pos_values_used[pos_tab_index] = pos_value
                        break
        else:
            for index, i in enumerate(pos_values):
                if i not in pos_values_used.values():
                    pos_value = pos_values.pop(index)
                    pos_values_used[pos_tab_index] = pos_value
                    break

        if len(pos_values) == 0:
            add_pos.disabled = True
        pos_box, pos_tag_entry = create_dictionary_pos_tag_section(
            lemma,
            pos_value,  # TODO: en vez de pasar lemma, deberia pasar lemma_entry y listo, lemma es un atributo de ese objeto!
            on_pos_change_partial(pos_tab_index),
            delete_pos_tab,
            dictionary.standard,
            index_name,
            pos_tag_entry_param,
            reg_set_lemma.value,
            dictionary,
        )

        pos_tab.children = [c for c in pos_tab.children] + [pos_box]
        pos_tab.set_title(pos_tab_index, pos_value.name)
        if append_pos_entry:
            lemma_entry.add_pos_tag_entry(pos_tag_entry)
        lemma_text.disabled = True
        reg_set_lemma.disabled = True

    def handle_add_pos_tab(sender):
        # hacer busqueda en local y cambiar lemma entry por el lemm_entry si ya existia
        existing_lemma_entry = dictionary.get_lemma(lemma_entry.lemma)
        if existing_lemma_entry is not None:
            # set afi in input
            box_lemma_search_add.children[1].value = existing_lemma_entry.afi
            for i in lemma_entry.__dict__:
                lemma_entry.__dict__[i] = existing_lemma_entry.__dict__[i]

        if existing_lemma_entry is not None and len(pos_tab.children) == 0:
            box_buttons.children = [update_def, create_new_dic]
            for i in existing_lemma_entry.postags_entries:
                add_pos_tab(existing_lemma_entry.lemma, len(pos_tab.children), False, i)
        elif existing_lemma_entry is not None and len(pos_tab.children) > 0:
            box_buttons.children = [update_def, create_new_dic]
            add_pos_tab(existing_lemma_entry.lemma, len(pos_tab.children), True, None)
        else:
            box_buttons.children = [append_def, create_new_dic]
            add_pos_tab(lemma_entry.lemma, len(pos_tab.children), True, None)

    add_pos.on_click(handle_add_pos_tab)
    # creamos los botones de accion final
    box_buttons = widgets.HBox([])
    append_def = widgets.Button(
        description="Agregar Definiciones al final",
        button_style="",
        tooltip="Agregar Definiciones al final",
        icon="check",
        layout=Layout(width="300px"),
    )
    update_def = widgets.Button(
        description="Editar y Agregar Definiciones al final",
        button_style="",
        tooltip="Agregar Definiciones al final",
        icon="check",
        layout=Layout(width="300px"),
    )
    create_new_dic = widgets.Button(
        description="Crear Diccionario Nuevo",
        button_style="",
        tooltip="Crear Diccionario Nuevo",
        icon="check",
        layout=Layout(width="300px"),
    )
    all_box_childrens = [box_lemma_search_add, accordion, pos_tab, box_buttons]
    all_box = widgets.VBox(all_box_childrens)

    def handle_append_def(sender):
        for b in pos_tab.children:
            b.close()
        pos_tab.children = []
        box_buttons.children = []
        del pos_values[0:]
        for i in list(dictionary.standard.pos_descriptor_list.values()):
            pos_values.append(i)
        pos_values_used.clear()
        try:
            receipt = dictionary.add_lemma_entry(lemma_entry, True)
            print(receipt)
        except Exception as ex:
            print("el paradigma no es valido para el lemma, error:", ex)

    def handle_update_def(sender):
        for b in pos_tab.children:
            b.close()
        pos_tab.children = []
        box_buttons.children = []
        del pos_values[0:]
        for i in list(dictionary.standard.pos_descriptor_list.values()):
            pos_values.append(i)
        pos_values_used.clear()
        try:
            receipt = dictionary.update_lemma_entry(lemma_entry, True)
            print(receipt)
        except Exception as ex:
            print("el paradigma no es valido para el lemma, error:", ex)

    def handle_create_new_dic(sender):
        result = dictionary.create_new_dictionary(reg_set_lemma.value)
        print(f"Resultado de crear nuevo diccionario: {result}")

    append_def.on_click(handle_append_def)
    update_def.on_click(handle_update_def)
    create_new_dic.on_click(handle_create_new_dic)
    return all_box


def show_restart_add_lemma_entry_section_button(dictionary, index_name: str):
    # TODO:este boton es necesario porque algo pasa cuando se van a agregar un objeto nuevo no estan vaccios los
    # definitions_entries y se generan el numero de objetos igual a los que que se han creado desde que se ejecuto
    # la celda sin reiniciarla
    add_lemma_entry_section = create_lemma_section(dictionary, index_name)
    restart_lemma_section_button = widgets.Button(
        description="Reiniciar",
        button_style="",
        tooltip="Reiniciar",
        icon="check",
        layout=Layout(width="900px"),
    )

    all_box_childrens = [restart_lemma_section_button, add_lemma_entry_section]
    all_box = widgets.VBox(all_box_childrens)
    return all_box


# Utilitarian functions


# Universal dependecies


def create_universal_dependencies_help_section():
    def get_postag_help_links_html(pos_tag):
        return """<html>
    <body>
    <p><a href="{0}" target="_blank">PoS Tags - Ayuda General</a></p>

    <p><a href="{1}" target="_blank">PoS Tags - Estadisticas Para Español</a></p>
    </body>
    </html>""".format(
            ud.pos_tags_description_sites[pos_tag], ud.pos_tags_stats_sites_es[pos_tag]
        )

    pos_tag_desc_dd = widgets.Dropdown(
        options=ud.pos_tags,
        value=ud.noun_pos_tag,
        description="Tipo de Palabra:",
        layout=Layout(width="300px"),
    )
    pos_tag_help_links_html = widgets.HTML(
        value=get_postag_help_links_html(ud.noun_pos_tag)
    )
    pos_tag_desc_html = widgets.HTML(
        value="<iframe src={0} width=1000 height=350></iframe>".format(
            ud.pos_tags_description_sites[ud.noun_pos_tag]
        )
    )
    pos_tag_stat_html = widgets.HTML(
        value="<iframe src={0} width=1000 height=350></iframe>".format(
            ud.pos_tags_stats_sites_es[ud.noun_pos_tag]
        )
    )
    pos_tag_desc_box = widgets.VBox(
        [pos_tag_desc_dd, pos_tag_help_links_html, pos_tag_desc_html, pos_tag_stat_html]
    )

    def get_features_help_links_html(feature_selected):
        return """<html>
    <body>
    <p><a href="{0}" target="_blank">Features - Ayuda General</a></p>

    <p><a href="{1}" target="_blank">Features - Estadisticas Para Español</a></p>
    </body>
    </html>""".format(
            feature_selected.url_doc, feature_selected.url_stats_es
        )

    default_feature_selected = ud.pronominal_types_descriptor
    feature_descriptor_dd = widgets.Dropdown(
        options=ud.feature_types_descriptor_per_id,
        value=default_feature_selected,
        description="Tipo de Palabra:",
        layout=Layout(width="300px"),
    )
    feature_name = widgets.Text(
        value=default_feature_selected.name,
        description="Name:",
        disabled=True,
        layout=Layout(width="300px"),
    )
    feature_description = widgets.Text(
        value=default_feature_selected.description,
        description="Description:",
        disabled=True,
        layout=Layout(width="300px"),
    )
    box_feature_texts = widgets.HBox(
        [feature_descriptor_dd, feature_name, feature_description]
    )
    feature_help_links_html = widgets.HTML(
        value=get_features_help_links_html(default_feature_selected)
    )
    feature_descriptor_html = widgets.HTML(
        value="<iframe src={0} width=1000 height=350></iframe>".format(
            default_feature_selected.url_doc
        )
    )
    feature_stat_html = widgets.HTML(
        value="<iframe src={0} width=1000 height=350></iframe>".format(
            default_feature_selected.url_stats_es
        )
    )
    feature_descriptor_box = widgets.VBox(
        [
            box_feature_texts,
            feature_help_links_html,
            feature_descriptor_html,
            feature_stat_html,
        ]
    )

    def on_drop_down_change(change):
        if change["owner"] == pos_tag_desc_dd:
            pos_tag_help_links_html.value = get_postag_help_links_html(change["new"])
            pos_tag_desc_html.value = "<iframe src={0} width=1000 height=350></iframe>".format(
                ud.pos_tags_description_sites[change["new"]]
            )
            pos_tag_stat_html.value = "<iframe src={0} width=1000 height=350></iframe>".format(
                ud.pos_tags_stats_sites_es[change["new"]]
            )
        elif change["owner"] == feature_descriptor_dd:
            selected_feature = ud.feature_types_descriptor_per_id[change["new"][0]]
            feature_name.value = selected_feature.name
            feature_description.value = selected_feature.description
            feature_help_links_html.value = get_features_help_links_html(
                selected_feature
            )
            feature_descriptor_html.value = "<iframe src={0} width=1000 height=350></iframe>".format(
                selected_feature.url_doc
            )
            feature_stat_html.value = "<iframe src={0} width=1000 height=350></iframe>".format(
                selected_feature.url_stats_es
            )

    pos_tag_desc_dd.observe(on_drop_down_change, names="value")
    feature_descriptor_dd.observe(on_drop_down_change, names="value")

    accordion = widgets.Accordion(children=[pos_tag_desc_box, feature_descriptor_box])
    accordion.set_title(0, "Ayuda y Estadisticas de Part of Speechs")
    accordion.set_title(1, "Ayuda y Estadisticas de Features")
    return accordion
