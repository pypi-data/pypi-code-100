import os
import streamlit.components.v1 as components
from streamlit.components.v1.components import CustomComponent
from typing import List

from streamlit_stepper_bar.version import __release__
# , __version__

if __release__:
    absolute_path = os.path.dirname(os.path.abspath(__file__))
    build_path = os.path.join(absolute_path, "frontend/build")
    _component_func = components.declare_component("stepper_bar", path=build_path)
else:
    _component_func = components.declare_component("stepper_bar", url="http://localhost:3000")

def stepper_bar(steps: List[str], default=0, is_completed=False, key=None) -> CustomComponent:
    component_value = _component_func(steps=steps, default=default, is_completed=is_completed, key=key)
    if component_value is None:
        return 0
    return component_value

