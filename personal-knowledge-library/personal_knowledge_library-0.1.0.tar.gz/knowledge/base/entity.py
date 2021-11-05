# -*- coding: utf-8 -*-
# Copyright © 2021 Wacom. All rights reserved.
import abc
import enum
from json import JSONEncoder
from typing import List, Dict, Any, Tuple, NewType, Optional, Set, Union

from knowledge import logger
from knowledge.base.access import TenantAccessRight
from knowledge.base.ontology import DataPropertyType, INVERSE_DATA_PROPERTY_TYPE_MAPPING, OntologyPropertyReference, \
    OntologyClassReference, THING_CLASS, SYSTEM_SOURCE_SYSTEM, SYSTEM_SOURCE_REFERENCE_ID

#  ---------------------------------------- Type definitions -----------------------------------------------------------
LanguageCode = NewType("LanguageCode", str)
ReferenceId = NewType("ReferenceId", str)


#  ---------------------------------------- Exceptions -----------------------------------------------------------------
class ServiceException(Exception):
    """Service exception."""
    pass


class KnowledgeException(Exception):
    """Knowledge exception."""
    pass


#  ---------------------------------------- Constants ------------------------------------------------------------------
VND_WACOM_INK_MODEL: str = 'application/vnd.wacom-knowledge.model'
RDF_SYNTAX_NS_TYPE: str = 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type'
RDF_SCHEMA_COMMENT: str = 'http://www.w3.org/2000/01/rdf-schema#comment'
RDF_SCHEMA_LABEL: str = 'http://www.w3.org/2000/01/rdf-schema#label'
ALIAS_TAG: str = 'alias'
DATA_PROPERTY_TAG: str = 'literal'
VALUE_TAG: str = 'value'
LANGUAGE_CODE_TAG: str = 'languageCode'
DATA_PROPERTIES_TAG: str = 'literals'
SOURCE_REFERENCE_ID_TAG: str = 'source_reference_id'
SOURCE_SYSTEM_TAG: str = 'source_system'
OBJECT_PROPERTIES_TAG: str = 'relations'
LOCALIZED_CONTENT_TAG: str = 'LocalizedContent'
STATUS_FLAG_TAG: str = 'status'
CONTENT_TAG: str = 'value'
URI_TAG: str = 'uri'
TYPE_TAG: str = 'type'
IMAGE_TAG: str = 'image'
DESCRIPTION_TAG: str = 'description'
COMMENT_TAG: str = 'text'
DESCRIPTIONS_TAG: str = 'descriptions'
RELATIONS_TAG: str = 'relations'
LABELS_TAG: str = 'labels'
IS_MAIN_TAG: str = 'isMain'
DATA_TYPE_TAG: str = 'dataType'
RELATION_TAG: str = 'relation'
OUTGOING_TAG: str = 'out'
INCOMING_TAG: str = 'in'
TENANT_RIGHTS_TAG: str = 'tenantRights'

# Mapping to map the simple language_code code to a default language_code / country code
language_code_mapping: Dict[str, LanguageCode] = {
    'en': LanguageCode('en_US'),
    'ja': LanguageCode('ja_JP'),
    'de': LanguageCode('de_DE'),
    'bg': LanguageCode('bg_BG')
}


class EntityStatus(enum.Enum):
    """
    Entity Status
    -------------
    Status of the entity synchronization (client and knowledge graph).
    """
    UNKNOWN = 0
    """Unkown status."""
    CREATED = 1
    """Entity has been created and not yet update."""
    UPDATED = 2
    """Entity has been updated by the client and must be synced."""
    SYNCED = 3
    """State of entity is in sync with knowledge graph."""


class LocalizedContent(abc.ABC):
    """
    Localized content
    -----------------
    Content that is multi-lingual.

    Parameters
    ----------
    content: str
        Content value
    language_code: LanguageCode (default:= 'en_US')
        ISO-3166 Country Codes and ISO-639 Language Codes in the format '<language_code>_<country>, e.g., en_US.
    """

    def __init__(self, content: str, language_code: LanguageCode = 'en_US'):
        self.__content: str = content
        self.__language_code: LanguageCode = language_code

    @property
    def content(self) -> str:
        """String representation of the content."""
        return self.__content

    @property
    def language_code(self) -> LanguageCode:
        """Language code of the content."""
        return self.__language_code

    def __repr__(self):
        return f'{self.content}@{self.language_code}'


