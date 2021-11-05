# -*- coding: utf-8 -*-
# Copyright © 2021 Wacom. All rights reserved.
import abc
import enum

# Vocabulary prefix
from typing import Dict, Tuple

PREFIX: str = "xsd"

# Vocabulary base URI
BASE_URI: str = "http://www.w3.org/2001/XMLSchema#"


class DataPropertyType(enum.Enum):
    """
    DataPropertyType.
    -----------------
    Data types that are used by Datatype properties.
    """
    STRING = BASE_URI + "string"
    """Character strings (but not all Unicode character strings) """
    BOOLEAN = BASE_URI + "boolean"
    """boolean: true, false"""
    DECIMAL = BASE_URI + "decimal"
    """Arbitrary-precision decimal numbers"""
    INTEGER = BASE_URI + "integer"
    """Arbitrary-size integer numbers"""
    DOUBLE = BASE_URI + "double"
    """64-bit floating point numbers incl. ±Inf, ±0, NaN"""
    FLOAT = BASE_URI + "float"
    """32-bit floating point numbers incl. ±Inf, ±0, NaN"""
    DATE = BASE_URI + "date"
    """Dates (yyyy-mm-dd) with or without timezone"""
    TIME = BASE_URI + "time"
    """Times (hh:mm:ss.sss…) with or without timezone"""
    DATE_TIME = BASE_URI + "dateTime"
    """Date and time with or without timezone"""
    DATE_TIMESTAMP = BASE_URI + "dateTimeStamp"
    """Date and time with required timezone """
    G_YEAR = BASE_URI + "gYear"
    """Gregorian calendar year"""
    G_MONTH = BASE_URI + "gMonth"
    """Gregorian calendar month"""
    G_DAY = BASE_URI + "gDay"
    """Gregorian calendar day of the month"""
    G_YEAR_MONTH = BASE_URI + "gYearMonth"
    """Gregorian calendar year and month"""
    G_MONTH_DAY = BASE_URI + "gMonthDay"
    """Gregorian calendar month and day"""
    DURATION = BASE_URI + "duration"
    """Duration of time"""
    YEAR_MONTH_DURATION = BASE_URI + "yearMonthDuration"
    """Duration of time (months and years only)"""
    DAYTIME_DURATION = BASE_URI + "dayTimeDuration"
    """Duration of time (days, hours, minutes, seconds only)"""
    BYTES = BASE_URI + "byte"
    """-128…+127 (8 bit)"""
    SHORT = BASE_URI + "short"
    """-32768… + 32767 (16 bit)"""
    INT = BASE_URI + "int"
    """-2147483648…+2147483647 (32 bit)"""
    LONG = BASE_URI + "long"
    """-9223372036854775808…+9223372036854775807 (64 bit)"""
    UNSIGNED_BYTE = BASE_URI + "unsignedByte"
    """0 … 255 (8 bit)"""
    UNSIGNED_SHORT = BASE_URI + "unsignedShort"
    """0 … 65535 (16 bit)"""
    UNSIGNED_INT = BASE_URI + "unsignedInt"
    """ 0 … 4294967295 (32 bit)"""
    UNSIGNED_LONG = BASE_URI + "unsignedLong"
    """  0 … 18446744073709551615 (64 bit)"""
    POSITIVE_INTEGER = BASE_URI + "positiveInteger"
    """Integer numbers > 0 """
    NON_NEGATIVE_INTEGER = BASE_URI + "nonNegativeInteger"
    """Integer numbers ≥ 0"""
    NEGATIVE_INTEGER = BASE_URI + "negativeInteger"
    """Integer numbers ≤ 0"""
    NON_POSITIVE_INTEGER = BASE_URI + "nonPositiveInteger"
    """Integer numbers ≤ 0"""
    HEX_BINARY = BASE_URI + "hexBinary"
    """Hex-encoded binary data"""
    BASE64_BINARY = BASE_URI + "base64Binary"
    """Base64-encoded binary data"""
    ANY_URI = BASE_URI + "anyURI"
    """Absolute or relative URIs and IRIs"""
    LANGUAGE = BASE_URI + "language_code"
    """Language tags per http://tools.ietf.org/html/bcp47"""
    NORMALIZED = BASE_URI + "normalizedString"
    """Whitespace-normalized strings"""
    TOKEN = BASE_URI + "token"
    """Tokenized strings"""
    NM_TOKEN = BASE_URI + "NMTOKEN"
    """XML NMTOKENs"""
    NAME = BASE_URI + "Name"
    """XML Names"""
    NC_NAME = BASE_URI + "NCName"
    """XML NCNames"""


