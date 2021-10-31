# coding=utf-8
from ipywidgets import *
from IPython.display import display
from django.template.loader import get_template
import chart_studio.plotly as py
import plotly.graph_objs as go

invalid_spans_table_template = get_template("invalid_spans_table.html")


def get_validator_widget(package):
    def event_validator_selector(corpus):
        # print('event validator selector')
        all_ea_validator = package.corpus_annotations_validator.annotations_validator_by_corpus[
            corpus.sheet_title
        ]
        all_events_dict = {}
        if valid_checkbox.value:
            events = all_ea_validator.valid_events
        else:
            events = all_ea_validator.invalid_events

        for annotaion_event_validator in events:
            for invalid_type in annotaion_event_validator.invalid_type:
                all_events_dict[
                    annotaion_event_validator.annotation.event["original_text"]
                    + invalid_type
                ] = annotaion_event_validator
        all_events_dict["None"] = "None"
        events_dropdown = widgets.Dropdown(
            options=all_events_dict,
            value="None",
            description="all events:",
            layout=Layout(width="800px"),
        )

        def show_overlaps(new_validator_event, selected_dimension):
            visualizers_list = all_ea_validator.visualize_overlap_from_event_validator(
                new_validator_event, selected_dimension
            )
            # TODO: de aqui en adelante es util el codigo o era cuando mostraba la grafica??
            # overlap_pair_type, events_appearence = all_ea_validator.get_event_overlap_and_overall_count(
            #    new_validator_event)
            # if overlap_pair_type is not None:
            #    overlap_count = all_ea_validator.get_event_overlap_and_overall_count(new_validator_event)
            return visualizers_list

        def dimension_selector(
            new_validator_event,
        ):  # TODO:  poner cual dimension se esta editando??
            event_annotation = new_validator_event.annotation
            # print('dimesion selector', event_annotation)
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

            def dimensions_dropdown_change(change):
                dimension = change["new"]
                if not only_overlaps_checkbox.value:
                    selected_dimension_visualizer = event_annotation.get_visualizer(
                        dimension, None
                    )
                    visualizer_list = show_overlaps(new_validator_event, dimension)
                    dimension_dropdown_vbox.children = [
                        dimensions_dropdown,
                        selected_dimension_visualizer,
                    ] + visualizer_list
                else:
                    visualizer_list = show_overlaps(new_validator_event, dimension)
                    if len(visualizer_list) == 0:
                        no_overlap_message = widgets.HTML(
                            value=dimension + " no tiene error de solapado"
                        )
                        dimension_dropdown_vbox.children = [
                            dimensions_dropdown,
                            no_overlap_message,
                        ]
                    else:
                        dimension_dropdown_vbox.children = [
                            dimensions_dropdown
                        ] + visualizer_list

            dimensions_dropdown.observe(dimensions_dropdown_change, names="value")
            dimension_dropdown_vbox = widgets.VBox([dimensions_dropdown])
            return dimension_dropdown_vbox

        def events_dropdown_change(change):
            if change["new"] is not "None":
                new_validator_event = change["new"]  # TODO: mejorar este nombre
                # print('new validator envent', new_validator_event)
                dimension_selector_widget = dimension_selector(new_validator_event)
                events_dropdow_selector_section.children = [
                    events_dropdown,
                    dimension_selector_widget,
                ]
            else:
                print("no se selecciono corpus")

        events_dropdown.observe(events_dropdown_change, names="value")

        show_chart_button = widgets.Button(
            description="mostrar charts",
            button_style="",
            tooltip="mostrar charts",
            icon="",
            layout=Layout(width="200px"),
        )

        def handle_show_chart_click(sender):
            new_validator_event = events_dropdown.value
            # display(all_ea_validator.visualize_overlap_from_event_validator(new_validator_event))
            (
                overlap_pair_type,
                events_appearence,
            ) = all_ea_validator.get_event_overlap_and_overall_count(
                new_validator_event
            )
            if overlap_pair_type is not None:
                overlap_count = all_ea_validator.get_event_overlap_and_overall_count(
                    new_validator_event
                )
                # print(overlap_count)
                # fig = tools.make_subplots(rows=2, cols=1)
                data = []
                annotations = []
                for i, vals in enumerate(overlap_count[1]):
                    # print(overlap_count[1])
                    labels = ["valid" + str(i), "invalid" + str(i)]
                    values = [overlap_count[1][vals], 1]
                    # print(labels, values)

                    if i == 0:
                        domain = {"x": [0, 0.5]}
                        text_domain = {"x": [0, 0.5], "y": [0, 0.5]}

                    else:
                        domain = {"x": [0.51, 1]}
                        text_domain = {"x": [0.51, 1], "y": [0, 0.5]}

                    trace = {
                        "labels": labels,
                        "values": values,
                        "type": "pie",
                        "name": list(overlap_count[1].keys())[i],
                        "domain": domain,
                        "hoverinfo": "label+percent+name",
                        "textinfo": "none",
                    }
                    data.append(trace)
                    annotation = {
                        "font": {"size": 20},
                        "showarrow": False,
                        "text": list(overlap_count[1].keys())[i],
                        "x": text_domain["x"][0],
                        "y": text_domain["y"][0],
                    }
                    annotations.append(annotation)
                layout = {
                    "title": "porcentaje del evento solapado conrespecto al total de cada anotacion",
                    "annotations": [],
                }
                fig = dict()
                fig["data"] = data
                fig["layout"] = layout
                fig["layout"]["annotations"] = annotations

                display(py.iplot(fig, filename="donut"))

        show_chart_button.on_click(handle_show_chart_click)
        events_dropdow_selector_section = widgets.VBox([events_dropdown])
        return events_dropdow_selector_section

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

    valid_checkbox = widgets.Checkbox(
        value=False, description="eventos validos", disabled=False
    )

    only_overlaps_checkbox = widgets.Checkbox(
        value=False, description="solo solapamiento", disabled=False
    )
    checkboxes = widgets.HBox([valid_checkbox, only_overlaps_checkbox])

    def valid_checkbox_change(d):
        corpus_dropdown.value = "None"
        validator_widget.children = [checkboxes, corpus_dropdown]

    valid_checkbox.observe(valid_checkbox_change)
    only_overlaps_checkbox.observe(valid_checkbox_change)

    def corpus_dropdown_change(change):
        if change["new"] != "None":
            validator_widget.children = [
                checkboxes,
                corpus_dropdown,
                event_validator_selector(change["new"]),
            ]
        else:
            validator_widget.children = [checkboxes, corpus_dropdown]

    corpus_dropdown.observe(corpus_dropdown_change, names="value")

    validator_widget = widgets.VBox([checkboxes, corpus_dropdown])
    return validator_widget


