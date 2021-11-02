from collections import defaultdict
from dataclasses import dataclass
from itertools import chain
from typing import Dict, List, Optional

import networkx as nx
import pydantic

from classiq_interface.generator.function_call import FunctionCall

IO_MULTI_USE_ERROR_MSG = "Input and output names can only be used once"
IO_NAME_MISMATCH_ERROR_MSG = "Inputs and outputs are not identical"


@dataclass
class Wire:
    start: Optional[pydantic.constr(min_length=1)] = None
    end: Optional[pydantic.constr(min_length=1)] = None


def _parse_call_inputs(function_call: FunctionCall, wires: Dict[str, Wire]) -> None:
    if not function_call.inputs:
        return

    for wire_name in function_call.inputs.values():
        wire = wires[wire_name]

        if wire.end:
            raise ValueError(
                IO_MULTI_USE_ERROR_MSG
                + f". The name {wire_name} is used multiple times."
            )
        wire.end = function_call.name


def _parse_call_outputs(function_call: FunctionCall, wires: Dict[str, Wire]) -> None:
    if not function_call.outputs:
        return

    for wire_name in function_call.outputs.values():
        wire = wires[wire_name]

        if wire.start:
            raise ValueError(
                IO_MULTI_USE_ERROR_MSG
                + f". The name {wire_name} is used multiple times."
            )
        wire.start = function_call.name


def create_flow_graph(logic_flow: List[FunctionCall]) -> nx.DiGraph:
    input_names = sorted(
        chain(
            *[
                function_call.inputs.values()
                for function_call in logic_flow
                if function_call.inputs
            ]
        )
    )
    output_names = sorted(
        chain(
            *[
                function_call.outputs.values()
                for function_call in logic_flow
                if function_call.outputs
            ]
        )
    )

    if not input_names == output_names:
        raise ValueError(IO_NAME_MISMATCH_ERROR_MSG)

    wires = defaultdict(Wire)
    for function_call in logic_flow:
        _parse_call_inputs(function_call, wires)
        _parse_call_outputs(function_call, wires)

    edges = [(wire.start, wire.end) for wire in wires.values()]

    graph = nx.DiGraph()

    graph.add_nodes_from(
        [(function_call.name, {"data": function_call}) for function_call in logic_flow]
    )
    graph.add_edges_from(edges)

    return graph
