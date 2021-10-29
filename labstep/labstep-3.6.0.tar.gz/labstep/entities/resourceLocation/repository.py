#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Barney Walker <barney@labstep.com>

from labstep.entities.resourceLocation.model import ResourceLocation
import labstep.generic.entity.repository as entityRepository


def getResourceLocation(user, resource_location_id):
    return entityRepository.getEntity(
        user, ResourceLocation, id=resource_location_id
    )


def getResourceLocations(
    user, count=100, search_query=None, tag_id=None, extraParams={}
):
    params = {
        "group_id": user.activeWorkspace,
        "search_query": search_query,
        "tag_id": tag_id,
        **extraParams,
    }
    return entityRepository.getEntities(user, ResourceLocation, count, params)


def newResourceLocation(user, name, outer_location_id=None, extraParams={}):
    params = {"name": name, "outer_location_id": outer_location_id, **extraParams}
    return entityRepository.newEntity(user, ResourceLocation, params)


def editResourceLocation(resourceLocation, name, extraParams={}):
    params = {"name": name, **extraParams}
    return entityRepository.editEntity(resourceLocation, params)
