from threading import Timer

import mammut
from mammut.common.mammut_api import *
from mammut.common.simulator_utilities import *
from ipywidgets import *
from datetime import datetime, date
import logging
from django.template.loader import get_template
import mammut.visualization.user_form as user_form
import mammut.visualization.room_form as room_form
import mammut.visualization.solve_thought_offer_to_be_learn as solve_thought_offer_to_be_learn
from mammut.visualization.simulator_widget_operation_utils import get_operations_boxes
from mammut.visualization.simulator_widget_simulation_utils import get_simulation_boxes
from mammut.visualization.simulator_widget_compilation_utils import (
    get_compilation_boxes,
)
import enum


log = logging.getLogger(__name__)

# quien debe instanciar el simulator_obj??
def get_simulator_widget(
    simulator_obj,
    mammut_api_url,
    redis_address,
    redis_port,
    package_file,
    standard_spreadsheet_id,
    users_filename,
    users_rooms_spreadsheet_id,
    users_sheet_name,
    rooms_sheet_name,
    rooms_filename,
):
    def move_to_next_box():
        accordion_size = len(accordion.children)
        if accordion.selected_index < accordion_size:
            accordion.selected_index = accordion.selected_index + 1
        else:
            accordion.selected_index = 0

    ## Select API URL ##
    def start_button_clicked(b):
        # clear_output()
        simulator_obj.mammut_api = Request(apiUrl_textBox.value)
        init_users(simulator_obj, users_filename)
        load_rooms(simulator_obj, rooms_filename)
        # Updates Alex Mammut #
        alex = simulator_obj.mammut_api.get_fixed_mammut()
        add_new_user(simulator_obj, alex, users_filename, UserType.machine.value)
        move_to_next_box()

    apiUrl_textBox = widgets.Text(
        value=mammut_api_url,
        description="Mammut API Url:",
        layout=Layout(width="100%", height="50px"),
    )
    redisUrl_textBox = widgets.Text(
        value=redis_address,
        description="Redis Url:",
        layout=Layout(width="100%", height="50px"),
    )
    start_button = widgets.Button(description="Comenzar", button_style="primary")
    configurationBox = widgets.VBox(
        [widgets.HBox([apiUrl_textBox]), redisUrl_textBox, start_button]
    )
    start_button.on_click(start_button_clicked)

    ## Select your operation mode ##
    class operation_modes(enum.Enum):
        COMPILATION = "Compilation"
        SIMULATION = "Simulation"
        OPERATIONS = "Operations"

    operation_modes_dict = {
        operation_modes.COMPILATION.value: operation_modes.COMPILATION.value,
        operation_modes.SIMULATION.value: operation_modes.SIMULATION.value,
        operation_modes.OPERATIONS.value: operation_modes.OPERATIONS.value,
    }
    operation_modes_dropdown = widgets.Dropdown(
        options=operation_modes_dict,
        value=operation_modes_dict[operation_modes.COMPILATION.value],
        description="Select your notebook operation mode",
        style={"description_width": "50%"},
        layout=Layout(width="100%"),
    )
    select_operation_mode_button = widgets.Button(
        description="Select", button_style="primary", style={"description_width": "50%"}
    )
    operation_modes_box = widgets.VBox(
        [widgets.HBox([operation_modes_dropdown]), select_operation_mode_button]
    )
    operation_mode_state = None

    def select_operation_mode(b):
        global operation_mode_state
        operation_mode_state = operation_modes(operation_modes_dropdown.value)
        if operation_mode_state == operation_modes.COMPILATION:
            new_boxes = get_compilation_boxes(
                simulator_obj, package_file, standard_spreadsheet_id, move_to_next_box
            )
            accordion.children = accordion.children + new_boxes
            accordion.set_title(2, "2. Seleccionar bot")
            accordion.set_title(3, "3. Validar Archivo")
            accordion.set_title(4, "4. Actualizar simulador")
            accordion.set_title(5, "5. Image retraining")

            def get_image_retrain_widget(b):
                if simulator_obj.package is not None:
                    if accordion.selected_index == 5:
                        image_retraining_widget = simulator_obj.package.get_image_retraining_widget(
                            simulator_obj.current_user
                        )
                        curr_childrens = list(accordion.children)
                        image_box = curr_childrens[5]
                        image_box.children = [image_retraining_widget]

            accordion.observe(get_image_retrain_widget)

        elif operation_mode_state == operation_modes.SIMULATION:
            new_boxes = get_simulation_boxes(simulator_obj, move_to_next_box)
            accordion.children = accordion.children + new_boxes
            accordion.set_title(2, "2. Seleccionar bot")
            accordion.set_title(3, "3. Seleccionar Usuario")
            accordion.set_title(4, "4. Seleccionar Room")
            accordion.set_title(5, "5. Enviar mensaje")
            accordion.set_title(6, "6. Solve Issue")

        elif operation_mode_state == operation_modes.OPERATIONS:
            new_boxes = get_operations_boxes(
                simulator_obj,
                users_rooms_spreadsheet_id,
                users_sheet_name,
                rooms_sheet_name,
                apiUrl_textBox.value,
                users_filename,
                rooms_filename,
                move_to_next_box,
            )
            accordion.children = accordion.children + new_boxes
            accordion.set_title(3, "Crear nuevas entidades")
            accordion.set_title(2, "Seleccionar bot")
            accordion.set_title(4, "Cargar Cargar Usuarios y Chats")
            accordion.set_title(5, "Cargar video")
            accordion.set_title(6, "Cargar Calendario")

        else:
            raise Exception("Unknown simulator operation mode.")

        move_to_next_box()

    select_operation_mode_button.on_click(select_operation_mode)
    ## /Select your operation mode ##
    ### Main Accordion ###
    accordion = widgets.Accordion(children=[configurationBox, operation_modes_box])
    accordion.set_title(0, "0. Configuracion")
    accordion.set_title(1, "1. Seleccionar operation mode")
    accordion.selected_index = 0
    return accordion
