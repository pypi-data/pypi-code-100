#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Thomas Bullier <thomas@labstep.com>

from labstep.entities.jupyterInstance.model import JupyterInstance
import labstep.generic.entity.repository as entityRepository


def getJupyterInstance(user, guid):
    return entityRepository.getEntity(user, JupyterInstance, id=guid)


def editJupyterInstance(
    jupyterInstance,
    startedAt=None,
    endedAt=None
):
    params = {
        "started_at": startedAt,
        "ended_at": endedAt,
    }

    return entityRepository.editEntity(jupyterInstance, params)
