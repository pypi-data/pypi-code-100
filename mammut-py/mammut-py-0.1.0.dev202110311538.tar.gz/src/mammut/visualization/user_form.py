# coding=utf-8
from mammut.common.mammut_api import *
from mammut.common.simulator_utilities import *
from ipywidgets import *
from datetime import datetime

### User Layout ###
def get_user_form():
    form_values = dict()
    personUserDropdown = widgets.Dropdown(
        description="Usuario:", disabled=False, button_style=""
    )
    form_values["personUserDropdown"] = personUserDropdown
    supervisorUserDropdown = widgets.Dropdown(
        description="Supervisor:", disabled=False, button_style=""
    )
    form_values["supervisorUserDropdown"] = supervisorUserDropdown

    languages = {}
    languages["Español"] = "es"
    languages["Ingles"] = "en"

    newMammutLayout = Layout(width="100%", height="50px")
    form_values["newMammutLayout"] = newMammutLayout
    nameTextBox = widgets.Text(
        value="",
        placeholder="Mammut Restaurant",
        description="Nombre:",
        layout=newMammutLayout,
    )
    form_values["nameTextBox"] = nameTextBox
    emailTextBox = widgets.Text(
        value="",
        placeholder="restaurant@mammut.io",
        description="Email:",
        layout=newMammutLayout,
    )
    form_values["emailTextBox"] = emailTextBox
    birthDateBox = widgets.Text(
        value="",
        placeholder="dd/mm/aaaa",
        description="Fecha de nacimiento:",
        layout=newMammutLayout,
    )
    form_values["birthDateBox"] = birthDateBox
    phoneTextBox = widgets.Text(
        value="",
        placeholder="+582129769097",
        description="Telefono:",
        layout=newMammutLayout,
    )
    form_values["phoneTextBox"] = phoneTextBox
    facebookIdTextBox = widgets.Text(
        value="",
        placeholder="301598836881228",
        description="Facebook Id:",
        layout=newMammutLayout,
    )
    form_values["facebookIdTextBox"] = facebookIdTextBox
    fbAccessTokenTextBox = widgets.Text(
        value="",
        placeholder="EAAZAbcJHTWr4BACnPewhF08OGZBZBZCOKyBn3rK9PDFveMJ4s1xHo0JXdXNgpKXveYOd3hj0spLEwJk0cAtt2Dt6Wl4ukaTjoRQCMvOS0hxFUSbNJp5T738VrCPN7q8XWp3QZBreGhyj8nEeLsZAhfxuJ9vZB9fGyl2kkpHPtzHiAZDZD",
        description="FB Page Access Token:",
        layout=newMammutLayout,
    )
    form_values["fbAccessTokenTextBox"] = fbAccessTokenTextBox
    langDropdown = widgets.Dropdown(
        options=languages, value="es", description="Idioma:"
    )
    form_values["langDropdown"] = langDropdown
    user_types = {user_type.value: user_type for user_type in UserType}
    userType = widgets.Dropdown(
        options=user_types, value=UserType.person, description="User Type:"
    )
    form_values["userType"] = userType
    lastname_style = {"description_width": "initial"}
    lastNameTextBox = widgets.Text(
        value="",
        placeholder="appellido",
        description="Apellido:",
        style=lastname_style,
        layout=newMammutLayout,
    )
    form_values["lastNameTextBox"] = lastNameTextBox

    newMammutButton = widgets.Button(
        description="Crear Nuevo ...", button_style="primary"
    )

    userMammutLayout = Layout(width="50%", height="80px", visibility="visible")

    userBox = widgets.VBox(
        [
            widgets.HBox(
                [
                    widgets.VBox(
                        [
                            nameTextBox,
                            lastNameTextBox,
                            emailTextBox,
                            birthDateBox,
                            langDropdown,
                        ],
                        layout=Layout(width="100%"),
                    ),
                    widgets.VBox(
                        [
                            phoneTextBox,
                            facebookIdTextBox,
                            fbAccessTokenTextBox,
                            userType,
                        ],
                        layout=Layout(width="100%"),
                    ),
                ],
                layout=Layout(width="100%"),
            ),
            newMammutButton,
        ]
    )

    selectUserButton = widgets.Button(description="Seleccionar", button_style="primary")
    selectSupervisorButton = widgets.Button(
        description="Seleccionar", button_style="primary"
    )

    selectUserBox = widgets.HBox([personUserDropdown, selectUserButton])
    selectSupervisorBox = widgets.HBox([supervisorUserDropdown, selectSupervisorButton])

    user_tab = widgets.Tab(children=[selectUserBox, selectSupervisorBox, userBox])
    user_tab.set_title(0, "Seleccionar Persona Trabajando")
    user_tab.set_title(1, "Seleccionar supervisor")
    user_tab.set_title(2, "Crear Nuevo  Persona...")

    return (
        selectUserButton,
        selectSupervisorButton,
        newMammutButton,
        user_tab,
        form_values,
    )
