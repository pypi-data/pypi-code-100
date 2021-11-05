from abc import abstractmethod, ABC


class IJobService(ABC):
    @abstractmethod
    def queue_jobs(self, jobs):
        pass

    @abstractmethod
    def peek_next_job(self):
        pass

    @abstractmethod
    def _get_next_job_file(self, job):
        pass

    @abstractmethod
    def download_next_job(self):
        pass

    @abstractmethod
    def start_next_job(self):
        pass