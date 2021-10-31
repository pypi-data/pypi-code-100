# coding=utf-8
from mammut.common.simulator_utilities import *
from ipywidgets import *

### Room Layout ###
def get_room_form():
    form_values = dict()
    roomDropdown = widgets.Dropdown(
        description="Room:", disabled=False, button_style=""
    )
    form_values["roomDropdown"] = roomDropdown

    newRoomLayout = Layout(width="100%", height="50px")
    nameTextBox = widgets.Text(
        value="", placeholder="test room", description="Nombre:", layout=newRoomLayout
    )
    form_values["nameTextBox"] = nameTextBox
    roomTypeDropdown = widgets.Dropdown(
        description="Room Type:", disabled=False, button_style=""
    )
    room_type_values_dict = {room_type.value: room_type.value for room_type in RoomType}

    roomTypeDropdown.options = room_type_values_dict
    form_values["roomTypeDropdown"] = roomTypeDropdown

    newRoomButton = widgets.Button(
        description="Crear Nuevo ...", button_style="primary"
    )

    roomBox = widgets.VBox(
        [
            widgets.HBox(
                [
                    widgets.VBox(
                        [nameTextBox, roomTypeDropdown], layout=Layout(width="100%")
                    )
                ],
                layout=Layout(width="100%"),
            ),
            newRoomButton,
        ]
    )

    selectRoomButton = widgets.Button(description="Seleccionar", button_style="primary")

    selectRoomBox = widgets.HBox([roomDropdown, selectRoomButton])

    room_tab = widgets.Tab(children=[selectRoomBox, roomBox])
    room_tab.set_title(0, "Seleccionar Room")
    room_tab.set_title(1, "Crear Nuevo Room...")

    return selectRoomButton, newRoomButton, room_tab, form_values
