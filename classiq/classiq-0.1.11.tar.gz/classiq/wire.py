from classiq_interface.generator import function_call


class Wire:
    def __init__(self, start_call: function_call.FunctionCall, output_name: str):
        self._start_call = start_call
        self._start_name: str = output_name
        self._wire_name = f"{start_call.name}_{self._start_name}"

    def connect_wire(self, end_call: function_call.FunctionCall, input_name: str):
        self._start_call.outputs[self._start_name] = self._wire_name
        end_call.inputs[input_name] = self._wire_name
