#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Barney Walker <barney@labstep.com>

from labstep.service.helpers import handleKeyword
from labstep.entities.orderRequest.model import OrderRequest
import labstep.generic.entity.repository as entityRepository


def getOrderRequest(user, orderRequest_id):
    return entityRepository.getEntity(user, OrderRequest, id=orderRequest_id)


def getOrderRequests(
    user,
    count=100,
    search_query=None,
    tag_id=None,
    status=None,
    extraParams={},
):
    params = {
        "group_id": user.activeWorkspace,
        "search_query": search_query,
        "tag_id": tag_id,
        "status": handleKeyword(status),
        **extraParams,
    }
    return entityRepository.getEntities(user, OrderRequest, count, params)


def newOrderRequest(user, resource_id=None, quantity=1, extraParams={}):
    params = {"resource_id": resource_id, "quantity": quantity, **extraParams}
    return entityRepository.newEntity(user, OrderRequest, params)


def editOrderRequest(
    orderRequest,
    status=None,
    resource_id=None,
    quantity=None,
    price=None,
    currency=None,
    deleted_at=None,
    extraParams={},
):
    params = {
        "status": handleKeyword(status),
        "resource_id": resource_id,
        "quantity": quantity,
        "price": price,
        "currency": currency,
        "deleted_at": deleted_at,
        **extraParams,
    }

    return entityRepository.editEntity(orderRequest, params)
