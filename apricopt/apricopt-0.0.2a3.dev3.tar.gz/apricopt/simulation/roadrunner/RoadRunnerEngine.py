"""
This file is part of Apricopt.

Apricopt is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Apricopt is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Apricopt.  If not, see <http://www.gnu.org/licenses/>.

Copyright (C) 2020-2021 Marco Esposito, Leonardo Picchiami.
"""

from typing import Type, Dict, List

from apricopt.model.Model import Model
from apricopt.model.ModelInstance import ModelInstance
from apricopt.simulation.SimulationEngine import SimulationEngine

import roadrunner
from roadrunner import RoadRunner

from apricopt.simulation.roadrunner.RoadRunnerModelInstance import RoadRunnerModelInstance


class RoadRunnerEngine(SimulationEngine):

    def __init__(self):
        super().__init__()

    def load_model(self, model_filename: str) -> ModelInstance:
        model_obj: RoadRunner = roadrunner.RoadRunner(model_filename)
        return RoadRunnerModelInstance(model_obj)

    def simulate_trajectory(self, model: Model, horizon: float) -> Dict[str, List[float]]:
        output = self.simulate_trajectory_and_set(model, horizon)
        model_obj: RoadRunner = model.instance.model_obj
        model_obj.resetAll()
        return output

    def simulate_trajectory_and_set(self, model: Model, horizon: float, exclude=None) -> Dict[str, List[float]]:
        if not isinstance(model.instance, RoadRunnerModelInstance):
            raise TypeError("The object in the field 'instance' of a 'Model' object passed to "
                            "'RoadRunnerEngine::simulate_trajectory' method must have type 'RoadRunnerModelInstance'.")
        model_obj: RoadRunner = model.instance.model_obj
        if model.instance.time_step == -1:
            raise RuntimeError("The time step must be set before running the simulation.")
        observed: List[str]
        if model.observed_outputs:
            observed = model.observed_outputs
        else:
            observed = model_obj.model.getFloatingSpeciesIds()
        model_obj.timeCourseSelections = observed

        trajectory = model_obj.simulate(0, horizon, steps=int(horizon / model.instance.time_step))
        output: Dict[str, List[float]] = dict()
        for obs_out in observed:
            output[obs_out] = trajectory[obs_out]
        return output

    def simulate_trajectory_and_get_state(self, model: Model, horizon: float, exclude=None) -> Dict[str, List[float]]:
        raise NotImplementedError()

    def restore_state(self, model: Model, changed_values: dict) -> None:
        raise NotImplementedError()

    def model_instance_class(self) -> Type[ModelInstance]:
        return RoadRunnerModelInstance
