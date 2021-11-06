from typing import List, Union, Any, Optional
from mitre_attack import DEFAULT_MITRE_VERSION, TOOL, MALWARE
from mitre_attack.data.types.data_component import DataComponent
from mitre_attack.data.types.data_source import DataSource
from mitre_attack.data.types.external_reference import ExternalReference
from mitre_attack.data.types.group import Group
from mitre_attack.data.types.identity import Identity
from mitre_attack.data.types.kill_chain_phase import KillChainPhase
from mitre_attack.data.types.malware import Malware
from mitre_attack.data.types.marking_definition import MarkingDefinition
from mitre_attack.data.types.matrix import Matrix
from mitre_attack.data.types.mitigation import Mitigation
from mitre_attack.data.types.object import Object
from mitre_attack.data.types.relationship import Relationship
from mitre_attack.data.types.tactic import Tactic
from mitre_attack.data.types.technique import EnterpriseTechnique, MobileTechnique

import copy
import hodgepodge.pattern_matching
import hodgepodge.stix
import hodgepodge.time
import hodgepodge.types
import logging
import mitre_attack.data.stix as stix
from mitre_attack.data.types.tool import Tool

logger = logging.getLogger(__name__)

X_MITRE_PREFIX = 'x_mitre_'


def parse_object(data: Any) -> Optional[Object]:
    data = hodgepodge.stix.stix2_to_dict(data)

    #: Ignore any deprecated objects.
    if data.get('x_mitre_deprecated'):
        logger.debug("Ignoring deprecated %s object: %s", data['type'], data['id'])
        return

    #: Ignore any revoked objects.
    revoked = data.pop('revoked', False)
    if revoked is True:
        logger.debug("Ignoring revoked %s object: %s", data['type'], data['id'])
        return

    #: Remove x_mitre_ prefix from all custom keys (e.g. 'x_mitre_data_sources' -> 'data_sources').
    for k, v in copy.copy(list(data.items())):
        if k.startswith(X_MITRE_PREFIX):
            del data[k]
            data[k[len(X_MITRE_PREFIX):]] = v

    data.update({
        'created': hodgepodge.time.to_datetime(data['created']),
        'modified': hodgepodge.time.to_datetime(data['modified']),
        'version': data.get('version', DEFAULT_MITRE_VERSION),
        'external_references': parse_external_references(data.get('external_references', []))
    })
    parser = STIX_TYPES_TO_PARSERS[data['type']]
    return parser(data)


def parse_identity(data: dict) -> Identity:
    return hodgepodge.types.dict_to_dataclass(data, Identity)


def parse_marking_definition(data: dict) -> MarkingDefinition:
    return hodgepodge.types.dict_to_dataclass(data, MarkingDefinition)


def parse_matrix(data: dict) -> Matrix:
    return hodgepodge.types.dict_to_dataclass(data, Matrix)


def parse_tactic(data: dict) -> Tactic:
    return hodgepodge.types.dict_to_dataclass(data, Tactic)


def parse_technique(data: dict) -> Union[EnterpriseTechnique, MobileTechnique]:
    mitre_attack_reference = next(ref for ref in data['external_references'] if ref.is_mitre_attack())
    if mitre_attack_reference.is_mitre_attack_enterprise():
        return parse_enterprise_technique(data)
    else:
        return parse_mobile_technique(data)


def parse_enterprise_technique(data: dict) -> EnterpriseTechnique:
    return hodgepodge.types.dict_to_dataclass(data, EnterpriseTechnique)


def parse_mobile_technique(data: dict) -> MobileTechnique:
    return hodgepodge.types.dict_to_dataclass(data, MobileTechnique)


def parse_group(data: dict) -> Group:
    return hodgepodge.types.dict_to_dataclass(data, Group)


def parse_software(data: dict) -> Union[Malware, Tool]:
    t = data['type']
    if t == MALWARE:
        data_class = Malware
    elif t == TOOL:
        data_class = Tool
    else:
        raise ValueError(t)
    return hodgepodge.types.dict_to_dataclass(data, data_class)


def parse_mitigation(data: dict) -> Mitigation:
    return hodgepodge.types.dict_to_dataclass(data, Mitigation)


def parse_data_component(data: dict) -> DataComponent:
    return hodgepodge.types.dict_to_dataclass(data, DataComponent)


def parse_data_source(data: dict) -> DataSource:
    return hodgepodge.types.dict_to_dataclass(data, DataSource)


def parse_relationship(data: dict):
    data.update({
        'external_references': data.get('external_references', []),
        'description': data.get('description'),
        'source_ref_type': stix.get_type_from_id(data['source_ref']),
        'target_ref_type': stix.get_type_from_id(data['target_ref']),
    })
    return hodgepodge.types.dict_to_dataclass(data, Relationship)


def parse_kill_chain_phases(kill_chain_phases: List[dict]):
    return [parse_kill_chain_phase(p) for p in kill_chain_phases]


def parse_kill_chain_phase(data: dict):
    return hodgepodge.types.dict_to_dataclass(data, KillChainPhase)


def parse_external_references(refs: List[dict]):
    return [parse_external_reference(ref) for ref in refs]


def parse_external_reference(data: dict):
    if isinstance(data, ExternalReference):
        return data
    return hodgepodge.types.dict_to_dataclass(data, ExternalReference)


STIX_TYPES_TO_PARSERS = {
    'identity': parse_identity,
    'marking-definition': parse_marking_definition,
    'x-mitre-matrix': parse_matrix,
    'x-mitre-tactic': parse_tactic,
    'x-mitre-data-source': parse_data_source,
    'x-mitre-data-component': parse_data_component,
    'attack-pattern': parse_technique,
    'intrusion-set': parse_group,
    'malware': parse_software,
    'tool': parse_software,
    'course-of-action': parse_mitigation,
    'relationship': parse_relationship,
}