class Label(LocalizedContent):
    """
    Label
    -----
    Label that is multi-lingual.

    Parameters
    ----------
    content: str
        Content value
    language_code: LanguageCode (default:= 'en_US')
        Language code of content
    main: bool (default:=False)
        Main content
    """
    def __init__(self, content: str, language_code: LanguageCode = 'en_US', main: bool = False):
        self.__main: bool = main
        super().__init__(content, language_code)

    @property
    def main(self) -> bool:
        """Flag if the content is the  main content or an alias."""
        return self.__main

    @staticmethod
    def create_from_dict(dict_label: Dict[str, Any]) -> 'Label':
        if CONTENT_TAG not in dict_label or LANGUAGE_CODE_TAG not in dict_label:
            raise ValueError("Dict is does not contain a localized label.")
        return Label(dict_label[CONTENT_TAG], dict_label[LANGUAGE_CODE_TAG], dict_label[IS_MAIN_TAG])

    @staticmethod
    def create_from_list(param: List[dict]) -> List[LOCALIZED_CONTENT_TAG]:
        return [Label.create_from_dict(p) for p in param]

    def __dict__(self):
        return {
            CONTENT_TAG: self.content,
            LANGUAGE_CODE_TAG: self.language_code,
            IS_MAIN_TAG: self.main
        }


class Description(LocalizedContent):
    """
    Description
    -----------
    Description that is multi-lingual.

    Parameters
    ----------
    description: str
        Description value
    language_code: LanguageCode (default:= 'en_US')
        Language code of content
    """

    def __init__(self, description: str, language_code: LanguageCode = 'en_US'):
        super().__init__(description, language_code)

    @staticmethod
    def create_from_dict(dict_description: Dict[str, Any]) -> 'Description':
        if DESCRIPTION_TAG not in dict_description or LANGUAGE_CODE_TAG not in dict_description:
            raise ValueError("Dict is does not contain a localized label.")
        return Description(dict_description[DESCRIPTION_TAG], dict_description[LANGUAGE_CODE_TAG])

    @staticmethod
    def create_from_list(param: List[Dict[str, Any]]) -> List['Description']:
        return [Description.create_from_dict(p) for p in param]

    def __dict__(self):
        return {
            DESCRIPTION_TAG: self.content,
            LANGUAGE_CODE_TAG: self.language_code,
        }


class Comment(LocalizedContent):
    """
    Comment
    -------
    Comment that is multi-lingual.

    Parameters
    ----------
    text: str
        Text value
    language_code: LanguageCode (default:= 'en_US')
        Language code of content
    """

    def __init__(self, text: str, language_code: LanguageCode = 'en_US'):
        super().__init__(text, language_code)

    @staticmethod
    def create_from_dict(dict_description: Dict[str, Any]) -> 'Comment':
        if DESCRIPTION_TAG not in dict_description or LANGUAGE_CODE_TAG not in dict_description:
            raise ValueError("Dict is does not contain a localized comment.")
        return Comment(dict_description[DESCRIPTION_TAG], dict_description[LANGUAGE_CODE_TAG])

    @staticmethod
    def create_from_list(param: List[Dict[str, Any]]) -> List['Description']:
        return [Description.create_from_dict(p) for p in param]

    def __dict__(self):
        return {
            DESCRIPTION_TAG: self.content,
            LANGUAGE_CODE_TAG: self.language_code,
        }


class EntityProperty(abc.ABC):
    """
    EntityProperty
    --------------
    Abstract class for the different types of properties.
    """
    pass


class DataProperty(EntityProperty):
    """
    DataProperty
    ------------
    Data property for entities.

    Parameter
    ---------
    content: Any
        Content
    literal_type: LiteralProperty
        OntologyPropertyReference type
    language_code: str
        Language code
    data_type: str
        Data type
    """

    def __init__(self, content: Any, property_ref: OntologyPropertyReference,
                 language_code: LanguageCode = LanguageCode('en_US'), data_type: DataPropertyType = None):
        self.__content: Any = content
        self.__language_code: LanguageCode = language_code
        self.__type: OntologyPropertyReference = property_ref
        self.__data_type: Optional[DataPropertyType] = data_type

    @property
    def data_property_type(self) -> OntologyPropertyReference:
        """Ontology type."""
        return self.__type

    @property
    def data_type(self) -> Optional[DataPropertyType]:
        """Data type (optional)."""
        return self.__data_type

    @property
    def value(self) -> Any:
        """Content of the data property."""
        return self.__content

    @property
    def language_code(self) -> LanguageCode:
        """Language code of the content."""
        return self.__language_code

    @staticmethod
    def create_from_dict(data_property_struct: dict):
        if CONTENT_TAG not in data_property_struct or \
                LANGUAGE_CODE_TAG not in data_property_struct \
                and DATA_PROPERTY_TAG not in data_property_struct:
            raise ValueError("Dict is does not contain a data_property structure.")
        data_property_type: str = data_property_struct[DATA_PROPERTY_TAG]
        data_type: DataPropertyType = DataPropertyType.STRING
        if DATA_TYPE_TAG in data_property_struct and data_property_struct[DATA_TYPE_TAG] is not None:
            if data_property_struct[DATA_TYPE_TAG] not in INVERSE_DATA_PROPERTY_TYPE_MAPPING:
                raise ValueError(f"DataProperty data type is not supported. Type: {data_type}")
            else:
                data_type = INVERSE_DATA_PROPERTY_TYPE_MAPPING[data_property_struct[DATA_TYPE_TAG]]
        return DataProperty(data_property_struct[CONTENT_TAG],
                            OntologyPropertyReference.parse(data_property_type),
                            data_property_struct[LANGUAGE_CODE_TAG], data_type)

    def __dict__(self):
        return {
            CONTENT_TAG: self.value,
            LANGUAGE_CODE_TAG: self.language_code,
            DATA_PROPERTY_TAG: self.data_property_type.iri,
            DATA_TYPE_TAG: None if self.data_type is None else self.data_type.value
        }

    def __repr__(self):
        return f'{self.value}@{self.language_code}<{self.data_property_type.name}>'

    @staticmethod
    def create_from_list(param: List[dict]) -> List['DataProperty']:
        DataProperty.create_from_dict(param[0])
        return [DataProperty.create_from_dict(p) for p in param]


