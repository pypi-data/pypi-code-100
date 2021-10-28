# api.py
from abc import ABC
from typing import Any, List, Optional, Union, cast
from typeguard import typechecked
from qilimanjaroq_client.devices.device import Device
from qilimanjaroq_client.errors import ConnectionException, RemoteExecutionException
from qilimanjaroq_client.typings.algorithm import ProgramDefinition
from qilimanjaroq_client.typings.connection import ConnectionConfiguration
from qilimanjaroq_client.connection import Connection
from qilimanjaroq_client.config import logger
from qilimanjaroq_client.devices.quantum_device import QuantumDevice
from qilimanjaroq_client.devices.simulator_device import SimulatorDevice
from qilimanjaroq_client.typings.device import DeviceType, QuantumDeviceInput, SimulatorDeviceInput
from qilimanjaroq_client.devices.devices import Devices
from qilimanjaroq_client.job import Job
from qilimanjaroq_client.typings.job import JobResponse


class API(ABC):
    """Qilimanjaro Client API class to communicate with the Quantum Service

    """
    API_VERSION = 'v1'
    API_PATH = f'/api/{API_VERSION}'
    JOBS_CALL_PATH = '/jobs'
    DEVICES_CALL_PATH = '/devices'
    PING_CALL_PATH = '/status'

    @typechecked
    def __init__(self, configuration: Optional[ConnectionConfiguration] = None):
        self._connection = Connection(configuration=configuration, api_path=self.API_PATH)
        self._devices = None
        self._jobs: List[Job] = []

    @property
    def jobs(self) -> List[Job]:
        return self._jobs

    @property
    def last_job(self) -> Job:
        return self._jobs[-1]

    def ping(self) -> str:
        """Checks if the connection is alive and response OK when it is.

        Returns:
            str: OK when connection is alive or raise Connection Error.
        """
        response, status_code = self._connection.send_get_remote_call(path=self.PING_CALL_PATH)
        if status_code != 200:
            raise ConnectionException('Error connecting to Qilimanjaro API')
        return response

    def _is_quantum_device_input(self, device_input: Union[QuantumDeviceInput, SimulatorDeviceInput]) -> bool:
        """Determine if the given device_input is from a Quantum Device or not

        Args:
            device_input (Union[QuantumDeviceInput, SimulatorDeviceInput]): Device Input structure

        Returns:
            bool: True if the device is from a Quantum Device
        """
        if 'last_calibration_time' in device_input:
            return True
        if 'calibration_details' in device_input:
            return True
        if ('characteristics' in device_input and
            (device_input['characteristics']['type'] is DeviceType.QUANTUM) or
                ((device_input['characteristics']['type'] == DeviceType.QUANTUM.value))):
            return True
        return False

    def _create_device(self, device_input: Union[QuantumDeviceInput, SimulatorDeviceInput]) -> Union[QuantumDevice, SimulatorDevice]:
        """Creates a Device from a given device input.

        Args:
            device_input (Union[QuantumDeviceInput, SimulatorDeviceInput]): Device Input structure

        Returns:
            Union[QuantumDevice, SimulatorDevice]: The constructed Device Object
        """
        if self._is_quantum_device_input(device_input=device_input):
            return QuantumDevice(device_input=device_input)
        return SimulatorDevice(device_input=device_input)

    @typechecked
    def list_devices(self) -> Devices:
        response, status_code = self._connection.send_get_auth_remote_api_call(path=self.DEVICES_CALL_PATH)
        if status_code != 200:
            raise RemoteExecutionException(
                message=('Devices could not be retrieved.'),
                status_code=status_code)

        # !!! TODO: handle all items, not only the returned on first call
        self._devices = Devices([self._create_device(
            device_input=cast(Union[QuantumDevice, SimulatorDevice], device_input))
            for device_input in response['items']])
        return self._devices

    @typechecked
    def select_device_id(self, device_id: int) -> None:
        if self._devices is None:
            raise ValueError("No devices collected. Please call 'list_devices' first.")
        self._selected_device = self._devices.select_device(id=device_id)
        logger.info(f"Device {device_id} selected.")

    @typechecked
    def execute(self, program: ProgramDefinition) -> Any:
        """Send a remote experiment from the provided algorithm to be executed on the remote service API

        Args:
            algorithm (Algorithm): algorithm details conforming the experiment

        Returns:
            Any: Result of the algorithm executed remotely
        """
        job = Job(program=program,
                  user=self._connection.user,
                  device=cast(Device, self._selected_device))

        logger.debug(f"Sending experiment for a remote execution...")
        response, status_code = self._connection.send_post_auth_remote_api_call(
            path=self.JOBS_CALL_PATH,
            data=job.job_request)
        if status_code != 201:
            raise RemoteExecutionException(
                message=('Experiment could not be executed.'),
                status_code=status_code)
        logger.debug(f"Experiment completed successfully.")
        job.update_with_job_response(job_response=JobResponse(response))
        self._jobs.append(job)

        return job.result
