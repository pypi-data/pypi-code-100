from typing import Optional

from camel_model.camel_model import CamelModel


class ComponentAttribute(CamelModel):
    name: str
    value: Optional[str]
    observations: Optional[str]
