# coding=utf-8
from ipywidgets import *
from django.template.loader import get_template
import pandas as pd
import plotly
import plotly.graph_objs as go
from collections import namedtuple

rae_verb_conjugation_models_template = get_template("rae_verb_conjugation_models.html")
pending_words_template = get_template("pending_words.html")
paradigm_application_template = get_template("paradigm_application.html")
ParadigmAppWordDesc = namedtuple("ParadigmAppWordDesc", ["morpheme", "features"])
PendingWordDesc = namedtuple("PendingWordDesc", ["text", "strike"])


def create_conjugator_section(verb: str, language_tool: str = "es-wr"):
    res = None
    if "en" in language_tool:
        verbix_style = ""  #'border: 0px none; margin-left: -132px; height: 650px; margin-top: -230px; width: 900px; margin-bottom: -170px;'
        verbix_url_pattern = "//www.verbix.com/webverbix/English/{0}.html"
        verbix_url = verbix_url_pattern.format(verb.lower().strip())
        if verbix_style:
            verbix_html_wrapper = """<div style="border: 2px solid #D5CC5A; overflow: hidden; margin: 15px auto; max-width: 950px;">
        <iframe src="{0}" style="{1}">
        </iframe>
        </div>"""
            verbix_html = verbix_html_wrapper.format(verbix_url, verbix_style)
        else:
            verbix_html_wrapper = '<iframe src="{0}" width=750 height=350></iframe>'
            verbix_html = verbix_html_wrapper.format(verbix_url)
        res = widgets.HTML(value=verbix_html)
    else:
        word_reference_style = "border: 0px none; margin-left: -132px; height: 650px; margin-top: -230px; width: 900px; margin-bottom: -170px;"
        word_reference_url_pattern = "//www.wordreference.com/conj/EsVerbs.aspx?v={0}"
        word_reference_url = word_reference_url_pattern.format(verb)
        if word_reference_style:
            word_reference_html_wrapper = """<div style="border: 2px solid #D5CC5A; overflow: hidden; margin: 15px auto; max-width: 950px;">
    <iframe src="{0}" style="{1}">
    </iframe>
    </div>"""
            word_reference_html = word_reference_html_wrapper.format(
                word_reference_url, word_reference_style
            )
        else:
            word_reference_html_wrapper = (
                '<iframe src="{0}" width=750 height=350></iframe>'
            )
            word_reference_html = word_reference_html_wrapper.format(word_reference_url)
        res = widgets.HTML(value=word_reference_html)
    return res


def create_rae_conjugation_section():
    # rae_url = 'http://www.rae.es/diccionario-panhispanico-de-dudas/apendices/modelos-de-conjugacion-verbal'
    rae_style = "border: 0px none; margin-left: -132px; height: 650px; margin-top: -230px; width: 900px; margin-bottom: -170px;"
    if rae_style:
        rae_html_wrapper = """<div style="border: 2px solid #D5CC5A; overflow: hidden; margin: 15px auto; max-width: 950px;">
    <iframe style="{1}">{0}</iframe></div>"""
        rae_html = rae_html_wrapper.format(
            rae_verb_conjugation_models_template.render(), rae_style
        )
    else:
        rae_html_wrapper = "<iframe width=750 height=350>{0}</iframe>"
        rae_html = rae_html_wrapper.format(
            rae_verb_conjugation_models_template.render()
        )
    rae = widgets.HTML(value=rae_verb_conjugation_models_template.render())
    box = widgets.Accordion([rae])
    box.set_title(0, "Modelos de conjugacion de RAE")
    return box


