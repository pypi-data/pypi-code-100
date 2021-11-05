# -*- coding: utf-8 -*-
# Copyright © 2021 Wacom. All rights reserved.
import enum
import urllib.parse
from typing import List, Dict, Any, Tuple

import requests
from requests import Response

from knowledge.base.entity import ThingObject, OntologyClassReference, LocalizedContent, OntologyPropertyReference, \
    DataProperty, ObjectProperty, TenantAccessRight, LanguageCode, DATA_PROPERTIES_TAG, DATA_PROPERTY_TAG, \
    LANGUAGE_CODE_TAG, VALUE_TAG, IMAGE_TAG, DESCRIPTION_TAG, TYPE_TAG, URI_TAG, LABELS_TAG, IS_MAIN_TAG, \
    DESCRIPTIONS_TAG, RELATIONS_TAG, EntityStatus, Label
from knowledge.services.base import WacomServiceAPIClient, WacomServiceException

# ------------------------------------------------- Constants ----------------------------------------------------------
SEARCH_TERM: str = 'searchTerm'
TEXT_TAG: str = 'text'
LANGUAGE_PARAMETER: str = 'language'
TYPES_PARAMETER: str = 'types'
LIMIT_PARAMETER: str = 'limit'
AUTHORIZATION_HEADER_FLAG: str = 'Authorization'
CONTENT_TYPE_HEADER_FLAG: str = 'Content-Type'
LISTING: str = 'listing'
TOTAL_COUNT: str = 'totalCount'
TARGET: str = 'target'
OBJECT: str = 'object'
PREDICATE: str = 'predicate'
SUBJECT: str = 'subject'
LIMIT: str = 'limit'
OBJECT_URI: str = 'objectUri'
RELATION_URI: str = 'relationUri'
SUBJECT_URI: str = 'subjectUri'
NEXT_PAGE_ID_TAG: str = 'nextPageId'
TENANT_RIGHTS_TAG: str = 'tenantRights'
RELATION_TAG: str = 'relation'


# ------------------------------- Enum ---------------------------------------------------------------------------------
class SearchPattern(enum.Enum):
    """
    SearchPattern
    -------------
    Different search pattern for literal search.
    """
    REGEX = 'regex'
    GT = 'gt'
    GTE = 'gte'
    LT = 'lt'
    LTE = 'lte'
    EQ = 'eq'
    RANGE = 'range'


