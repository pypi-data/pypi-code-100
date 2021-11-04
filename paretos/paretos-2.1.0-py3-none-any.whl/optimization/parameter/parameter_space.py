from typing import Generic, Iterator, List, Optional, TypeVar

from . import Parameter

ParameterT = TypeVar("ParameterT", bound=Parameter, covariant=True)


class ParameterSpace(Generic[ParameterT]):
    """
    Class describing the set of all design parameters for a specific problem
    """

    def __init__(self, parameters: List[ParameterT]):
        self.__parameters = parameters.copy()

        self.__parameters_by_id = {}
        self.__parameters_by_name = {}

        for index, parameter in enumerate(self.__parameters):
            parameter_id = parameter.get_id()
            parameter_name = parameter.get_name()

            self.__parameters_by_id[parameter_id] = parameter
            self.__parameters_by_name[parameter_name] = parameter

    def __iter__(self) -> Iterator[ParameterT]:
        return iter(self.__parameters)

    def get_parameter_by_id(self, id_: str) -> Optional[ParameterT]:
        try:
            return self.__parameters_by_id[id_]
        except KeyError:
            return None

    def get_parameter_by_name(self, name: str) -> Optional[ParameterT]:
        try:
            return self.__parameters_by_name[name]
        except KeyError:
            return None

    def size(self):
        return len(self.__parameters)
