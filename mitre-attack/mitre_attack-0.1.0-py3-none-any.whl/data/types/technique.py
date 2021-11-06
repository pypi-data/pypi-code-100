from dataclasses import dataclass, field
from typing import List, Union
from mitre_attack.data.types.kill_chain_phase import KillChainPhase
from mitre_attack.data.types.object import Object


@dataclass(frozen=True)
class _Technique(Object):
    name: str
    contributors: List[str] = field(default_factory=list)
    detection: Union[str, None] = None
    is_subtechnique: bool = False
    kill_chain_phases: List[KillChainPhase] = field(default_factory=list)


@dataclass(frozen=True)
class EnterpriseTechnique(_Technique):
    data_sources: List[str] = field(default_factory=list)
    defense_bypassed: List[str] = field(default_factory=list)
    effective_permissions: List[str] = field(default_factory=list)
    impact_type: List[str] = field(default_factory=list)
    network_requirements: bool = False
    old_attack_id: Union[str, None] = None
    permissions_required: List[str] = field(default_factory=list)
    platforms: List[str] = field(default_factory=list)
    remote_support: bool = False
    system_requirements: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class MobileTechnique(_Technique):
    old_attack_id: Union[str, None] = None
    platforms: List[str] = field(default_factory=list)
    tactic_type: List[str] = field(default_factory=list)

    def requires_device_access(self):
        for tactic_type in ['Pre-Adversary Device Access', 'Post-Adversary Device Access']:
            if tactic_type in self.tactic_type:
                return True
        return False
