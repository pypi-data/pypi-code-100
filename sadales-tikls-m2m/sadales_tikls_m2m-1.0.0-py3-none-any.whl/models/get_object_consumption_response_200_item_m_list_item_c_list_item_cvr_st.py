from enum import Enum


class GetObjectConsumptionResponse200ItemMListItemCListItemCVRSt(str, Enum):
    C = "C"
    D = "D"
    M = "M"
    E = "E"
    N = "N"
    U = "U"
    CD = "CD"

    def __str__(self) -> str:
        return str(self.value)