class ObjectProperty(EntityProperty):
    """
    Object Property
    ---------------
    ObjectProperty for entities.

    Parameter
    ---------
    relation: OntologyPropertyReference
        OntologyPropertyReference type
    incoming: List[str] (default:= [])
        Incoming relations
    outgoing: List[str] (default:= [])
        Outgoing relations
    """

    def __init__(self, relation: OntologyPropertyReference,
                 incoming: Optional[List[Union[str, 'ThingObject']]] = None,
                 outgoing: Optional[List[Union[str, 'ThingObject']]] = None):
        self.__relation: OntologyPropertyReference = relation
        self.__incoming: List[Union[str, 'ThingObject']] = incoming if incoming is not None else []
        self.__outgoing: List[Union[str, 'ThingObject']] = outgoing if outgoing is not None else []

    @property
    def relation(self) -> OntologyPropertyReference:
        """Reference from the ontology."""
        return self.__relation

    @property
    def incoming_relations(self) -> List[Union[str, 'ThingObject']]:
        """Incoming relation"""
        return self.__incoming

    @property
    def outgoing_relations(self) -> List[Union[str, 'ThingObject']]:
        return self.__outgoing

    @staticmethod
    def create_from_dict(relation_struct: Dict[str, Any]) -> Tuple[OntologyPropertyReference, 'ObjectProperty']:
        relation_type: OntologyPropertyReference = \
            OntologyPropertyReference.parse(relation_struct[RELATION_TAG])
        incoming: List[Union[str, ThingObject]] = []

        for incoming_relation in relation_struct[INCOMING_TAG]:
            if isinstance(incoming_relation, dict):
                incoming.append(ThingObject.from_dict(incoming_relation))
            elif isinstance(incoming_relation, str):
                incoming.append(incoming_relation)

        outgoing: List[Union[str, ThingObject]] = []
        for outgoing_relation in relation_struct[OUTGOING_TAG]:
            if isinstance(outgoing_relation, dict):
                outgoing.append(ThingObject.from_dict(outgoing_relation))
            elif isinstance(outgoing_relation, str):
                outgoing.append(outgoing_relation)
        return relation_type, ObjectProperty(relation_type, incoming, outgoing)

    def __dict__(self):
        return {
            RELATION_TAG: self.relation.iri,
            INCOMING_TAG: [e.uri if isinstance(e, ThingObject) else e for e in self.incoming_relations],
            OUTGOING_TAG: [e.uri if isinstance(e, ThingObject) else e for e in self.outgoing_relations]
        }

    def __repr__(self):
        return f'{self.relation.iri}, in:={self.incoming_relations}, out:={self.outgoing_relations}'

    @staticmethod
    def create_from_list(param: List[dict]) -> Dict[OntologyPropertyReference, 'ObjectProperty']:
        return dict([ObjectProperty.create_from_dict(p) for p in param])


