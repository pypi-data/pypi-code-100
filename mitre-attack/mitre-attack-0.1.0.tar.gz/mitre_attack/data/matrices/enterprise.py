from stix2 import Filter
from typing import Iterator, Union, Optional, Iterable, Any
from mitre_attack import TACTIC, MALWARE, TOOL, COURSE_OF_ACTION, ATTACK_PATTERN, INTRUSION_SET, RELATIONSHIP
from mitre_attack.data.types.relationship import Relationship
from mitre_attack.data.types.technique import EnterpriseTechnique as Technique
from mitre_attack.data.types.mitigation import Mitigation
from mitre_attack.data.types.group import Group
from mitre_attack.data.types.malware import Malware
from mitre_attack.data.types.tool import Tool
from mitre_attack.data.types.tactic import Tactic

import mitre_attack.data.parser as parser
import hodgepodge.pattern_matching
import hodgepodge.stix
import itertools


MITRE_ATTACK_ENTERPRISE_URL = 'https://cti-taxii.mitre.org/stix/collections/95ecc380-afe9-11e4-9b6c-751b66dd541e'


class MitreAttackEnterprise:
    def __init__(self):
        self.data_source = hodgepodge.stix.get_taxii_data_source(
            url=MITRE_ATTACK_ENTERPRISE_URL,
            allow_custom=True,
        )

    def _get_object(self, stix_type: str, stix_id: Optional[str] = None, name: Optional[str] = None) -> Any:
        if stix_id:
            row = self.data_source.get(stix_id=stix_id)
            if row:
                row = parser.parse_object(row)
        else:
            names = [name] if name else []
            row = next(self._iter_objects(stix_type=stix_type, names=names), None)
        return row

    def _iter_objects(
            self,
            stix_type: str,
            stix_ids: Optional[Iterable[str]] = None,
            names: Optional[Iterable[str]] = None,
            limit: Optional[int] = None) -> Iterator[Any]:

        filters = [
            Filter("type", "=", stix_type)
        ]
        total = 0
        for row in self.data_source.query(filters):
            row = parser.parse_object(row)
            if row:

                #: Filter by ID.
                if stix_ids and row.id not in stix_ids:
                    continue

                #: Filter by name.
                if names:
                    found_names = [name for name in [getattr(row, 'name', None)] + getattr(row, 'aliases', []) if name]
                    if not hodgepodge.pattern_matching.str_matches_glob(names, found_names):
                        continue

                yield row

                if limit and total >= limit:
                    return

    def get_tactic(self, tactic_id: Optional[str] = None, tactic_name: Optional[str] = None) -> Optional[Tactic]:
        return self._get_object(stix_type=TACTIC, stix_id=tactic_id, name=tactic_name)

    def get_technique(self, technique_id: Optional[str] = None, technique_name: Optional[str] = None) -> Optional[Technique]:
        return self._get_object(stix_type=ATTACK_PATTERN, stix_id=technique_id, name=technique_name)

    def get_group(self, group_id: Optional[str] = None, group_name: Optional[str] = None) -> Optional[Group]:
        return self._get_object(stix_type=INTRUSION_SET, stix_id=group_id, name=group_name)

    def get_software(self, software_id: Optional[str] = None, software_name: Optional[str] = None) -> Optional[Union[Malware, Tool]]:
        return self._get_object(stix_type=MALWARE, stix_id=software_id, name=software_name)

    def get_malware_family(self, software_id: Optional[str] = None, software_name: Optional[str] = None) -> Optional[Malware]:
        return self._get_object(stix_type=MALWARE, stix_id=software_id, name=software_name)

    def get_tool(self, software_id: Optional[str] = None, software_name: Optional[str] = None) -> Optional[Tool]:
        return self._get_object(stix_type=TOOL, stix_id=software_id, name=software_name)

    def get_mitigation(self, mitigation_id: Optional[str] = None, mitigation_name: Optional[str] = None) -> Optional[Mitigation]:
        return self._get_object(stix_type=COURSE_OF_ACTION, stix_id=mitigation_id, name=mitigation_name)

    def get_relationship(self, relationship_id: str = None) -> Optional[Relationship]:
        return self._get_object(stix_type=RELATIONSHIP, stix_id=relationship_id)

    def iter_tactics(
            self,
            tactic_ids: Optional[Iterable[str]] = None,
            tactic_names: Iterable[Optional[str]] = None,
            technique_ids: Optional[Iterable[str]] = None,
            technique_names: Iterable[Optional[str]] = None,
            limit: Optional[int] = None) -> Iterator[Tactic]:

        i = 0

        #: Filter tactics by technique, group, software, or mitigation.
        if technique_ids or technique_names:
            techniques = self.iter_techniques(
                technique_ids=technique_ids,
                technique_names=technique_names,
            )
            kill_chain_phases = itertools.chain.from_iterable(technique.kill_chain_phases for technique in techniques)
            tactic_names = {
                phase.phase_name for phase in kill_chain_phases if phase.kill_chain_name == 'mitre-attack'
            }

        #: Filter tactics.
        tactics = self._iter_objects(
            stix_type=TACTIC,
            stix_ids=tactic_ids,
            names=tactic_names,
        )
        for tactic in tactics:
            assert isinstance(tactic, Tactic)
            yield tactic
            i += 1

            if limit and i >= limit:
                return

    def count_tactics(
            self,
            tactic_ids: Optional[Iterable[str]] = None,
            tactic_names: Iterable[Optional[str]] = None,
            technique_ids: Optional[Iterable[str]] = None,
            technique_names: Iterable[Optional[str]] = None) -> int:

        tactics = self.iter_tactics(
            tactic_ids=tactic_ids,
            tactic_names=tactic_names,
            technique_ids=technique_ids,
            technique_names=technique_names,
        )
        total = sum(1 for _ in tactics)
        return total

    def iter_techniques(
            self,
            technique_ids: Optional[Iterable[str]] = None,
            technique_names: Iterable[Optional[str]] = None,
            tactic_ids: Optional[Iterable[str]] = None,
            tactic_names: Iterable[Optional[str]] = None,
            limit: Optional[int] = None) -> Iterator[Technique]:

        i = 0

        #: Lookup tactic names if filtering techniques by tactic.
        if tactic_ids or tactic_names:
            tactics = self.iter_tactics(tactic_ids=tactic_ids, tactic_names=tactic_names)
            tactic_names = {tactic.name for tactic in tactics}

        #: Lookup techniques.
        for technique in self._iter_objects(
            stix_type=ATTACK_PATTERN,
            stix_ids=technique_ids,
            names=technique_names,
        ):
            #: Filter techniques by tactic name.
            if tactic_names:
                kill_chain_phase_names = {p.phase_name for p in technique.kill_chain_phases if p.is_mitre_attack()}
                if not hodgepodge.pattern_matching.str_matches_glob(kill_chain_phase_names, tactic_names):
                    continue

            yield technique
            i += 1

            if limit and i >= limit:
                return

    def count_techniques(
            self,
            technique_ids: Optional[Iterable[str]] = None,
            technique_names: Iterable[Optional[str]] = None,
            tactic_ids: Optional[Iterable[str]] = None,
            tactic_names: Iterable[Optional[str]] = None) -> int:

        techniques = self.iter_techniques(
            technique_ids=technique_ids,
            technique_names=technique_names,
            tactic_ids=tactic_ids,
            tactic_names=tactic_names,
        )
        total = sum(1 for _ in techniques)
        return total

    def iter_software(
            self,
            software_ids: Optional[Iterable[str]] = None,
            software_names: Iterable[Optional[str]] = None,
            limit: Optional[int] = None) -> Iterator[Union[Malware, Tool]]:

        i = 0
        malware = self.iter_malware_families(
            software_ids=software_ids,
            software_names=software_names,
            limit=limit,
        )
        tools = self.iter_tools(
            software_ids=software_ids,
            software_names=software_names,
            limit=limit,
        )
        for row in itertools.chain.from_iterable((malware, tools)):
            yield row
            i += 1

            if limit and i >= limit:
                return

    def count_software(
            self,
            software_ids: Optional[Iterable[str]] = None,
            software_names: Iterable[Optional[str]] = None) -> int:

        software = self.iter_software(
            software_ids=software_ids,
            software_names=software_names,
        )
        total = sum(1 for _ in software)
        return total

    def iter_malware_families(
            self,
            software_ids: Optional[Iterable[str]] = None,
            software_names: Iterable[Optional[str]] = None,
            limit: Optional[int] = None) -> Iterator[Malware]:

        i = 0
        malware_families = self._iter_objects(
            stix_type=MALWARE,
            stix_ids=software_ids,
            names=software_names,
        )
        for malware_family in malware_families:
            yield malware_family
            i += 1

            if limit and i >= limit:
                return

    def count_malware_families(
            self,
            software_ids: Optional[Iterable[str]] = None,
            software_names: Iterable[Optional[str]] = None) -> int:

        software = self.iter_malware_families(
            software_ids=software_ids,
            software_names=software_names,
        )
        total = sum(1 for _ in software)
        return total

    def iter_tools(
            self,
            software_ids: Optional[Iterable[str]] = None,
            software_names: Iterable[Optional[str]] = None,
            limit: Optional[int] = None) -> Iterator[Tool]:

        i = 0
        tools = self._iter_objects(
            stix_type=TOOL,
            stix_ids=software_ids,
            names=software_names,
            limit=limit,
        )
        for tool in tools:
            yield tool
            i += 1

            if limit and i >= limit:
                break

    def count_tools(
            self,
            software_ids: Optional[Iterable[str]] = None,
            software_names: Iterable[Optional[str]] = None) -> int:

        software = self.iter_tools(
            software_ids=software_ids,
            software_names=software_names,
        )
        total = sum(1 for _ in software)
        return total

    def iter_groups(
            self,
            group_ids: Optional[Iterable[str]] = None,
            group_names: Iterable[Optional[str]] = None,
            limit: Optional[int] = None) -> Iterator[Group]:

        i = 0
        groups = self._iter_objects(
            stix_type=INTRUSION_SET,
            stix_ids=group_ids,
            names=group_names,
            limit=limit,
        )
        for group in groups:
            yield group
            i += 1

            if limit and i >= limit:
                break

    def count_groups(
            self,
            group_ids: Optional[Iterable[str]] = None,
            group_names: Iterable[Optional[str]] = None) -> int:

        groups = self.iter_groups(group_ids=group_ids, group_names=group_names)
        total = sum(1 for _ in groups)
        return total

    def iter_mitigations(
            self,
            mitigation_ids: Optional[Iterable[str]] = None,
            mitigation_names: Iterable[Optional[str]] = None,
            limit: Optional[int] = None) -> Iterator[Mitigation]:

        i = 0
        mitigations = self._iter_objects(
            stix_type=COURSE_OF_ACTION,
            stix_ids=mitigation_ids,
            names=mitigation_names,
            limit=limit,
        )
        for mitigation in mitigations:
            yield mitigation
            i += 1

            if limit and i >= limit:
                break

    def count_mitigations(
            self,
            mitigation_ids: Optional[Iterable[str]] = None,
            mitigation_names: Iterable[Optional[str]] = None) -> int:

        mitigations = self.iter_mitigations(
            mitigation_ids=mitigation_ids,
            mitigation_names=mitigation_names,
        )
        total = sum(1 for _ in mitigations)
        return total

    def iter_relationships(
            self,
            relationship_ids: Optional[Iterable[str]] = None,
            relationship_types: Optional[Iterable[str]] = None,
            source_refs: Optional[Iterable[str]] = None,
            source_ref_types: Optional[Iterable[str]] = None,
            target_refs: Optional[Iterable[str]] = None,
            target_ref_types: Optional[Iterable[str]] = None,
            limit: Optional[int] = None) -> Iterable[Relationship]:

        i = 0
        for relationship in self._iter_objects(
            stix_type=RELATIONSHIP,
            stix_ids=relationship_ids,
        ):
            #: Filter relationships by type.
            if relationship_types and relationship.type not in relationship_types:
                continue

            #: Filter relationships by source object ID.
            if source_refs and relationship.source_ref not in source_refs:
                continue

            #: Filter relationships by source object type.
            if source_ref_types and relationship.source_ref_type not in source_ref_types:
                continue

            #: Filter relationships by target object ID.
            if target_refs and relationship.target_ref not in target_ref_types:
                continue

            #: Filter relationships by target type.
            if target_ref_types and relationship.target_ref_type not in target_ref_types:
                continue

            yield relationship
            i += 1

            if limit and i >= limit:
                return

    def count_relationships(
            self,
            relationship_ids: Optional[Iterable[str]] = None,
            relationship_types: Optional[Iterable[str]] = None,
            source_refs: Optional[Iterable[str]] = None,
            source_ref_types: Optional[Iterable[str]] = None,
            target_refs: Optional[Iterable[str]] = None,
            target_ref_types: Optional[Iterable[str]] = None) -> int:

        relationships = self.iter_relationships(
            relationship_ids=relationship_ids,
            relationship_types=relationship_types,
            source_refs=source_refs,
            source_ref_types=source_ref_types,
            target_refs=target_refs,
            target_ref_types=target_ref_types,
        )
        total = sum(1 for _ in relationships)
        return total
