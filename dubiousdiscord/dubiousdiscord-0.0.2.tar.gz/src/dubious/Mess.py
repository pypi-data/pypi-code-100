
from typing import Optional, Union
import dubious.objects as data

class Embed:
    def __init__(self, *, title: str, description: str):
        self.title = title
        self.description = description
    
    def asJson(self) -> dict:
        pass

class Emoji:
    def __init__(self, emoji: Union[str, int]):
        self.emoji = emoji
    
    def asJson(self) -> dict:
        j = {}
        if isinstance(self.emoji, str): j["name"] = self.emoji
        if isinstance(self.emoji, int): j["id"] = self.emoji
        return j

class Component:
    def __init__(self, typ: int):
        self.type = typ

    def asJson(self) -> dict:
        return {
            "type": self.type
        }

class Row(Component):
    def __init__(self, components: list[Component]):
        super().__init__(1)
        self.components = components
    
    def add(self, component: Component):
        self.components.append(component)
    
    def asJson(self) -> dict:
        j = super().asJson()
        if self.components: j["components"] = [component.asJson() for component in self.components]
        return j

class Button(Component):
    def __init__(self, customID: Optional[str]=None, label: Optional[str]=None, *, disabled: Optional[bool]=False, style: Optional[int]=None, emoji: Emoji | str | None=None, url: Optional[str]=None):
        super().__init__(2)
        self.label = label
        self.customID = customID
        self.disabled = disabled
        self.style = style
        self.emoji = emoji if isinstance(emoji, Emoji) and emoji else Emoji(emoji)
        self.url = url
    
    def asJson(self) -> dict:
        j = super().asJson()
        j["style"] = self.style if self.style else 1
        j["disabled"] = self.disabled
        if self.label: j["label"] = self.label
        if self.customID: j["custom_id"] = self.customID
        if self.emoji: j["emoji"] = self.emoji.asJson()
        if self.url: j["url"] = self.url
        return j

class DropdownOption:
    def __init__(self, label: str, *, value: Optional[str]=None, description: Optional[str]=None, emoji: Optional[data.Emoji]=None, default: bool=False):
        self.label = label
        self.value = value if value else label
        self.description = description
        self.emoji = emoji
        self.default = default
    
    def asJson(self) -> dict:
        j = {
            "label": self.label,
            "value": self.value
        }
        if self.description: j["description"] = self.description
        if self.emoji: j["emoji"] = self.emoji
        if self.default: j["default"] = self.default
        return j

class Dropdown(Component):
    def __init__(self, options: list[DropdownOption], *, placeholder: Optional[str]=None, min: Optional[int]=None, max: Optional[int]=None):
        super().__init__(3)
        self.options = options
        self.placeholder = placeholder
        self.min = min
        self.max = max
    
    def asJson(self) -> dict:
        j = super().asJson()
        j["options"] = [option.asJson() for option in self.options]
        if self.placeholder: j["placeholder"] = self.placeholder
        if self.min: j["min_values"] = self.min
        if self.max: j["max_values"] = self.max
        return j

class Mess:
    def __init__(self, content: Optional[str]=None, *, tts: bool=False, file: Optional[bytes]=None, embeds: Optional[list[Embed]]=None, reference: Optional[int]=None, components: Optional[list[Component]]=None):
        self.content = content
        self.tts = tts
        self.embeds = embeds if embeds else []
        self.reference = reference
        self.components = components if components else []

    def asJson(self) -> dict:
        j = {
            "tts": self.tts
        }
        if self.content: j["content"] = self.content
        if self.embeds: j["embeds"] = [embed.asJson() for embed in self.embeds]
        if self.reference: j["reference"] = {"message_id": self.reference}
        if self.components: j["components"] = [component.asJson() for component in self.components]
        return j