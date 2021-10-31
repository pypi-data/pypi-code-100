from mammut.common.simulator_utilities import *
from ipywidgets import *


def get_operations_boxes(
    simulator_obj,
    users_rooms_spreadsheet_id,
    users_sheet_name,
    rooms_sheet_name,
    api_url,
    users_filename,
    rooms_filename,
    move_box_callback,
):

    # Unique fields in API for checking#
    unique_fields = [
        "facebook-id",
        "facebook-access-token",
        "main-phone-number",
        "main-email",
    ]

    def users_check_for_property_existence(prop_name: str, prop_val: str):
        user = simulator_obj.mammut_api.get_unique_vertex("user", prop_name, prop_val)
        if "error" in user:
            return {"error": "Error communicating with Mammut API"}

        if len(user) is 0:
            return {"user": False, "id": -1}
        else:
            return {"user": True, "id": user["id"]}

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

    # Create entities #
    bot_custom_properties_box = widgets.VBox(
        [
            widgets.HBox(
                [
                    widgets.Text(value="user-type", layout=Layout(width="50%")),
                    widgets.Text(value="machine", layout=Layout(width="50%")),
                ]
            )
        ]
    )
    add_bot_property_button = widgets.Button(
        description="+",
        button_style="primary",
        layout=Layout(width="35px", height="100%",),
        style={"button_color": "green"},
    )
    add_bot_output = widgets.HTML("")

    def add_bot_custom_property_button_clicked(b):
        new_property_name = widgets.Text(
            value="Property name", layout=Layout(width="50%")
        )
        new_property_value = widgets.Text(
            value="Property value", layout=Layout(width="50%")
        )
        bot_custom_properties_box.children = bot_custom_properties_box.children + tuple(
            [widgets.HBox([new_property_name, new_property_value])]
        )

    def create_bot_button_clicked(b):
        props_and_values = bot_custom_properties_box.children
        props_and_values_dic = {}
        for index in range(0, len(props_and_values)):
            props_and_values_dic[props_and_values[index].children[0].value] = (
                props_and_values[index].children[1].value
            )

        for i, j in props_and_values_dic.items():
            if i in unique_fields:
                exists = users_check_for_property_existence(i, j)
                print(exists)
                if exists["user"]:
                    bot_id = exists["id"]
                    add_user_output.value = (
                        f"User already exists with that {i}. User Id - {bot_id}"
                    )
                    return

        res = simulator_obj.mammut_api.post_request(
            simulator_obj.mammut_api.post_user_path, props_and_values_dic
        )
        if res.status_code == 200:
            res_json = res.json()
            created_user_id = -1
            for result in res_json["taskResult"]:
                if result["affectedElementName"] == "user":
                    created_user_id = result["affectedElementId"]
                    break
            add_bot_output.value = f"<h2>Bot created: ID-{created_user_id}</h2>"
            user = simulator_obj.mammut_api.get_user(created_user_id)
            add_new_user(simulator_obj, user, users_filename, UserType.machine.value)
        else:
            add_bot_output.value = "<h2>Error creating bot.</h2>"

    add_bot_property_button.on_click(add_bot_custom_property_button_clicked)
    create_bot_button = widgets.Button(
        description="Create bot",
        button_style="primary",
        layout=Layout(width="225px", height="100%"),
    )
    create_bot_button.on_click(create_bot_button_clicked)
    create_bot_box = widgets.VBox(
        [
            bot_custom_properties_box,
            add_bot_property_button,
            create_bot_button,
            add_bot_output,
        ],
        layout=Layout(width="100%", align_items="center"),
    )

    user_custom_properties_box = widgets.VBox(
        [
            widgets.HBox(
                [
                    widgets.Text(value="user-type", layout=Layout(width="50%")),
                    widgets.Text(value="normal", layout=Layout(width="50%")),
                ]
            )
        ]
    )
    add_user_property_button = widgets.Button(
        description="+",
        button_style="primary",
        layout=Layout(width="35px", height="100%",),
        style={"button_color": "green"},
    )
    add_user_output = widgets.HTML("")

    def add_user_custom_property_button_clicked(b):
        new_property_name = widgets.Text(
            value="Property name", layout=Layout(width="50%")
        )
        new_property_value = widgets.Text(
            value="Property value", layout=Layout(width="50%")
        )
        user_custom_properties_box.children = (
            user_custom_properties_box.children
            + tuple([widgets.HBox([new_property_name, new_property_value])])
        )

    def create_user_button_clicked(b):
        props_and_values = user_custom_properties_box.children
        props_and_values_dic = {}
        for index in range(0, len(props_and_values)):
            props_and_values_dic[props_and_values[index].children[0].value] = (
                props_and_values[index].children[1].value
            )

        for i, j in props_and_values_dic.items():
            if i in unique_fields:
                exists = users_check_for_property_existence(i, j)
                print(exists)
                if exists["user"]:
                    user_id = exists["id"]
                    add_user_output.value = (
                        f"User already exists with that {i}. User Id - {user_id}"
                    )
                    return

        if not "main-email" in props_and_values_dic:
            add_user_output.value = "<h2>Error: Es necesario el campo main-email.</h2>"
        else:
            res = simulator_obj.mammut_api.post_request(
                simulator_obj.mammut_api.post_user_path, props_and_values_dic
            )
            if res.status_code == 200:
                res_json = res.json()
                created_user_id = -1
                room_with_alex_id = -1
                for result in res_json["taskResult"]:
                    if result["affectedElementName"] == "user":
                        created_user_id = result["affectedElementId"]
                        break
                for result in res_json["taskResult"]:
                    if result["affectedElementName"] == "room":
                        room_with_alex_id = result["affectedElementId"]
                        break
                add_user_output.value = f"<h2>User created: ID-{created_user_id}</h2><h2>Room with Alex: ID-{room_with_alex_id}</h2>"
                user = simulator_obj.mammut_api.get_user(created_user_id)
                room_with_alex = simulator_obj.mammut_api.get_room(room_with_alex_id)
                add_new_user(
                    simulator_obj,
                    user,
                    users_filename,
                    props_and_values_dic["user-type"],
                )
                user_email = props_and_values_dic["main-email"]
                add_new_room(
                    simulator_obj,
                    room_with_alex,
                    rooms_filename,
                    "private",
                    f"_{user_email}",
                )
            else:
                add_user_output.value = "<h2>Error creating user.</h2>"

    add_user_property_button.on_click(add_user_custom_property_button_clicked)
    add_user_button = widgets.Button(
        description="Create user",
        button_style="primary",
        layout=Layout(width="225px", height="100%"),
    )
    add_user_button.on_click(create_user_button_clicked)
    create_user_box = widgets.VBox(
        [
            user_custom_properties_box,
            add_user_property_button,
            add_user_button,
            add_user_output,
        ],
        layout=Layout(width="100%", align_items="center"),
    )

    room_custom_properties_box = widgets.VBox(
        [
            widgets.HBox(
                [
                    widgets.Text(value="room-type", layout=Layout(width="50%")),
                    widgets.Text(value="group", layout=Layout(width="50%")),
                ]
            )
        ]
    )
    room_created_by_user_box = widgets.IntText(
        value=1234, description="Creator ID: ", style={"description_width": "initial"}
    )
    room_add_property_button = widgets.Button(
        description="+",
        button_style="primary",
        layout=Layout(width="35px", height="100%",),
        style={"button_color": "green"},
    )
    create_room_output = widgets.HTML("")

    def add_room_custom_property_button_clicked(b):
        new_property_name = widgets.Text(
            value="Property name", layout=Layout(width="50%")
        )
        new_property_value = widgets.Text(
            value="Property value", layout=Layout(width="50%")
        )
        room_custom_properties_box.children = (
            room_custom_properties_box.children
            + tuple([widgets.HBox([new_property_name, new_property_value])])
        )

    def create_room_button_clicked(b):
        props_and_values = room_custom_properties_box.children
        props_and_values_dict = {}
        for index in range(0, len(props_and_values)):
            if props_and_values[index].children[0].value == "has@user":
                props_and_values_dict[props_and_values[index].children[0].value] = {
                    "id": int(props_and_values[index].children[1].value)
                }
            else:
                props_and_values_dict[props_and_values[index].children[0].value] = (
                    props_and_values[index].children[1].value
                )
        create_room_path = simulator_obj.mammut_api.post_room_path.replace(
            "{userId}", str(room_created_by_user_box.value)
        )
        res = simulator_obj.mammut_api.post_request(
            create_room_path, props_and_values_dict
        )
        if res.status_code == 200:
            res_json = res.json()
            created_room_id = -1
            for result in res_json["taskResult"]:
                if result["affectedElementName"] == "room":
                    created_room_id = result["affectedElementId"]
                    break
            create_room_output.value = f"<h2>Room created: ID-{created_room_id}</h2>"
            room = simulator_obj.mammut_api.get_room(created_room_id)
            add_new_room(
                simulator_obj, room, rooms_filename, props_and_values_dict["room-type"]
            )
        else:
            create_room_output.value = "<h2>Error creating room.</h2>"

    room_add_property_button.on_click(add_room_custom_property_button_clicked)
    create_room_button = widgets.Button(
        description="Create Room",
        button_style="primary",
        layout=Layout(width="225px", height="100%"),
    )
    create_room_button.on_click(create_room_button_clicked)
    create_room_box = widgets.VBox(
        [
            room_custom_properties_box,
            room_add_property_button,
            room_created_by_user_box,
            create_room_button,
            create_room_output,
        ],
        layout=Layout(width="100%", align_items="center"),
    )

    create_entities_tab = widgets.Tab(
        children=[create_bot_box, create_user_box, create_room_box]
    )
    create_entities_tab.set_title(0, "Crear nuevo bot")
    create_entities_tab.set_title(1, "Crear nuevo user")
    create_entities_tab.set_title(2, "Crear nuevo room")
    # /Create entities #

    # load users & rooms#
    load_user_and_rooms_spreadsheet_id = widgets.Text(
        value=users_rooms_spreadsheet_id,
        description="Id Archivo:",
        layout=Layout(width="90%"),
        style={"description_width": "initial"},
    )
    users_sheetname = widgets.Text(
        value=users_sheet_name,
        description="Nombre del sheet de usuarios:",
        layout=Layout(width="80%", height="50px", pading="10px 15px 10px 8px"),
    )
    rooms_sheetname = widgets.Text(
        value=rooms_sheet_name,
        description="Nombre del sheet de chats:",
        layout=Layout(width="80%", height="50px", pading="10px 15px 10px 8px"),
    )
    load_users_btn = widgets.Button(
        description="Cargar Usuarios",
        button_style="primary",
        layout=Layout(width="225px", height="100%"),
    )
    load_rooms_btn = widgets.Button(
        description="Cargar Chats",
        button_style="primary",
        layout=Layout(width="225px", height="100%"),
    )
    users_output_html = widgets.HTML(value="")
    rooms_output_html = widgets.HTML(value="")

    def load_users_btn_clicked(b):
        mammut_api = Request(api_url)
        sheet_names = [s.strip() for s in users_sheet_name.value.split(",")]
        for sn in sheet_names:
            user_loader = UsersLoader(
                spreadsheet_id=load_user_and_rooms_spreadsheet_id.value,
                sheet_name=sn,
                mammut_api=mammut_api,
            )
            user_loader.load_users()

    def load_rooms_btn_clicked(b):
        mammut_api = Request(api_url)
        sheet_names = [s.strip() for s in rooms_sheet_name.value.split(",")]
        for sn in sheet_names:
            room_creator = RoomsCreator(
                simulator_obj.current_user,
                load_user_and_rooms_spreadsheet_id.value,
                mammut_api,
            )
            room_creator.activate(sn)

    load_users_btn.on_click(load_users_btn_clicked)
    load_rooms_btn.on_click(load_rooms_btn_clicked)

    load_users_rooms_box = widgets.VBox(
        [
            load_user_and_rooms_spreadsheet_id,
            widgets.HBox([users_sheetname, load_users_btn]),
            widgets.HBox([rooms_sheetname, load_rooms_btn]),
            users_output_html,
            rooms_output_html,
        ]
    )
    # /Cargar usuarios y rooms #

    # Cargar videos #
    video_url_textbox = widgets.Text(
        value="", description="Url:", layout=Layout(width="100%", height="50px")
    )
    video_name_textbox = widgets.Text(
        value="", description="Nombre:", layout=Layout(width="100%", height="50px")
    )
    save_video_btn = widgets.Button(
        description="Guardar video",
        button_style="primary",
        layout=Layout(width="225px", height="100%"),
    )

    def save_video_button_clicked(b):
        if video_name_textbox.value != "" and video_url_textbox.value != "":
            post_result = simulator_obj.mammut_api.post_video(
                video_name_textbox.value,
                video_url_textbox.value,
                simulator_obj.current_user.id,
            )
        else:
            print("Complete los campos")
        video_url_textbox.value = ""
        video_name_textbox.value = ""

    save_video_btn.on_click(save_video_button_clicked)
    register_video_box = widgets.VBox(
        [video_url_textbox, video_name_textbox, save_video_btn]
    )
    # /Cargar videos #

    # Cargar Calendario #
    style = {"description_width": "initial"}
    calendar_config_layout = Layout(
        width="80%", height="50px", pading="10px 15px 10px 8px"
    )

    calendar_title_textbox = widgets.Text(
        value="", description="Nombre:", layout=calendar_config_layout, style=style
    )

    calendar_supervisor_email_textbox = widgets.Text(
        value="",
        description="Supervisor User email:",
        layout=calendar_config_layout,
        style=style,
    )
    places_textboxes = widgets.VBox([])

    def add_places_textbox(index):
        posible_places_textbox = widgets.Text(
            value="",
            description="Lugar " + str(index + 1) + ":",
            layout=calendar_config_layout,
            style=style,
        )
        places_textboxes.children = list(places_textboxes.children) + [
            posible_places_textbox
        ]

    def add_place_button_clicked(b):
        add_places_textbox(len(places_textboxes.children))

    add_places_textbox(len(places_textboxes.children))
    add_place_button = widgets.Button(
        description="Agregar Lugar",
        button_style="primary",
        layout=Layout(width="225px", height="100%", margin="10px 15px 10px 8px"),
    )
    add_place_button.on_click(add_place_button_clicked)
    posibles_places_format_dict = dict()
    for i in PosiblePlacesFormat:
        posibles_places_format_dict[i.name] = i.value
    posibles_places_format = widgets.Dropdown(
        options=posibles_places_format_dict,
        value=0,
        layout=calendar_config_layout,
        description="Formato Campo Lugares:",
        style=style,
    )

    country_code_dict = dict()
    for i in CountryCodes:
        country_code_dict[i.name + "(" + i.value + ")"] = i.value
    country_code_selector = widgets.Dropdown(
        options=country_code_dict,
        value=CountryCodes.US.value,
        description="Coding de Pais:",
        layout=calendar_config_layout,
        style=style,
    )

    languages_options = dict()
    for i in RegionalSettingsType:
        languages_options[i.name] = i.value

    languages_box = widgets.VBox([])

    def add_language_to_box(index):
        language_dropdown = widgets.Dropdown(
            options=languages_options,
            value="es",
            description="Idioma " + str(index + 1) + ":",
            layout=calendar_config_layout,
            style=style,
        )
        languages_box.children = list(languages_box.children) + [language_dropdown]

    add_language_to_box(len(languages_box.children))
    add_language_button = widgets.Button(
        description="Agregar Idioma",
        button_style="primary",
        layout=Layout(width="225px", height="100%", margin="10px 15px 10px 8px"),
    )

    def add_language_button_clicked(b):
        add_language_to_box(len(languages_box.children))

    add_language_button.on_click(add_language_button_clicked)

    ## CUSTOM FIELDS SUBSECTION ##
    custom_fields_box = widgets.VBox([])

    def add_custom_fields_section(index):
        custom_fields_section_title = widgets.HTML(
            value="<b>Campos Adicionales " + str(index + 1) + "</b>"
        )
        custom_data_name = widgets.Text(
            value="",
            description="Nombre del Campo:",
            layout=calendar_config_layout,
            style=style,
        )

        custom_data_values_textboxes = widgets.VBox([])

        def add_custom_data_values_textboxes(index):
            custom_data_value = widgets.Text(
                value="",
                description="Valor del Campo " + str(index + 1) + ":",
                layout=calendar_config_layout,
                style=style,
            )
            custom_data_values_textboxes.children = list(
                custom_data_values_textboxes.children
            ) + [custom_data_value]

        add_custom_data_values_textboxes(len(custom_data_values_textboxes.children))
        add_custom_data_values_button = widgets.Button(
            description="Agregar Valor",
            button_style="primary",
            layout=Layout(width="225px", height="100%", margin="10px 15px 10px 8px"),
        )

        def add_custom_data_values_button_clicked(b):
            add_custom_data_values_textboxes(len(custom_data_values_textboxes.children))

        add_custom_data_values_button.on_click(add_custom_data_values_button_clicked)

        def add_videos_selector():
            response = simulator_obj.mammut_api.get_videos(
                simulator_obj.current_user.id
            )
            videos_dict = dict()
            print(response)
            for i in response:
                videos_dict[i["title"]] = i["id"]
            videos_dropdown = widgets.Dropdown(
                options=videos_dict,
                value=response[0]["id"],
                description="Videos Disponibles:",
                layout=calendar_config_layout,
                style=style,
            )
            if (
                len(custom_data_template_box.children) <= 6
            ):  # TODO:como soluciono esto?? parece que se activa dos veces el callback
                custom_data_template_box.children = list(
                    custom_data_template_box.children
                ) + [videos_dropdown]

        custom_data_format = widgets.Dropdown(
            options=posibles_places_format_dict,
            value=0,
            description="Formato del Campo:",
            layout=calendar_config_layout,
            style=style,
        )

        def custom_data_format_change(b):
            if b["new"] == PosiblePlacesFormat.video.value:
                add_videos_selector()

        custom_data_format.observe(custom_data_format_change)

        mandatory_widget = widgets.Checkbox(
            value=False, description="Requerido", disabled=False
        )

        custom_data_template_box = widgets.VBox(
            [
                custom_fields_section_title,
                custom_data_name,
                custom_data_values_textboxes,
                add_custom_data_values_button,
                custom_data_format,
                mandatory_widget,
            ],
            layout=Layout(
                display="flex",
                flex_flow="column",
                border="solid 1px",
                align_items="stretch",
                width="100%",
                pading="10px 15px 10px 8px",
            ),
        )
        custom_fields_box.children = list(custom_fields_box.children) + [
            custom_data_template_box
        ]

    add_custom_fields_section(len(custom_fields_box.children))
    add_custom_section_button = widgets.Button(
        description="Agregar seccion de Campos Adicionales",
        button_style="primary",
        layout=Layout(width="225px", height="100%", margin="10px 15px 10px 8px"),
    )

    def add_custom_section_button_clicked(b):
        add_custom_fields_section(len(custom_fields_box.children))

    add_custom_section_button.on_click(add_custom_section_button_clicked)

    available_reminder_varibales = widgets.HTML(
        value="&lt;date&gt;&lt;arrive&gt;&lt;place&gt;&lt;language&gt;",
        description="Variables disponibles: ",
        style={"description_width": "initial"},
    )
    reminder_text_templates_box = widgets.VBox(
        [available_reminder_varibales],
        layout=Layout(
            display="flex",
            flex_flow="column",
            border="solid 1px",
            align_items="stretch",
            width="100%",
            pading="10px 15px 10px 8px",
        ),
    )

    def add_reminder_text_template(index=0):
        reminder_text_area = widgets.Textarea(
            value="",
            placeholder="Mensaje Recordatorio",
            description="Texto Recordatorio " + str(index + 1) + ":",
            disabled=False,
            layout=calendar_config_layout,
        )
        reminder_text_lang_dropdown = widgets.Dropdown(
            options=languages_options,
            value="es",
            description="Idioma Recordatorio:",
            layout=calendar_config_layout,
            style=style,
        )
        reminder_text_templates_elem = widgets.VBox(
            [reminder_text_area, reminder_text_lang_dropdown]
        )
        reminder_text_templates_box.children = list(
            reminder_text_templates_box.children
        ) + [reminder_text_templates_elem]

    add_reminder_text_template(len(reminder_text_templates_box.children))
    add_reminder_button = widgets.Button(
        description="Agrgar Recordatorio",
        button_style="primary",
        layout=Layout(width="225px", height="100%", margin="10px 15px 10px 8px"),
    )

    def add_reminder_button_clicked(b):
        add_reminder_text_template(len(reminder_text_templates_box.children))

    add_reminder_button.on_click(add_reminder_button_clicked)

    save_calendar_button = widgets.Button(
        description="Guardar Calendario",
        button_style="primary",
        layout=Layout(width="225px", height="100%", margin="10px 15px 10px 8px"),
    )

    def save_calendar_button_clicked(b):
        #  calendar = Calendar(custom_data_name.value)
        title = calendar_title_textbox.value
        supervisor_user_by_mail = simulator_obj.mammut_api.get_user_by_mail(
            calendar_supervisor_email_textbox.value
        )
        if supervisor_user_by_mail is not None:
            admin_user_id_value = supervisor_user_by_mail.id
        else:
            print(
                "error, no hay supervisor para el email",
                calendar_supervisor_email_textbox.value,
            )
        posibles_places_values = [i.value for i in places_textboxes.children]
        posibles_places_format_value = posibles_places_format.value
        country_code_selector_value = country_code_selector.value
        regional_setings_values = [i.value for i in languages_box.children]
        custom_sections_values = dict()
        children_list = [i for i in custom_fields_box.children]
        elems = [i for i in children_list]
        a = []
        for i in children_list:
            a.append(i)
        for custom_section in list(children_list):
            custom_data_name_value = custom_section.children[1].value
            custom_data_values_textboxes_values = [
                i.value for i in custom_section.children[2].children
            ]
            custom_data_format_value = custom_section.children[4].value
            if custom_data_format_value == PosiblePlacesFormat.video.value:
                custom_data_values_textboxes_values[0] = (
                    custom_data_values_textboxes_values[0]
                    + "/video?id="
                    + str(custom_section.children[6].value)
                )
            mandatory_widget_value = custom_section.children[5].value
            custom_fields_values = CalendarCustomValues(
                name=custom_data_name_value,
                value=custom_data_values_textboxes_values,
                value_type=custom_data_format_value,
                mandatory=mandatory_widget_value,
            )
            custom_sections_values[
                custom_data_name_value
            ] = custom_fields_values.to_json()[custom_data_name_value]
        reminders = {}
        for i, vbox in enumerate(list(reminder_text_templates_box.children)[1:]):
            reminders[vbox.children[1].value] = vbox.children[0].value
        calendar = Calendar(
            user_id=admin_user_id_value,
            mammut_user=simulator_obj.current_user,
            title=title,
            possible_places=posibles_places_values,
            possible_places_format=posibles_places_format_value,
            possible_regional_settings=regional_setings_values,
            custom_fields=custom_sections_values,
            reminder_text_templates=reminders,
            country_code=country_code_selector_value,
        )

        response = simulator_obj.mammut_api.post_calendar(calendar)
        print("response", response)
        if response["status"] != "Failed":
            print("reponse\n", response)
        else:
            print("Error creating calendar")

    save_calendar_button.on_click(save_calendar_button_clicked)
    register_calendar_event_content_box = widgets.VBox(
        [
            calendar_title_textbox,
            calendar_supervisor_email_textbox,
            places_textboxes,
            add_place_button,
            posibles_places_format,
            country_code_selector,
            languages_box,
            add_language_button,
            custom_fields_box,
            add_custom_section_button,
            reminder_text_templates_box,
            add_reminder_button,
            save_calendar_button,
        ]
    )
    # /Cargar Calendario #

    return tuple(
        [
            select_mammut_box,
            create_entities_tab,
            load_users_rooms_box,
            register_video_box,
            register_calendar_event_content_box,
        ]
    )