def get_invalid_spans_list(package):
    def display_invalid_spans(events_validator):
        definitions = [
            {"overlap": i[0], "original_text": i[1], "dimension": i[2]}
            for i in events_validator.overlap_spans_list
        ]
        context_dict = {"spans_values": definitions}
        invalid_spans_table_html = invalid_spans_table_template.render(context_dict)
        invalid_spans = widgets.HTML(value=invalid_spans_table_html)
        return invalid_spans

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
        if change["new"] != "None":
            corpus = change["new"]
            all_ea_validator = package.corpus_annotations_validator.annotations_validator_by_corpus[
                corpus.sheet_title
            ]
            validator_widget.children = [
                corpus_dropdown,
                display_invalid_spans(all_ea_validator),
            ]
        else:
            validator_widget.children = [corpus_dropdown]

    corpus_dropdown.observe(corpus_dropdown_change, names="value")

    validator_widget = widgets.VBox([corpus_dropdown])
    return validator_widget


def get_valid_and_invalid_events_graph(all_ea_validator):
    x = [i.valid for i in all_ea_validator.event_annotation_validator_list]
    data = [go.Histogram(x=x)]
    return py.iplot(data, filename="basic histogram")


def get_overlaps_by_dimension_graph(all_ea_validator):
    event_dim_keys = list()
    event_dim_values = list()
    entities_dim_keys = list()
    entities_dim_values = list()
    for key, val in all_ea_validator.invalid_by_dimension.items():
        for list_type, dimension_val in val.items():
            if list_type == "events_list":
                event_dim_keys.append(key)
                event_dim_values.append(len(dimension_val))
            else:
                entities_dim_keys.append(key)
                entities_dim_values.append(len(dimension_val))
    events_bars = go.Bar(x=event_dim_keys, y=event_dim_values, name="invalid events")
    entities_bars = go.Bar(
        x=entities_dim_keys, y=entities_dim_values, name="invalid entities"
    )
    data = [events_bars, entities_bars]

    layout = go.Layout(barmode="group")

    fig = go.Figure(data=data, layout=layout)
    return py.iplot(fig, filename="grouped-bar")


