# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CERN.
#
# My site is free software; you can redistribute it and/or modify it under
# the terms of the MIT License; see LICENSE file for more details.

"""JSON Schemas."""
from marshmallow import Schema, fields
from marshmallow.fields import Nested
from marshmallow_utils.fields import EDTFDateString, SanitizedUnicode
from nr_datasets_metadata.marshmallow import DataSetMetadataSchemaV3
from oarepo_communities.marshmallow import OARepoCommunitiesMixin
from oarepo_fsm.marshmallow import FSMRecordSchemaMixin
from oarepo_invenio_model.marshmallow import InvenioRecordMetadataFilesMixin, InvenioRecordMetadataSchemaV1Mixin


class DOIRequested(Schema):
    publisher = SanitizedUnicode(required=True, many=False)
    requestedBy = fields.Integer(required=True)
    requestedDate = EDTFDateString(required=True)


class NRDatasetMetadataSchemaV3(OARepoCommunitiesMixin,
                                FSMRecordSchemaMixin,
                                InvenioRecordMetadataSchemaV1Mixin,
                                InvenioRecordMetadataFilesMixin,
                                DataSetMetadataSchemaV3):
    """Schema for NR dataset record metadata."""
    _doi_requested = Nested(DOIRequested(), required=True,
                            data_key='oarepo:doirequest',
                            attribute='oarepo:doirequest')
