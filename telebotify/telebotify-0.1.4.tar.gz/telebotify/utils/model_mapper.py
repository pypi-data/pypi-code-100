class ModelMapper:

    @staticmethod
    def map(object_dict: dict, cls):
        object_instance = cls()
        attributes = list(vars(object_instance).keys())
        for attribute in attributes:
            try:
                setattr(object_instance, attribute, object_dict[attribute])
            except KeyError:
                setattr(object_instance, attribute, None)
        return object_instance
