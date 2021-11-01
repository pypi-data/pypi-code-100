from abc import abstractmethod


def get_place_field_from_model(model):
    places_meta = getattr(model, 'PlacesMeta', None)
    return getattr(places_meta, 'field')


def get_census_values_from_model(model):
    places_meta = getattr(model, 'PlacesMeta', None)
    return getattr(places_meta, 'census_values')


class BaseCensusValue:
    @property
    @abstractmethod
    def variables(self):
        pass

    @abstractmethod
    def get_value_from_results(self, results):
        pass


class CensusValue(BaseCensusValue):
    def __init__(self, input_variable):
        self._input_variable = input_variable

    @property
    def variables(self):
        return [self._input_variable,]

    def get_value_from_results(self, results):
        return results[self._input_variable]


class ComputedCensusValue(BaseCensusValue):
    def __init__(self, input_variable0,  operator, input_variable1):
        self._input_variable0 = input_variable0
        self._operator = operator
        self._input_variable1 = input_variable1

    @property
    def variables(self):
        return [self._input_variable0, self._input_variable1,]

    def get_value_from_results(self, results):
        try:
            value = eval(f'{results[self._input_variable0]}{self._operator}{results[self._input_variable1]}')
            return value
        except:
            return None


class CensusValues(dict):
    @property
    def variables(self):
        variables = []
        for value in self.values():
            variables += value.variables
        return variables

    def get_values_from_results(self, results):
        results_dict = {}
        for name, value in self.items():
            results_dict[name] = value.get_value_from_results(results)
        return results_dict
