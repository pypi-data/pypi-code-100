# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2018 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Dataset permisssion factories."""

from oarepo_fsm.permissions import require_all, require_any
from oarepo_communities.permissions import read_object_permission_impl

from nr_datasets.constants import open_access_slug, restricted_slug
from nr_datasets.utils import access_rights_factory


def access_rights_required(rights):
    rights = set(rights)

    def factory(record, *_args, **_kwargs):
        def can():
            current_rights = record.get('accessRights')
            if current_rights and len(current_rights) == 1:
                current_rights = current_rights[0]
            else:
                current_rights = []

            return current_rights['links']['self'] in rights

        return type('AccessRightsRequiredPermission', (), {'can': can})

    return factory


def files_read_permission_factory(record, *args, **kwargs):
    return require_any(
        require_all(
            read_object_permission_impl,
            access_rights_required(access_rights_factory(restricted_slug))
        ),
        access_rights_required(access_rights_factory(open_access_slug))
    )