INVERSE_DATA_PROPERTY_TYPE_MAPPING: Dict[str, DataPropertyType] = dict([(lit_type.value, lit_type)
                                                                        for lit_type in DataPropertyType])
"""Maps the string representation of the XSD data types to the data types enum constants."""


# ------------------------------------------ Ontology References -------------------------------------------------------

class OntologyObjectReference(abc.ABC):
    """
        Ontology class type
        ------------------
        Associated to an entity to link the type of the entity.

        Parameters
        ----------
        scheme: str
            Scheme or owner of the ontology object
        context: str
            Context of ontology object
        name: str
            Ontology object reference name
    """

    def __init__(self, scheme: str, context: str, name: str):
        self.__scheme: str = scheme
        self.__context: str = context
        self.__name: str = name

    @property
    def scheme(self):
        """Scheme."""
        return self.__scheme

    @property
    def context(self):
        """Context."""
        return self.__context

    @property
    def name(self):
        """Name."""
        return self.__name

    @property
    def iri(self):
        """Internationalized Resource Identifier (IRI) encoded ontology class name."""
        return f'{self.scheme}:{self.context}#{self.name}'

    def __repr__(self):
        return self.iri

    @classmethod
    def parse_iri(cls, iri: str) -> Tuple[str, str, str]:
        colon_idx: int = iri.index(':')
        hash_idx: int = iri.index('#')
        scheme: str = iri[:colon_idx]
        context: str = iri[colon_idx + 1:hash_idx]
        name: str = iri[hash_idx + 1:]
        return scheme, context, name


class OntologyClassReference(OntologyObjectReference):
    """
    Ontology class type
    -------------------
    Associated to an ontology class.

    Parameters
    ----------
    scheme: str
        Scheme or owner
    context: str
        Context of class
    class_name: str
        Class name
    """

    def __init__(self, scheme: str, context: str, class_name: str):
        super().__init__(scheme, context, class_name)

    @property
    def class_name(self):
        """Class name."""
        return self.name

    @classmethod
    def parse(cls, iri: str) -> 'OntologyClassReference':
        scheme, context, name = OntologyObjectReference.parse_iri(iri)
        return OntologyClassReference(scheme, context, name)

    def __eq__(self, other):
        if not isinstance(other, OntologyClassReference):
            return False
        return self.iri == other.iri

    def __hash__(self):
        return hash(self.iri)


class OntologyPropertyReference(OntologyObjectReference):
    """
    Property reference
    ------------------
    Associated to an ontology property.

    Parameters
    ----------
    scheme: str
        Scheme or owner
    context: str
        Context of class
    property_name: str
        Property name
    """

    def __init__(self, scheme: str, context: str, property_name: str):
        super().__init__(scheme, context, property_name)

    @property
    def property_name(self):
        """Property name."""
        return self.name

    @classmethod
    def parse(cls, iri: str) -> 'OntologyPropertyReference':
        scheme, context, name = OntologyObjectReference.parse_iri(iri)
        return OntologyPropertyReference(scheme, context, name)

    def __eq__(self, other):
        if not isinstance(other, OntologyPropertyReference):
            return False
        return self.iri == other.iri

    def __hash__(self):
        return hash(self.iri)


# ------------------------------------------------- Constants ----------------------------------------------------------
THING_CLASS: OntologyClassReference = OntologyClassReference('wacom', 'core', 'Thing')
SYSTEM_SOURCE_SYSTEM: OntologyPropertyReference = OntologyPropertyReference('wacom', 'core', 'sourceSystem')
SYSTEM_SOURCE_REFERENCE_ID: OntologyPropertyReference = OntologyPropertyReference('wacom', 'core', 'sourceReferenceId')