# -------------------------------------------- Service API Client ------------------------------------------------------
class WacomKnowledgeService(WacomServiceAPIClient):
    """
    WacomKnowledgeService
    ---------------------
    Client for the Semantic Ink Privat knowledge system.

    Operations for concepts:
        - Creation of concepts
        - Update of concepts
        - Deletion of concepts
        - Listing of concepts

    Parameters
    ----------
    application_name: str
        Name of the application using the service
    service_url: str
        URL of the service
    service_endpoint: str
        Base endpoint
    """
    PERSONAL_KNOWLEDGE_URL: str = 'https://semantic-ink-private.wacom.com'
    USER_ENDPOINT: str = 'user'
    CONCEPT_ENDPOINT: str = 'entity'
    ACTIVATIONS_ENDPOINT: str = 'entity/activations'
    DELETION_ENDPOINT: str = 'entity/{}'
    LABELS_ENDPOINT: str = 'entity/{}/labels'
    LISTING_ENDPOINT: str = 'entity/types'
    LITERAL_ENDPOINT: str = 'entity/{}/literals'
    RELATION_ENDPOINT: str = 'entity/{}/relation'
    RELATIONS_ENDPOINT: str = 'entity/{}/relations'
    SEARCH_LABELS_ENDPOINT: str = "semantic-search/labels"
    SEARCH_TYPES_ENDPOINT: str = "semantic-search/types"
    SEARCH_LITERALS_ENDPOINT: str = "semantic-search/literal"
    SEARCH_DESCRIPTION_ENDPOINT: str = "semantic-search/description"
    SEARCH_RELATION_ENDPOINT: str = "semantic-search/relation"
    ONTOLOGY_UPDATE_ENDPOINT: str = 'ontology-update'

    def __init__(self, application_name: str, service_url: str = PERSONAL_KNOWLEDGE_URL,
                 service_endpoint: str = 'graphdata'):
        super().__init__(application_name, service_url, service_endpoint)

    def entity(self, auth_key: str, uri: str) -> ThingObject:
        """
        Retrieve entity information from personal knowledge, using the  URI as identifier.

        **Remark:** Object properties (relations) must be requested separately.

        Parameters
        ----------
        auth_key: str
            Auth key identifying a user within the Wacom personal knowledge service.
        uri: str
            URI of concept

        Returns
        -------
        thing: ThingObject
            Entity with is type URI, description, an image/icon, and tags (labels).

        Raises
        ------
        WacomServiceException
            If the graph service returns an error code or the entity is not found in the knowledge graph
        """
        url: str = f'{self.service_base_url}{WacomKnowledgeService.CONCEPT_ENDPOINT}/{urllib.parse.quote(uri)}'
        headers: Dict[str, str] = {
            AUTHORIZATION_HEADER_FLAG: f'Bearer {auth_key}'
        }
        response: Response = requests.get(url, headers=headers, verify=self.verify_calls)
        if response.ok:
            e: Dict[str, Any] = response.json()
            pref_label: List[LocalizedContent] = []
            aliases: List[LocalizedContent] = []
            # Extract labels and alias
            for label in e[LABELS_TAG]:
                if label[IS_MAIN_TAG]:  # Labels
                    pref_label.append(self.__import_locale__(label))
                else:  # Alias
                    aliases.append(self.__import_locale__(label))
            # Create ThingObject
            thing: ThingObject = ThingObject(label=pref_label, icon=e[IMAGE_TAG],
                                             description=[self.__import_locale__(d, DESCRIPTION_TAG)
                                                          for d in e[DESCRIPTIONS_TAG]],
                                             concept_type=OntologyClassReference.parse(e[TYPE_TAG]),
                                             uri=e[URI_TAG])
            # Set the alias
            thing.alias = aliases
            # Configure data properties
            if DATA_PROPERTIES_TAG in e:
                for data_property in e[DATA_PROPERTIES_TAG]:
                    data_property_type: OntologyPropertyReference = \
                        OntologyPropertyReference.parse(data_property[DATA_PROPERTY_TAG])
                    language_code: LanguageCode = data_property[LANGUAGE_CODE_TAG]
                    value: str = data_property[VALUE_TAG]
                    thing.add_data_property(DataProperty(value, data_property_type, language_code))
            # Tenant rights
            if TENANT_RIGHTS_TAG in e:
                thing.tenant_access_right = TenantAccessRight.parse(e[TENANT_RIGHTS_TAG])
            else:
                thing.tenant_access_right = TenantAccessRight()
            return thing
        raise WacomServiceException(f'Pushing concept failed. '
                                    f'Response code:={response.status_code}, exception:= {response.content}')

    def delete_entities(self, auth_key: str, uris: List[str], force: bool = False):
        """
        Delete a list of entities.

        Parameters
        ----------
        auth_key: str
            Auth key from user
        uris: List[str]
            List of URI of concepts. **Remark:** More than 100 entities are not possible in one request
        force: bool
            Force deletion process

        Raises
        ------
        WacomServiceException
            If the graph service returns an error code
        """
        if len(uris) > 100:
            raise WacomServiceException("Please delete less than 100 entities.")
        url: str = f'{self.service_base_url}{WacomKnowledgeService.CONCEPT_ENDPOINT}'
        headers: Dict[str, str] = {
            AUTHORIZATION_HEADER_FLAG: f'Bearer {auth_key}'
        }
        params: Dict[str, Any] = {
            'uris': uris,
            'forceDelete': force
        }
        response: Response = requests.delete(url, headers=headers, params=params, verify=self.verify_calls)
        if not response.ok:
            raise WacomServiceException(f'Deletion of concept failed.'
                                        f'Response code:={response.status_code}, exception:= {response.content}')

    def delete_entity(self, auth_key: str, uri: str, force: bool = False):
        """
        Deletes a entity.

        Parameters
        ----------
        auth_key: str
            Auth key from user
        uri: str
            URI of concept
        force: bool
            Force deletion process

        Raises
        ------
        WacomServiceException
            If the graph service returns an error code
        """
        url: str = f'{self.service_base_url}{WacomKnowledgeService.DELETION_ENDPOINT.format(urllib.parse.quote(uri))}'
        headers: Dict[str, str] = {
            AUTHORIZATION_HEADER_FLAG: f'Bearer {auth_key}'
        }
        response: Response = requests.delete(url, headers=headers, params={'forceDelete': force},
                                             verify=self.verify_calls)
        if not response.ok:
            raise WacomServiceException('Deletion of concept failed. Response code:={}, exception:= {}'
                                        .format(response.status_code,
                                                response.content))

    def exists(self, auth_key: str, uri: str) -> bool:
        """
        Check if entity exists in knowledge graph.

        Parameters
        ----------
        auth_key: str -
            User token
        uri: str -
            URI for entity

        Returns
        -------
        flag: bool
            Flag if entity does exist
        """
        try:
            obj: ThingObject = self.entity(auth_key, uri)
            return obj is not None
        except WacomServiceException:
            return False

    def create_entity(self, auth_key: str, concept: ThingObject):
        """
        Creates concept in graph.

        Parameters
        ----------
        auth_key: str
            Auth key from user
        concept: ThingObject
            Concept object

        Returns
        -------
        uri: str
            URI of entity

        Raises
        ------
        WacomServiceException
            If the graph service returns an error code
        """
        url: str = f'{self.service_base_url}{WacomKnowledgeService.CONCEPT_ENDPOINT}'
        # Different localized content
        labels: List[dict] = []
        descriptions: List[dict] = []
        literals: List[dict] = []
        # Header info
        headers: dict = {
            'Content-Type': 'application/json',
            AUTHORIZATION_HEADER_FLAG: f'Bearer {auth_key}'
        }
        # Add description in different languages
        for desc in concept.description:
            if len(desc.content) > 0 and not desc.content == ' ':
                descriptions.append({
                    DESCRIPTION_TAG: desc.content,
                    LANGUAGE_CODE_TAG: desc.language_code
                })
        if len(descriptions) == 0:
            #  Adding an empty description
            for label in concept.label:
                if len(label.content) > 0 and not label.content == ' ':
                    descriptions.append({
                        DESCRIPTION_TAG: f'Description of {label.content}',
                        LANGUAGE_CODE_TAG: label.language_code
                    })

        # Labels are tagged as main label
        for label in concept.label:
            if len(label.content) > 0 and label.content != " ":
                labels.append({
                    'value': label.content,
                    LANGUAGE_CODE_TAG: label.language_code,
                    'isMain': True
                })
        # Alias are no main labels
        for label in concept.alias:
            if len(label.content) > 0 and label.content != " ":
                labels.append({
                    'value': label.content,
                    LANGUAGE_CODE_TAG: label.language_code,
                    'isMain': False
                })
        # Labels are tagged as main label
        for literal_property, list_literals in concept.data_properties.items():
            for li in list_literals:
                if li.data_property_type:
                    literals.append({
                        'value': li.value,
                        LANGUAGE_CODE_TAG: li.language_code,
                        DATA_PROPERTY_TAG: li.data_property_type.iri
                    })
        payload: dict = {
            TYPE_TAG: concept.concept_type.iri,
            DESCRIPTIONS_TAG: descriptions,
            IMAGE_TAG: concept.image,
            LABELS_TAG: labels,
            DATA_PROPERTIES_TAG: literals
        }
        if concept.tenant_access_right:
            payload['tenantRights'] = concept.tenant_access_right.to_list()
        response: Response = requests.post(url, json=payload, headers=headers, verify=self.verify_calls)
        if response.ok:
            uri: str = response.json()[URI_TAG]
            return uri

        import json
        raise WacomServiceException(f'Pushing concept failed. '
                                    f'Response code:={response.status_code}, exception:= {response.content}. '
                                    f'Payload: \n{json.dumps(payload, indent=4)}')

    def relations(self, auth_key: str, uri: str) -> Dict[OntologyPropertyReference, ObjectProperty]:
        """
        Retrieve the relations (object properties) of an entity.

        Parameters
        ----------
        auth_key: str
            Auth key from user
        uri: str
            Entity URI of the source

        Returns
        -------
        relations: Dict[OntologyPropertyReference, ObjectProperty]
            All relations a dict

        Raises
        ------
        WacomServiceException
            If the graph service returns an error code
        """
        url: str = f'{self.service_base_url}{WacomKnowledgeService.RELATIONS_ENDPOINT.format(urllib.parse.quote(uri))}'
        headers: dict = {
            AUTHORIZATION_HEADER_FLAG: f'Bearer {auth_key}'
        }
        response: Response = requests.get(url, headers=headers, verify=self.verify_calls)
        if response.ok:
            rel: list = response.json().get(RELATIONS_TAG)
            return ObjectProperty.create_from_list(rel)
        raise WacomServiceException(f'Failed to pull relations. '
                                    f'Response code:={response.status_code}, exception:= {response.content}')

    def labels(self, auth_key: str, uri: str) -> List[LocalizedContent]:
        """
        Extract list labels of entity.

        Parameters
        ----------
        auth_key: str
            Auth key from user
        uri: str
            Entity URI of the source

        Returns
        -------
        labels: List[LocalizedContent]
            List of labels of an entity.

        Raises
        ------
        WacomServiceException
            If the graph service returns an error code
        """
        url: str = f'{self.service_base_url}{WacomKnowledgeService.LABELS_ENDPOINT.format(urllib.parse.quote(uri))}'
        headers: dict = {
            AUTHORIZATION_HEADER_FLAG: f'Bearer {auth_key}'
        }
        response: Response = requests.get(url, headers=headers, verify=self.verify_calls)
        if response.ok:
            response_dict: dict = response.json()
            if LABELS_TAG in response_dict:
                return [self.__import_locale__(label) for label in response_dict[LABELS_TAG]]
            return []
        raise WacomServiceException('Failed to pull literals. Response code:={}, exception:= {}'
                                    .format(response.status_code, response.content))

    def literals(self, auth_key: str, uri: str) -> List[DataProperty]:
        """
        Collect all literals of entity.

        Parameters
        ----------
        auth_key: str
            Auth key from user
        uri: str
            Entity URI of the source

        Returns
        -------
        labels: List[LocalizedContent]
            List of literals of an entity.

        Raises
        ------
        WacomServiceException
            If the graph service returns an error code
        """
        url: str = f'{self.service_base_url}{WacomKnowledgeService.LITERAL_ENDPOINT.format(urllib.parse.quote(uri))}'
        headers: dict = {
            AUTHORIZATION_HEADER_FLAG: f'Bearer {auth_key}'
        }
        response: Response = requests.get(url, headers=headers, verify=self.verify_calls)
        if response.ok:
            literals: list = response.json().get(DATA_PROPERTIES_TAG)
            return DataProperty.create_from_list(literals)
        raise WacomServiceException('Failed to pull literals. Response code:={}, exception:= {}'
                                    .format(response.status_code, response.content))

    def create_relation(self, auth_key: str, source: str, relation: OntologyPropertyReference, target: str):
        """
        Creates a relation for a entity to a source entity.

        Parameters
        ----------
        auth_key: str
            Auth key from user
        source: str
            Entity URI of the source
        relation: OntologyPropertyReference
            ObjectProperty property
        target: str
            Entity URI of the target

        Raises
        ------
        WacomServiceException
            If the graph service returns an error code
        """
        url: str = f'{self.service_base_url}{WacomKnowledgeService.RELATION_ENDPOINT.format(source)}'
        headers: dict = {
            AUTHORIZATION_HEADER_FLAG: f'Bearer {auth_key}'
        }
        params: dict = {
            RELATION_TAG: relation.iri,
            TARGET: target
        }
        response: Response = requests.post(url, params=params, headers=headers, verify=self.verify_calls)
        if not response.ok:
            import json
            raise WacomServiceException(f'Create relations failed. '
                                        f'Response code:={response.status_code}, exception:= {response.content}. '
                                        f'URL: {url}'
                                        f'Parameters: \n{json.dumps(params, indent=4)}')

    def remove_relation(self, auth_key: str, source: str, relation: OntologyPropertyReference, target: str):
        """
        Removes a relation.

        Parameters
        ----------
        auth_key: str
            Auth key from user
        source: str
            Entity uri of the source
        relation: OntologyPropertyReference
            ObjectProperty property
        target: str
            Entity uri of the target

        Raises
        ------
        WacomServiceException
            If the graph service returns an error code
        """
        url: str = f'{self.service_base_url}' \
                   f'{WacomKnowledgeService.RELATION_ENDPOINT.format(urllib.parse.quote(source))}'
        params: Dict[str, str] = {
            RELATION_TAG: relation.iri,
            TARGET: target
        }
        headers: Dict[str, str] = {
            AUTHORIZATION_HEADER_FLAG: f'Bearer {auth_key}'
        }
        # Get response
        response: Response = requests.delete(url, params=params, headers=headers, verify=self.verify_calls)
        if not response.ok:
            raise WacomServiceException(f'Deletion of relation failed. '
                                        f'Response code:={response.status_code}, exception:= {response.content}')

    def activations(self, auth_key: str, uris: List[str], depth: int) \
            -> Tuple[Dict[str, ThingObject], List[Tuple[str, OntologyPropertyReference, str]]]:
        """
        Spreading activation, retrieving the entities related to a  entity.

        Parameters
        ----------
        auth_key: str
            Auth key for user
        uris: List[str]
            List of URIS for entity.
        depth: int
            Depth of activations

        Returns
        -------
        entity_map: Dict[str, ThingObject]
            Map with entity and its URI as key.
        relations: List[Tuple[str, OntologyPropertyReference, str]]
            List of relations with subject predicate, (Property), and subject

        Raises
        ------
        WacomServiceException
            If the graph service returns an error code, and activation failed.
        """
        url: str = f'{self.service_url}/{self.service_endpoint}{WacomKnowledgeService.ACTIVATIONS_ENDPOINT}'

        headers: Dict[str, str] = {
            AUTHORIZATION_HEADER_FLAG: f'Bearer {auth_key}'
        }
        params: dict = {
            'uris': uris,
            'activation': depth
        }

        response: Response = requests.get(url, headers=headers, params=params, verify=self.verify_calls)
        if response.ok:
            entities: Dict[str, Any] = response.json()
            things: Dict[str, ThingObject] = dict([(e[URI_TAG], ThingObject.from_dict(e))
                                                   for e in entities['entities']])
            relations: List[Tuple[str, OntologyPropertyReference, str]] = []
            for r in entities[RELATIONS_TAG]:
                relation: OntologyPropertyReference = OntologyPropertyReference.parse(r[PREDICATE])
                relations.append((r[SUBJECT], relation, r[OBJECT]))
                if r[SUBJECT] in things:
                    things[r[SUBJECT]].add_relation(ObjectProperty(relation, outgoing=[r[OBJECT]]))
            return things, relations

    def listing(self, auth_key: str, filter_type: OntologyClassReference, page_id: str = 0, limit: int = 30,
                language_code: LanguageCode = 'en_US') \
            -> Tuple[List[ThingObject], int, str]:
        """
        List all entities visible to users.

        Parameters
        ----------
        auth_key: str
            Auth key from user
        filter_type: OntologyClassReference
            Filtering with concept
        page_id: str
            Page id. Start from this page id
        limit: int
            Limit of the returned entities
        language_code: LanguageCode
            Language code

        Returns
        -------
        entities: List[ThingObject]
            List of entities
        total_number: int
            Number of all entities
        next_page_id: str
            Identifier of the next page

        Raises
        ------
        WacomServiceException
            If the graph service returns an error code
        """
        url: str = f'{self.service_url}/{self.service_endpoint}{WacomKnowledgeService.LISTING_ENDPOINT}'
        # Header with auth token
        headers: Dict[str, str] = {
            AUTHORIZATION_HEADER_FLAG: f'Bearer {auth_key}'
        }
        # Parameter with filtering and limit
        parameters: dict = {
            TYPE_TAG: filter_type.iri,
            LIMIT_PARAMETER: limit,
            LANGUAGE_PARAMETER: language_code
        }
        # If filtering is configured
        if page_id is not None:
            parameters[NEXT_PAGE_ID_TAG] = page_id
        # Send request
        response: Response = requests.get(url, params=parameters, headers=headers, verify=self.verify_calls)
        # If response is successful
        if response.ok:
            entities_resp: dict = response.json()
            next_page_id: str = entities_resp[NEXT_PAGE_ID_TAG]
            total_number: int = entities_resp[TOTAL_COUNT]
            entities: List[ThingObject] = []
            if LISTING in entities_resp:
                for e in entities_resp[LISTING]:
                    thing: ThingObject = ThingObject.from_dict(e)
                    thing.status_flag = EntityStatus.SYNCED
                    entities.append(thing)
            return entities, total_number, next_page_id
        else:
            raise WacomServiceException('Failed to list the entities (since:= {}, limit:={}). '
                                        'Response code:={}, exception:= {}'
                                        .format(page_id, limit, response.status_code, response.content))

    def ontology_update(self, auth_key: str):
        """
        Update the ontology.
        Parameters
        ----------
        auth_key: str

        """
        url: str = f'{self.service_base_url}{WacomKnowledgeService.ONTOLOGY_UPDATE_ENDPOINT}'
        # Header with auth token
        headers: dict = {
            AUTHORIZATION_HEADER_FLAG: f'Bearer {auth_key}'
        }
        response: Response = requests.patch(url, headers=headers, verify=self.verify_calls)
        if not response.ok:
            raise WacomServiceException(f'Ontology update fails. '
                                        f'Response code:={response.status_code}, exception:= {response.content}')

    def search_types(self, auth_key: str, search_term: str, language_code: LanguageCode,
                     types: List[OntologyClassReference], limit: int = 30, next_page_id: str = None)\
            -> Tuple[List[ThingObject], str]:

        headers: Dict[str, str] = {
            AUTHORIZATION_HEADER_FLAG:  f'Bearer {auth_key}'
        }
        parameters: Dict[str, Any] = {
            SEARCH_TERM: search_term,
            LANGUAGE_PARAMETER: language_code,
            TYPES_PARAMETER: [ot.iri for ot in types],
            LIMIT: limit,
            NEXT_PAGE_ID_TAG: next_page_id
        }
        url: str = f'{self.service_url}/{self.service_endpoint}{WacomKnowledgeService.SEARCH_TYPES_ENDPOINT}'
        response: Response = requests.get(url, headers=headers, params=parameters, verify=self.verify_calls)
        if response.ok:
            return WacomKnowledgeService.__search_results__(response.json())
        raise WacomServiceException(f'Search on labels {search_term} failed. '
                                    f'Response code:={response.status_code}, exception:= {response.content}')

    def search_labels(self, auth_key: str, search_term: str, language_code: LanguageCode, limit: int = 30,
                      next_page_id: str = None)\
            -> Tuple[List[ThingObject], str]:
        headers: Dict[str, str] = {
            AUTHORIZATION_HEADER_FLAG:  f'Bearer {auth_key}'
        }
        parameters: Dict[str, Any] = {
            SEARCH_TERM: search_term,
            LANGUAGE_PARAMETER: language_code,
            LIMIT: limit,
            NEXT_PAGE_ID_TAG: next_page_id
        }
        url: str = f'{self.service_url}/{self.service_endpoint}{WacomKnowledgeService.SEARCH_LABELS_ENDPOINT}'
        response: Response = requests.get(url, headers=headers, params=parameters, verify=self.verify_calls)
        if response.ok:
            return WacomKnowledgeService.__search_results__(response.json())
        raise WacomServiceException(f'Search on labels {search_term} failed. '
                                    f'Response code:={response.status_code}, exception:= {response.content}')

    def search_literal(self, auth_key: str, search_term: str,  literal: OntologyPropertyReference,
                       pattern: SearchPattern = SearchPattern.REGEX,
                       language_code: LanguageCode = LanguageCode('en_US'),
                       limit: int = 30, next_page_id: str = None) -> Tuple[List[ThingObject], str]:
        url: str = f'{self.service_url}/{self.service_endpoint}{WacomKnowledgeService.SEARCH_LITERALS_ENDPOINT}'
        parameters: Dict[str, Any] = {
            'Value': search_term,
            'Literal': literal.iri,
            LANGUAGE_PARAMETER: language_code,
            LIMIT_PARAMETER: limit,
            'SearchPattern': pattern.value,
            NEXT_PAGE_ID_TAG: next_page_id
        }
        headers: dict = {
            AUTHORIZATION_HEADER_FLAG: f'Bearer {auth_key}'
        }
        response: Response = requests.get(url, headers=headers, params=parameters, verify=self.verify_calls)
        if response.ok:
            return WacomKnowledgeService.__search_results__(response.json())
        raise WacomServiceException(f'Search on labels {search_term} failed. '
                                    f'Response code:={response.status_code}, exception:= {response.content}')

    def search_relation(self, auth_key: str, relation: OntologyPropertyReference,
                        language_code: LanguageCode, subject_uri: str = None, object_uri: str = None,
                        limit: int = 30, next_page_id: str = None) \
            -> Tuple[List[ThingObject], str]:
        url: str = f'{self.service_url}/{self.service_endpoint}{WacomKnowledgeService.SEARCH_RELATION_ENDPOINT}'
        parameters: Dict[str, Any] = {
            SUBJECT_URI: subject_uri,
            RELATION_URI: relation.iri,
            OBJECT_URI: object_uri,
            LANGUAGE_PARAMETER: language_code,
            LIMIT: limit,
            NEXT_PAGE_ID_TAG: next_page_id
        }
        headers: dict = {
            AUTHORIZATION_HEADER_FLAG: f'Bearer {auth_key}'
        }

        response = requests.get(url, headers=headers, params=parameters, verify=self.verify_calls)
        if response.ok:
            return WacomKnowledgeService.__search_results__(response.json())
        raise WacomServiceException(f'Search on: subject:={subject_uri}, relation {relation.iri}, '
                                    f'object:= {object_uri} failed. '
                                    f'Response code:={response.status_code}, exception:= {response.content}')

    def search_description(self, auth_key: str, search_term: str, language_code: LanguageCode, limit: int = 30,
                           next_page_id: str = None) -> Tuple[List[ThingObject], str]:
        url: str = f'{self.service_base_url}{WacomKnowledgeService.SEARCH_DESCRIPTION_ENDPOINT}'
        parameters: Dict[str, Any] = {
            SEARCH_TERM: search_term,
            LANGUAGE_PARAMETER: language_code,
            LIMIT: limit,
            NEXT_PAGE_ID_TAG: next_page_id
        }
        headers: dict = {
            AUTHORIZATION_HEADER_FLAG: f'Bearer {auth_key}'
        }

        response = requests.get(url, headers=headers, params=parameters, verify=self.verify_calls)
        if response.ok:
            return WacomKnowledgeService.__search_results__(response.json())
        raise WacomServiceException(f'Search on labels {search_term} failed. '
                                    f'Response code:={response.status_code}, exception:= {response.content}')

    @staticmethod
    def __search_results__(response: Dict[str, Any]) -> Tuple[List[ThingObject], str]:
        results: List[ThingObject] = []
        for elem in response['result']:
            results.append(ThingObject.from_dict(elem))
        return results, response[NEXT_PAGE_ID_TAG]

    @staticmethod
    def __import_locale__(param: Dict[str, Any], tag_name: str = 'value') -> LocalizedContent:
        value: str = param[tag_name]
        language_code: LanguageCode = param[LANGUAGE_CODE_TAG]
        if IS_MAIN_TAG in param:
            is_main: bool = bool(param[IS_MAIN_TAG])
        else:
            is_main: bool = True
        return Label(content=value, language_code=language_code, main=is_main)


