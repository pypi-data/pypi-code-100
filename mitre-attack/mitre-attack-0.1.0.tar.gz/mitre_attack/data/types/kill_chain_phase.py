from dataclasses import dataclass


@dataclass(frozen=True)
class KillChainPhase:
    kill_chain_name: str
    phase_name: str

    def is_mitre_attack(self) -> bool:
        return self.kill_chain_name == 'mitre-attack'
