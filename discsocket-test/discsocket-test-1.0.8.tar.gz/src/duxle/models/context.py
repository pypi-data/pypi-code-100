from .components import ActionRow, Button, SelectMenu, SelectMenuOption
from .user import User
from .message import Message


class Context:
    def __init__(self, socket, data):
        injected = data.get('injected', None)
        if injected:
            self.injected = injected

        self.socket = socket
        self.raw = data
        self.command = self.raw['data'].get('name', None)
        self.command_id = self.raw['data'].get('id', None)
        self.channel_id = self.raw.get('channel_id', None)
        self.id = self.raw.get('id', None)
        self.token = self.raw.get('token', None)
        self.type = self.raw.get('type', None)
        self.callback_url = f"https://discord.com/api/v8/interactions/{self.id}/{self.token}/callback"

    async def callback(self, content: str = '', embeds: list = [], components: list = [], mentions: list = [], ephemeral: bool= False):
        message = {
            "type": 4,
            "data": {
                "content": content,
                "embeds": embeds,
                "allowed_mentions": mentions,
            }
        }
        if ephemeral and len(components) > 0:
            raise ValueError("Ephemeral messages cannot be sent with components")

        if len(components) > 0:
            built_action_rows = []
            for action_row in components:
                if isinstance(action_row, ActionRow):
                    built_action_rows.append(action_row.build())
        
            fully_built = []
            for bar in built_action_rows:
                new_ar = {"type": 1, "components": []}
                for component in bar['components']:
                    if isinstance(component, Button):
                        new_ar['components'].append(component.build())
                    elif isinstance(component, SelectMenu):
                        select_options = []
                        built_select = component.build()
                        for option in built_select['options']:
                            if isinstance(option, SelectMenuOption):
                                select_options.append(option.build())
                        new_ar['components'].append({"type": 3, "custom_id": built_select['custom_id'], "options": select_options})
                fully_built.append(new_ar)
            message['data']['components'] = fully_built

        if ephemeral:
            message['data']['flags'] = 64

        async with self.socket.session.post(self.callback_url, json=message, headers=self.socket.headers) as maybe_send:
            self.message = Message(self.socket, await (await self.socket.session.get(f"https://discord.com/api/v8/webhooks/{self.raw['application_id']}/{self.token}/messages/@original", headers=self.socket.headers)).json())
            if maybe_send.status != 204:
                print(await maybe_send.json())

class SelectMenuContext:
    def __init__(self, socket, data):
        self.socket = socket
        self.raw = data
        self.values = self.raw['data']['values']
        self.used = User(self.raw['member']['user'])
        self.invoked = User(data['message']['interaction']['user'])
        self.callback_url = f"https://discord.com/api/v8/interactions/{self.raw['id']}/{self.raw['token']}/callback"

    async def callback(self, content: str = '', embeds: list = [], components: list = [], mentions: list = [], ephemeral: bool= False):
        message = {
            "type": 4,
            "data": {
                "content": content,
                "embeds": embeds,
                "allowed_mentions": mentions,
            }
        }
        if ephemeral and len(components) > 0:
            raise ValueError("Ephemeral messages cannot be sent with components")

        if len(components) > 0:
            built_action_rows = []
            for action_row in components:
                if isinstance(action_row, ActionRow):
                    built_action_rows.append(action_row.build())
        
            fully_built = []
            for bar in built_action_rows:
                new_ar = {"type": 1, "components": []}
                for component in bar['components']:
                    if isinstance(component, Button):
                        new_ar['components'].append(component.build())
                    elif isinstance(component, SelectMenu):
                        select_options = []
                        built_select = component.build()
                        for option in built_select['options']:
                            if isinstance(option, SelectMenuOption):
                                select_options.append(option.build())
                        new_ar['components'].append({"type": 3, "custom_id": built_select['custom_id'], "options": select_options})
                fully_built.append(new_ar)
            message['data']['components'] = fully_built

        if ephemeral:
            message['data']['flags'] = 64

        async with self.socket.session.post(self.callback_url, json=message, headers=self.socket.headers) as maybe_send:
            self.message = Message(self.socket, await (await self.socket.session.get(f"https://discord.com/api/v8/webhooks/{self.raw['application_id']}/{self.raw['token']}/messages/@original", headers=self.socket.headers)).json())
            if maybe_send.status != 204:
                print(await maybe_send.json())

class ButtonContext:
    def __init__(self, socket, data):
        self.socket = socket
        self.raw = data
        self.ucid = self.raw['data']['custom_id']
        self.invoked = User(data['message']['interaction']['user'])
        self.used = User(data['member']['user'])
        self.callback_url = f"https://discord.com/api/v8/interactions/{self.raw['id']}/{self.raw['token']}/callback"

    async def callback(self, content: str = '', embeds: list = [], components: list = [], mentions: list = [], ephemeral: bool= False):
        message = {
            "type": 4,
            "data": {
                "content": content,
                "embeds": embeds,
                "allowed_mentions": mentions,
            }
        }
        if ephemeral and len(components) > 0:
            raise ValueError("Ephemeral messages cannot be sent with components")

        if len(components) > 0:
            built_action_rows = []
            for action_row in components:
                if isinstance(action_row, ActionRow):
                    built_action_rows.append(action_row.build())
        
            fully_built = []
            for bar in built_action_rows:
                new_ar = {"type": 1, "components": []}
                for component in bar['components']:
                    if isinstance(component, Button):
                        new_ar['components'].append(component.build())
                    elif isinstance(component, SelectMenu):
                        select_options = []
                        built_select = component.build()
                        for option in built_select['options']:
                            if isinstance(option, SelectMenuOption):
                                select_options.append(option.build())
                        new_ar['components'].append({"type": 3, "custom_id": built_select['custom_id'], "options": select_options})
                fully_built.append(new_ar)
            message['data']['components'] = fully_built

        if ephemeral:
            message['data']['flags'] = 64

        async with self.socket.session.post(self.callback_url, json=message, headers=self.socket.headers) as maybe_send:
            self.message = Message(self.socket, await (await self.socket.session.get(f"https://discord.com/api/v8/webhooks/{self.raw['application_id']}/{self.raw['token']}/messages/@original", headers=self.socket.headers)).json())
            if maybe_send.status != 204:
                print(await maybe_send.json())
