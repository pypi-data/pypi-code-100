from typing import Dict


class AsyncEnvironmentInterface:
    """
    Interface to provide an environment for non-blocking individual evaluation
    of designs. Allows the usage of the await keyword within the evaluation function.
    """

    async def evaluate_async(
        self,
        design_values: Dict[str, float],
    ) -> Dict[str, float]:
        """
        Function which wraps the model to be modified and evaluated on performance
        :param design_values: raw design parameter values by name
        :return: kpi values by kpi parameter name - values have to be real numbers
        """
        raise NotImplementedError()
