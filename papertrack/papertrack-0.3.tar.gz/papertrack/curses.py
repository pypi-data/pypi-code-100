import easy_widgets
from easy_widgets.Menu import Menu

def _curses_ask(creator):
    easy_widgets.Application.init()
    res_value = []
    def callback(value):
        res_value.append(value)
        easy_widgets.Application.exit()
    creator(callback)
    easy_widgets.Application.run()
    return res_value[0]


def curses_ask_str(prompt):
    return _curses_ask(lambda fn: easy_widgets.TextInput(prompt, lambda value: fn(value)).show())

def curses_ask_menu(prompt, choices):
    def menu_creator(fn):
            menu = easy_widgets.Menu(prompt)
            for choice in choices:
                menu.addOption(choice, lambda btn, params: fn(params[0]), params=[choice])
            menu.show()
    return _curses_ask(menu_creator)

def curses_ask_fn(name, param_type, description, choices: list) -> str:
    value = None
    while value is None:
        if choices and len(choices) > 0:
            value = curses_ask_menu("%s - %s" % (name, description), choices)
        else:
            if param_type == "list":
                resulting_list = [] 
                item = None
                while item != "Finish":
                    item = curses_ask_menu("%s -%s" % (name, description), [
                        "New item",
                        "Finish", 
                        *resulting_list
                    ])
                    if item != "Finish":
                        resulting_list.append(curses_ask_str("Enter value")) 
                value = resulting_list
            else:
                value = curses_ask_str("%s - %s" % (name, description))
    return value
