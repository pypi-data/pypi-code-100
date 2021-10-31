# coding=utf-8

from ipywidgets import *
from django.template.loader import get_template

disambiguation_template = get_template("disambiguation.html")
tokens_type_resume_template = get_template("token_type_resume.html")


def disambiguation_widget_section(package):
    def definition_selector(defintion_set_entry_id, morpheme_info):
        definitions_options = {}
        selected_definition_id = {"value": None}
        definitions_set_entries = package.dictionary.get_definitions_entries_as_list(
            defintion_set_entry_id
        )

        def get_disambiguation_aplication_html():
            definitions_dict = {}
            current_definition = None
            for index, definition_entry in enumerate(definitions_set_entries):
                if package.dictionary.is_disambiguation_selected(
                    morpheme_info,
                    package.dictionary.get_definition_complete_id(
                        defintion_set_entry_id, index
                    ),
                ):
                    definitions_dict[
                        "def " + str(index + 1) + " - actual"
                    ] = definition_entry  # TODO mejorar estos string, constantes?
                    current_definition = definition_entry
                else:
                    definitions_dict["def " + str(index + 1)] = definition_entry
            disambiguation_application_html = disambiguation_template.render(
                {
                    "definition_sets": definitions_dict,
                    "current_definition": current_definition,
                }
            )
            disambiguation_application = widgets.HTML(
                value=disambiguation_application_html
            )
            return disambiguation_application

        for index, i in enumerate(definitions_set_entries):
            definitions_options[
                "def " + str(index + 1)
            ] = package.dictionary.get_definition_complete_id(
                defintion_set_entry_id, index
            )
        disambiguation_application = get_disambiguation_aplication_html()
        defintions_radio_buttons = widgets.RadioButtons(
            options=definitions_options,
            value=None,
            description="select one definition:",
            layout=Layout(width="900px"),
        )

        def defintions_radio_buttons_change(change):
            if change["new"] is not None:
                selected_definition_id["value"] = change["new"]

        defintions_radio_buttons.observe(defintions_radio_buttons_change, names="value")
        save_definition_button = widgets.Button(
            description="Guardar Definition",
            button_style="",
            tooltip="Guardar Defiinition",
            icon="",
            layout=Layout(width="200px"),
        )

        def handle_save_definition(sender):
            if selected_definition_id["value"] is not None:
                package.dictionary.save_lema_disambiguation(
                    morpheme_info, selected_definition_id["value"]
                )
                tokens_selector_elements.children = [
                    get_disambiguation_aplication_html(),
                    defintions_radio_buttons,
                    save_definition_button,
                ]

        save_definition_button.on_click(handle_save_definition)

        tokens_selector_elements = widgets.VBox(
            [
                disambiguation_application,
                defintions_radio_buttons,
                save_definition_button,
            ]
        )

        return tokens_selector_elements

    def token_selector(event_annotation):
        (
            tokens_dict,
            tokens_info_dict,
            tokens_type_resume,
        ) = package.dictionary.get_event_tokens_dict_and_info(event_annotation)

        tokens_type_resume_html = tokens_type_resume_template.render(
            {"token_types": tokens_type_resume}
        )
        tokens_type_resume = widgets.HTML(value=tokens_type_resume_html)
        tokens_dict["None"] = "None"
        tokens = [i for i in tokens_dict]
        tokens_dropdown = widgets.Dropdown(
            options=tokens,
            value="None",
            description="select one token:",
            layout=Layout(width="500px"),
        )

        def tokens_dropdown_change(change):
            if change["new"] is not "None":
                tokens_selector_elements.children = [
                    tokens_dropdown,
                    definition_selector(
                        tokens_dict[change["new"]], tokens_info_dict[change["new"]]
                    ),
                ]
            else:
                tokens_selector_elements.children = [tokens_dropdown]

        tokens_dropdown.observe(tokens_dropdown_change, names="value")

        tokens_selector_elements = widgets.VBox([tokens_type_resume, tokens_dropdown])

        return tokens_selector_elements

    def event_selector(corpus):
        annotation_object = package.annotations
        all_events = annotation_object.get_event_messages(corpus)
        annotation_events = annotation_object.get_annotation_event_messages(corpus)
        all_events_dict = {}
        for annotaion_event_message in annotation_events:
            all_events_dict[
                annotaion_event_message.event["original_text"]
            ] = annotaion_event_message
        all_events_dict["None"] = "None"

        events_dropdown = widgets.Dropdown(
            options=all_events_dict,
            value="None",
            description="all events:",
            layout=Layout(width="800px"),
        )

        def events_dropdown_change(change):
            if change["new"] is not "None":
                disambiguation_widget.children = [
                    corpus_dropdown,
                    events_dropdown,
                    token_selector(change["new"]),
                ]
            else:
                disambiguation_widget.children = [corpus_dropdown, events_dropdown]

        events_dropdown.observe(events_dropdown_change, names="value")
        return events_dropdown

    all_corpus = package.corpus_map.get_all_corpus()
    all_corpus_dict = {}
    for i in all_corpus:
        all_corpus_dict[i.sheet_title] = i
    all_corpus_dict["None"] = "None"
    corpus_dropdown = widgets.Dropdown(
        options=all_corpus_dict,
        value="None",
        description="select corpus:",
        layout=Layout(width="500px"),
    )

    def corpus_dropdown_change(change):
        if change["new"] is not "None":
            disambiguation_widget.children = [
                corpus_dropdown,
                event_selector(change["new"]),
            ]
        else:
            disambiguation_widget.children = [corpus_dropdown]

    corpus_dropdown.observe(corpus_dropdown_change, names="value")

    disambiguation_widget = widgets.VBox([corpus_dropdown])
    return disambiguation_widget
