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


import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

import time
import yaml
import logging


log = logging.getLogger('settings_yaml')


class SpinButtonSetting(Gtk.SpinButton):
  def set_setting(self, setn):
    self.setting = setn
  def get_setting(self):
    return self.setting
  def set_val(self, val):
    self.setting['value'] = val
  def get_val(self):
    return self.setting['value']    

class ComboBoxTextSetting(Gtk.ComboBoxText):
  def set_setting(self, setn):
    self.setting = setn
  def get_setting(self):
    return self.setting
  def set_val(self, val):
    self.setting['value'] = val
  def get_val(self):
    return self.setting['value'] 

class FileChooserButtonSetting(Gtk.FileChooserButton):
  def set_setting(self, setn):
    self.setting = setn
  def get_setting(self):
    return self.setting
  def set_val(self, val):
    self.setting['value'] = val
  def get_val(self):
    return self.setting['value']

class SwitchSetting(Gtk.Switch):
  def set_setting(self, setn):
    self.setting = setn
  def get_setting(self):
    return self.setting
  def set_val(self, val):
    self.setting['value'] = val
  def get_val(self):
    return self.setting['value']

# class TextViewSetting(Gtk.TextView):
#   def set_setting(self, setn):
#     self.setting = setn
#   def get_setting(self):
#     return self.setting
#   def set_val(self, val):
#     self.setting['value'] = val
#   def get_val(self):
#     return self.setting['value']

class SettingsYaml():
  def __init__(self, filename):
      self.filename = filename
      self.raw_settings = {}
      self.settings = {}
      # this ts is changed on load and parse
      self.lastupdated = -1

  def load(self):
      self.raw_settings = yaml.load(open(self.filename, 'r'), Loader=yaml.SafeLoader)
      log.debug("loaded settings")
      self.parse()
      self.lastupdated = time.time()
      return self.raw_settings

  def save(self):
      yaml.dump(self.raw_settings, open(self.filename, 'w'), sort_keys=False)
      log.debug("saved settings")

  def parse_and_save(self):
      self.parse()
      self.save()

  def get_lastupdated(self):
    return self.lastupdated

  def get_raw(self):
    return self.raw_settings

  def get(self):
    return self.settings

  def parse(self):
    items = {}
    for category_key,category_v in self.raw_settings.items():
      # our top-level key  is category key
      # but we're going to have to extract the actual key value pairs from v
      kv = {}
      for item in category_v['items']:
        # such is the structure of this yaml
        # it contains other stuff as well for display purposes
        k = item['key']
        v = item['value']
        kv[k] = v

      items[category_key] = kv

    self.settings = items
    log.debug("parsed settings")
    self.lastupdated = time.time()
    return self.settings

