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

import sys
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GdkPixbuf

import logging

log = logging.getLogger('license_dialogs')



class LicenseDialog(Gtk.AboutDialog):
  def __init__(self, title = '', comments = '', license_str = '', icon_file = None):
        Gtk.AboutDialog.__init__(self)

        # No need for the close button
#        self.get_title_bar().set_show_close_button(False)
        self.set_modal(True)

        self.set_program_name(title)
        self.set_comments(comments)
        self.set_license_type(Gtk.License.GPL_3_0)
        self.set_resizable(True)

        self.set_license(license_str)
        if icon_file is not None:
            icon = GdkPixbuf.Pixbuf.new_from_file(icon_file)
            super().set_logo(icon)

        hbox = Gtk.Box(spacing = 20)
        self.radio_yes = Gtk.RadioButton.new_with_label_from_widget(None, "I accept")
        radio_no = Gtk.RadioButton.new_with_label_from_widget(self.radio_yes, "I do not accept")
        radio_no.set_active(True)
        
        button = Gtk.Button(label="Submit")
        button.connect("clicked", self.submitted)

        hbox.pack_end(button, False, False, 10)
        hbox.pack_end(radio_no, False, False, 0)
        hbox.pack_end(self.radio_yes, False, False, 0)

        self.get_content_area().add(hbox)
        self.show_all()


        

  def submitted(self,m):
      if self.radio_yes.get_active():
        self.response(Gtk.ResponseType.OK)
      else:
        self.response(Gtk.ResponseType.CANCEL) 


# strictly for testing
if __name__ == '__main__':

  log.setLevel(logging.DEBUG)
  log.addHandler(logging.StreamHandler())
  log.debug("starting..")
  ICON_DEFAULT = "/home/dima/nvdss/nvdsw/images/nvidia.png"

  with open ("../LICENSE", "r") as lfile:
    LICENSE = lfile.readlines()

  license_str = ' '.join(LICENSE)

  comments = 'Please carefully review the terms of the End User License Agreement located in the License tab and then indicate your agreement by clicking below.\n\nTo exit, choose "I do not accept".'
  dialog = LicenseDialog(title = "Data Science Workbench", comments = comments, license_str = license_str, icon_file = ICON_DEFAULT)

  response = dialog.run()
#  log.debug(response)
  if response == Gtk.ResponseType.OK:
    log.debug("license accepted!")
  else:
    log.debug("license not accepted")
