#!/usr/bin/env python3
#
# coding: utf-8

# Copyright (c) 2019-2020, NVIDIA CORPORATION.  All Rights Reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.
#



import logging
import os
import sys
import time
import traceback
from copy import copy

import docker

log = logging.getLogger('curated_menu_item')
client = docker.DockerClient()

class CuratedMenuItem:
  

  def __init__(self, config, uimenu):

    self.config = config
    self.uimenu = uimenu
    self.image = None
    try:
      self.image = client.images.get(config['image'])
      self.inited = True
    except Exception:
      log.error("unable to find image")
      exc_type, exc_value, exc_tb = sys.exc_info()
      log.warerrorning(traceback.format_exception(exc_type, exc_value, exc_tb))
      self.inited = False

  def initialized(self):
      return self.inited