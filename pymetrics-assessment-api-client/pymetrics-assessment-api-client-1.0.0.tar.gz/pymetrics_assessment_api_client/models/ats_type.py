from enum import Enum


class AtsType(str, Enum):
    ADP = "adp"
    AVATURE = "avature"
    ICIMS = "icims"
    KENEXA = "kenexa"
    MERCURY_API = "mercury_api"
    CLIENT_PORTAL = "client_portal"
    OLEEO = "oleeo"
    ORC = "orc"
    SAP_SF = "sap_sf"
    WORKDAY = "workday"

    def __str__(self) -> str:
        return str(self.value)