class ThingObject(abc.ABC):
    """
    ThingObject
    -----------
    Generic entity within knowledge graph.

    Each entity is derived from this object, thus all entity shares:
    - **uri**: A unique resource identity to identify the entity and reference it in relations
    - **label**: Human understandable label
    - **icon**: Visual representation of the entity
    - **description**: Description of entity
    - **concept_type**: Type of the concept
    - **concept_type_info**: Information on the concept type

    Parameters
    ----------
    label: List[Label]
        List of labels
    icon: str (optional)
        Icon
    description: List[Description] (optional)
        List of descriptions
    concept_type: OntologyClassReference
        Type of the concept
    uri: str
         URI for entity. For new entities the URI is None, as the knowledge graph backend assigns this.
    tenant_rights: TenantAccessRight
        Rights for tenants
    """

    def __init__(self, label: List[Label] = None, concept_type: OntologyClassReference = THING_CLASS,
                 description: Optional[List[Description]] = None, uri: Optional[str] = None, icon: Optional[str] = None,
                 tenant_rights: TenantAccessRight = TenantAccessRight()):
        self.__uri: str = uri
        self.__icon: Optional[str] = icon
        self.__label: List[Label] = label if label else []
        self.__description: List[Description] = description if description else []
        self.__alias: List[Label] = []
        self.__concept_type: OntologyClassReference = concept_type
        self.__data_properties: Dict[OntologyPropertyReference, List[DataProperty]] = {}
        self.__object_properties: Dict[OntologyPropertyReference, ObjectProperty] = {}
        self.__tenants_rights: TenantAccessRight = tenant_rights
        self.__status_flag: EntityStatus = EntityStatus.UNKNOWN
        self.__ontology_types: Optional[Set[str]] = None

    @property
    def uri(self) -> str:
        """Unique identifier for entity."""
        return self.__uri

    @uri.setter
    def uri(self, uri: str):
        self.__uri = uri

    @property
    def status_flag(self) -> EntityStatus:
        """Status flag."""
        return self.__status_flag

    @status_flag.setter
    def status_flag(self, flag: EntityStatus):
        self.__status_flag = flag

    @property
    def label(self) -> List[Label]:
        """LocalizedContent of the entity."""
        return self.__label

    @label.setter
    def label(self, value: List[Label]):
        self.__label = value

    def label_lang(self, language_code: LanguageCode) -> Optional[Label]:
        """
        Get label for language_code code.

        Parameters
        ----------
        language_code: LanguageCode
            Requested language_code code
        Returns
        -------
        label: Label
            Returns the label for a specific language_code code
        """
        for label in self.label:
            if label.language_code == language_code:
                return label
        return None

    @property
    def source_system(self) -> Optional[List[DataProperty]]:
        """Source of the entity."""
        if SYSTEM_SOURCE_SYSTEM in self.__data_properties:
            return self.__data_properties[SYSTEM_SOURCE_SYSTEM]
        return None

    def add_source_system(self, value: DataProperty):
        """
        Adding the source system  of the entity.

        Parameters
        -----------
        value: DataProperty
            Adds the source system as a Data Property. **Remark:** The data property must have the property type
            'wacom:core#sourceSystem'.
        """
        if value.data_property_type != SYSTEM_SOURCE_SYSTEM:
            raise ValueError(f'Data property {value.data_property_type.iri} not supported. '
                             f'Expected:={SYSTEM_SOURCE_SYSTEM.iri}')
        if SYSTEM_SOURCE_SYSTEM not in self.__data_properties:
            self.__data_properties[SYSTEM_SOURCE_SYSTEM] = []
        for idx in range(0, len(self.__data_properties[SYSTEM_SOURCE_SYSTEM])):
            if self.__data_properties[SYSTEM_SOURCE_SYSTEM][idx].language_code == value.language_code:
                del self.__data_properties[SYSTEM_SOURCE_SYSTEM][idx]
        self.__data_properties[SYSTEM_SOURCE_SYSTEM].append(value)

    @property
    def source_reference_id(self) -> Optional[List[DataProperty]]:
        """Reference id for to the source."""
        if SYSTEM_SOURCE_REFERENCE_ID in self.__data_properties:
            return self.__data_properties[SYSTEM_SOURCE_REFERENCE_ID]
        return None

    def add_source_reference_id(self, value: DataProperty):
        """
        Adding the reference id from the source system of the entity.

        Parameters
        -----------
        value: DataProperty
            Adds the source system reference id as a Data Property.
            **Remark:** The data property must have the property type 'wacom:core#sourceReferenceId'.
        """
        if value.data_property_type != SYSTEM_SOURCE_REFERENCE_ID:
            raise ValueError(f'Data property {value.data_property_type.iri} not supported. '
                             f'Expected:={SYSTEM_SOURCE_REFERENCE_ID.iri}')
        if SYSTEM_SOURCE_REFERENCE_ID not in self.__data_properties:
            self.__data_properties[SYSTEM_SOURCE_REFERENCE_ID] = []
        for idx in range(0, len(self.__data_properties[SYSTEM_SOURCE_REFERENCE_ID])):
            if self.__data_properties[SYSTEM_SOURCE_REFERENCE_ID][idx].language_code == value.language_code:
                del self.__data_properties[SYSTEM_SOURCE_REFERENCE_ID][idx]
        self.__data_properties[SYSTEM_SOURCE_REFERENCE_ID].append(value)

    def default_source_reference_id(self, language: LanguageCode = LanguageCode('en_US')) -> Optional[str]:
        """
        Getting the source reference id for a certain language code.

        Parameters
        ----------
        language:
        :return:
        """
        if SYSTEM_SOURCE_REFERENCE_ID in self.__data_properties:
            for sr in self.data_properties[SYSTEM_SOURCE_REFERENCE_ID]:
                if sr.language_code == language:
                    return sr.value
        return None

    @property
    def image(self) -> Optional[str]:
        """Image depicting the entities (optional)."""
        return self.__icon

    @image.setter
    def image(self, value: str):
        self.__icon = value

    @property
    def description(self) -> Optional[List[Description]]:
        """Description of the thing (optional)."""
        return self.__description

    @description.setter
    def description(self, value: List[Description]):
        self.__description = value

    def description_lang(self, language_code: str) -> Optional[Description]:
        """
        Get description for entity.

        Parameters
        ----------
        language_code: LanguageCode
            Requested language_code code
        Returns
        -------
        label: LocalizedContent
            Returns the  label for a specific language_code code
        """
        for label in self.description:
            if label.language_code == language_code:
                return label
        return None

    @property
    def concept_type(self) -> OntologyClassReference:
        """Concept type."""
        return self.__concept_type

    @concept_type.setter
    def concept_type(self, value: OntologyClassReference):
        self.__concept_type = value

    @property
    def ontology_types(self) -> Set[str]:
        """Ontology types. For public entities."""
        return self.__ontology_types

    @ontology_types.setter
    def ontology_types(self, value: Set[str]):
        self.__ontology_types = value

    @property
    def data_properties(self) -> Dict[OntologyPropertyReference, List[DataProperty]]:
        """Literals of the concept."""
        return self.__data_properties

    @data_properties.setter
    def data_properties(self, data_properties: Dict[OntologyPropertyReference, List[DataProperty]]):
        """Literals of the concept."""
        self.__data_properties = data_properties

    @property
    def object_properties(self) -> Dict[OntologyPropertyReference, ObjectProperty]:
        """Relations of the concept."""
        return self.__object_properties

    @object_properties.setter
    def object_properties(self, relations: Dict[OntologyPropertyReference, ObjectProperty]):
        self.__object_properties = relations

    @property
    def alias(self) -> List[Label]:
        """Alternative labels of the concept."""
        return self.__alias

    @alias.setter
    def alias(self, alias: List[Label]):
        self.__alias = alias

    def add_relation(self, prop: ObjectProperty):
        """Adding a relation to the entity.

        :param prop: ObjectProperty -
            ObjectProperty
        """
        if prop.relation in self.object_properties:
            self.__object_properties[prop.relation].incoming_relations.extend(prop.incoming_relations)
            self.__object_properties[prop.relation].outgoing_relations.extend(prop.outgoing_relations)
        else:
            self.__object_properties[prop.relation] = prop

    def add_data_property(self, data_property: DataProperty):
        """Add data property to the entity.

        :param data_property: DataProperty -
            DataProperty
        """
        if data_property.data_property_type not in self.__data_properties:
            self.__data_properties[data_property.data_property_type] = []
        self.__data_properties[data_property.data_property_type].append(data_property)

    def add_alias(self, alias: str, language_code: LanguageCode):
        """Adding an alias for entity.

        :param alias: str -
            Alias
        :param language_code: LanguageCode -
            Language code
        """
        self.__alias.append(Label(alias, language_code, False))

    @property
    def tenant_access_right(self) -> TenantAccessRight:
        """Access rights for tenant. """
        return self.__tenants_rights

    @tenant_access_right.setter
    def tenant_access_right(self, rights: TenantAccessRight):
        self.__tenants_rights = rights

    def __dict__(self):
        labels: List[Dict[str, Any]] = []
        labels.extend([la.__dict__() for la in self.label])
        labels.extend([la.__dict__() for la in self.alias])
        dict_object: Dict[str, Any] = {
            URI_TAG: self.uri,
            IMAGE_TAG: self.image,
            LABELS_TAG: labels,
            DESCRIPTIONS_TAG: [desc.__dict__() for desc in self.description],
            TYPE_TAG: self.concept_type.iri,
            STATUS_FLAG_TAG: self.status_flag.value,
            DATA_PROPERTIES_TAG: {},
            OBJECT_PROPERTIES_TAG: {}
        }
        for literal_type, items in self.data_properties.items():
            dict_object[DATA_PROPERTIES_TAG][literal_type.iri] = [i.__dict__() for i in items]
        for relation_type, item in self.object_properties.items():
            dict_object[OBJECT_PROPERTIES_TAG][relation_type.iri] = item.__dict__()

        return dict_object

    @staticmethod
    def from_dict(entity: Dict[str, Any]) -> 'ThingObject':
        labels: List[Label] = []
        alias: List[Label] = []
        descriptions: List[Description] = []

        for label in entity[LABELS_TAG]:
            if label[IS_MAIN_TAG]:
                labels.append(Label.create_from_dict(label))
            else:
                alias.append(Label.create_from_dict(label))

        for desc in entity[DESCRIPTIONS_TAG]:
            descriptions.append(Description.create_from_dict(desc))

        thing: ThingObject = ThingObject(label=labels, icon=entity[IMAGE_TAG], description=descriptions,
                                         uri=entity[URI_TAG],
                                         concept_type=OntologyClassReference.parse(entity[TYPE_TAG]))
        if DATA_PROPERTIES_TAG in entity:
            if isinstance(entity[DATA_PROPERTIES_TAG], dict):
                for data_property_type_str, data_properties in entity[DATA_PROPERTIES_TAG].items():
                    data_property_type: OntologyPropertyReference = \
                        OntologyPropertyReference.parse(data_property_type_str)
                    for data_property in data_properties:
                        language_code: LanguageCode = LanguageCode(data_property[LANGUAGE_CODE_TAG])
                        value: str = data_property[VALUE_TAG]
                        thing.add_data_property(DataProperty(value, data_property_type, language_code))
            elif isinstance(entity[DATA_PROPERTIES_TAG], list):
                for data_property in entity[DATA_PROPERTIES_TAG]:
                    language_code: LanguageCode = LanguageCode(data_property[LANGUAGE_CODE_TAG])
                    value: str = data_property[VALUE_TAG]
                    data_property_type: OntologyPropertyReference = \
                        OntologyPropertyReference.parse(data_property[DATA_PROPERTY_TAG])
                    thing.add_data_property(DataProperty(value, data_property_type, language_code))
        if OBJECT_PROPERTIES_TAG in entity:
            for object_property in entity[OBJECT_PROPERTIES_TAG].values():
                prop, obj = ObjectProperty.create_from_dict(object_property)
                thing.add_relation(obj)
        thing.alias = alias
        # Finally, retrieve rights
        if TENANT_RIGHTS_TAG in entity:
            thing.tenant_access_right = TenantAccessRight.parse(entity[TENANT_RIGHTS_TAG])
        return thing

    def __hash__(self):
        return 0

    def __eq__(self, other):
        # another object is equal to self, iff
        # it is an instance of MyClass
        return isinstance(other, ThingObject) and other.uri == self.uri

    def __repr__(self):
        return f'<{self.concept_type}: uri:={self.uri}, labels:={self.label}, ' \
               f'tenant access right:={self.tenant_access_right}]>'


