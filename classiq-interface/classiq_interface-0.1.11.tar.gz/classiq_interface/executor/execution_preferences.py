from typing import List, Optional, Union

import pydantic

from classiq_interface.backend.backend_preferences import (
    AwsBackendPreferences,
    AzureBackendPreferences,
    IBMBackendPreferences,
    IonqBackendPreferences,
)
from classiq_interface.executor.error_mitigation import ErrorMitigationMethod
from classiq_interface.generator.noise_properties import NoiseProperties
from classiq_interface.generator.preferences.randomness import create_random_seed
from classiq_interface.hybrid.vqe_problem import VQEPreferences


class AmplitudeEstimation(pydantic.BaseModel):
    alpha: float = pydantic.Field(
        default=0.05, description="Confidence level of the AE algorithm"
    )
    epsilon: float = pydantic.Field(
        default=0.01, description="precision for estimation target `a`"
    )
    binary_search_threshold: Optional[pydantic.confloat(ge=0, le=1)] = pydantic.Field(
        description="The required probability on the tail of the distribution (1 - percentile)"
    )


class AmplitudeAmplification(pydantic.BaseModel):
    iterations: Union[List[int], int, None] = pydantic.Field(
        default=None, description="Number or list of numbers of iteration to use"
    )
    growth_rate: Optional[float] = pydantic.Field(
        default=None,
        description="Number of iteration used is set to round(growth_rate**iterations)",
    )
    sample_from_iterations: bool = pydantic.Field(
        default=False,
        description="If True, number of iterations used is picked randomly from [1, iteration] range",
    )


class VQEOptimization(pydantic.BaseModel):
    vqe_preferences: VQEPreferences = pydantic.Field(
        default_factory=VQEPreferences, description="preferences for the VQE execution"
    )
    is_maximization: bool = pydantic.Field(
        default=False,
        description="Whether the VQE goal is to maximize",
    )
    initial_point: List[float] = pydantic.Field(
        default=None,
        description="Initial values for the ansatz parameters",
    )


class ExecutionPreferences(pydantic.BaseModel):
    num_shots: int = 100
    timeout_sec: Optional[pydantic.PositiveInt] = pydantic.Field(
        default=None,
        description="If set, limits the execution runtime. Value is in seconds. Not supported on all platforms.",
    )
    amplitude_estimation: Optional[AmplitudeEstimation]
    amplitude_amplification: Optional[AmplitudeAmplification]
    vqe_optimization: Optional[VQEOptimization]
    error_mitigation_method: Optional[ErrorMitigationMethod] = pydantic.Field(
        default=None,
        description="Error mitigation method. Currently supports complete and tensored measurement calibration.",
    )
    noise_properties: Optional[NoiseProperties] = pydantic.Field(
        default=None, description="Properties of the noise in the circuit"
    )
    random_seed: int = pydantic.Field(
        default_factory=create_random_seed,
        description="The random seed used for the generation",
    )
    backend_preferences: Union[
        AzureBackendPreferences,
        IBMBackendPreferences,
        AwsBackendPreferences,
        IonqBackendPreferences,
    ] = pydantic.Field(
        default_factory=lambda: IBMBackendPreferences(
            backend_service_provider="IBMQ", backend_name="aer_simulator_statevector"
        ),
        description="Preferences for the requested backend to run the quantum circuit.",
    )
