class Jsonable(object):

    @classmethod
    def from_json(cls, json_dict: dict):
        raise NotImplementedError
