from . import utils

class Container:
    """
    Container class to hold commands, events, and component event listeners.
    """

    def __init__(self):
        self.commands = {}
        self.events = {}
        self.components = {}
        self.user_commands = {}
        self.message_commands = {}

    def add_command(self, command):
        """
        Add a command to the container.
        """
        if command.type == utils.SLASH:
            self.commands[command.name] = command.func
        elif command.type == utils.USER:
            self.user_commands[command.name] = command.func
        elif command.type == utils.MESSAGE:
            self.message_commands[command.name] = command.func

    def add_event(self, event):
        """
        Add an event to the container.
        """
        try:
            self.events[event.name].append(event.func)
        except KeyError:
            self.events[event.name] = [event.func]

    def add_component(self, component):
        """
        Add a component to the container.
        """
        self.components[component.ucid] = (component.func, component.timeout, component.parent_context)