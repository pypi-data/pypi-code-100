


def storable(storable_class):
    def to_storable(self):
        """
        convert all class variables to dictionary
        :return:
        """
        return self.__dict__

    if storable_class.__dict__.get("to_storable"):
        raise TypeError(f"{storable_class.__name__} isn't storable as the method 'to_storable' would be overwritten.")
    else:
        storable_class.to_storable = to_storable

    return storable_class


class StorableClass:

    def to_storable(self):
        """
        convert all class variables to dictionary
        :return:
        """
        return self.__dict__
