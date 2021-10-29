from dash import html
import dash_bootstrap_components as dbc
import random
import string

#style of navitem
padding = "5px"
def __random__(len = 20):
    return "".join(random.choice(string.ascii_letters) for i in range(20))

#normal button for navbar
def normal(text, id = None, color = "primary", size = None):
    if not id: id = __random__()
    return dbc.NavItem(
        children = [
            html.Div(style = {"width": padding}),
            dbc.Button(text, color = color, id = id, size = size),
            html.Div(style = {"width": padding})
        ],
        style = {"display": "flex", "padding": "0.5rem  0"}
    )

#href button for navbar
def href(text, id = None, href = "/", target = None, color = "primary", size = None):
    if not id: id = __random__()
    return dbc.NavItem(
        children = [
            html.Div(style = {"width": padding}),
            html.A(
                dbc.Button(text, color = color, id = id, size = size),
                href = href,
                target = target,
            ),
            html.Div(style = {"width": padding})
        ],
        style = {"display": "flex", "padding": "0.5rem  0"}
    )