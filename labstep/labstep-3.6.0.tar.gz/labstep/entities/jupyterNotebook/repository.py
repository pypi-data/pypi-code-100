#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Thomas Bullier <thomas@labstep.com>

from labstep.entities.jupyterNotebook.model import JupyterNotebook
import labstep.generic.entity.repository as entityRepository


def newJupyterNotebook(user, name=None, data=None):
    return entityRepository.newEntity(user, JupyterNotebook, {"name": name, "data": data})


def getJupyterNotebook(user, guid):
    return entityRepository.getEntity(user, JupyterNotebook, id=guid)


def editJupyterNotebook(
    jupyterNotebook,
    name=None,
    status=None,
    data=None,
    extraParams={},
):
    params = {
        "name": name,
        "status": status,
        "data": data,
        **extraParams,
    }

    return entityRepository.editEntity(jupyterNotebook, params)