def create_defined_words_section(words, as_data_frame=True):
    buckets = {}
    max_bucket_size = 0
    for word in words:
        bucket = []
        if word[0] not in buckets:
            buckets[word[0]] = bucket
        else:
            bucket = buckets[word[0]]
        bucket.append(word)
        if len(bucket) > max_bucket_size:
            max_bucket_size = len(bucket)
    for bid in buckets:
        buckets[bid] = sorted(buckets[bid])
    bids = sorted(buckets.keys())
    word_groups_rows = []
    for i in range(0, max_bucket_size):
        row = []
        word_groups_rows.append(row)
        for bkt_id in bids:
            bucket = buckets[bkt_id]
            if len(bucket) > i:
                if as_data_frame:
                    row.append(bucket[i])
                else:
                    row.append(PendingWordDesc(bucket[i], False))
            else:
                if as_data_frame:
                    row.append("")
                else:
                    row.append(PendingWordDesc("-", False))
    if as_data_frame:
        return pd.DataFrame(data=word_groups_rows, columns=bids)
    else:
        context_dict = {"word_groups": bids, "word_groups_rows": word_groups_rows}
        pending_words_html = pending_words_template.render(context_dict)
        return widgets.HTML(value=pending_words_html)


def create_pending_words_section(
    dictionary, regional_settings: str, layer=0, as_data_frame=True
):
    return create_words_section(
        dictionary, regional_settings, layer, as_data_frame, True
    )


def create_ready_words_section(
    dictionary, regional_settings: str, layer=0, as_data_frame=True
):
    return create_words_section(
        dictionary, regional_settings, layer, as_data_frame, False
    )


def create_words_section(
    dictionary, regional_settings: str, layer, as_data_frame, undefined
):
    buckets = {}
    max_bucket_size = 0
    word_list = (
        dictionary.get_undefined_morphemes_generator(regional_settings, layer, True)
        if undefined
        else dictionary.get_defined_morphemes_generator(regional_settings, layer, True)
    )
    for word, index in word_list:
        bucket = []
        if word[0] not in buckets:
            buckets[word[0]] = bucket
        else:
            bucket = buckets[word[0]]
        bucket.append("{0} | {1:.2f}".format(word, index))
        if len(bucket) > max_bucket_size:
            max_bucket_size = len(bucket)
    for bid in buckets:
        buckets[bid] = sorted(buckets[bid])
    bids = sorted(buckets.keys())
    word_groups_rows = []
    for i in range(0, max_bucket_size):
        row = []
        word_groups_rows.append(row)
        for bkt_id in bids:
            bucket = buckets[bkt_id]
            if len(bucket) > i:
                if as_data_frame:
                    row.append(bucket[i])
                else:
                    row.append(PendingWordDesc(bucket[i], False))
            else:
                if as_data_frame:
                    row.append("")
                else:
                    row.append(PendingWordDesc("-", False))
    if as_data_frame:
        return pd.DataFrame(data=word_groups_rows, columns=bids)
    else:
        context_dict = {"word_groups": bids, "word_groups_rows": word_groups_rows}
        pending_words_html = pending_words_template.render(context_dict)
        return widgets.HTML(value=pending_words_html)


def create_undefined_functionals_section(
    standard, regional_settings: str, as_data_frame=True
):
    buckets = {}
    max_bucket_size = 0
    for func in standard.get_undefined_functionals(regional_settings):
        word = func.lemma + " (" + func.pos_paradigm + ")"
        bucket = []
        if word[0] not in buckets:
            buckets[word[0]] = bucket
        else:
            bucket = buckets[word[0]]
        bucket.append(word)
        if len(bucket) > max_bucket_size:
            max_bucket_size = len(bucket)
    for bid in buckets:
        buckets[bid] = sorted(buckets[bid])
    bids = sorted(buckets.keys())
    word_groups_rows = []
    for i in range(0, max_bucket_size):
        row = []
        word_groups_rows.append(row)
        for bkt_id in bids:
            bucket = buckets[bkt_id]
            if len(bucket) > i:
                if as_data_frame:
                    row.append(bucket[i])
                else:
                    row.append(PendingWordDesc(bucket[i], False))
            else:
                if as_data_frame:
                    row.append("")
                else:
                    row.append(PendingWordDesc("-", False))
    if as_data_frame:
        return pd.DataFrame(data=word_groups_rows, columns=bids)
    else:
        context_dict = {"word_groups": bids, "word_groups_rows": word_groups_rows}
        pending_words_html = pending_words_template.render(context_dict)
        return widgets.HTML(value=pending_words_html)


