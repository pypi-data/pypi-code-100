from mammut.common.simulator_utilities import *
from ipywidgets import *
from django.template.loader import get_template

from mammut.common.mammut_api import UserType
from mammut.common.package import Package, log
from mammut.common.simulator_utilities import to_sp_string


def get_compilation_boxes(
    simulator_obj, package_file, standard_spreadsheet_id, move_box_callback
):
    # Select your mammut layout #
    mammut_user_dropdown = widgets.Dropdown(
        description="Mammut bot", disabled=False, button_style=""
    )
    mammut_user_dropdown.options = simulator_obj.users[UserType.machine.value]
    select_mammut_user_btn = widgets.Button(
        description="Seleccionar", button_style="primary"
    )

    def select_user_button_clicked(b):
        simulator_obj.current_user = simulator_obj.mammut_api.get_user(
            mammut_user_dropdown.value
        )
        move_box_callback()

    select_mammut_user_btn.on_click(select_user_button_clicked)
    select_mammut_box = widgets.VBox(
        [widgets.HBox([mammut_user_dropdown, select_mammut_user_btn])]
    )
    # /Select your mammut layout #

    # Validate package #
    validate_package_html = widgets.HTML(value="")
    validate_package_file_box = widgets.Text(
        value=package_file, description="Id Archivo:", layout=Layout(width="100%")
    )
    validate_package_btn = widgets.Button(
        description="Validar Archivo", button_style="primary"
    )

    def validate_package_btn_clicked(b):
        try:
            # clear_output()
            # validar archivo
            validate_package_html.value = (
                "Validando archivo... <br> Por favor espere..."
            )
            simulator_obj.package = Package(
                validate_package_file_box.value,
                standard_spreadsheet_id
            )
            validate_package_html.value = "El archivo " + to_sp_string(True) + "<br>"
            move_box_callback()
        except Exception as ex:
            validate_package_html.value = "Error validando archivo... <br> " + str(ex)
            log.exception("Error validating file")

    update_simulator_corpus_list = widgets.Text(
        value="1",
        description="Corpus Id's (csv)",
        style={"description_width": "50%"},
        layout=Layout(width="100%"),
    )
    validate_package_btn.on_click(validate_package_btn_clicked)
    validate_package_box = widgets.VBox(
        [
            widgets.HBox(
                [
                    validate_package_html,
                    validate_package_file_box,
                    validate_package_btn,
                ],
                layout=Layout(width="100%", align_items="center"),
            )
        ]
    )
    # /Validate package #

    # /Update simulator #
    update_simulator_html = widgets.HTML(
        value='Presione "Actualizar Simulador" para guardar los cambios del excel en el servidor Mammut.'
    )
    update_simulator_html.layout = Layout(width="50%", height="100%")
    update_simulator_btn = widgets.Button(
        description="Actualizar Simulador", button_style="primary"
    )

    def get_update_button_clicked():
        def update_output_html_callback(mess, output):
            if output is not None:
                update_simulator_html.value += mess + " </br>" + output + " </br>"
            else:
                update_simulator_html.value += mess + " </br>"

        def update_button_clicked(b):
            update_simulator_html.value = (
                "Iniciando proceso de compilacion... </br> </br>"
            )
            corpus_list_to_compile = [
                int(x) for x in update_simulator_corpus_list.value.split(",")
            ]
            simulator_obj.package.compile_corpus_list(
                simulator_obj.current_user.id,
                update_output_html_callback,
                corpus_list_to_compile,
            )
            # TODO: ELiminar o cambiar por el nuevo compilador
            # TODO: aqui debemos colocar las preguntas que se puedan sacar del sampling corpus

        return update_button_clicked

    update_simulator_btn.on_click(get_update_button_clicked())
    update_simulator_box = widgets.VBox(
        [update_simulator_html, update_simulator_corpus_list, update_simulator_btn],
        layout=Layout(width="100%", align_items="center"),
    )
    # /Update simulator #

    # Update simulator embedded #
    update_simulator_embedded_sampling_corpus_text = widgets.Text(
        value="True",
        description="Ejecutar sampling corpus",
        style={"description_width": "50%"},
        layout=Layout(width="100%"),
    )
    update_simulator_embedded_corpus_list = widgets.Text(
        value="1",
        description="Corpus Id's (csv)",
        style={"description_width": "50%"},
        layout=Layout(width="100%"),
    )
    update_simulator_embedded_metadata_token = widgets.Text(
        value="->",
        description="Metadata token separator",
        style={"description_width": "50%"},
        layout=Layout(width="100%"),
    )
    update_simulator_embedded_person = widgets.Text(
        description="Su Id",
        style={"description_width": "50%"},
        layout=Layout(width="100%"),
    )
    update_simulator_embedded_mammut_logger = widgets.Text(
        description="Id del Mammut que reporta",
        style={"description_width": "50%"},
        layout=Layout(width="100%"),
    )
    update_simulator_embedded_compilation_room = widgets.Text(
        description="El ID de su room de reporte",
        style={"description_width": "50%"},
        layout=Layout(width="100%"),
    )
    update_simulator_embedded_regional_settings = widgets.Text(
        value="en",
        description="Idioma de reporte",
        style={"description_width": "50%"},
        layout=Layout(width="100%"),
    )
    update_embedded_button = widgets.Button(
        description="Actualizar Mammut Embedded", button_style="primary"
    )

    def __refresh_output(b):
        thoughts_list_template = get_template("thoughts_list.html")
        thoughts = simulator_obj.mammut_api.get_thoughts_since(
            int(update_simulator_embedded_compilation_room.value),
            __refresh_output.last_date,
        )
        thoughts = [thought.text for thought in thoughts]
        context_dict = {"thoughts_list": thoughts}
        thoughts_list_html = thoughts_list_template.render(context_dict)
        if len(thoughts) > 0:
            __refresh_output.last_date = (
                mammut.get_str_format_timezone_aware_datetime_now()
            )
            update_simulator_html.value = (
                update_simulator_html.value + "<br>" + thoughts_list_html
            )

    __refresh_output.last_date = mammut.get_str_format_timezone_aware_datetime_now()

    def update_embedded_response_eval(r):
        if r is 200:
            update_simulator_html.value = (
                "Iniciando proceso exitoso de compilacion...<br><br>"
            )
        elif r is 428:
            update_simulator_html.value = "El room de reporte no es un room entre el usuario y el bot de reporte.<br><br>"
        elif r is 503:
            update_simulator_html.value = "Se ha detectado otra compilacion en curso. Intente nuevamente en unos minutos...<br><br>"
        else:
            update_simulator_html.value = (
                "Error al comunicarse con Mammut API...<br><br>"
            )

        update_embedded_button.description = "Refresh output"
        update_embedded_button.on_click(update_embedded_button_clicked, True)
        update_embedded_button.on_click(__refresh_output)
        return

    def update_embedded_button_clicked(b):
        compile_payload = dict()
        compile_payload["packageId"] = simulator_obj.package.main_id
        compile_payload["executeSamplingCorpus"] = (
            update_simulator_embedded_sampling_corpus_text.value == "True"
        )
        compile_payload["corpusIds"] = [
            int(x) for x in update_simulator_embedded_corpus_list.value.split(",")
        ]
        compile_payload[
            "slideMetadataTokenSeparator"
        ] = update_simulator_embedded_metadata_token.value
        compile_payload["mammutId"] = simulator_obj.current_user.id
        compile_payload["userId"] = int(update_simulator_embedded_person.value)
        compile_payload["roomId"] = int(
            update_simulator_embedded_compilation_room.value
        )
        compile_payload[
            "regionalSettings"
        ] = update_simulator_embedded_regional_settings.value
        compile_payload["mammutLoggerId"] = int(
            update_simulator_embedded_mammut_logger.value
        )
        compile_payload_json = json.dumps(compile_payload)
        post_compilation_response = simulator_obj.mammut_api.post_compilation(
            compile_payload_json
        )
        __last_date = mammut.get_str_format_timezone_aware_datetime_now()
        update_embedded_response_eval(post_compilation_response)

    update_embedded_button.on_click(update_embedded_button_clicked)
    update_simulator_embedded_box = widgets.VBox(
        [
            update_simulator_embedded_sampling_corpus_text,
            update_simulator_embedded_corpus_list,
            update_simulator_embedded_metadata_token,
            update_simulator_embedded_person,
            update_simulator_embedded_mammut_logger,
            update_simulator_embedded_compilation_room,
            update_simulator_embedded_regional_settings,
            update_simulator_html,
            update_embedded_button,
        ],
        layout=Layout(width="100%", align_items="center"),
    )
    # /Update simulator embedded #

    # Image retraining #
    initial_image_message = widgets.HTML(
        value="<b>No package selected</b>",
        placeholder="Message: ",
        description="Message: ",
    )
    retrain_images_box = widgets.VBox([initial_image_message])
    # /Image retraining #

    if simulator_obj.embedded:
        return tuple(
            [
                select_mammut_box,
                validate_package_box,
                update_simulator_embedded_box,
                retrain_images_box,
            ]
        )
    else:
        return tuple(
            [
                select_mammut_box,
                validate_package_box,
                update_simulator_box,
                retrain_images_box,
            ]
        )
