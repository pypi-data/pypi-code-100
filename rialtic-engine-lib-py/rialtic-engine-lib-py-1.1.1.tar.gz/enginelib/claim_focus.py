import datetime as dt
import re
from enum import Enum
from typing import Dict, List, Optional, Union, cast, Tuple, Set

from fhir.resources.address import Address
from fhir.resources.claim import Claim, ClaimInsurance, ClaimItem, ClaimRelated, ClaimSupportingInfo
from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.coding import Coding
from fhir.resources.coverage import Coverage
from fhir.resources.fhirtypes import Date, Decimal
from fhir.resources.humanname import HumanName
from fhir.resources.identifier import Identifier
from fhir.resources.location import Location
from fhir.resources.money import Money
from fhir.resources.organization import Organization
from fhir.resources.patient import Patient
from fhir.resources.practitioner import Practitioner
from fhir.resources.practitionerrole import PractitionerRole
from fhir.resources.quantity import Quantity
from fhir.resources.reference import Reference
from fhir.resources.relatedperson import RelatedPerson
from fhir.resources.resource import Resource
from fhir.resources.servicerequest import ServiceRequest
from schema.insight_engine_request import InsightEngineRequest

from enginelib.claim_insurance_focus import (ClaimInsuranceFocus,
                                             find_primary_insurance)
from enginelib.claim_line_focus import ClaimLineFocus
from enginelib.comparator import ClaimComparator, CompareResult
from enginelib.errors import ClaimError
from enginelib.types import Period


class ClaimTypeFocus(str, Enum):
    PROFESSIONAL = "professional"
    INSTITUTIONAL = "institutional"
    DENTAL = "dental"
    PHARMACY = "pharmacy"

    @staticmethod
    def get_claim_type_set():
        return (
            (
                {"cms1500", "837p", "005010x222", "professional", "vision"},
                ClaimTypeFocus.PROFESSIONAL
            ),
            (
                {"ub04", "837i", "005010x223", "institutional"},
                ClaimTypeFocus.INSTITUTIONAL
            ),
            (
                {"ada2006", "837d", "005010x224", "dental", "oral"},
                ClaimTypeFocus.DENTAL
            ),
            (
                {"837", "ncpdpd0", "ncpdpbatch12",
                 "ncpdpwcpcucf", "pharmacy", "drug"},
                ClaimTypeFocus.PHARMACY
            )
        )

    @classmethod
    def from_string(cls, value: str) -> "ClaimTypeFocus":
        normalized_value = re.sub("[^0-9a-z]", "", value.lower())

        for values, claim_type in cls.get_claim_type_set():
            if normalized_value in values:
                return cls.__new__(cls, claim_type)

        raise ClaimError("Unsupported claim type %s" % value)


