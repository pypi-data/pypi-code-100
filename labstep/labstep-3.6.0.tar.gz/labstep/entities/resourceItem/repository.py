#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Barney Walker <barney@labstep.com>

from labstep.entities.resourceItem.model import ResourceItem
import labstep.generic.entity.repository as entityRepository
from labstep.service.helpers import handleKeyword


def getResourceItem(user, resourceItem_id):
    return entityRepository.getEntity(user, ResourceItem, id=resourceItem_id)


def getResourceItems(
    user, resource_id=None, count=100, search_query=None, extraParams={}
):
    params = {
        "search_query": search_query,
        "resource_id": resource_id,
        **extraParams,
    }
    return entityRepository.getEntities(user, ResourceItem, count, params)


def newResourceItem(
    user,
    resource_id,
    name=None,
    availability=None,
    quantity_amount=None,
    quantity_unit=None,
    resource_location_id=None,
    extraParams={},
):
    params = {
        "resource_id": resource_id,
        "resource_location_id": resource_location_id,
        "name": name,
        "status": handleKeyword(availability),
        "quantity_amount": quantity_amount,
        "quantity_unit": quantity_unit,
        **extraParams,
    }

    return entityRepository.newEntity(user, ResourceItem, params)


def editResourceItem(
    resourceItem,
    name=None,
    availability=None,
    quantity_amount=None,
    quantity_unit=None,
    resource_location_id=None,
    deleted_at=None,
    extraParams={},
):
    params = {
        "name": name,
        "status": handleKeyword(availability),
        "resource_location_id": resource_location_id,
        "quantity_unit": quantity_unit,
        "deleted_at": deleted_at,
        **extraParams,
    }

    if quantity_amount is not None:
        params["quantity_amount"] = float(quantity_amount)

    return entityRepository.editEntity(resourceItem, params)
