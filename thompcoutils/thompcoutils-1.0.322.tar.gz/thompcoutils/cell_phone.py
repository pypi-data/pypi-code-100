from enum import Enum


class CellPhone:
    class Carrier(Enum):
        T_MOBILE = 'tmomail.net'
        ATT = 'txt.att.net'

    def __init__(self, carrier, number):
        self.carrier = carrier
        self.number = number

    def as_email(self):
        return '{}@{}'.format(self.number, self.carrier.value)
