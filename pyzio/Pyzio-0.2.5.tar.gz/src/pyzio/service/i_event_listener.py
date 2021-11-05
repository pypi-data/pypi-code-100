from abc import ABCMeta, abstractmethod

from ..pyzio_listener import PyzioListener


class IEventListener(PyzioListener, metaclass=ABCMeta):
    @abstractmethod
    def on_candidate_registered(self, candidate_id):
        pass

    @abstractmethod
    def on_pairing_code_generated(self, pairing_code):
        pass

    @abstractmethod
    def on_printer_registered(self, printer_id):
        pass

    @abstractmethod
    def on_sensor_registered(self, sensor_id, request_id):
        pass

    @abstractmethod
    def on_job_received(self):
        pass

    @abstractmethod
    def on_markready_received(self):
        pass

    @abstractmethod
    def on_update_command_received(self):
        pass