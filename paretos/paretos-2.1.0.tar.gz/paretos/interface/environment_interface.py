from typing import Dict


class EnvironmentInterface:
    """
    Interface to provide an environment for individual evaluation of designs.
    """

    def evaluate(
        self,
        design_values: Dict[str, float],
    ) -> Dict[str, float]:
        """
        Function which wraps the model to be modified and evaluated on performance
        :param evaluation_uuid: uuid of the simulation
        :param design_values: raw design parameter values by name
        :return: kpi values by kpi parameter name - values have to be real numbers
        """
        raise NotImplementedError()