class TenantManagementServiceAPI(WacomServiceAPIClient):
    """
    Tenant Management Service API
    -----------------------------

    Functionality:
        - List all tenants
        - Create tenants
        - Create users

    Parameters
    ----------
    tenant_token: str
        Tenant Management token
    service_url: str
        URL of the service
    service_endpoint: str
        Base endpoint
    """

    TENANT_ENDPOINT: str = 'tenant'
    USER_DETAILS_ENDPOINT: str = f'{WacomServiceAPIClient.USER_ENDPOINT}/users'
    SERVICE_URL: str = 'https://semantic-ink-private.wacom.com'

    def __init__(self, tenant_token: str, service_url: str = SERVICE_URL, service_endpoint: str = 'graphdata'):
        self.__tenant_management_token: str = tenant_token
        super().__init__("TenantManagementServiceAPI", service_url=service_url, service_endpoint=service_endpoint)

    @property
    def tenant_management_token(self) -> str:
        """Tenant Management token."""
        return self.__tenant_management_token

    @tenant_management_token.setter
    def tenant_management_token(self, value: str):
        self.__tenant_management_token = value

    # ------------------------------------------ Tenants handling ------------------------------------------------------

    def create_tenant(self, name: str) -> Dict[str, str]:
        """
        Creates a tenant.

        Parameters
        ----------
        name: str -
            Name of the tenant

        Returns
        -------
        tenant_dict: Dict[str, str]

        Newly created tenant structure.
        >>>     {
        >>>       "id": "<Tenant-ID>",
        >>>       "apiKey": "<Tenant-API-Key>",
        >>>       "name": "<Tenant-Name>"
        >>>    }

        Raises
        ------
        WacomServiceException
            If the tenant service returns an error code.
        """
        url: str = '{}/{}{}'.format(self.service_url, self.service_endpoint,
                                    TenantManagementServiceAPI.TENANT_ENDPOINT)
        headers: dict = {
            AUTHORIZATION_HEADER_FLAG: f'Bearer {self.__tenant_management_token}',
            'Content-Type': 'application/json'
        }
        payload: dict = {
            'name': name
        }
        response: Response = requests.post(url, headers=headers, json=payload, verify=self.verify_calls)
        if response.ok:
            return response.json()

    def listing_tenant(self) -> List[Dict[str, str]]:
        """
        Listing all tenants configured for this instance.

        Returns
        -------
        tenants:  List[Dict[str, str]]
            List of tenants:
            >>> [
            >>>     {
            >>>        "id": "<Tenant-ID>",
            >>>        "apiKey": "<Tenant-API-Key>",
            >>>        "name": "<Tenant-Name>"
            >>>     },
            >>>     ...
            >>> ]
        Raises
        ------
        WacomServiceException
            If the tenant service returns an error code.
        """
        url: str = '{}/{}{}'.format(self.service_url, self.service_endpoint,
                                    TenantManagementServiceAPI.TENANT_ENDPOINT)
        headers: dict = {
            AUTHORIZATION_HEADER_FLAG: f'Bearer {self.__tenant_management_token}'
        }
        response: Response = requests.get(url, headers=headers, data={}, verify=self.verify_calls)
        if response.ok:
            return response.json()
        raise WacomServiceException(f'Response code:={response.status_code}, exception:= {response.text}')

    # ------------------------------------------ Users handling --------------------------------------------------------

    def create_user(self, tenant_key: str, external_id: str, meta_data: Dict[str, str] = None,
                    roles: List[str] = None) -> Dict[str, Any]:
        """
        Creates user for a tenant.

        Parameters
        ----------
        tenant_key: str -
            API key for tenant
        external_id: str -
            External id of user identification service.
        meta_data: Dict[str, str]
            Meta-data dictionary.
        roles: List[str]
            List of roles.

        Returns
        -------
        user: Dict[str, Any]
            User info.

        Raises
        ------
        WacomServiceException
            If the tenant service returns an error code.
        """
        url: str = '{}/{}{}'.format(self.service_url, self.service_endpoint, TenantManagementServiceAPI.USER_ENDPOINT)
        headers: dict = {
            AUTHORIZATION_HEADER_FLAG: f'Bearer {self.__tenant_management_token}',
            'x-tenant-api-key': tenant_key,
            'Content-Type': 'application/json'
        }
        payload: dict = {
            "externalUserId": external_id,
            "metaData": meta_data if meta_data is not None else {},
            "roles": roles if roles is not None else ['User']
        }
        response: Response = requests.post(url, headers=headers, json=payload, verify=self.verify_calls)
        if response.ok:
            return response.json()
        raise WacomServiceException(f'Response code:={response.status_code}, exception:= {response.text}')

    def update_user(self, tenant_key: str, internal_id: str, external_id: str, meta_data: Dict[str, str] = None,
                    roles: List[str] = None) -> Dict[str, Any]:
        """Updates user for a tenant.

        Parameters
        ----------
        tenant_key: str
            API key for tenant
        internal_id: str
            Internal id of semantic service.
        external_id: str
            External id of user identification service.
        meta_data: Dict[str, str]
            Meta-data dictionary.
        roles: List[str]
            List of roles.

        Returns
        -------
        update: Dict[str, Any]
            Updated information

        Raises
        ------
        WacomServiceException
            If the tenant service returns an error code.
        """
        url: str = '{}/{}{}'.format(self.service_url,
                                    self.service_endpoint,
                                    TenantManagementServiceAPI.USER_ENDPOINT)
        headers: dict = {
            AUTHORIZATION_HEADER_FLAG: f'Bearer {self.__tenant_management_token}',
            'x-tenant-api-key': tenant_key,
            'Content-Type': 'application/json'
        }
        payload: dict = {
            "metaData": meta_data if meta_data is not None else {},
            "roles": roles if roles is not None else []
        }
        params: dict = {
            'userId': internal_id,
            'externalUserId': external_id
        }
        response: Response = requests.patch(url, headers=headers, json=payload, params=params, verify=self.verify_calls)
        if response.ok:
            return response.json()
        raise WacomServiceException(f'Response code:={response.status_code}, exception:= {response.text}')

    def delete_user(self, tenant_key: str, external_id: str, internal_id: str):
        """Deletes user from tenant.

        Parameters
        ----------
        tenant_key: str
            API key for tenant
        external_id: str
            External id of user identification service.
        internal_id: str
            Internal id of user.

        Raises
        ------
        WacomServiceException
            If the tenant service returns an error code.
        """
        url: str = '{}/{}{}'.format(self.service_url, self.service_endpoint, TenantManagementServiceAPI.USER_ENDPOINT)
        headers: dict = {
            AUTHORIZATION_HEADER_FLAG: f'Bearer {self.__tenant_management_token}',
            'x-tenant-api-key': tenant_key
        }
        params: dict = {
            'userId': internal_id,
            'externalUserId': external_id
        }
        response: Response = requests.delete(url, headers=headers, params=params, verify=self.verify_calls)
        if not response.ok:
            raise WacomServiceException(f'Response code:={response.status_code}, exception:= {response.text}')

    def user_internal_id(self, tenant_key: str, external_id: str) -> Dict[str, Any]:
        """User internal id.

        Parameters
        ----------
        tenant_key: str
            API key for tenant
        external_id: str
            External id of user

        Returns
        -------
        user_id: Dict[str, Any]
            Internal id of users

        Raises
        ------
        WacomServiceException
            If the tenant service returns an error code.
        """
        url: str = f'{self.service_url}/{self.service_endpoint}{TenantManagementServiceAPI.USER_DETAILS_ENDPOINT}'
        headers: dict = {
            AUTHORIZATION_HEADER_FLAG: f'Bearer {self.__tenant_management_token}',
            'x-tenant-api-key': tenant_key
        }
        parameters: Dict[str, str] = {
            'externalUserId':  external_id
        }
        response: Response = requests.get(url, headers=headers, params=parameters, verify=self.verify_calls)
        if response.ok:
            return response.json()
        raise WacomServiceException(f'Response code:={response.status_code}, exception:= {response.text}')

    def listing_users(self, tenant_key: str, offset: int = 0, limit: int = 20) -> List[Dict[str, str]]:
        """
        Listing all users configured for this instance.

        Parameters
        ----------
        tenant_key: str
            API key for tenant
        offset: int - [optional]
            Offset value to define starting position in list. [DEFAULT:= 0]
        limit: int - [optional]
            Define the limit of the list size. [DEFAULT:= 20]

        Returns
        -------
        user:  List[Dict[str, str]]
            List of users.
        """
        url: str = f'{self.service_url}/{self.service_endpoint}{TenantManagementServiceAPI.USER_ENDPOINT}'
        headers: dict = {
            AUTHORIZATION_HEADER_FLAG: f'Bearer {self.__tenant_management_token}',
            'x-tenant-api-key': tenant_key
        }
        params: dict = {
            'offset': offset,
            'limit': limit
        }
        response: Response = requests.get(url, headers=headers, params=params, verify=self.verify_calls)
        if response.ok:
            return response.json()
        raise WacomServiceException(f'Response code:={response.status_code}, exception:= {response.text}')