def update_language_code(lang: str):
    return language_code_mapping.get(lang, lang)


def localized_list_description(entity_dict: Dict[str, str]) -> List[Description]:
    return [Description(cont, update_language_code(lang)) for lang, cont in entity_dict.items()]


def localized_list_label(entity_dict: Dict[str, str]) -> List[Label]:
    return [Label(cont, update_language_code(lang), main=True) for lang, cont in entity_dict.items()]


def localized_flatten_alias_list(entity_dict: Dict[str, List[str]]) -> List[Label]:
    flatten: List[Label] = []
    for language, items in entity_dict.items():
        for i in items:
            flatten.append(Label(i, update_language_code(language), main=False))
    return flatten


def from_dict(entity: Dict[str, Any], concept_type: OntologyClassReference) -> 'ThingObject':
    labels: List[Label] = localized_list_label(entity['label'])
    description: List[Description] = localized_list_description(entity['description'])
    alias: List[Label] = localized_flatten_alias_list(entity['alias'])
    if IMAGE_TAG in entity:
        icon: str = entity[IMAGE_TAG]
    else:
        logger.warning(f"Entity has no image: {entity}")
        icon: str = ''
    # Create the entity
    thing: ThingObject = ThingObject(label=labels, concept_type=concept_type, description=description, icon=icon)
    thing.alias = alias
    if STATUS_FLAG_TAG in entity:
        thing.status_flag = entity[STATUS_FLAG_TAG]
    return thing


class ThingEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, Label):
            return o.__dict__()
        elif isinstance(o, Description):
            return o.__dict__()
        elif isinstance(o, ThingObject):
            return o.__dict__()
        return str(o)


class PropertyType(enum.Enum):
    """
    PropertyType
    -----------
    Within the ontology two different property types are defined. A data- and an object property.
    """
    OBJECT_PROPERTY = "Relation"
    DATA_PROPERTY = "Literal"


INVERSE_PROPERTY_TYPE: Dict[str, PropertyType] = dict([(pt.value, pt) for pt in PropertyType])


class OntologyObject(abc.ABC):
    """
    Generic ontology object
    -----------------------

    Parameters
    ----------
    tenant_id: str
        Reference id for tenant
    iri: str
        IRI of the ontology object
    icon: str
        Icon assigned to object, visually representing it
    labels: List[Label]
        List of multi-language_code labels
    comments: List[Label]
        List of multi-language_code comments
    context: str
        Context
    """

    def __init__(self, tenant_id: str, iri: str, icon: str, labels: List[Label],
                 comments: List[Comment], context: str):
        self.__tenant_id: str = tenant_id
        self.__labels: List[Label] = labels
        self.__comments: List[Comment] = comments
        self.__iri: str = iri
        self.__icon: str = icon
        self.__context: str = context

    @property
    def tenant_id(self) -> str:
        """Tenant id."""
        return self.__tenant_id

    @property
    def iri(self) -> str:
        """IRI """
        return self.__iri

    @property
    def context(self) -> str:
        """Context."""
        return self.__context

    @property
    def icon(self) -> str:
        """Icon."""
        return self.__icon

    @icon.setter
    def icon(self, value: str):
        self.__icon = value

    @property
    def labels(self) -> List[Label]:
        return self.__labels

    def label_for_lang(self, language_code: LanguageCode) -> Optional[Label]:
        for label in self.labels:
            if label.language_code == language_code:
                return label
        return None

    @property
    def comments(self) -> List[Comment]:
        return self.__comments

    def comment_for_lang(self, language_code: LanguageCode) -> Optional[Comment]:
        for comment in self.comments:
            if comment.language_code == language_code:
                return comment
        return None


