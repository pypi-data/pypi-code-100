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
import sys
import traceback

log = logging.getLogger('hardware')


class HWStats:
  def __init__(self, config):
    self.conf = config 

  def get_gpus(self):
    GPU = []
    try:
      from pynvml import nvmlDeviceGetCount, nvmlDeviceGetName, nvmlDeviceGetHandleByIndex, nvmlInit, nvmlShutdown
      nvmlInit()
      for i in range(nvmlDeviceGetCount()):
        GPU.append(nvmlDeviceGetName(nvmlDeviceGetHandleByIndex(i)).decode('utf-8'))

      nvmlShutdown()
    except ImportError as error:
      log.warning("pynvml failed to import; the driver may not be installed") 
      exc_type, exc_value, exc_tb = sys.exc_info()
      log.warning(traceback.format_exception(exc_type, exc_value, exc_tb))


    except Exception as exception:
      log.warning("unable to quey NVML")
      exc_type, exc_value, exc_tb = sys.exc_info()
      log.warning(traceback.format_exception(exc_type, exc_value, exc_tb))

    return GPU

  def get_driver_version(self):
    DRIVER_VER = "not found"
    try:
      from pynvml import nvmlSystemGetDriverVersion, nvmlInit, nvmlShutdown
      nvmlInit()
      DRIVER_VER = nvmlSystemGetDriverVersion().decode('utf-8')
      nvmlShutdown()
    except ImportError as error:
      log.warning("pynvml failed to import; the driver may not be installed") 
      exc_type, exc_value, exc_tb = sys.exc_info()
      log.warning(traceback.format_exception(exc_type, exc_value, exc_tb))
    except Exception as exception:
      log.warning("unable to quey NVML")
      exc_type, exc_value, exc_tb = sys.exc_info()
      log.warning(traceback.format_exception(exc_type, exc_value, exc_tb))
      
    return DRIVER_VER 