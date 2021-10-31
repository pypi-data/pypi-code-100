from mammut.common.simulator_utilities import *
from ipywidgets import *
from django.template.loader import get_template

from mammut.common.mammut_api import UserType, RoomType, Thought, Issue


def get_simulation_boxes(simulator_obj, move_boxes_callback):
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
        move_boxes_callback()

    select_mammut_user_btn.on_click(select_user_button_clicked)
    select_mammut_box = widgets.VBox(
        [widgets.HBox([mammut_user_dropdown, select_mammut_user_btn])]
    )
    # /Select your mammut layout #

    # Select person user #
    select_person_user_dropdown = widgets.Dropdown(
        description="Su usuario:", disabled=False, button_style=""
    )
    select_person_dict = simulator_obj.users[UserType.person.value]
    select_person_dict.update(simulator_obj.users[UserType.normal.value])
    select_person_user_dropdown.options = select_person_dict
    select_user_btn = widgets.Button(description="Seleccionar", button_style="primary")

    def select_person_user_clicked(b):
        simulator_obj.current_person_user = simulator_obj.mammut_api.get_user(
            select_person_user_dropdown.value
        )
        move_boxes_callback()

    select_user_btn.on_click(select_person_user_clicked)
    select_user_box = widgets.VBox(
        [widgets.HBox([select_person_user_dropdown, select_user_btn])]
    )
    # /Select person user #

    # Select conversation room #
    select_room_dropdown = widgets.Dropdown(
        description="Conversation room:", disabled=False, button_style=""
    )
    rooms_dict = simulator_obj.rooms[RoomType.private.value]
    rooms_dict.update(simulator_obj.rooms[RoomType.group.value])
    select_room_dropdown.options = rooms_dict
    select_room_btn = widgets.Button(description="Seleccionar", button_style="primary")

    def select_room_clicked(b):
        simulator_obj.chat_room = simulator_obj.mammut_api.get_room(
            select_room_dropdown.value
        )
        move_boxes_callback()

    select_room_btn.on_click(select_room_clicked)
    select_room_box = widgets.VBox(
        [widgets.HBox([select_room_dropdown, select_room_btn])]
    )
    # /Select conversation room #

    # Send conversation messages #
    thoughts_list_template = get_template("thoughts_list.html")
    context_dict = {"thoughts_list": ["Hey bot", "Hello you!"]}
    thoughts_list_html = thoughts_list_template.render(context_dict)
    thoughts_list_widget = widgets.HTML(value=thoughts_list_html)
    send_message_textbox = widgets.Text(
        value="Hola Mammut", description="Mensaje:", layout=Layout(width="100%")
    )
    send_message_btn = widgets.Button(
        description="Enviar mensaje", button_style="primary"
    )
    get_thoughts_btn = widgets.Button(
        description="refresh thoughts", button_style="primary"
    )
    issue_is_present_output_alert = widgets.HTML(value="")

    def get_thouhts_btn_clicked(b):
        thoughts = simulator_obj.mammut_api.get_thoughts(
            simulator_obj.chat_room.id, from_type="Room"
        )
        room_thoughts = thoughts
        print("mensajes", thoughts)
        thoughts_text = [thought.text for thought in thoughts]
        print(thoughts)
        context_dict = {"thoughts_list": thoughts_text}
        thoughts_list_html = thoughts_list_template.render(context_dict)
        thoughts_list_widget.value = thoughts_list_html

        if room_thoughts[len(room_thoughts) - 1].issue is not None:
            issue_is_present_output_alert.value = (
                "<h4>There is a new Issue in the conversation</h4>"
            )
        elif (
            len(room_thoughts) > 1
            and room_thoughts[len(room_thoughts) - 2].issue is not None
        ):
            issue_is_present_output_alert.value = (
                "<h4>There is a new Issue in the conversation</h4>"
            )
        else:
            issue_is_present_output_alert.value = ""

    get_thoughts_btn.on_click(get_thouhts_btn_clicked)

    def send_message_btn_clicked(b):
        message = send_message_textbox.value
        test_thought = Thought(
            simulator_obj.current_person_user.id,
            simulator_obj.chat_room.id,
            message,
            mammut.get_str_format_timezone_aware_datetime_now(),
        )
        simulator_obj.mammut_api.post_thought(test_thought)

    send_message_btn.on_click(send_message_btn_clicked)
    send_message_box = widgets.VBox(
        [
            thoughts_list_widget,
            issue_is_present_output_alert,
            get_thoughts_btn,
            send_message_textbox,
            send_message_btn,
        ],
        layout=Layout(width="100%", align_items="center"),
    )

    # /Send conversation messages #

    # Solve conversation issues #
    ignore_issue_html = widgets.HTML("<h2>Ignorar Issue</h2>")
    ignore_issue_label = widgets.Label(
        value="Ignorar y desbloquear conversacion",
        layout=Layout(width="100%", align_items="center"),
    )
    ignore_issue_button = widgets.Button(description="Ignorar", button_style="primary")
    ignore_issue_output_html = widgets.HTML("")

    def ignore_issue_button_clicked(b):
        issue = Issue(
            room_id=simulator_obj.chat_room.id,
            issue_type="RemoveHaltedMark",
            machine_id=simulator_obj.current_user.id,
            causative_connected=False,
            resolution_text="",
            issue_state="open",
            custom_code="SomeCustomCode",
        )
        res = simulator_obj.mammut_api.post_remove_halted_mark_issue(issue)
        if res.status_code == 200:
            ignore_issue_output_html.value = "<p>Issue ignorado correctamente!</p>"
        else:
            ignore_issue_output_html.value = (
                "<p>Hubo un problema al intentar ignorar el Issue!</p>"
            )

    ignore_issue_button.on_click(ignore_issue_button_clicked)
    ignore_issue_box = widgets.VBox(
        [
            ignore_issue_html,
            ignore_issue_label,
            ignore_issue_button,
            ignore_issue_output_html,
        ],
        layout=Layout(width="100%", align_items="center"),
    )

    solve_issues_box = widgets.VBox(
        [widgets.HBox([ignore_issue_box])], layout=Layout(width="100%")
    )

    # /Solve conversation issues #

    return tuple(
        [
            select_mammut_box,
            select_user_box,
            select_room_box,
            send_message_box,
            solve_issues_box,
        ]
    )
