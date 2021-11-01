from daipecore.widgets.Widgets import Widgets
from jupyterbundle.server_detector import is_jupyter_server_running
import ipywidgets


class JupyterWidgets(Widgets):
    def __init__(self):
        self.__widgets = dict()

    def add_text(self, name: str, default_value: str = "", label: str = None):
        widget = ipywidgets.Text(default_value, description=label if label is not None else name)
        self.__widgets[name] = widget

        self.__display_widget(widget)

    def add_select(self, name: str, choices: list, default_value: str, label: str = None):
        if None in choices:
            raise Exception("Value None cannot be used as choice, use empty string instead")

        if default_value not in choices:
            raise Exception(f'Default value "{default_value}" not among choices')

        widget = ipywidgets.Dropdown(options=choices, value=default_value, description=label if label is not None else name)
        self.__widgets[name] = widget

        self.__display_widget(widget)

    def add_multiselect(self, name: str, choices: list, default_values: list, label: str = None):
        widget = ipywidgets.SelectMultiple(options=choices, value=default_values, description=label if label is not None else name)
        self.__widgets[name] = widget

        self.__display_widget(widget)

    def remove(self, name: str):
        widget = self.__widgets[name]
        widget.close()
        del self.__widgets[name]

    def remove_all(self):
        for name in list(self.__widgets.keys()):
            self.remove(name)

    def get_value(self, name: str):
        selected_widgets = [widget for _name, widget in self.__widgets.items() if _name == name]

        if selected_widgets == []:
            raise Exception(f'No widget defined for name "{name}"')

        selected_widget = selected_widgets[0]

        if isinstance(selected_widget, ipywidgets.Dropdown) and selected_widget.value not in selected_widget.options:
            choices_str = "', '".join(selected_widget.options)
            raise Exception(f"argument --{name}: invalid choice: '{selected_widget.value}' (choose from '" + choices_str + "')")

        if isinstance(selected_widget, ipywidgets.SelectMultiple):
            return list(selected_widget.value)

        return selected_widget.value

    def _get_widget(self, name):
        if name not in self.__widgets:
            raise Exception(f'No widget defined for name "{name}"')

        return self.__widgets[name]

    def __display_widget(self, widget: object):
        from IPython.display import display

        return display(widget)

    def should_be_resolved(self):
        return is_jupyter_server_running()
