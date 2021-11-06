from dataclasses import dataclass
from typing import Union


@dataclass(frozen=True)
class ExternalReference:
    source_name: str
    url: Union[str, None] = None
    external_id: Union[str, None] = None
    description: Union[str, None] = None

    def is_mitre_attack(self):
        return self.is_mitre_attack_enterprise() or self.is_mitre_attack_mobile()

    def is_mitre_attack_enterprise(self):
        return self.source_name == 'mitre-attack'

    def is_mitre_attack_mobile(self):
        return self.source_name == 'mitre-mobile-attack'
