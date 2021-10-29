from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State

#clientside callback arguments
clientside_callback_args = (
    """
    function(n) {          
        const local_time_str = new Date().toLocaleTimeString('en-GB');                   
        return local_time_str
    }
    """,
    Output('browser-time', 'children'),
    Input('browser-time-interval', 'n_intervals'),
)

def htmlObj():
    return html.Div(
        children = [
            html.Div(id = "browser-time"),
            dcc.Interval(id = "browser-time-interval")
        ],
        style = {"display": "none"}
    )