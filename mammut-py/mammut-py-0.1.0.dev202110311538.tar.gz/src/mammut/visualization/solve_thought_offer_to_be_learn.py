# coding=utf-8
from mammut.common.simulator_utilities import *
from ipywidgets import *


def get_solve_totbl_box():
    form_values = dict()
    responseLayout = Layout(width="100%", height="50px")
    responseTextBox = widgets.Text(
        value="", placeholder="Respuesta", description="Nombre:", layout=responseLayout
    )
    form_values["responseTextBox"] = responseTextBox

    solveTotblButton = widgets.Button(
        description="Crear Nuevo ...", button_style="primary"
    )

    solveTotblBox = widgets.VBox([responseTextBox, solveTotblButton])
    return solveTotblBox, solveTotblButton, form_values
