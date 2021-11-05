# -*- coding: utf-8 -*-
# Copyright © 2021 Wacom. All rights reserved.
import urllib.parse
from http import HTTPStatus
from typing import Dict, List, Any, Optional

import requests
from requests import Response

from knowledge.base.entity import OntologyContext, OntologyProperty, LocalizedContent, PropertyType, OntologyClass, \
    Label, Comment
from knowledge.base.ontology import OntologyClassReference, OntologyPropertyReference
from knowledge.services.base import WacomServiceAPIClient, WacomServiceException
from knowledge.services.graph import AUTHORIZATION_HEADER_FLAG


class OntologyService(WacomServiceAPIClient):
    """
    Ontology API Client
    -------------------
    Client to access the ontology service. Offers the following functionality:
    - Listing class names and property names
    - Create new ontology types
    - Update ontology types

    Parameters
    ----------
    service_url: str
        URL of the service
    service_endpoint: str
        Base endpoint
    """
    CONTEXT_ENDPOINT: str = 'context'
    CONCEPTS_ENDPOINT: str = 'context/{}/concepts'
    CONCEPT_ENDPOINT: str = 'context/{}/concepts/{}'
    PROPERTIES_ENDPOINT: str = "context/{}/properties"
    COMMIT_ENDPOINT: str = "context/{}/commit"
    PROPERTY_ENDPOINT: str = "context/{}/properties/{}"

    def __init__(self, service_url: str, service_endpoint: str = 'ontology'):
        super().__init__(application_name="Ontology Service", service_url=service_url,
                         service_endpoint=service_endpoint)

    def contexts(self, auth_key: str) -> List[OntologyContext]:
        """List all concepts.

        **Remark:**
        Works for users with role 'User' and 'TenantAdmin'.

        Parameters
        ----------
        auth_key: str
            Auth key from user.

        Returns
        -------
        contexts: List[OntologyContext]
            List of ontology contexts
        """
        headers: Dict[str, str] = {
            AUTHORIZATION_HEADER_FLAG: f'Bearer {auth_key}'
        }
        response: Response = requests.get(f'{self.service_base_url}{OntologyService.CONTEXT_ENDPOINT}',
                                          headers=headers, verify=self.verify_calls)
        if response.ok:
            response_list: List[OntologyContext] = []
            for c in response.json():
                response_list.append(OntologyContext.from_dict(c))
            return response_list
        raise WacomServiceException(f'Listing of context failed. '
                                    f'Response code:={response.status_code}, exception:= {response.text}')

    def concepts(self, auth_key: str, context: str) -> List[OntologyClassReference]:
        """Retrieve all concept classes.

        **Remark:**
        Works for users with role 'User' and 'TenantAdmin'.

        Parameters
        ----------
        auth_key: str
            Auth key from user.
        context: str
            Context of the ontology

        Returns
        -------
        concepts: List[OntologyClassReference]
            List of ontology classes
        """
        headers: Dict[str, str] = {
            AUTHORIZATION_HEADER_FLAG: f'Bearer {auth_key}'
        }
        response: Response = requests.get(f'{self.service_base_url}{OntologyService.CONCEPTS_ENDPOINT.format(context)}',
                                          headers=headers, verify=self.verify_calls)
        if response.ok:
            response_list: List[OntologyClassReference] = []
            result = response.json()
            for c in result:
                response_list.append(OntologyClassReference.parse(c))
            return response_list
        raise WacomServiceException(f'Response code:={response.status_code}, exception:= {response.text}')

    def properties(self, auth_key: str, context_name: str) -> List[OntologyPropertyReference]:
        """List all properties.

        **Remark:**
        Works for users with role 'User' and 'TenantAdmin'.

        Parameters
        ----------
        auth_key: str
            Auth key from user.
        context_name: str
            Name of the context

        Returns
        -------
        contexts: List[OntologyPropertyReference]
            List of ontology contexts
        """
        headers: Dict[str, str] = {
            AUTHORIZATION_HEADER_FLAG: f'Bearer {auth_key}'
        }
        context_url: str = urllib.parse.quote_plus(context_name)

        response: Response = requests.get(f'{self.service_base_url}'
                                          f'{OntologyService.PROPERTIES_ENDPOINT.format(context_url)}',
                                          headers=headers, verify=self.verify_calls)
        # Return empty list if the NOT_FOUND is reported
        if response.status_code == HTTPStatus.NOT_FOUND:
            return []
        if response.ok:
            response_list: List[OntologyPropertyReference] = []
            for c in response.json():
                response_list.append(OntologyPropertyReference.parse(c))
            return response_list
        raise WacomServiceException(f'Response code:={response.status_code}, exception:= {response.text}')

    def concept(self, auth_key: str, context_name: str, concept_name: str) -> OntologyClass:
        """Retrieve a concept instance.

        **Remark:**
        Works for users with role 'User' and 'TenantAdmin'.

        Parameters
        ----------
        auth_key: str
            Auth key from user.
        context_name: str
            Name of the context
        concept_name: str
            IRI of the concept

        Returns
        -------
        instance: OntologyClass
            Instance of the concept
        """
        headers: Dict[str, str] = {
            AUTHORIZATION_HEADER_FLAG: f'Bearer {auth_key}'
        }
        context_url: str = urllib.parse.quote_plus(context_name)
        concept_url: str = urllib.parse.quote_plus(concept_name)
        response: Response = requests.get(f'{self.service_base_url}'
                                          f'{OntologyService.CONCEPT_ENDPOINT.format(context_url, concept_url)}',
                                          headers=headers, verify=self.verify_calls)
        if response.ok:
            result: Dict[str, Any] = response.json()
            return OntologyClass.from_dict(result)
        raise WacomServiceException(f'Response code:={response.status_code}, exception:= {response.text}')

    def property(self, auth_key: str, context_name: str, property_name: str) -> OntologyProperty:
        """Retrieve a property instance.

        **Remark:**
        Works for users with role 'User' and 'TenantAdmin'.

        Parameters
        ----------
        auth_key: str
            Auth key from user.
        context_name: str
            Name of the context
        property_name: str
            IRI of the property

        Returns
        -------
        instance: OntologyProperty
            Instance of the property
        """
        headers: Dict[str, str] = {
            AUTHORIZATION_HEADER_FLAG: f'Bearer {auth_key}'
        }
        context_url: str = urllib.parse.quote_plus(context_name)
        concept_url: str = urllib.parse.quote_plus(property_name)
        param: str = OntologyService.PROPERTY_ENDPOINT.format(context_url, concept_url)
        response: Response = requests.get(f'{self.service_base_url}{param}',
                                          headers=headers, verify=self.verify_calls)
        if response.ok:
            return OntologyProperty.from_dict(response.json())
        raise WacomServiceException(f'Response code:={response.status_code}, exception:= {response.text}')

    def create_concept(self, auth_key: str, context: str, name: str, subclass_of: Optional[str],
                       icon: Optional[str] = None, labels: Optional[List[Label]] = None,
                       comments: Optional[List[Comment]] = None) -> Dict[str, str]:
        """Create concept class.

        **Remark:**
        Only works for users with role 'TenantAdmin'.

        Parameters
        ----------
        auth_key: str
            Auth key from user.
        context: str
            Context of ontology
        name: str
            Name of the concept
        subclass_of: Optional[str]
            Super class of the concept
        icon: Optional[str] (default:= None)
            Icon representing the concept
        labels: Optional[List[Label]] (default:= None)
            Labels for the class
        comments: Optional[List[Comment]] (default:= None)
            Comments for the class
        Returns
        -------
        result: Dict[str, str]
            Result from the service

        Raises
        ------
        WacomServiceException
            If the ontology service returns an error code, exception is thrown.
        """
        headers: Dict[str, str] = {
            AUTHORIZATION_HEADER_FLAG: f'Bearer {auth_key}'
        }
        payload: Dict[str, Any] = {
            "subClassOf": subclass_of,
            "name": name,
            "labels": [],
            "comments": [],
            "icon": icon
        }
        context_url: str = urllib.parse.quote_plus(context)
        for label in labels if labels is not None else []:
            payload["labels"].append({'text': label.content, 'locale': label.language_code})
        for comment in comments if comments is not None else []:
            payload["comments"].append({'text': comment.content, 'locale': comment.language_code})
        url: str = f'{self.service_base_url}{OntologyService.CONCEPTS_ENDPOINT.format(context_url)}'
        response: Response = requests.post(url, headers=headers, json=payload, verify=self.verify_calls)
        if response.ok:
            result_dict: Dict[str, str] = response.json()
            return result_dict
        raise WacomServiceException(f'Creation of concept failed. '
                                    f'Response code:={response.status_code}, exception:= {response.text}')

    def update_concept(self, auth_key: str, context: str, name: str, subclass_of: Optional[str],
                       icon: Optional[str] = None, labels: Optional[List[Label]] = None,
                       comments: Optional[List[Comment]] = None):
        """Update concept class.

        **Remark:**
        Only works for users with role 'TenantAdmin'.

        Parameters
        ----------
        auth_key: str
            Auth key from user.
        context: str
            Context of ontology
        name: str
            Name of the concept
        subclass_of: Optional[str]
            Super class of the concept
        icon: Optional[str] (default:= None)
            Icon representing the concept
        labels: Optional[List[Label]] (default:= None)
            Labels for the class
        comments: Optional[List[Comment]] (default:= None)
            Comments for the class

        Raises
        ------
        WacomServiceException
            If the ontology service returns an error code, exception is thrown.
        """
        headers: Dict[str, str] = {
            AUTHORIZATION_HEADER_FLAG: f'Bearer {auth_key}'
        }
        payload: Dict[str, Any] = {
            "subClassOf": subclass_of,
            "name": name,
            "labels": [],
            "comments": [],
            "icon": icon
        }
        context_url: str = urllib.parse.quote_plus(context)
        for label in labels if labels is not None else []:
            payload["labels"].append({'text': label.content, 'locale': label.language_code})
        for comment in comments if comments is not None else []:
            payload["comments"].append({'text': comment.content, 'locale': comment.language_code})
        url: str = f'{self.service_url}{self.service_endpoint}' \
                   f'{OntologyService.CONCEPTS_ENDPOINT.format(context_url)}'
        response: Response = requests.put(url, headers=headers, json=payload, verify=self.verify_calls)
        if response.ok:
            result_dict: Dict[str, str] = response.json()
            return result_dict
        raise WacomServiceException(f'Update of concept failed. '
                                    f'Response code:={response.status_code}, exception:= {response.text}')

    def create_property(self, auth_key: str, context: str, property_type: PropertyType, name: OntologyPropertyReference,
                        domain_cls: OntologyClassReference, range_cls: OntologyClassReference,
                        inverse_of: Optional[OntologyPropertyReference] = None,
                        subproperty_of: Optional[OntologyPropertyReference] = None,
                        icon: Optional[str] = None,
                        labels: Optional[List[LocalizedContent]] = None,
                        comments: Optional[List[LocalizedContent]] = None) -> Dict[str, str]:
        """Create concept class.

        Parameters
        ----------
        auth_key: str
            Auth key from user.
        context: str
            Context of ontology
        property_type: PropertyType
            Type of the property
        name: OntologyPropertyReference
            Name of the concept
        domain_cls: OntologyClassReference
            IRI of the domain
        range_cls: OntologyClassReference
            IRI of the range
        inverse_of: Optional[OntologyPropertyReference] (default:= None)
            Inverse property
        subproperty_of: Optional[OntologyPropertyReference] = None,
            Super property of the concept
        icon: Optional[str] (default:= None)
            Icon representing the concept
        labels: Optional[List[Label]] (default:= None)
            Labels for the class
        comments: Optional[List[Comment]] (default:= None)
            Comments for the class
        Returns
        -------
        result: Dict[str, str]
            Result from the service

        Raises
        ------
        WacomServiceException
            If the ontology service returns an error code, exception is thrown.
        """
        headers: Dict[str, str] = {
            AUTHORIZATION_HEADER_FLAG: f'Bearer {auth_key}'
        }
        payload: Dict[str, Any] = {
            "kind": property_type.value,
            "domain": domain_cls.iri,
            "range": range_cls.iri,
            "subPropertyOf": subproperty_of.iri,
            "inverseOf": inverse_of.iri,
            "name": name.iri,
            "labels": [],
            "comments": [],
            "icon": icon
        }
        context_url: str = urllib.parse.quote_plus(context)
        for label in labels if labels is not None else []:
            payload["labels"].append({'text': label.content, 'locale': label.language_code})
        for comment in comments if comments is not None else []:
            payload["comments"].append({'text': comment.content, 'locale': comment.language_code})
        url: str = f'{self.service_url}{self.service_endpoint}' \
                   f'{OntologyService.PROPERTIES_ENDPOINT.format(context_url)}'
        response: Response = requests.post(url, headers=headers, json=payload, verify=self.verify_calls)
        if response.ok:
            result_dict: Dict[str, str] = response.json()
            return result_dict
        raise WacomServiceException(f'Update of concept failed. '
                                    f'Response code:={response.status_code}, exception:= {response.text}')

    def create_context(self, auth_key: str, name: str, base_uri: Optional[str] = None, icon: Optional[str] = None,
                       labels: List[Label] = None, comments: List[Comment] = None) -> Dict[str, str] :
        """Create context class.

        Parameters
        ----------
        auth_key: str
            Auth key from user.
        base_uri: str
            Base URI
        name: str
            Name of the context
        icon: Optional[str] (default:= None)
            Icon representing the concept
        labels: Optional[List[Label]] (default:= None)
            Labels for the context
        comments: Optional[List[Comment]] (default:= None)
            Comments for the context

        Returns
        -------
        result: Dict[str, str]
            Result from the service

        Raises
        ------
        WacomServiceException
            If the ontology service returns an error code, exception is thrown.
        """
        headers: Dict[str, str] = {
            'Authorization': f'Bearer {auth_key}'
        }
        payload: Dict[str, Any] = {
            "baseUri": base_uri if base_uri is not None else f'wacom:{name}',
            "name": name,
            "labels": [],
            "comments": [],
            "icon": icon
        }
        for label in labels if labels is not None else []:
            payload["labels"].append({'text': label.content, 'locale': label.language_code})
        for comment in comments if comments is not None else []:
            payload["comments"].append({'text': comment.content, 'locale': comment.language_code})
        url: str = f'{self.service_base_url}{OntologyService.CONTEXT_ENDPOINT}'

        response: Response = requests.post(url, headers=headers, json=payload, verify=self.verify_calls)
        if response.ok:
            result_dict: Dict[str, str] = response.json()
            return result_dict
        raise WacomServiceException(f'Update of concept failed. '
                                    f'Response code:={response.status_code}, exception:= {response.text}')

    def commit(self, auth_key: str, context_name: str):
        """
        Commit the ontology.

        Parameters
        ----------
        auth_key: str
            User token (must have TenantAdmin) role
        context_name: str
            Name of the context.
        """
        headers: Dict[str, str] = {
            'Authorization': f'Bearer {auth_key}'
        }
        context_url: str = urllib.parse.quote_plus(context_name)
        url: str = f'{self.service_base_url}{OntologyService.COMMIT_ENDPOINT.format(context_url)}'
        response: Response = requests.put(url, headers=headers, verify=self.verify_calls)
        if not response.ok:
            raise WacomServiceException(f'Commit of ontology failed. '
                                        f'Response code:={response.status_code}, exception:= {response.text}')
