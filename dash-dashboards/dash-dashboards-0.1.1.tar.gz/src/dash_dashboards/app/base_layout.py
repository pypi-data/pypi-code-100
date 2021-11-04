from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Union

import dash_bootstrap_components as dbc
from dash.development.base_component import Component

ItemLayoutClass = Union[
    dbc.DropdownMenuItem,
    dbc.NavLink,
    dbc.NavItem,
    dbc.DropdownMenu,
]


class BaseMenuItem(ABC):
    @abstractmethod
    def get_menu_item_layout(self) -> ItemLayoutClass:
        ...  # pragma: no cover

    @property
    @abstractmethod
    def pages(self) -> List["MenuItem"]:
        ...  # pragma: no cover


@dataclass
class MenuItem(BaseMenuItem):
    name: str
    layout: Component
    route: str

    def get_menu_item_layout(self, nested: bool = False) -> ItemLayoutClass:
        el = dbc.DropdownMenuItem if nested else dbc.NavLink
        item = el(
            self.name,
            href=self.route,
        )
        if not nested:
            return dbc.NavItem(item)
        return item

    @property
    def pages(self) -> List["MenuItem"]:
        return [self]


@dataclass
class MenuGroup(BaseMenuItem):
    name: str
    items: List[MenuItem]

    def get_menu_item_layout(self) -> ItemLayoutClass:
        return dbc.DropdownMenu(
            children=[item.get_menu_item_layout(nested=True) for item in self.items],
            nav=True,
            in_navbar=True,
            label=self.name,
        )

    @property
    def pages(self) -> List["MenuItem"]:
        return self.items


Menu = List[BaseMenuItem]