class OntologyContextSettings(object):
    """
    OntologyContextSettings
    -----------------------
    Describes the settings of the context, such as:
    - prefixes for RDF, RDFS and OWL
    - Base literal URI
    - Base class URI
    - Description literal name
    - depth
    """

    def __init__(self, rdf_prefix: str, rdfs_prefix: str, owl_prefix: str, base_literal_uri: str, base_class_uri: str,
                 description_literal_name: str, depth: int):
        self.__rdf_prefix: str = rdf_prefix
        self.__rdfs_prefix: str = rdfs_prefix
        self.__owl_prefix: str = owl_prefix
        self.__base_literal_uri: str = base_literal_uri
        self.__base_class_uri: str = base_class_uri
        self.__description_literal_name: str = description_literal_name
        self.__depth: int = depth

    @property
    def rdf_prefix(self):
        """RDF prefix"""
        return self.__rdf_prefix

    @property
    def rdfs_prefix(self):
        """RDFS prefix"""
        return self.__rdfs_prefix

    @property
    def owl_prefix(self):
        """OWL prefix"""
        return self.__owl_prefix

    @property
    def base_literal_uri(self):
        """Base literal URI."""
        return self.__base_literal_uri

    @property
    def base_class_uri(self):
        """Base class URI."""
        return self.__base_class_uri

    @property
    def description_literal_name(self) -> str:
        """Literal name of the description."""
        return self.__description_literal_name

    @property
    def depth(self) -> int:
        """Depth."""
        return self.__depth


class OntologyContext(OntologyObject):
    """
    OntologyContext
    ----------------
    Ontology context representation.

    Parameters
    ----------
    cid: str
        Context id
    tenant_id: str
        Tenant id.
    name: str
        Name of the ontology context
    icon: str
        Icon or Base64 encoded
    labels: List[Label]
        List of labels
    comments: List[Comment]
        List of comments
    last_update:
        Last update
    context: str
        context name
    base_uri: str
        Base URI
    """

    def __init__(self, cid: str, tenant_id: str, name: str, icon: str, labels: List[Label],
                 comments: List[Comment], last_update: str, context: str, base_uri: str, version: int,
                 settings: OntologyContextSettings):
        self.__id = cid
        self.__base_uri: str = base_uri
        self.__version: int = version
        self.__last_update: str = last_update
        self.__settings: OntologyContextSettings = settings
        super().__init__(tenant_id, name, icon, labels, comments, context)

    @property
    def id(self) -> str:
        return self.__id

    @property
    def base_uri(self) -> str:
        return self.__base_uri

    @classmethod
    def from_dict(cls, context_dict: Dict[str, Any]):
        context_data: Dict[str, Any] = context_dict['data']
        context_settings: Dict[str, Any] = context_data['settings']
        labels: List[Label] = [] if context_data['labels'] is None else \
            [Label(content=la['text'], language_code=la['locale']) for la in context_data['labels']]
        comments: List[Comment] = [] if context_data['comments'] is None else \
            [Comment(text=la['text'], language_code=la['locale']) for la in context_data['comments']]
        settings: OntologyContextSettings = OntologyContextSettings(
            context_settings['rdfPrefix'], context_settings['rdfsPrefix'], context_settings['owlPrefix'],
            context_settings['baseLiteralUri'], context_settings['baseClassUri'],
            context_settings['descriptionLiteralName'], context_settings['depth']
        )
        return OntologyContext(context_data['id'], context_data['tenantId'], context_data['name'],
                               context_data['icon'], labels, comments, context_data['lastUpdated'],
                               context_data['context'], context_data['baseURI'], context_dict['version'],
                               settings)

    def __repr__(self):
        return f'<OntologyContext> - [id:={self.id}, iri:={self.iri}]'


