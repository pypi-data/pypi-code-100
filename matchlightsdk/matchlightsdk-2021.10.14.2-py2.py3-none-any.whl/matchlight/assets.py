"""An interface for creating and retrieving PII records in Matchlight."""
from __future__ import absolute_import

import io
import json

import six
from matchlight.utils import blind_email, blind_name

import matchlight.error
import matchlight.utils
from pylibfp import (
    fingerprint,
    fingerprints_pii_address_variants,
    fingerprints_pii_city_state_zip_variants,
    fingerprints_pii_credit_card,
    fingerprints_pii_email_address,
    fingerprints_pii_iban,
    fingerprints_pii_medicare_id,
    fingerprints_pii_name_variants,
    fingerprints_pii_passport,
    fingerprints_pii_phone_number,
    fingerprints_pii_ssn,
    MODE_CODE,
    OPTIONS_TILED,
)

import pandas as pd
from time import time
import sys
import time
import json
import uuid
import datetime

__all__ = (
    'Asset',
    'AssetMethods',
)

MAX_DOCUMENT_FINGERPRINTS = 1024000


class Asset(object):
    """Represents a personal information record."""

    # def __init__(self, id, name, description, ctime=None, mtime=None, metadata=None):
    def __init__(self):
        """Initializes a new personal information record. """
    #     if metadata is None:
    #         metadata = {}
    #     self.id = id
    #     self.name = name
    #     self.description = description
    #     self.ctime = ctime
    #     self.mtime = mtime
    #     self.metadata = metadata
    #
    # @classmethod
    # def from_mapping(cls, mapping):
    #     """Creates a new project instance from the given mapping."""
    #     return cls(
    #         id=mapping['id'],
    #         name=mapping['name'],
    #         description=mapping['description'],
    #         ctime=mapping['ctime'],
    #         mtime=mapping['mtime'],
    #         metadata=mapping['metadata'],
    #     )
    #
    # @property
    # def user_provided_id(self):
    #     """:obj:`int`: The user provided record identifier."""
    #     return self.metadata.get('user_record_id', None)
    #
    # @property
    # def details(self):
    #     """:obj:`dict`: Returns the feed details as a mapping."""
    #     return {
    #         'id': self.id,
    #         'name': self.name,
    #         'description': self.description,
    #         'ctime': self.ctime,
    #         'mtime': self.mtime,
    #         'metadata': self.metadata,
    #     }
    #
    # def __repr__(self):  # pragma: no cover
    #     return '<Record(name="{}", id="{}")>'.format(self.name, self.id)


