from typing import Dict, List, Tuple
# %%

import logging
from typing import Callable, Optional, Any

from pydantic import BaseModel, validator, Extra

from .types import LabelType, NodeLabelType, ConditionType
from .normalization import normalize_response, normalize_processing, normalize_transitions, normalize_plot


logger = logging.getLogger(__name__)


Actor = BaseModel
Context = BaseModel


class Node(BaseModel, extra=Extra.forbid):
    transitions: Dict[NodeLabelType, ConditionType] = {}
    response: Optional[Any] = None
    processing: Dict[Any, Callable] = {}
    misc: dict = {}

    _normalize_transitions = validator("transitions", allow_reuse=True)(normalize_transitions)

    def run_response(self, ctx: Context, actor: Actor, *args, **kwargs) -> Context:
        response = normalize_response(self.response)
        return response(ctx, actor, *args, **kwargs)

    def run_processing(self, ctx: Context, actor: Actor, *args, **kwargs) -> Context:
        processing = normalize_processing(self.processing)
        return processing(ctx, actor, *args, **kwargs)


class Plot(BaseModel, extra=Extra.forbid):
    plot: Dict[LabelType, Dict[LabelType, Node]]

    _normalize_plot = validator("plot", allow_reuse=True, pre=True)(normalize_plot)

    def __getitem__(self, key):
        return self.plot[key]

    def get(self, key, value=None):
        return self.plot.get(key, value)

    def keys(self):
        return self.plot.keys()

    def items(self):
        return self.plot.items()

    def values(self):
        return self.plot.values()

    def __iter__(self):
        return self.plot.__iter__()