class OntologyClass(OntologyObject):
    """
    OntologyClass
    ----------------
    Concept for ontology.

    Parameters
    ----------
    tenant_id: str
        Tenant id for ontology
    context: str
        Context
    reference: OntologyClassReference
        Reference for ontology class
    icon: str
        Icon representing concept
    labels: List[Label]
        List of labels
    comments: List[Comment]
        List of comments

    subclass_of: str (default: None)
        Subclass of ontology class
    """

    def __init__(self, tenant_id: str, context: str, reference: OntologyClassReference,
                 subclass_of: OntologyClassReference = None, icon: Optional[str] = None,
                 labels: Optional[List[Label]] = None, comments: Optional[List[Comment]] = None):
        self.__subclass_of: OntologyClassReference = subclass_of
        self.__reference: OntologyClassReference = reference
        super().__init__(tenant_id, reference.iri, icon, labels, comments, context)

    @property
    def subclass_of(self) -> Optional[OntologyClassReference]:
        """
        Superclass of the class.
        """
        return self.__subclass_of

    @property
    def reference(self) -> OntologyClassReference:
        """
        Reference of ontology class.
        """
        return self.__reference

    def __repr__(self):
        return f'<OntologyClass> - [reference:={self.reference}, subclass_of:={self.subclass_of}]'

    @classmethod
    def from_dict(cls, concept_dict: Dict[str, Any]):
        labels: List[Label] = [] if concept_dict['labels'] is None else \
            [Label(content=la['text'], language_code=la['locale']) for la in concept_dict['labels']]
        comments: List[Comment] = [] if concept_dict['comments'] is None else \
            [Comment(text=la['text'], language_code=la['locale']) for la in concept_dict['comments']]
        return OntologyClass(tenant_id=concept_dict['tenantId'], context=concept_dict['context'],
                             reference=OntologyClassReference.parse(concept_dict['name']),
                             subclass_of=OntologyClassReference.parse(concept_dict['subClassOf']),
                             icon=concept_dict['icon'], labels=labels, comments=comments)

    @classmethod
    def new(cls) -> 'OntologyClass':
        return OntologyClass('', '', THING_CLASS)


class OntologyProperty(OntologyObject):
    """
    Ontology Property
    -----------------
    Property ontology object.

    Parameters
    ----------
    kind: str
        Kind of relation
    tenant_id: str
        Tenant id
    context: str
        Context
    name: OntologyPropertyReference
        Name of property object
    icon: str
        Icon describing the property
    property_domain: OntologyClassReference
        Domain for the property
    property_range: OntologyClassReference
        Range for the property
    labels: List[Label]
        List of labels (localized)
    comments: List[Comment],
        List of comments
    subproperty_of: str (default: = None)
        Subproperty
    inverse_property_of: str (optional)
        Inverse property
    """

    def __init__(self, kind: PropertyType, tenant_id: str, context: str, name: OntologyPropertyReference,
                 icon: str = None,
                 property_domain: Optional[OntologyClassReference] = None,
                 property_range: Optional[OntologyClassReference] = None,
                 labels: Optional[List[Label]] = None,
                 comments: Optional[List[Comment]] = None,
                 subproperty_of: Optional[OntologyPropertyReference] = None,
                 inverse_property_of: Optional[OntologyPropertyReference] = None):
        self.__kind: PropertyType = kind
        self.__subproperty_of: OntologyPropertyReference = subproperty_of
        self.__inverse_property_of: OntologyPropertyReference = inverse_property_of
        self.__domain: OntologyClassReference = property_domain
        self.__range: OntologyClassReference = property_range
        super().__init__(tenant_id, name.iri, icon, labels, comments, context)

    @property
    def is_data_property(self) -> bool:
        return self.kind != PropertyType.OBJECT_PROPERTY

    @property
    def kind(self) -> PropertyType:
        """Kind of the property."""
        return self.__kind

    @property
    def subproperty_of(self) -> OntologyPropertyReference:
        """Reference to the super property"""
        return self.__subproperty_of

    @property
    def inverse_property_of(self) -> OntologyPropertyReference:
        """Reference to the inverse property"""
        return self.__inverse_property_of

    @property
    def domain(self) -> OntologyClassReference:
        """Domain of the property."""
        return self.__domain

    @property
    def range(self) -> OntologyClassReference:
        return self.__range

    def __repr__(self):
        return f'<OntologyProperty> - [name:= {self.iri} domain:={self.domain}, range:={self.range}, ' \
               f'subproperty_of:={self.subproperty_of}, type:={self.kind}]'

    @classmethod
    def from_dict(cls, property_dict: Dict[str, Any]):
        labels: List[Label] = [] if property_dict[LABELS_TAG] is None else \
            [Label(content=la['text'], language_code=la['locale']) for la in property_dict[LABELS_TAG]]
        comments: List[Comment] = [] if property_dict['comments'] is None else \
            [Comment(text=la['text'], language_code=la['locale']) for la in property_dict['comments']]
        return OntologyProperty(INVERSE_PROPERTY_TYPE[property_dict['kind']],
                                property_dict['tenantId'], property_dict['context'],
                                OntologyPropertyReference.parse(property_dict['name']),
                                property_dict['icon'],
                                OntologyClassReference.parse(property_dict['domain'])
                                if property_dict['domain'] is not None else None,
                                OntologyClassReference.parse(property_dict['range'])
                                if property_dict['range'] is not None else None,
                                labels, comments,
                                OntologyPropertyReference.parse(property_dict['subPropertyOf'])
                                if property_dict['subPropertyOf'] is not None else None,
                                OntologyPropertyReference.parse(property_dict['inverseOf'])
                                if property_dict['inverseOf'] is not None else None)

    @classmethod
    def new(cls, kind: PropertyType) -> 'OntologyProperty':
        return OntologyProperty(kind, '', '',
                                OntologyPropertyReference.parse('http://www.w3.org/2002/07/owl#topObjectProperty'))
