from .specific import Alliances, Cities, Nations
import threading


class Apathy:
    def __init__(self, types=(Alliances, Cities, Nations)):
        self.threads = []

        for T in types:
            thing = T()
            self.threads.append(threading.Thread(target=thing.run, daemon=True, name=T.__name__))

    def run(self):
        for thread in self.threads:
            thread.start()
        for thread in self.threads:
            thread.join()

        # combination placeholder