def create_words_in_definitions_out_of_vocabulary_section(
    dictionary, regional_settings: str, as_data_frame=True
):
    buckets = {}
    max_bucket_size = 0
    for word in dictionary.get_words_in_definitions_out_of_vocabulary(
        regional_settings
    ):
        bucket = []
        if word[0] not in buckets:
            buckets[word[0]] = bucket
        else:
            bucket = buckets[word[0]]
        bucket.append(word)
        if len(bucket) > max_bucket_size:
            max_bucket_size = len(bucket)
    for bid in buckets:
        buckets[bid] = sorted(buckets[bid])
    bids = sorted(buckets.keys())
    word_groups_rows = []
    for i in range(0, max_bucket_size):
        row = []
        word_groups_rows.append(row)
        for bkt_id in bids:
            bucket = buckets[bkt_id]
            if len(bucket) > i:
                if as_data_frame:
                    row.append(bucket[i])
                else:
                    row.append(PendingWordDesc(bucket[i], False))
            else:
                if as_data_frame:
                    row.append("")
                else:
                    row.append(PendingWordDesc("-", False))
    if as_data_frame:
        return pd.DataFrame(data=word_groups_rows, columns=bids)
    else:
        context_dict = {"word_groups": bids, "word_groups_rows": word_groups_rows}
        pending_words_html = pending_words_template.render(context_dict)
        return widgets.HTML(value=pending_words_html)


def show_lexicalization_evolution(tokenizer, regional_settings: str):
    (
        plot_data_words_count,
        plot_data_words_count_colors,
        plot_data_undefined_morphemes_count,
        plot_data_undefined_morphemes_count_colors,
    ) = tokenizer.stats[regional_settings].get_plot_data()
    trace_words_count = go.Scatter(
        y=plot_data_words_count,
        mode="markers+lines",
        name="Cantidad de Palabras",
        marker=dict(color=plot_data_words_count_colors),
    )
    trace_plot_data_undefined_morphemes_count = go.Scatter(
        y=plot_data_undefined_morphemes_count,
        mode="markers+lines",
        name="Palabras sin definicion",
        marker=dict(color=plot_data_undefined_morphemes_count_colors),
    )
    data = [trace_words_count, trace_plot_data_undefined_morphemes_count]

    plotly.offline.iplot(data)


def show_paradigm_application(title, word_rows, parad_application):
    context_dict = {"title": title, "word_rows": word_rows}
    parad_application_html = paradigm_application_template.render(context_dict)
    parad_application.value = parad_application_html


def show_paradigm(morpheme_res, words_inflections):
    parad_application = widgets.HTML(value="")
    word_rows = [
        ParadigmAppWordDesc(
            m.text, ", ".join(map(lambda f: f.feature_name, m.features))
        )
        for m in morpheme_res
    ]
    show_paradigm_application(
        "Paradigma Morfema Aplicado", word_rows, parad_application
    )
    messages = []
    if len(words_inflections) != 0:
        s_i = set(words_inflections)
        s_w = set([m.text for m in morpheme_res])
        c_words_inflections_expected_not_generated = list(s_i - s_w)
        c_words_inflections_generated_not_expected = list(s_w - s_i)
        if len(c_words_inflections_expected_not_generated) != 0:
            messages.append(
                "Inflexiones esperadas NO generadas: "
                + ", ".join(c_words_inflections_expected_not_generated)
            )
        if len(c_words_inflections_generated_not_expected) != 0:
            messages.append(
                "Inflexiones generadas NO esperadas: "
                + ", ".join(c_words_inflections_generated_not_expected)
            )
    if len(messages) != 0:
        message = "\n".join(messages)
        text_message = widgets.Textarea(
            value=message,
            description="Errores:",
            disabled=True,
            layout=widgets.Layout(width="350px", height="120px"),
        )
        parad_application = widgets.HBox([parad_application, text_message])
    # else:
    #     display(parad_application)

    return parad_application
