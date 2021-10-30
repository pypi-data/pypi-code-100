from __future__ import annotations
from typing import Final, TypeVar

E = TypeVar('E', bound="Embed")
class _EmptyEmbed:
    def __bool__(self) -> bool:
        return False
    def __repr__(self) -> str:
        return "Embed.Empty"
    def __len__(self) -> int:
        return 0

EmptyEmbed: Final = _EmptyEmbed()

class Embed:
    def __init__(self, title: str = None, description: str = None, color = None):
        self.title = None if title is None else title
        self.description = None if description is None else description
        self.color = 0x2f3136 if color is None else color
        self.fields = []
        self.footer = {}
        self.author = {}
        self.author = {}

    def add_field(self, name: str = None, value: str = None, inline: bool = False) -> E:
        """Adds a field object to the Embed"""
        if name is None:
            raise ValueError("Embed.field name expected string, received NoneType.")
        if value is None:
            raise ValueError("Embed.field value expected string, received NoneType.")
        if name is None and value is None:
            raise ValueError("Embed.field object cannot be empty.")

        self.fields.append({"name": name, "value": value, "inline": inline})

    def set_footer(self, text: str = None, icon_url: str = None) -> E:
        if text is None and icon_url is None:
            raise ValueError("Embed.footer object cannot be empty.")
        self.footer['text'] = text
        if icon_url is not None:
            self.footer['icon_url'] = icon_url

    def set_author(self, name: str = None, url: str = None, icon_url: str = None) -> E:
        if name is None and url is None and icon_url is None:
            raise ValueError("Embed.author object cannot be empty.")
        
        if name is not None:
            self.author['name'] = name
        if url is not None:
            self.author['url'] = url
        if icon_url is not None:
            self.author['icon_url'] = icon_url

    def build(self) -> dict:
        built = {}
        if self.title is not None:
            built['title'] = self.title
        if self.description is not None:
            built['description'] = self.description
        built['color'] = self.color

        if len(self.fields) > 0:
            built['fields'] = self.fields
        
        if len(self.footer.keys()) > 0:
            built['footer'] = self.footer
        if len(self.author.keys()) > 0:
            built['author'] = self.author

        return built