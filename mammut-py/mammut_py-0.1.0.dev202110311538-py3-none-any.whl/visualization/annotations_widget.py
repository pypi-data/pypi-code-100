# coding=utf-8

from ipywidgets import *
from django.template.loader import get_template
from mammut.common.corpus.dictionary_corpus import DictionaryCorpus
from mammut.common.annotations import MammutEventAnnotation

functionals_template = get_template("functionals_help.html")


def annotations_widget_section(package):
    def restitution_section(event_annotation, single_annotator):
        # creamos el control donde se debe introducir la restutucion
        # restitution_str = ''
        restitution_input = widgets.Text(
            value="",
            placeholder="tu restitucion",
            description="Restitucion:",
            layout=Layout(width="250px"),
        )

        def on_restitution_text_value_change(change):
            return

        restitution_input.observe(on_restitution_text_value_change, names="value")

        delete_restitution_button = widgets.Button(
            description="eliminar restituciones",
            button_style="",
            tooltip="eliminar Restituciones",
            icon="",
            layout=Layout(width="200px"),
        )

        def handle_delete_restitution(sender):
            package.delete_restitutions(event_annotation)
            new_anotator = event_annotation.get_annotations_elements("exchange")[
                0
            ]  # TODO:revisar este cero
            restitution_input.value = ""
            mixed_box.children = [restitution_box, new_anotator]

        delete_restitution_button.on_click(handle_delete_restitution)

        save_restitution_button = widgets.Button(
            description="Guardar restitucion",
            button_style="",
            tooltip="Guardar Restitucion",
            icon="",
            layout=Layout(width="200px"),
        )

        def handle_save_restitution(sender):
            package.add_restitution(event_annotation, restitution_input)
            new_anotator = event_annotation.get_annotations_elements("exchange")[
                0
            ]  # TODO:revisar este cero
            restitution_input.value = ""
            mixed_box.children = [restitution_box, new_anotator]

        save_restitution_button.on_click(handle_save_restitution)

        restitution_box = widgets.HBox(
            [restitution_input, save_restitution_button, delete_restitution_button]
        )
        mixed_box = widgets.VBox([restitution_box, single_annotator])
        return mixed_box

    def dimension_selector(
        event_annotation,
    ):  # TODO:  poner cual dimension se esta editando??
        dimensions_dict = {}
        for dimension in event_annotation.dimensions:
            dimensions_dict[dimension] = dimension
        dimensions_dict["None"] = "None"

        dimensions_dropdown = widgets.Dropdown(
            options=dimensions_dict,
            value="None",
            description="select dimension:",
            layout=Layout(width="500px"),
        )
        save_annotation_button = widgets.Button(
            description="Guardar Anotacion",
            button_style="",
            tooltip="Guardar Anotacion",
            icon="",
            layout=Layout(width="200px"),
        )

        def handle_save_annotation(change):
            if (
                len(
                    list(
                        event_annotation.documents_by_dimension[
                            dimensions_dropdown.value
                        ].ann_obj.get_textbounds()
                    )
                )
                > 0
            ):
                event_annotation.add_annotation_to_sheet(dimensions_dropdown.value)
                event_annotation.is_annotated_dimention[
                    dimensions_dropdown.value
                ] = True
                if (
                    event_annotation.current_dimension(dimensions_dropdown.value)
                    is not None
                ):
                    dimensions_dropdown_change(
                        {
                            "new": event_annotation.current_dimension(
                                dimensions_dropdown.value
                            )
                        }
                    )
                    # TODO: se simula el objeto change, deberia crear un nuevo metodo en lugar de utilizar el mismo dimension_dropdow_change

        save_annotation_button.on_click(handle_save_annotation)

        def dimensions_dropdown_change(change):
            if change["new"] is not "None":
                annotation_elements = event_annotation.get_annotations_elements(
                    change["new"]
                )
                if (
                    event_annotation.current_dimension(dimensions_dropdown.value)
                    is not None
                ):
                    dimensions_dropdown.value = event_annotation.current_dimension(
                        dimensions_dropdown.value
                    )
                if len(annotation_elements) == 1:
                    if not isinstance(corpus_dropdown.value, DictionaryCorpus):
                        box = [
                            dimensions_dropdown,
                            restitution_section(
                                event_annotation, annotation_elements[0]
                            ),
                            save_annotation_button,
                        ]
                    else:
                        box = (
                            [dimensions_dropdown]
                            + annotation_elements
                            + [save_annotation_button]
                        )
                else:
                    box = (
                        [dimensions_dropdown]
                        + annotation_elements
                        + [save_annotation_button]
                    )
                dimension_selector_elements.children = box
            else:
                dimension_selector_elements.children = [dimensions_dropdown]

        dimensions_dropdown.observe(dimensions_dropdown_change, names="value")

        dimension_selector_elements = widgets.VBox([dimensions_dropdown])

        return dimension_selector_elements

    def event_selector(corpus):
        annotation_object = package.annotations
        all_events = annotation_object.get_event_messages(corpus)
        annotation_events = annotation_object.get_annotation_event_messages(corpus)
        all_events_dict = {}
        for annotaion_event_message in annotation_events:
            try:
                selector_key = corpus.hash_lemma_dict[
                    annotaion_event_message.event[
                        MammutEventAnnotation.SCENARIO_INDEX_ID
                    ]
                ]
            except AttributeError:
                selector_key = annotaion_event_message.event["original_text"]

            if annotaion_event_message.event["event_entry"] > 0:
                all_events_dict[
                    selector_key
                    + "-"
                    + str(annotaion_event_message.event["event_entry"])
                ] = annotaion_event_message
            else:
                all_events_dict[selector_key] = annotaion_event_message
        all_events_dict["None"] = "None"

        events_dropdown = widgets.Dropdown(
            options=all_events_dict,
            value="None",
            description="all events:",
            layout=Layout(width="800px"),
        )

        def events_dropdown_change(change):
            if change["new"] is not "None":
                anotation_widget.children = [
                    corpus_dropdown,
                    events_dropdown,
                    dimension_selector(change["new"]),
                ]
            else:
                anotation_widget.children = [corpus_dropdown, events_dropdown]

        events_dropdown.observe(events_dropdown_change, names="value")
        return events_dropdown

    all_corpus = package.corpus_map.get_all_corpus()
    all_corpus_dict = {}
    for i in all_corpus:
        if i.annotable:
            all_corpus_dict[i.sheet_title] = i
    all_corpus_dict["None"] = "None"
    corpus_dropdown = widgets.Dropdown(
        options=all_corpus_dict,
        value="None",
        description="select corpus:",
        layout=Layout(width="500px"),
    )

    def corpus_dropdown_change(change):
        if change["new"] != "None":
            anotation_widget.children = [corpus_dropdown, event_selector(change["new"])]
        else:
            anotation_widget.children = [corpus_dropdown]

    corpus_dropdown.observe(corpus_dropdown_change, names="value")

    anotation_widget = widgets.VBox([corpus_dropdown])
    return anotation_widget