class AssetMethods(object):
    """Provides methods for interfacing with the records API. """

    def __init__(self, ml_connection):  # noqa: D205,D400
        """Initializes a records interface with the given Matchlight
        connection.

            :param :class:`~.Connection` ml_connection: A Matchlight connection instance.

        """
        self.conn = ml_connection

    def add_document(self, custom_id, asset_detail, tags,
                     content, match_score_threshold=70, offline=False):
        result_json = fingerprint(content, flags=OPTIONS_TILED)
        result = json.loads(result_json)
        fingerprints = result['data']['fingerprints']

        data = {
            'customId': custom_id,
            'asset_detail': asset_detail,
            'type': "document",
            'metadata': {
                'fingerprinting_tool_name': 'Python SDK',
                'fingerprinting_tool_version': matchlight.__version__
            }
        }

        fields = dict()
        fields['type'] = 'document'
        fields['variants'] = [fingerprints]
        fields['field_detail'] = asset_detail

        data['fields'] = [fields]

        if tags is not None:
            if isinstance(tags, list):
                data['tags'] = tags
            else:
                data['tags'] = tags
        if match_score_threshold is not None:
            data['match_score_threshold'] = match_score_threshold

        if offline:
            return data
        else:
            return self.add_document_from_fingerprints(data)

    def add_document_from_fingerprints(self, fingerprint_data):
        path = '/v3/public/asset/'
        response = self.conn.request(
            path,
            data=json.dumps(fingerprint_data)
        )
        return response

    def update_document(self, asset_id, custom_id, asset_detail, tags, match_score_threshold=70, offline=False):
        data = {
            'id':asset_id,
            'customId': custom_id,
            'asset_detail': asset_detail,
            'type': "document",
            'metadata': {
                'fingerprinting_tool_name': 'Python SDK',
                'fingerprinting_tool_version': matchlight.__version__
            }
        }

        fields = dict()
        fields['type'] = 'document'
        #fields['variants'] = [fingerprints]
        fields['field_detail'] = asset_detail

        data['fields'] = [fields]

        if tags is not None:
            if isinstance(tags, list):
                data['tags'] = tags
            else:
                data['tags'] = tags
        if match_score_threshold is not None:
            data['match_score_threshold'] = match_score_threshold

        path = '/v3/public/asset/update'
        response = self.conn.request(
            path,
            data=json.dumps(data)
        )
        return response

    def add_pii_from_fingerprints(self, fingerprint_data):
        path = '/v3/public/asset/'
        response = self.conn.request(
            path,
            data=json.dumps(fingerprint_data)
        )
        return response



    def update_pii_from_fingerprints(self, fingerprint_data):
        path = '/v3/public/asset/update'
        response = self.conn.request(
            path,
            data=json.dumps(fingerprint_data)
        )
        return response

    def add_plain_text(self, custom_id=str(), asset_type=str(), asset_detail=str(), customer_request_term=str(),
                       monitoring_term=str(), data_science_term=str(), tags=list()):
        data = {
            'customId':custom_id,
            "type": asset_type,
            "label": asset_detail,
            "tags": tags,
            'metadata': {
                'fingerprinting_tool_name': 'Python SDK',
                'fingerprinting_tool_version': matchlight.__version__
            }
        }

        fields = dict()
        fields['field_detail'] = customer_request_term
        fields['type'] = asset_type
        fields['status'] = 'approved'

        terms = list()
        terms.append({"type": "customer_request", "term": customer_request_term})
        terms.append({"type": "regex", "term": monitoring_term})
        terms.append({"type": "data_science", "term": data_science_term})

        fields['terms'] = terms
        data['fields'] = [fields]
        path = '/v3/public/asset?unsafe=true'
        response = self.conn.request(
            path,
            data=json.dumps(data)
        )
        return response

    def update_plain_text(self, id, custom_id, asset_type, asset_detail=str(), customer_request_term=str(),
                       monitoring_term=str(), data_science_term=str(), tags=list(), offline=True):
        data = {
            "id": id,
            "customId":custom_id,
            "type": asset_type,
            "asset_detail": asset_detail,
            "tags": tags,
            'metadata': {
                'fingerprinting_tool_name': 'Python SDK',
                'fingerprinting_tool_version': matchlight.__version__
            }
        }

        fields = dict()
        fields['field_detail'] = customer_request_term
        fields['type'] = asset_type
        fields['status'] = 'approved'

        terms = list()
        terms.append({"type": "customer_request", "term": customer_request_term})
        terms.append({"type": "regex", "term": monitoring_term})
        terms.append({"type": "data_science", "term": data_science_term})

        fields['terms'] = terms
        data['fields'] = [fields]

        path = '/v3/public/asset/update?unsafe=true'
        response = self.conn.request(
            path,
            data=json.dumps(data)
        )
        return response

    def add_source_code(self, custom_id, asset_detail, tags, code_path,
                        match_score_threshold=70, offline=False):
        with io.open(code_path, 'r', encoding='utf-8') as document:
            content = document.read()

        if len(content) > MAX_DOCUMENT_FINGERPRINTS:
            raise matchlight.error.SDKError(
                f"Fingerprinter Failed: the maximum length of a Source Code record is {MAX_DOCUMENT_FINGERPRINTS} characters. Your Content size is: {len(content)}"
            )

        result_json = fingerprint(content, flags=OPTIONS_TILED, mode=MODE_CODE)
        result = json.loads(result_json)
        fingerprints = result['data']['fingerprints']

        data = {
            'customId': custom_id,
            'asset_detail': asset_detail,
            'type': "source_code",
            'metadata': {
                'fingerprinting_tool_name': 'Python SDK',
                'fingerprinting_tool_version': matchlight.__version__
            }
        }

        fields = dict()
        fields['type'] = 'sourceCode'
        fields['variants'] = [fingerprints]
        fields['field_detail'] = asset_detail

        data['fields'] = [fields]
        if tags is not None:
            if isinstance(tags, list):
                data['tags'] = tags
            else:
                data['tags'] = [tags]
        if match_score_threshold is not None:
            # data['metadata']['min_score'] = str(match_score_threshold)
            data['match_score_threshold'] = match_score_threshold
        if offline:
            return data
        else:
            return self.add_source_code_from_fingerprints(data)

    def add_source_code_from_fingerprints(self, fingerprint_data):
        path = '/v3/public/asset/'
        response = self.conn.request(
            path,
            data=json.dumps(fingerprint_data)
        )
        return response

    def update_source_code(self, asset_id, custom_id, asset_detail, tags, match_score_threshold=70, offline=False):
        data = {
            'id': asset_id,
            'customId': custom_id,
            'asset_detail': asset_detail,
            'type': "source_code",
            'metadata': {
                'fingerprinting_tool_name': 'Python SDK',
                'fingerprinting_tool_version': matchlight.__version__
            }
        }

        fields = dict()
        fields['type'] = 'sourceCode'
        #fields['variants'] = [fingerprints]
        fields['field_detail'] = asset_detail

        data['fields'] = [fields]
        if tags is not None:
            if isinstance(tags, list):
                data['tags'] = tags
            else:
                data['tags'] = [tags]
        if match_score_threshold is not None:
            # data['metadata']['min_score'] = str(match_score_threshold)
            data['match_score_threshold'] = match_score_threshold

        path = '/v3/public/asset/update'
        response = self.conn.request(
            path,
            data=json.dumps(data)
        )
        return response

    def add_pii(self, custom_id, tags, pii_type, email, first_name=None,
                      middle_name=None, last_name=None, ssn=None, street_address=None, city=None, state_province=None,
                      zip_postal_code=None, phone=None, credit_card=None, medicare_id=None, passport=None, iban=None,
                      offline=False):
        data = {
            'customId': custom_id,
            'type': "employee_pii",
            'metadata': {
                'fingerprinting_tool_name': 'Python SDK',
                'fingerprinting_tool_version': matchlight.__version__
            }
        }

        if pii_type:
            data['type'] = pii_type
            # TODO change to asset_detail
            data["asset_detail"] = pii_type

        if tags:
            if isinstance(tags, list):
                data['tags'] = tags
            else:
                data['tags'] = [tags]

        fields_list = list()
        if any((first_name, middle_name, last_name)):
            if first_name:
                for m in first_name:
                    pii_group = m['pii_group']
                    first_name1, middle_name1, last_name1 = merge_data(pii_group, first_name, middle_name, last_name)
                    if first_name1 and last_name1:
                        # res = merge_data(pii_group,first_name1,middle_name1,last_name1)
                        first_text, middle_text, last_text = first_name1, middle_name1, last_name1
                        if first_text and last_text:
                            detail = blind_name(first_text) + " " + blind_name(middle_text) + " " + blind_name(
                                last_text)
                            name_fingerprints = fingerprints_pii_name_variants(first_text or '', middle_text or None,
                                                                               last_text or '')
                            field = dict()
                            field["pii_group"] = pii_group
                            field['field_detail'] = detail
                            field['type'] = 'name'
                            field['variants'] = name_fingerprints
                            fields_list.append(field)
                        else:
                            if not first_text and not last_text:
                                raise matchlight.error.SDKError(
                                    'Fingerprinter Failed: the last_name argument is required '
                                    'along with the first_name argument.'
                                )

                            if not first_text:
                                raise matchlight.error.SDKError(
                                    'Fingerprinter Failed: the first_name argument is required '
                                )

                            if not last_text:
                                raise matchlight.error.SDKError(
                                    'Fingerprinter Failed: the last_name argument is required '
                                )

                            if first_text is not None and last_text is None:
                                raise matchlight.error.SDKError(
                                    'Fingerprinter Failed: the last_name argument is required '
                                    'along with the first_name argument.'
                                )

                            if first_text is None and last_text is not None:
                                raise matchlight.error.SDKError(
                                    'Fingerprinter Failed: the first_name argument is required '
                                    'along with the last_name argument.'
                                )
                    else:
                        if not first_name1 and not last_name1:
                            raise matchlight.error.SDKError(
                                'Fingerprinter Failed: the last_name argument is required '
                                'along with the first_name argument.'
                            )

                        if not first_name1:
                            raise matchlight.error.SDKError(
                                'Fingerprinter Failed: the first_name argument is required '
                            )

                        if not last_name1:
                            raise matchlight.error.SDKError(
                                'Fingerprinter Failed: the last_name argument is required '
                            )

                        if first_name1 is not None and last_name1 is None:
                            raise matchlight.error.SDKError(
                                'Fingerprinter Failed: the last_name argument is required '
                                'along with the first_name argument.'
                            )

                        if first_name1 is None and last_name1 is not None:
                            raise matchlight.error.SDKError(
                                'Fingerprinter Failed: the first_name argument is required '
                                'along with the last_name argument.'
                            )

        if email:
            for m in email:
                email1 = m['value']
                email_fingerprints = fingerprints_pii_email_address(email1)
                field = dict()
                field["pii_group"] = m['pii_group']
                field['field_detail'] = blind_email(email1)
                field['type'] = 'email'
                field['variants'] = email_fingerprints
                fields_list.append(field)

        if ssn:
            for m in ssn:
                ssn1 = m['value']
                ssn_fingerprints = [fingerprints_pii_ssn(ssn1)]
                field = dict()
                field["pii_group"] = m['pii_group']
                field['field_detail'] = 'ssn_fingerprints'
                field['type'] = 'ssn'
                field['variants'] = ssn_fingerprints

                fields_list.append(field)

        if street_address:
            for m in street_address:
                street_address1 = m['value']
                address_fingerprints = fingerprints_pii_address_variants(street_address1)
                field = dict()
                field["pii_group"] = m['pii_group']
                field['field_detail'] = 'street_address_fingerprints'
                field['type'] = 'address'
                field['variants'] = address_fingerprints

                fields_list.append(field)

        if any((city, state_province, zip_postal_code)):
            if city:
                for m in city:
                    pii_group = m['pii_group']
                    res = merge_data(pii_group,city,state_province,zip_postal_code)
                    city1, state_province1, zip_postal_code1 = res[0], res[1], res[2]
                    if city1 and state_province1 and zip_postal_code1:
                        csz_fingerprints = fingerprints_pii_city_state_zip_variants(*[six.text_type(text) if text is not None else '' for text in (city1, state_province1, zip_postal_code1)])
                        field = dict()
                        field['field_detail'] = 'city_state_zip_fingerprints'
                        field['type'] = 'region'
                        field['pii_group'] = pii_group
                        field['variants'] = csz_fingerprints
                        fields_list.append(field)
                    else:
                        if not city1 and not state_province1 and not zip_postal_code1:
                            raise matchlight.error.SDKError(
                                'Fingerprinter Failed: the city and state_province and zip_postal_code  argument is required '
                            )
                        if city1 and not state_province1 and not zip_postal_code1:
                            raise matchlight.error.SDKError(
                                'Fingerprinter Failed: the state_province and zip_postal_code  argument is required '
                            )
                        if not city1 and state_province1 and not zip_postal_code1:
                            raise matchlight.error.SDKError(
                                'Fingerprinter Failed: the city and zip_postal_code  argument is required '
                            )
                        if not city1 and not state_province1 and zip_postal_code1:
                            raise matchlight.error.SDKError(
                                'Fingerprinter Failed: the city1 and state_province  argument is required '
                            )
                        if not city1 and state_province1 and zip_postal_code1:
                            raise matchlight.error.SDKError(
                                'Fingerprinter Failed: the city1  is required '
                            )
                        if city1 and not state_province1 and zip_postal_code1:
                            raise matchlight.error.SDKError(
                                'Fingerprinter Failed: the State province  is required '
                            )
                        if city1 and state_province1 and not zip_postal_code1:
                            raise matchlight.error.SDKError(
                                'Fingerprinter Failed: the Zip  is required '
                            )

        if phone:
            for m in phone:
                phone1 = m['value']
                phone_fingerprints = fingerprints_pii_phone_number(phone1)
                field = dict()
                field["pii_group"] = m['pii_group']
                field['field_detail'] = 'phone_fingerprints'
                field['type'] = 'phone'
                field['variants'] = [phone_fingerprints]

                fields_list.append(field)

        if credit_card:
            for m in credit_card:
                credit_card1 = m['value']
                cc_fingerprints = fingerprints_pii_credit_card(credit_card1)
                field = dict()
                field["pii_group"] = m['pii_group']
                field['field_detail'] = 'credit_card_fingerprints'
                field['type'] = 'credit_card'
                field['variants'] = [cc_fingerprints]

                fields_list.append(field)

        if medicare_id:
            for m in medicare_id:
                medicare_id1 = m['value']
                medicare_id_fingerprints = fingerprints_pii_medicare_id(
                    medicare_id1
                )
                field = dict()
                field["pii_group"] = m['pii_group']
                field['field_detail'] = 'medicare_fingerprints'
                field['type'] = 'medicare_id'
                field['variants'] = [medicare_id_fingerprints]

                fields_list.append(field)

        if passport:
            for m in passport:
                passport1 = m['value']
                passport_fingerprints = fingerprints_pii_passport(passport1)
                field = dict()
                field["pii_group"] = m['pii_group']
                field['field_detail'] = 'passport_fingerprints'
                field['type'] = 'passport'
                field['variants'] = [passport_fingerprints]

                fields_list.append(field)

        if iban:
            for m in iban:
                iban1 = m['value']
                iban_fingerprints = fingerprints_pii_iban(iban1)
                field = dict()
                field["pii_group"] = m['pii_group']
                field['field_detail'] = 'iban_fingerprints'
                field['type'] = 'iban'
                field['variants'] = iban_fingerprints

                fields_list.append(field)

        data['fields'] = fields_list
        if offline:
            return data
        else:
            path = '/v3/public/asset/createmulti'
            response = self.conn.request(
                path,
                data=json.dumps(data)
            )
            return response
            #return response.json()

    #new
    def update_pii(self, asset_id, custom_id, tags, pii_type, email, first_name=None,
                         middle_name=None, last_name=None, ssn=None, street_address=None, city=None,
                         state_province=None,
                         zip_postal_code=None, phone=None, credit_card=None, medicare_id=None, passport=None, iban=None,
                         offline=False):
        # if first_name is not None and last_name is None:
        #     raise matchlight.error.SDKError(
        #         'Fingerprinter Failed: the last_name argument is required '
        #         'along with the first_name argument.'
        #     )
        #
        # if first_name is None and last_name is not None:
        #     raise matchlight.error.SDKError(
        #         'Fingerprinter Failed: the first_name argument is required '
        #         'along with the last_name argument.'
        #     )

        data = {
            "id": asset_id,
            "customId": custom_id,
            'type': "employee_pii",
            'metadata': {
                'fingerprinting_tool_name': 'Python SDK',
                'fingerprinting_tool_version': matchlight.__version__
            }
        }
        if pii_type:
            data['type'] = pii_type
            # TODO change to asset_detail
            data["asset_detail"] = pii_type

        if tags:
            if isinstance(tags, list):
                data['tags'] = tags
            else:
                data['tags'] = [tags]

        fields_list = list()
        if any((first_name, middle_name, last_name)):
            if first_name:
                for m in first_name:
                    pii_group = m['pii_group']
                    first_name1, middle_name1, last_name1 = merge_data(pii_group, first_name, middle_name, last_name)
                    if first_name1 and last_name1:
                        #res = merge_data(pii_group,first_name1,middle_name1,last_name1)
                        first_text,middle_text,last_text=first_name1,middle_name1,last_name1
                        if first_text and last_text:
                            detail = blind_name(first_text)+" "+blind_name(middle_text)+" "+blind_name(last_text)
                            name_fingerprints = fingerprints_pii_name_variants(first_text or '', middle_text or None, last_text or '')
                            field = dict()
                            field["pii_group"] = pii_group
                            field['field_detail'] = detail
                            field['type'] = 'name'
                            field['variants'] = name_fingerprints
                            fields_list.append(field)
                        else:
                            if not first_text and not last_text:
                                raise matchlight.error.SDKError(
                                    'Fingerprinter Failed: the last_name argument is required '
                                    'along with the first_name argument.'
                                )

                            if not first_text:
                                raise matchlight.error.SDKError(
                                    'Fingerprinter Failed: the first_name argument is required '
                                )

                            if not last_text:
                                raise matchlight.error.SDKError(
                                    'Fingerprinter Failed: the last_name argument is required '
                                )

                            if first_text is not None and last_text is None:
                                raise matchlight.error.SDKError(
                                    'Fingerprinter Failed: the last_name argument is required '
                                    'along with the first_name argument.'
                                )

                            if first_text is None and last_text is not None:
                                raise matchlight.error.SDKError(
                                    'Fingerprinter Failed: the first_name argument is required '
                                    'along with the last_name argument.'
                                )
                    else:
                        if not first_name1 and not last_name1:
                            raise matchlight.error.SDKError(
                                'Fingerprinter Failed: the last_name argument is required '
                                'along with the first_name argument.'
                            )

                        if not first_name1:
                            raise matchlight.error.SDKError(
                                'Fingerprinter Failed: the first_name argument is required '
                            )

                        if not last_name1:
                            raise matchlight.error.SDKError(
                                'Fingerprinter Failed: the last_name argument is required '
                            )

                        if first_name1 is not None and last_name1 is None:
                            raise matchlight.error.SDKError(
                                'Fingerprinter Failed: the last_name argument is required '
                                'along with the first_name argument.'
                            )

                        if first_name1 is None and last_name1 is not None:
                            raise matchlight.error.SDKError(
                                'Fingerprinter Failed: the first_name argument is required '
                                'along with the last_name argument.'
                            )


        if email is not None:
            for m in email:
                email1 = m['value']
                field = dict()
                field["pii_group"] = m['pii_group']
                if email1 == "":
                    field['variants'] = []
                else:
                    field['variants'] = fingerprints_pii_email_address(email1)

                field['field_detail'] = blind_email(email1)
                field['type'] = 'email'

                fields_list.append(field)

        if ssn is not None:
            for m in ssn:
                ssn1 = m['value']
                field = dict()
                field["pii_group"] = m['pii_group']
                if ssn1 == "":
                    field['variants'] = []
                else:
                    field['variants'] = [fingerprints_pii_ssn(ssn1)]
                field['field_detail'] = 'ssn_fingerprints'
                field['type'] = 'ssn'

                fields_list.append(field)

        if street_address is not None:
            for m in street_address:
                street_address1 = m['value']
                field = dict()
                field["pii_group"] = m['pii_group']
                if street_address1 == "":
                    field['variants'] = []
                else:
                    field['variants'] = fingerprints_pii_address_variants(street_address1)

                field['field_detail'] = 'street_address_fingerprints'
                field['type'] = 'address'

                fields_list.append(field)

        if any((city, state_province, zip_postal_code)):
            city_text, state_province_text, zip_postal_code_text = "", "", ""
            if city:
                for m in city:
                    pii_group = m['pii_group']
                    res = merge_data(pii_group, city, state_province, zip_postal_code)
                    city1, state_province1, zip_postal_code1 = res[0], res[1], res[2]
                    if city1 and state_province1 and zip_postal_code1:
                        csz_fingerprints = fingerprints_pii_city_state_zip_variants(
                            *[six.text_type(text) if text is not None else '' for text in
                              (city1, state_province1, zip_postal_code1)])
                        field = dict()
                        field['field_detail'] = 'city_state_zip_fingerprints'
                        field['type'] = 'region'
                        field['pii_group'] = pii_group
                        field['variants'] = csz_fingerprints
                        fields_list.append(field)
                    else:
                        if not city1 and not state_province1 and not zip_postal_code1:
                            raise matchlight.error.SDKError(
                                'Fingerprinter Failed: the city and state_province and zip_postal_code  argument is required '
                            )
                        if city1 and not state_province1 and not zip_postal_code1:
                            raise matchlight.error.SDKError(
                                'Fingerprinter Failed: the state_province and zip_postal_code  argument is required '
                            )
                        if not city1 and state_province1 and not zip_postal_code1:
                            raise matchlight.error.SDKError(
                                'Fingerprinter Failed: the city and zip_postal_code  argument is required '
                            )
                        if not city1 and not state_province1 and zip_postal_code1:
                            raise matchlight.error.SDKError(
                                'Fingerprinter Failed: the city1 and state_province  argument is required '
                            )
                        if not city1 and state_province1 and zip_postal_code1:
                            raise matchlight.error.SDKError(
                                'Fingerprinter Failed: the city1  is required '
                            )
                        if city1 and not state_province1 and zip_postal_code1:
                            raise matchlight.error.SDKError(
                                'Fingerprinter Failed: the State province  is required '
                            )
                        if city1 and state_province1 and not zip_postal_code1:
                            raise matchlight.error.SDKError(
                                'Fingerprinter Failed: the Zip  is required '
                            )



        if phone is not None:
            for m in phone:
                phone1 = m['value']
                field = dict()
                field["pii_group"] = m['pii_group']
                if phone1 == "":
                    field['variants'] = []
                else:
                    field['variants'] = [fingerprints_pii_phone_number(phone1)]
                field['field_detail'] = 'phone_fingerprints'
                field['type'] = 'phone'

                fields_list.append(field)

        if credit_card is not None:
            for m in credit_card:
                credit_card1 = m['value']
                field = dict()
                field["pii_group"] = m['pii_group']
                if credit_card1 == "":
                    field['variants'] = []
                else:
                    field['variants'] = [fingerprints_pii_credit_card(credit_card1)]

                field['field_detail'] = 'credit_card_fingerprints'
                field['type'] = 'credit_card'

                fields_list.append(field)

        if medicare_id is not None:
            for m in medicare_id:
                medicare_id1 = m['value']
                field = dict()
                field["pii_group"] = m['pii_group']
                if medicare_id1 == "":
                    field['variants'] = []
                else:
                    field['variants'] = [fingerprints_pii_medicare_id(medicare_id1)]

                field['field_detail'] = 'medicare_fingerprints'
                field['type'] = 'medicare_id'

                fields_list.append(field)

        if passport is not None:
            for m in passport:
                passport1 = m['value']
                field = dict()
                field["pii_group"] = m['pii_group']
                if passport1 == "":
                    field['variants'] = []
                else:
                    field['variants'] = [fingerprints_pii_passport(passport1)]
                field['field_detail'] = 'passport_fingerprints'
                field['type'] = 'passport'

                fields_list.append(field)

        if iban is not None:
            for m in iban:
                iban1 = m['value']
                field = dict()
                field["pii_group"] = m['pii_group']
                if iban1 == "":
                    field['variants'] = []
                else:
                    field['variants'] = fingerprints_pii_iban(iban1)

                field['field_detail'] = 'iban_fingerprints'
                field['type'] = 'iban'

                fields_list.append(field)

        data['fields'] = fields_list

        if offline:
            return data
        else:
            path = '/v3/public/asset/updatemulti'
            response = self.conn.request(
                path,
                data=json.dumps(data)
            )
            return response
            #return response.json

    def delete_asset(self, asset_id):
        self.conn.public_request('/v3/public/asset/delete/{}'.format(asset_id), method="DELETE")

    def list_assets(self, status=None, createdFrom=None, createdTo=None, updatedFrom=None,
                    updatedTo=None, limit=None, offset=None, tags=None):
        statuses = status if status else None
        path = "/v3/public/asset/"

        response = self.conn.public_request(
            path,
            params={
                'status': statuses,
                'tags': tags,
                'createdFrom': createdFrom,
                'createdTo': createdTo,
                'updatedFrom': updatedFrom,
                'updatedTo': updatedTo,
                'limit': limit,
                'offset': offset,
            },
            method='GET',
        )

        return response

    def assets_count(self, status=None, createdFrom=None, createdTo=None, updatedFrom=None,
                     updatedTo=None, tags=None):
        statuses = status if status else None
        path = "/v3/public/asset/count"

        response = self.conn.public_request(
            path,
            params={
                'status': statuses,
                'tags': tags,
                'createdFrom': createdFrom,
                'createdTo': createdTo,
                'updatedFrom': updatedFrom,
                'updatedTo': updatedTo,
            },
            method='GET',
        )

        return response


def merge_data(pii_group,first,middle,last):
        first_text,middle_text,last_text = "","",""
        for first_temp in first:
            if first_temp['pii_group'] == pii_group:
                first_text = first_temp['value']

        for middle_temp in middle:
            if middle_temp['pii_group'] == pii_group:
                middle_text = middle_temp['value']

        for last_temp in last:
            if last_temp['pii_group'] == pii_group:
                last_text = last_temp['value']

        return [first_text,middle_text,last_text]