class ClaimFocus:
    _fields_looked_at: Set[str] = set()

    def __init__(self, claim: Claim, request: InsightEngineRequest = None):
        self.claim = claim
        self.request = request if request is not None else InsightEngineRequest(
            claim=claim)
        self._contained: Optional[Dict[str, Resource]] = None
        self._lines: Optional[List[ClaimLineFocus]] = None

        self._supporting_info_category_codes_cache: Dict[int, List[str]] = dict()

    @property
    def contained(self) -> Dict[str, Resource]:
        self._fields_looked_at.add('contained')
        if self._contained is not None:
            return self._contained

        self._contained = dict()
        if getattr(self.claim, "contained", None):
            resources = [cast(Resource, elem) for elem in self.claim.contained]
            self._contained = {
                resource.id: resource for resource in resources
                if resource.id is not None
            }

        return self._contained

    @property
    def reference_claim_num(self) -> str:
        """
        [new FHIR mapping]
        """
        self._fields_looked_at.add('reference_claim_num')

        try:
            related = cast(ClaimRelated, self.claim.related[0])
            identifier = cast(Identifier, related.reference)
            return identifier.value.strip().lower()
        except (AttributeError, TypeError):
            pass

        raise ClaimError("Field referenceClaimNum was not found on this claim.")

    @property
    def lines(self) -> Optional[List[ClaimLineFocus]]:
        self._fields_looked_at.add('lines')
        if self._lines is not None:
            return self._lines

        if self.request is None:
            self.request = InsightEngineRequest.construct(claim=self.claim)

        self._lines = [ClaimLineFocus(cast(ClaimItem, c), self.request)
                       for c in self.claim.item]
        return self._lines

    @property
    def billable_period(self) -> Period:
        try:
            period = cast(Period, self.claim.billablePeriod)
            if period.start is not None and period.end is not None:
                return Period(start=period.start, end=period.end)
        except AttributeError:
            pass

        raise ClaimError('Field billablePeriod was not found in this claim or was incomplete.')

    @property
    def _svc_facility(self) -> Location:
        """
        [new FHIR mapping]
        """
        ref = cast(Reference, self.claim.facility).reference
        ref = self._cleanup(ref)
        resource = self.contained[ref]
        if resource.resource_type != 'Location':
            raise TypeError()

        return cast(Location, resource)

    @property
    def facility_place_of_service(self) -> str:
        """
        [new FHIR mapping]
        """
        self._fields_looked_at.add('facility_place_of_service')
        try:
            location = self._svc_facility
            physical_type = cast(CodeableConcept, location.physicalType)
            coding = cast(Coding, physical_type.coding[0])
            return coding.code.strip().lower()
        except (AttributeError, KeyError, TypeError, IndexError):
            raise ClaimError('Field facilityPlaceOfService was not found on claim.')

    @property
    def svc_facility_name(self) -> str:
        self._fields_looked_at.add('svc_facility_name')
        try:
            facility = self._svc_facility
            return facility.name.strip().lower()
        except (AttributeError, KeyError, TypeError):
            raise ClaimError('Field svcFacilityName was not found on claim.')

    def _svc_facility_add(self, index: int) -> str:
        """
        [new FHIR mapping]
        """
        facility = self._svc_facility
        address = cast(Address, facility.address)
        return address.line[index].strip().lower()

    @property
    def svc_facility_add1(self) -> str:
        self._fields_looked_at.add('svc_facility_add1')
        try:
            return self._svc_facility_add(0)
        except (AttributeError, KeyError, TypeError, IndexError):
            raise ClaimError(f'Field svcFacilityAdd1 was not found on claim.')

    @property
    def svc_facility_add2(self) -> str:
        self._fields_looked_at.add('svc_facility_add2')
        try:
            return self._svc_facility_add(1)
        except (AttributeError, KeyError, TypeError, IndexError):
            raise ClaimError(f'Field svcFacilityAdd2 was not found on claim.')

    @property
    def svc_facility_city(self) -> str:
        self._fields_looked_at.add('svc_facility_city')
        try:
            facility = self._svc_facility
            city = cast(Address, facility.address).city
            return city.strip().lower()
        except (AttributeError, KeyError, TypeError):
            raise ClaimError(f"Field svcFacilityCity was not found on claim.")

    @property
    def svc_facility_state(self) -> str:
        self._fields_looked_at.add('svc_facility_state')
        try:
            facility = self._svc_facility
            state = cast(Address, facility.address).state
            return state.strip().lower()
        except (AttributeError, KeyError, TypeError):
            raise ClaimError(f"Field svcFacilityState was not found on claim.")

    @property
    def svc_facility_zip(self) -> str:
        self._fields_looked_at.add('svc_facility_zip')
        try:
            facility = self._svc_facility
            postal_code = cast(Address, facility.address).postalCode
            return postal_code.strip().lower()
        except (AttributeError, KeyError, TypeError):
            raise ClaimError(f"Field svcFacilityZip was not found on claim.")

    @property
    def _billing_provider(self) -> Practitioner:
        ref = cast(Reference, self.claim.provider).reference
        ref = self._cleanup(ref)
        resource = self.contained[ref]
        if resource.resource_type != 'PractitionerRole':
            raise TypeError()

        practitioner_role = cast(PractitionerRole, resource)
        ref = cast(Reference, practitioner_role.practitioner).reference
        ref = self._cleanup(ref)
        resource = self.contained[ref]
        if resource.resource_type != 'Practitioner':
            raise TypeError()

        # Stephanie: no need to check this explicitly as only
        #     billing providers are mapped to claim.provider.
        # practitioner = cast(Practitioner, resource)
        # if '85' not in practitioner.id:
        #     raise TypeError()

        return cast(Practitioner, resource)

    @staticmethod
    def _slash_suffix(text: str) -> str:
        match = re.search('/([^/]*)$', text)
        if match is not None:
            return match.group(1)
        return text

    @property
    def _prov_tax_id_and_qual(self) -> Tuple[str, str]:
        practitioner = self._billing_provider
        for identifier in cast(List[Identifier], practitioner.identifier):
            try:
                if self._slash_suffix(identifier.system) != 'XX':
                    tax_id = identifier.value.strip().lower()
                    tax_id_qual = self._slash_suffix(identifier.system.strip()).lower()
                    return tax_id, tax_id_qual
            except AttributeError:
                pass

        raise AttributeError()

    @property
    def prov_tax_id_qual(self) -> str:
        """
        [new FHIR mapping]
        """
        try:
            _, tax_id_qual = self._prov_tax_id_and_qual
            return tax_id_qual
        except (AttributeError, TypeError, KeyError):
            pass

        raise ClaimError('Field provTaxIDQual not found on claim.')

    @property
    def prov_tax_id(self) -> str:
        """
        [new FHIR mapping]
        """
        try:
            tax_id, _ = self._prov_tax_id_and_qual
            return tax_id
        except (AttributeError, TypeError, KeyError):
            pass

        raise ClaimError('Field provTaxID not found on claim.')

    @property
    def bill_prov_npi(self) -> str:
        """
        [new FHIR mapping]
        """
        try:
            practitioner = self._billing_provider
            for identifier in cast(List[Identifier], practitioner.identifier):
                try:
                    if identifier.system.endswith('XX'):
                        return identifier.value.strip().lower()
                except AttributeError:
                    pass
        except (AttributeError, TypeError, KeyError):
            pass

        raise ClaimError('Field billProvNPI not found on claim.')

    @property
    def bill_prov_last_name(self) -> str:
        """
        [new FHIR mapping]
        """
        try:
            practitioner = self._billing_provider
            name = cast(HumanName, practitioner.name[0])
            if name.family:
                return name.family.strip().lower()

        except (AttributeError, TypeError, KeyError):
            pass

        raise ClaimError('Field billProvLastName was not found on this claim.')

    @property
    def bill_prov_taxonomy(self) -> str:
        """
        [new FHIR mapping]
        """
        try:
            ref = cast(Reference, self.claim.provider).reference
            ref = self._cleanup(ref)
            resource = self.contained[ref]
            if resource.resource_type != 'PractitionerRole':
                raise TypeError()

            practitioner_role = cast(PractitionerRole, resource)
            specialty = cast(CodeableConcept, practitioner_role.specialty[0])
            coding = cast(Coding, specialty.coding[0])
            if coding.code:
                return coding.code.strip().lower()
        except (AttributeError, TypeError, KeyError):
            pass

        raise ClaimError('Field billProvTaxonomy was not found on this claim.')

    @property
    def patient(self) -> Patient:
        self._fields_looked_at.add('patient')
        try:
            ref = cast(Reference, self.claim.patient).reference
            ref = self._cleanup(ref)
        except AttributeError:
            raise ClaimError(f"reference to patient not found on claim")

        try:
            return cast(Patient, self.contained[ref])
        except KeyError:
            raise ClaimError(
                f"Patient with id: {ref} not found in contained objects")

    @property
    def patient_birthDate(self) -> dt.date:
        self._fields_looked_at.add('patient_birthDate')
        """
        Birth Date of patient
        """
        try:
            patient = self.patient
        except ClaimError:
            raise ClaimError("Patient not found on claim")

        try:
            birthDate = patient.birthDate
            return birthDate
        except AttributeError:
            raise ClaimError(
                f"Birthdate not found on patient with id {self.patient.id}")

    @property
    def provider(self) -> Union[Practitioner, Organization, PractitionerRole]:
        self._fields_looked_at.add('provider')
        try:
            ref = cast(Reference, self.claim.provider).reference
            ref = self._cleanup(ref)
        except AttributeError:
            raise ClaimError("reference to provider not found on the claim")
        try:
            return self.contained[ref]
        except KeyError:
            raise ClaimError(
                f"provider with id: {ref} not found in contained objects")

    def _supporting_info_category_codes(self, info: ClaimSupportingInfo) -> List[str]:
        """
        Returns:
            All codes in info.category.coding[·].code

        Raises:
            AttributeError
            TypeError
        """
        seq = info.sequence
        if seq not in self._supporting_info_category_codes_cache:
            codeable_concept = cast(CodeableConcept, info.category)
            coding = cast(List[Coding], codeable_concept.coding)
            codes = [c.code.strip().lower() for c in coding]
            self._supporting_info_category_codes_cache[seq] = codes

        return self._supporting_info_category_codes_cache[seq]

    def _supporting_info_with_given_code(self, *args: str) -> List[ClaimSupportingInfo]:
        """
        Returns:
            List containing all ClaimSupportingInfo objects in
            self.claim.supportingInfo for which key appears in
            category.coding[·].code
        """
        info_list: List[ClaimSupportingInfo] = list()
        keys = [key.strip().lower() for key in args]

        try:
            supporting_info = cast(List[ClaimSupportingInfo], self.claim.supportingInfo)
            for info in supporting_info:
                try:
                    codes = self._supporting_info_category_codes(info)
                    if any(key in codes for key in keys):
                        info_list.append(info)
                except (AttributeError, TypeError):
                    continue

        except (AttributeError, TypeError):
            pass

        return info_list

    @property
    def info_indicator(self) -> bool:
        """
        [new FHIR mapping]
        """
        self._fields_looked_at.add('info_indicator')
        info_list = self._supporting_info_with_given_code('info')
        return len(info_list) > 0

    @property
    def supporting_info(self) -> List[str]:
        """
        [new FHIR mapping]

        Returns:
            List of all possible values for supportingInfo field.

        Raises:
            ClaimError
        """
        self._fields_looked_at.add('supporting_info')
        info_list = self._supporting_info_with_given_code('info')
        all_info: Set[str] = set()

        try:
            for info in info_list:
                try:
                    codes = set(self._supporting_info_category_codes(info))
                    codes.remove('info')
                    all_info.update(codes)
                except (AttributeError, TypeError, KeyError):
                    continue

        except (AttributeError, TypeError, IndexError):
            pass

        return list(all_info)

    @property
    def cob_paid_amt(self) -> Decimal:
        """
        [new FHIR mapping]
        """
        self._fields_looked_at.add('cob_paid_amt')
        info_list = self._supporting_info_with_given_code('D')
        if len(info_list) > 1:
            raise ClaimError('Too many candidate values for field cobPaidAmt.')

        try:
            info = info_list[0]
            quantity = cast(Quantity, info.valueQuantity)
            return quantity.value
        except (AttributeError, TypeError, IndexError):
            pass

        raise ClaimError('Field cobPaidAmt not found on claim.')

    @property
    def date_current_illness(self) -> dt.date:
        """
        [new FHIR mapping]
        """
        self._fields_looked_at.add('date_current_illness')
        info_list = self._supporting_info_with_given_code('431')
        if len(info_list) > 1:
            raise ClaimError('Too many candidate values for field dateCurrentIllness.')

        try:
            info = info_list[0]
            period = cast(Period, info.timingPeriod)
            if period.start:
                return period.start

        except (AttributeError, TypeError, IndexError):
            pass

        raise ClaimError('Field dateCurrentIllness not found on claim.')

    def other_date(self, qualifier: str) -> dt.date:
        """
        [new FHIR mapping]
        """
        self._fields_looked_at.add('other_date')
        other_date_qualifiers = ('453', '454', '304', '484', '455', '471', '090', '091', '444', '050', '439')
        if qualifier not in other_date_qualifiers:
            raise ClaimError('The given qualifier is not a valid otherDateQualifier.')

        info_list = self._supporting_info_with_given_code(qualifier)
        if len(info_list) > 1:
            raise ClaimError(f'Too many candidate values for field otherDate with qualifier {qualifier}.')

        try:
            info = info_list[0]
            period = cast(Period, info.timingPeriod)
            if period.start:
                return period.start

        except (AttributeError, TypeError, IndexError):
            pass

        raise ClaimError(f'Field otherDate for qualifier {qualifier} was not found on claim.')

    @property
    def other_date_qualifier(self) -> str:
        """
        [new FHIR mapping]

        | Field name                    | Description                                        | Qualifier |
        |-------------------------------|----------------------------------------------------|:---------:|
        | accidentDate                  | Accident                                           |    439    |
        | admitDate                     | Admission                                          |    435    |
        | dateCurrentIllness            | Onset of Current Illness or Symptom                |    431    |
        | disabilityEnd                 | Disability Period End                              |    361    |
        | disabilityStart               | Disability Period Start                            |    360    |
        | disabilityStart/disabilityEnd | Disability Dates                                   |    314    |
        | dischargeDate                 | Discharge                                          |    096    |
        | otherDate                     | Initial Treatment Date                             |    454    |
        | otherDate                     | Last Seen Date                                     |    304    |
        | otherDate                     | Acute Manifestation                                |    453    |
        | otherDate                     | Last Menstrual Period                              |    484    |
        | otherDate                     | Last X-ray Date                                    |    455    |
        | otherDate                     | Hearing and Vision Prescription Date               |    471    |
        | otherDate                     | Assumed and Relinquished Care Dates - report start |    090    |
        | otherDate                     | Assumed and Relinquished Care Dates - report end   |    091    |
        | otherDate                     | Property and Casualty Date of First Contact        |    444    |
        | otherDate                     | Repricer Received Date                             |    050    |
        | workReturnDate                | Authorized Return to Work                          |    296    |
        | workStopDate                  | DateLastWorked                                     |    297    |
        """
        message = 'This field is not supposed to be accessed directly; rather, it should be passed to the ' \
                  'other_date() method, so that the desired otherDate field can be returned.'
        raise NotImplementedError(message)

    @property
    def work_stop_date(self) -> dt.date:
        """
        [new FHIR mapping]
        """
        self._fields_looked_at.add('work_stop_date')
        info_list = self._supporting_info_with_given_code('297')
        if len(info_list) > 1:
            raise ClaimError('Too many candidate values for field workStopDate.')

        try:
            info = info_list[0]
            period = cast(Period, info.timingPeriod)
            if period.start:
                return period.start

        except (AttributeError, TypeError, IndexError):
            pass

        raise ClaimError('Field workStopDate not found on claim.')

    @property
    def work_return_date(self) -> dt.date:
        """
        [new FHIR mapping]
        """
        self._fields_looked_at.add('work_return_date')
        info_list = self._supporting_info_with_given_code('296')
        if len(info_list) > 1:
            raise ClaimError('Too many candidate values for field workReturnDate.')

        try:
            info = info_list[0]
            period = cast(Period, info.timingPeriod)
            if period.end:
                return period.end

        except (AttributeError, TypeError, IndexError):
            pass

        raise ClaimError('Field workReturnDate not found on claim.')

    @property
    def admit_date(self) -> Date:
        """
        [new FHIR mapping]
        """
        self._fields_looked_at.add('admit_date')
        info_list = self._supporting_info_with_given_code('435')
        if len(info_list) > 1:
            raise ClaimError('Too many candidate values for field admitDate.')

        try:
            info = info_list[0]
            period = cast(Period, info.timingPeriod)
            if period.start:
                return period.start

        except (AttributeError, TypeError, IndexError):
            pass

        raise ClaimError("Field admitDate was not found on this claim.")

    @property
    def discharge_date(self) -> Date:
        """
        [new FHIR mapping]
        """
        self._fields_looked_at.add('discharge_date')
        info_list = self._supporting_info_with_given_code('096')
        if len(info_list) > 1:
            raise ClaimError('Too many candidate values for field dischargeDate.')

        try:
            info = info_list[0]
            period = cast(Period, info.timingPeriod)
            if period.end:
                return period.end

        except (AttributeError, TypeError, IndexError):
            pass

        raise ClaimError("Field dischargeDate was not found on this claim.")

    @property
    def attachment(self) -> bool:
        """
        [new FHIR mapping]
        """
        self._fields_looked_at.add('attachment')
        info_list = self._supporting_info_with_given_code('attachment')
        return len(info_list) > 0

    @property
    def attachments(self) -> List[str]:
        """
        [OLD MAPPING]
        """
        self._fields_looked_at.add('attachments')
        try:
            target = list()
            info_list = cast(List[ClaimSupportingInfo], self.claim.supportingInfo)
            for info in info_list:
                category = cast(CodeableConcept, info.category)
                code = cast(Coding, category.coding[0]).code
                if code == 'attachment':
                    target.append(info.valueString)
            if target:
                return target
            raise AttributeError()
        except (AttributeError, IndexError, TypeError):
            return list()

    @property
    def claim_type(self) -> str:
        self._fields_looked_at.add('claim_type')
        try:
            code = cast(Coding,
                        cast(CodeableConcept,
                             self.claim.type
                             ).coding[0]
                        ).code
            if not code:
                raise ClaimError()
            return code
        except (AttributeError, IndexError, ClaimError):
            raise ClaimError("No type found on this claim")

    @property
    # TODO(plyq): replace existing `claim_type` with this once versioning will be done.
    def claim_type_normalized(self) -> ClaimTypeFocus:
        self._fields_looked_at.add('claim_type_normalized')
        return ClaimTypeFocus.from_string(self.claim_type)

    @property
    def related_claim(self) -> str:
        """
        [new FHIR mapping]

        Confirmed by the Content Team: there can be only one value for this field.
        """
        self._fields_looked_at.add('related_claim')
        try:
            related = cast(ClaimRelated, self.claim.related[0])
            relationship = cast(CodeableConcept, related.relationship)
            coding = cast(Coding, relationship.coding[0])
            if coding.code:
                return coding.code.strip().lower()
        except (AttributeError, TypeError, IndexError):
            pass

        raise ClaimError('Field relatedClaim was not found on this claim.')


    @property
    def relatedClaimRelations(self) -> List[str]:
        """
        Legacy. Should be removed in future version.
        """
        self._fields_looked_at.add('relatedClaimRelations')
        if self.claim.related is None:
            return []

        try:
            codes = []
            for rel in self.claim.related:
                code = cast(
                    Coding,
                    cast(
                        CodeableConcept,
                        cast(
                            ClaimRelated,
                            rel
                        ).relationship
                    ).coding[0]
                ).code
                codes.append(code)
            return codes
        except (AttributeError, TypeError):
            raise ClaimError("")

    @property
    def pre_auth_ref(self) -> List[str]:
        self._fields_looked_at.add('pre_auth_ref')
        try:
            insurance = cast(List[ClaimInsurance], self.claim.insurance)
            for ins in insurance:
                if ins.sequence == 1:
                    if ins.preAuthRef:
                        return ins.preAuthRef
            raise AttributeError()
        except (AttributeError, TypeError):
            raise ClaimError('Field preAuthRef not found on claim.')

    @staticmethod
    def _cleanup(ref: str) -> str:
        return ref[1:] if ref and ref[0] == '#' else ref

    @property
    def referring_provider(self) -> Optional[Union[Practitioner, Organization]]:
        self._fields_looked_at.add('referring_provider')
        try:
            ref = cast(Reference, self.claim.referral).reference
            ref = self._cleanup(ref)
            service_request = cast(ServiceRequest, self.contained[ref])
            ref = cast(Reference, service_request.requester).reference
            ref = self._cleanup(ref)
            provider = self.contained[ref]
            if provider:
                if provider.resource_type.lower() == 'practitioner':
                    return cast(Practitioner, provider)
                if provider.resource_type.lower() == 'organization':
                    return cast(Organization, provider)
                raise AttributeError()
        except (AttributeError, KeyError, TypeError):
            raise ClaimError(f"Referring provider not found on this claim.")

    @property
    def ordering_provider(self) -> Optional[Union[Practitioner, Organization]]:
        """In the OLD FHIR mapping, there are three sets of fields that are mapped to the same
        place providerReferring*, providerOrdering* and providerSupervising*
        This is why we just make an alias to referring_provider here."""
        self._fields_looked_at.add('ordering_provider')
        return self.referring_provider

    @property
    def supervising_provider(self) -> Optional[Union[Practitioner, Organization]]:
        """In the OLD FHIR mapping, there are three sets of fields that are mapped to the same
        place providerReferring*, providerOrdering* and providerSupervising*
        This is why we just make an alias to referring_provider here."""
        self._fields_looked_at.add('supervising_provider')
        return self.referring_provider

    # noinspection DuplicatedCode
    @staticmethod
    def practitioner_identifiers(provider: Union[Practitioner, Organization]) -> Dict[str, str]:
        ids = dict()
        for prov_id in provider.identifier:
            if hasattr(prov_id, 'type') and prov_id.type:
                prov_id_type = cast(
                    Coding,
                    cast(
                        CodeableConcept,
                        prov_id.type
                    ).coding[0]
                ).code.upper()
            else:
                # The default type is assumed to be NPI
                prov_id_type = 'NPI'

            # ATTENTION: assuming each Practitioner referenced in a claim line
            #     has only one identifier of each type.
            ids[prov_id_type] = cast(
                Identifier,
                prov_id
            ).value.strip()

        return ids

    @property
    def referring_npi_number(self) -> str:
        self._fields_looked_at.add('referring_npi_number')
        referring_provider = self.referring_provider
        try:
            identifiers = self.practitioner_identifiers(referring_provider)
            return identifiers['NPI']
        except (KeyError, ClaimError):
            raise ClaimError('Field orderingNPINumber not found on this claim.')

    @property
    def ordering_npi_number(self) -> str:
        self._fields_looked_at.add('ordering_npi_number')
        return self.referring_npi_number

    @property
    def supervising_npi_number(self) -> str:
        self._fields_looked_at.add('supervising_npi_number')
        return self.referring_npi_number

    @property
    def subscriberIDs(self) -> List[str]:
        """Only used by mcr-nl-telconsultfuinp-py,
        Once that engine is fixed, it can be removed. """
        # |claim.insurance| = 1..*.
        self._fields_looked_at.add('subscriberIDs')
        if not self.claim.insurance:
            raise ClaimError("No insurance found on this claim")

        ids = []
        for ins in self.claim.insurance:
            claim_ins = cast(ClaimInsurance, ins).coverage
            try:
                ref = cast(Reference, claim_ins).reference
                cov = self.contained[ref]
            except KeyError:
                continue

            sub_id = cast(Coverage, cov).subscriberId
            if sub_id is not None:
                ids.append(sub_id)
        return ids

    @property
    def totalChargedAmount(self) -> Optional[Decimal]:
        self._fields_looked_at.add('totalChargedAmount')
        if self.claim.total:
            if cast(Money, self.claim.total).value is not None:
                return cast(Money, self.claim.total).value
        return None

    @property
    def bill_type(self) -> str:
        self._fields_looked_at.add('bill_type')
        # Claim.subType.coding.code
        try:
            code = cast(Coding,
                        cast(CodeableConcept,
                             self.claim.subType
                             ).coding[0]
                        ).code
            if not code:
                raise ClaimError()
            return code
        except (AttributeError, IndexError, ClaimError):
            raise ClaimError("No bill type found on this claim")

    @property
    def claim_num(self) -> str:
        self._fields_looked_at.add('claim_num')
        try:
            return cast(Identifier, self.claim.identifier[0]).value
        except (IndexError, AttributeError, TypeError) as exc:
            raise ClaimError("Could not find claimNum") from exc

    @property
    def hospitalized_period(self) -> Period:
        """
        Hospitalization Period for claim.

        NOTE: It is different with claim line hospitalization properties.

        Returns
        -------
            If the claim has a single hospitalizatoin timing date, both
            dates in this tuple will be same. Otherwise they will be start
            and end date of hospitalization timing period
        """
        raise NotImplementedError('PLEASE, update engine code to use admit_date and/or discharge_date'
                                  ' getters and not hospitalized_period property directly!')

    def __eq__(self, other: object) -> bool:
        """Check that claim id-s are same.

        Args:
            other: claim focus to compare

        Returns:
            True if id-s are the same

        Raises:
            NotImplementedError: if comparing with non-ClaimFocus
            ClaimError: if there are not any id.
        """
        if not isinstance(other, ClaimFocus):
            raise NotImplementedError(
                "ClaimFocus object is comparable only "
                "with another ClaimFocus object"
            )
        compare_result = ClaimComparator.compare(self.claim, other.claim)
        return compare_result == CompareResult.EQ

    @property
    def insurance(self) -> List[ClaimInsurance]:
        self._fields_looked_at.add('insurance')
        try:
            return [
                cast(ClaimInsurance, insurance)
                for insurance in self.claim.insurance
            ]
        except AttributeError:
            raise ClaimError(f"Insurance not found on claim")

    @property
    def primary_insurance(self) -> ClaimInsurance:
        self._fields_looked_at.add('primary_insurance')
        return find_primary_insurance(self.insurance, self.request)

    @property
    def subscriber_id(self) -> str:
        """
        [new FHIR mapping]
        """
        self._fields_looked_at.add('subscriber_id')
        try:
            for insurance in cast(List[ClaimInsurance], self.claim.insurance):
                if not insurance.focal:
                    continue
                ref = cast(Reference, insurance.coverage).reference
                ref = self._cleanup(ref)
                coverage = cast(Coverage, self.contained[ref])
                return coverage.subscriberId.strip().lower()
        except (AttributeError, TypeError, KeyError):
            pass

        raise ClaimError('Field subscriberId not found on claim.')

    @property
    def _subscriber_name(self) -> Optional[HumanName]:
        for insurance in cast(List[ClaimInsurance], self.claim.insurance):
            if not insurance.focal:
                continue

            ref = cast(Reference, insurance.coverage).reference
            ref = self._cleanup(ref)
            resource = self.contained[ref]
            if resource.resource_type != 'Coverage':
                break

            coverage = cast(Coverage, resource)
            ref = cast(Reference, coverage.subscriber).reference
            ref = self._cleanup(ref)
            resource = self.contained[ref]
            if resource.resource_type != 'RelatedPerson':
                break

            related_person = cast(RelatedPerson, resource)
            return cast(HumanName, related_person.name[0])

    @property
    def subscriber_first_name(self) -> str:
        """
        [new FHIR mapping]
        """
        self._fields_looked_at.add('subscriber_first_name')
        try:
            name = self._subscriber_name
            if name is not None:
                return name.given[0].strip().lower()
        except (AttributeError, TypeError, KeyError, IndexError):
            pass

        raise ClaimError('Field subscriberFirstName not found on claim.')

    @property
    def subscriber_last_name(self) -> str:
        """
        [new FHIR mapping]
        """
        self._fields_looked_at.add('subscriber_last_name')
        try:
            name = self._subscriber_name
            if name is not None:
                return name.family.strip().lower()
        except (AttributeError, TypeError, KeyError, IndexError):
            pass

        raise ClaimError('Field subscriberLastName not found on claim.')

    @property
    def relation_to_insured(self) -> str:
        """
        [new FHIR mapping]
        """
        self._fields_looked_at.add('relation_to_insured')
        try:
            for insurance in cast(List[ClaimInsurance], self.claim.insurance):
                if not insurance.focal:
                    continue
                ref = cast(Reference, insurance.coverage).reference
                ref = self._cleanup(ref)
                coverage = cast(Coverage, self.contained[ref])
                relationship = cast(CodeableConcept, coverage.relationship)
                return cast(Coding, relationship.coding[0]).code.strip().lower()
        except (AttributeError, TypeError, IndexError, KeyError):
            pass

        raise ClaimError('Field relationToInsured not found on claim.')

    @property
    def group_num(self) -> str:
        """
        Returns the Value of coverage class type "group"
        primary insurance
        :return: str
        """
        self._fields_looked_at.add('group_num')
        primary_insurance = ClaimInsuranceFocus(
            self.primary_insurance, request=self.request)
        return primary_insurance.group_number

    @property
    def group_name(self) -> str:
        """
        Returns the Name of coverage class type "group"
        primary insurance
        :return: str
        """
        self._fields_looked_at.add('group_name')
        primary_insurance = ClaimInsuranceFocus(
            self.primary_insurance, request=self.request)
        return primary_insurance.group_name

    @classmethod
    def used_fields(cls) -> Set[str]:
        return cls._fields_looked_at
