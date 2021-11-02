
class Disk(object):

    manufacturer = None
    model = None
    serial = None

    def __init__(self, manufacturer=None, model=None, serial=None):
        self.manufacturer = manufacturer
        self.model = model
        self.serial = serial

    def __eq__(self, other):
        return (self.manufacturer == other.manufacturer and
                self.serial == other.serial and
                self.model == other.model)

    def _sort_key(self):
        return (self.model, self.serial)

    def __lt__(self, other):
        return self._sort_key() < other._sort_key()
