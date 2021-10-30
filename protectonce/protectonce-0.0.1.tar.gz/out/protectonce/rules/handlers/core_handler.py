from ctypes import c_char_p
from ...core_interface import po_interface
from orjson import orjson as json


class CoreHandler(object):
    def __init__(self, rule, method) -> None:
        super(CoreHandler, self).__init__()
        self._method = method
        self._rule = rule

    def handle_before(self, method_data, args, kwargs) -> bool:
        data = {
            'context': self._rule.context,
            'args': args
        }

        str_data = json.dumps(data)
        result, out_data_type, out_data_size, mem_buffer_id = po_interface.invoke(
            self._method, str_data, len(str_data))

        result = c_char_p(result).value
        result_json = json.loads(result.decode('utf-8'))

        action = result_json.get('action', "none")

        # This function returns True if the payload is allowed and false otherwise
        return action != "block"

    def handle_after(self, method_data, result, args, kwargs) -> bool:
        # Not Implemented
        return True