def functionals_help_widget_section(package):
    def display_information(functional_lemma_descriptor):
        definitions = [
            {"index": i.index, "description": i.get_description()}
            for i in functional_lemma_descriptor.definitions
        ]
        context_dict = {"functionals_indexes": definitions}
        functionals_help_html = functionals_template.render(context_dict)
        functionals_help = widgets.HTML(value=functionals_help_html)
        return functionals_help

    def functionals_selector(option):
        lang, pos_id = option.split("-")
        all_functionals = package.standard.functionals  # debe ser un diccionario
        option_functionals = {}
        for key, val in all_functionals.items():
            if val.pos_paradigm == pos_id and val.regional_settings_lemma == lang:
                option_functionals[val.lemma] = val
        option_functionals["None"] = "None"

        functionals_dropdown = widgets.Dropdown(
            options=option_functionals,
            value="None",
            description="select " + option + ":",
            layout=Layout(width="600px"),
        )

        def functionals_dropdown_change(change):
            if change["new"] != "None":
                functionals_help_widget.children = [
                    functional_options_dropdown,
                    functionals_dropdown,
                    display_information(change["new"]),
                ]
            else:
                functionals_help_widget.children = [
                    functional_options_dropdown,
                    functionals_dropdown,
                ]

        functionals_dropdown.observe(functionals_dropdown_change, names="value")

        return functionals_dropdown

    functional_pos = []
    functional_options = {}
    for key, val in package.standard.functionals.items():
        if not val.is_bound:
            functional_pos.append(val.pos_paradigm)
    functional_pos = set(functional_pos)
    for functional_pos_id in functional_pos:
        pos_descriptor = package.standard.pos_descriptor_list[functional_pos_id]
        for lang in pos_descriptor.regional_settings_list:
            functional_options[f"{lang}-{pos_descriptor.name}"] = (
                lang + "-" + pos_descriptor.id
            )
    # TODO: si hago un reduce de las clases de todos los funcionales?sera el mismo widget para describir otros funcionales o solo para prep/conj
    functional_options["None"] = "None"
    functional_options_dropdown = widgets.Dropdown(
        options=functional_options,
        value="None",
        description="select pos pardigm:",
        layout=Layout(width="600px"),
    )

    def functionals_options_dropdown_change(change):
        if change["new"] != "None":
            functionals_help_widget.children = [
                functional_options_dropdown,
                functionals_selector(change["new"]),
            ]
        else:
            functionals_help_widget.children = [functional_options_dropdown]

    functional_options_dropdown.observe(
        functionals_options_dropdown_change, names="value"
    )

    functionals_help_widget = widgets.VBox([functional_options_dropdown])
    return functionals_help_widget
