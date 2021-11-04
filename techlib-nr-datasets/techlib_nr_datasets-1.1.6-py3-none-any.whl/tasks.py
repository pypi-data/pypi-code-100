# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2018 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Dataset records celery tasks."""
from datetime import datetime

from edtf.parser import parse_edtf
from flask import current_app
from invenio_db import db
from invenio_pidstore.models import PersistentIdentifier
from invenio_records_rest.utils import obj_or_import_string
from sqlalchemy.orm.exc import NoResultFound

from nr_datasets.constants import embargoed_slug, open_access_slug
from nr_datasets.utils import access_rights_factory, edtf_to_date


def update_access_rights():
    endpoints = current_app.config.get("RECORDS_REST_ENDPOINTS").endpoints
    for config in endpoints.values():
        try:
            pid_type: str = config["pid_type"]
            print(f'PID type: {pid_type}')
            record_class = obj_or_import_string(config["record_class"])
            pids = PersistentIdentifier.query.filter_by(pid_type=pid_type).all()
            for i, pid in enumerate(pids):
                try:
                    record = record_class.get_record(pid.object_uuid)
                except NoResultFound:
                    continue

                ar = record.get('accessRights')
                if ar and len(ar) == 1:
                    link = ar[0].get('links', {}).get('self')
                    if link.endswith(embargoed_slug):
                        date_embargo = edtf_to_date(record.get('dateAvailable'))

                        if datetime.today() >= date_embargo:
                            print(f"Embargo expired. Setting OpenAccess rights on record: {record['InvenioID']}")
                            record['accessRights'] = access_rights_factory(open_access_slug)
                            record.commit()
        finally:
            db.session.commit()