def get_overlaps_by_annotation_pair(all_ea_validator):
    keys = list()
    values = list()
    for key, val in all_ea_validator.invalid_annotations_pairs_count.items():
        keys.append(key)
        values.append(val)
    data = [go.Bar(x=keys, y=values)]

    return py.iplot(data, filename="basic-bar")


def get_overlaps_heatmap_by_annotation_pair(all_ea_validator):
    keys = list()
    values = list()
    for key, val in all_ea_validator.invalid_annotations_pairs_count.items():
        keys.append(key)
        values.append(val)

    x = [i.split("-")[0] for i in keys]
    y = [i.split("-")[1] for i in keys]
    trace = go.Heatmap(z=values, x=x, y=y)
    data = [trace]
    return py.iplot(data, filename="labelled-heatmap")


def get_overlap_representation_vs_appearance(all_ea_validator):
    pair_annotation_count_dict = dict()
    for invalid_event in all_ea_validator.invalid_events:
        overlap_pair_type_count = all_ea_validator.get_event_overlap_and_overall_count(
            invalid_event
        )
        for pair in overlap_pair_type_count:
            pair_annotation_count_dict[pair] = overlap_pair_type_count[pair]
    # debemos sacar los que no estan en parir_annotation_count_dict
    clean_annotation_pairs_count = dict()
    for key, val in all_ea_validator.invalid_annotations_pairs_count.items():
        if key in pair_annotation_count_dict:
            clean_annotation_pairs_count[key] = val
        else:
            print("key not in dict", key, "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
    data_list = list()
    overlap_data_list = list()
    x = list()
    index = 0
    for key, val in clean_annotation_pairs_count.items():
        index += 1
        print(key, val)
        if index % 2 == 0:
            total_count_color = "#448"
        else:
            total_count_color = "#458917"
        if key in pair_annotation_count_dict:
            print(pair_annotation_count_dict[key])
            # veces que aparecen el evento
            a1 = go.Bar(
                x=list(pair_annotation_count_dict[key].keys()),
                y=list(pair_annotation_count_dict[key].values()),
                type="bar",
                name=key,
                xaxis="x" + str(index),
                marker={"color": total_count_color},
            )
            data_list.append(a1)
            # veces que se solapa
            a2 = go.Bar(
                x=list(pair_annotation_count_dict[key].keys()),
                y=[val, val],
                type="bar",
                name=key + " solapados",
                xaxis="x" + str(index),
                marker={"color": "#CCF"},
            )
            overlap_data_list.append(a2)

        else:
            print("key not in dict", key, "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
            # TODO: porque hay un key que no coincide????
        # print(key, parir_annotation_count_dict[key], val)

    # creamos el alyout para agrupar los por eventos
    layout_vals = dict(
        barmode="stack",
        # yaxis= {'tickformat': '%'}
    )
    data_len = len(data_list)
    step_size = 1 / data_len
    step_val = 0
    for i, list_elem in enumerate(data_list):
        if i == 0:
            layout_vals["xaxis"] = dict(
                domain=[step_val, step_val + step_size], anchor=list_elem["xaxis"],
            )
        else:
            layout_vals["xaxis" + str(i + 1)] = dict(
                domain=[step_val, step_val + step_size], anchor=list_elem["xaxis"],
            )
        step_val = step_val + step_size
    # unimos las dos listas(cuanta de solapados y aparciones de eventoss)
    graph_data = list()
    for index, i in enumerate(data_list):
        graph_data.append(overlap_data_list[index])
        graph_data.append(i)

    data = graph_data

    fig = go.Figure(data=data, layout=layout_vals)
    return py.iplot(fig, filename="")
