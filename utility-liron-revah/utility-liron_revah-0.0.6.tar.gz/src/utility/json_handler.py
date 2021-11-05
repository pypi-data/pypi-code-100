from utility.path_handler import PathHandler
from numpy import integer, floating, ndarray
from json import load, loads, dump, dumps, JSONEncoder, JSONDecodeError

class NpEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, integer):
            return int(obj)
        elif isinstance(obj, floating):
            return float(obj)
        elif isinstance(obj, ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)

class JsonHandler():
    cls_encoder: JSONEncoder = None
    file_encoder: str = 'utf-8'
    ensure_ascii: bool = True
    indent: int = 4

    def __init__(self, cls_encoder: str = None):
        self.setClsEncoder(cls_encoder)
        
    def setFileEncoder(self, file_encoder: str = 'utf-8'):
        # TODO add validator for correct input? like utf-8, utf-16, etc...
        self.file_encoder = file_encoder

    def setClsEncoder(self, cls_encoder: str = None):
        if cls_encoder == "NpEncoder":
                self.encoder = NpEncoder()

    def enableAscii(self, flag: bool = True):
        self.ensure_ascii = flag

    def setIndent(self, indent: int = 4):
        self.indent = indent

    def encode_data(self, data: dict):
        return loads(dumps(data, cls=self.cls_encoder))

    def save(self, data: dict, name: str = None, path: str = None):
        """Description: This save only localy"""
        name = 'NoName.json' if name is None else f"{name}.json"
        path = PathHandler().get_path(path)
        # File output
        with open(f"{path}\{name}", 'w') as outfile:
            data = data if type(data) is not object else data.decode(self.file_encoder)
            dump(data, outfile, indent=self.indent, ensure_ascii=self.ensure_ascii, cls=self.cls_encoder)
            print(f'File {name} was save on the path: {path}')

    def read(self, name: str, path: str = None):
        path = PathHandler().get_path(path)
        try:
            with open(f"{path}\{name}", encoding=self.file_encoder) as json_file:
                data = load(json_file)
            return data
        except JSONDecodeError as _:
            print(f'Error in decoding this file: {name}')
            return None

    def str_to_dict(self, data: str or list):
        if type(data) is str:
            return self.encode_data(data)
        elif type(data) is list:
            temp = list()
            for item in data:
                temp.append(self.str_to_dict(item))
            return temp
