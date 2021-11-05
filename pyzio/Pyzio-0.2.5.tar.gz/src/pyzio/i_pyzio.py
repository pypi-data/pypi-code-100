from abc import ABCMeta, abstractmethod


class IPyzio(metaclass=ABCMeta):
    @abstractmethod
    def start_listening(self):
        pass

    @abstractmethod
    def is_mqtt_connected(self):
        pass

    @abstractmethod
    def initialise_printer(self):
        pass

    @abstractmethod
    def peek_next_job(self):
        pass

    @abstractmethod
    def get_printer_service(self):
        pass

    @abstractmethod
    def listen_for_sensor_ids(self):
        pass

    @abstractmethod
    def on_markready_received(self):
        pass

    @abstractmethod
    def send_sensor_registration(self, sensor_name, sensor_type):
        pass

    @abstractmethod
    def start_next_job(self):
        pass

    @abstractmethod
    def download_next_job(self):
        pass

    @abstractmethod
    def mark_job_failed(self, job_id):
        pass

    @abstractmethod
    def mark_job_complete(self, job_id, filepath):
        pass

    @abstractmethod
    def mark_job_inprogress(self, job_id):
        pass

    @abstractmethod
    def send_sensor_update(self, sensor_id, value, sensor_type):
        pass

    @abstractmethod
    def shutdown(self):
        pass