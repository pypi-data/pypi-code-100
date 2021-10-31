import os
import sys
from mammut.models.imaging.mammut_image_retraining import *
from ipywidgets import *

### Retrain Image Recognition ###
def get_image_retraining_widget(package, current_mammut_user):

    image_layout = Layout(width="80%", height="50px")
    image_style = {"description_width": "initial"}
    initial_image_message = widgets.HTML(
        value="<b>No package selected</b>",
        placeholder="Message: ",
        description="Message: ",
    )
    samples_textbox = widgets.Text(
        value="50",
        description="Numero de magenes geneneradas aleatoriamente:",
        layout=image_layout,
        style=image_style,
    )
    training_steps_textbox = widgets.Text(
        value="150",
        description="Numero de magenes geneneradas aleatoriamente:",
        layout=image_layout,
        style=image_style,
    )

    def get_retrain_content(package, current_mammut_user):

        images_corpus = ""
        for corpus in package.corpus_map.switch_get[
            package.corpus_map.DEFAULT_IMAGES_TYPE
        ]:
            images_corpus = images_corpus + "<br>" + corpus.sheet_title
        images_corpus_availables = widgets.HTML(
            value=images_corpus,
            placeholder="Images corpus: ",
            description="Images corpus: ",
        )
        retrain_images_button = widgets.Button(
            description="Retrain listed corpus",
            button_style="primary",
            layout=Layout(width="225px", height="100%"),
        )
        retrain_images_content = widgets.VBox(
            [
                images_corpus_availables,
                samples_textbox,
                training_steps_textbox,
                retrain_images_button,
            ]
        )

        def retrain_images_button_clicked(b):
            corpus = package.corpus_map.switch_get[
                package.corpus_map.DEFAULT_IMAGES_TYPE
            ][0]
            mammut_id = current_mammut_user.id
            retrained_graph_path, labels_path = package.image_retraining(
                corpus.destination_folder,
                mammut_id,
                int(samples_textbox.value),
                int(training_steps_textbox.value),
            )
            retrianed_graph_textbox.value = retrained_graph_path
            labels_textbox.value = labels_path

        retrain_images_button.on_click(retrain_images_button_clicked)
        return retrain_images_content

    inference_text = widgets.HTML(
        value="<b>inference</b>", placeholder="Message: ", description="Message: ",
    )

    retrianed_graph_textbox = widgets.Text(
        value="",
        description="retrined graph path:",
        layout=image_layout,
        style=image_style,
    )
    labels_textbox = widgets.Text(
        value="", description="labels path:", layout=image_layout, style=image_style
    )
    test_image_path_text_box = widgets.Text(
        value="", description="test image path:", layout=image_layout, style=image_style
    )

    image_inference_button = widgets.Button(
        description="Probar imagen",
        button_style="primary",
        layout=Layout(width="225px", height="100%"),
    )
    inference_result = widgets.HTML(value="<b></b>")
    images_inference_box = widgets.VBox(
        [
            retrianed_graph_textbox,
            labels_textbox,
            test_image_path_text_box,
            image_inference_button,
            inference_result,
        ]
    )
    retrain_images_box = widgets.VBox(
        [get_retrain_content(package, current_mammut_user), images_inference_box]
    )

    def image_inference_button_clicked(b):
        labels = label_image(
            retrianed_graph_textbox.value,
            test_image_path_text_box.value,
            labels_textbox.value,
        )
        inference_result.value = "<b>" + labels[0] + "<b>"
        inference_result.description = "result: "

    image_inference_button.on_click(image_inference_button_clicked)

    return retrain_images_box
