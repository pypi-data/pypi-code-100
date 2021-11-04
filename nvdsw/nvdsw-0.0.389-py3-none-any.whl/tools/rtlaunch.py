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
import os
import re
import collections

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GdkPixbuf

import logging

log = logging.getLogger('rtlaunch_dialogs')



DEFAULT_WINDOW_HEIGHT = 184
DEFAULT_WINDOW_WIDTH = 555



class NVAIELaunchDialog(Gtk.Dialog):
    def __init__(self, parent, title, menu_item, flavors, preset_flavor, icon_file):
        super().__init__(title=title,transient_for=parent, flags=0)

        self.set_size_request(DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT)
        if icon_file is not None:
          icon = GdkPixbuf.Pixbuf.new_from_file(icon_file)
          super().set_default_icon(icon)
#         self.get_title_bar().set_show_close_button(False)
#        self.get_header_bar().set_show_close_button(False)
        self.set_border_width(10)
        self.set_resizable(False)
#         self.get_titlebar().set_show_close_button(False)


        self.menu_item = menu_item


        root_vbox = Gtk.Box.new(orientation = Gtk.Orientation.VERTICAL, spacing = 10)
        root_vbox.set_border_width(10)
        root_vbox.show()

        box = self.get_content_area()
        box.add(root_vbox)

#         descr_frame = Gtk.Frame(label = 'descr frame')
        descr_frame = Gtk.Frame(label = 'image details')

        description_box = Gtk.Box()
        description_box.set_border_width(10)
        description_box.pack_start(Gtk.Label(label=menu_item['description']), True, True, 0)
        
        descr_frame.add(description_box)
        descr_frame.show_all()

        root_vbox.pack_start(descr_frame, False, False, 0)


        b = Gtk.ToggleButton(label="...")
        b.set_active(False)
        b.set_relief(Gtk.ReliefStyle.NONE)
        b.connect("toggled", self.toggle_advanced)
        box = Gtk.Box()
        box.pack_start(b, True, False, 0)
        box.show_all()
        root_vbox.pack_start(box, True, False, 0)

        self.name_frame = Gtk.Frame(label = 'Size')
        name_box = Gtk.Box()
        name_box.set_border_width(10)
        self.flavor_box = Gtk.ComboBoxText()
        for _,f in flavors.items():
#           print(f)
          self.flavor_box.append(f['id'],f['name'])

        self.flavor_box.set_active_id(preset_flavor['id'])

        self.container_name_entry = Gtk.Entry()
        self.container_name_entry.set_max_length(128)
        self.container_name_entry.set_text("auto-assigned")
        name_box.pack_start(self.flavor_box, True, True, 0)
#         name_box.pack_start(Gtk.Label(label='some container name'), False, False, 0)
        self.name_frame.add(name_box)
        root_vbox.pack_start(self.name_frame, False, False, 0)

        


        hbox = Gtk.Box(spacing=10)
        hbox.set_homogeneous(False)
        

        b1 = Gtk.Button(label = "Run")
        b1.connect("clicked", self.on_run_clicked)
        b2 = Gtk.Button(label = "Cancel")
        b2.connect("clicked", self.on_cancel_clicked)
        
        hbox.pack_end(b1, False, False, 0)
        hbox.pack_end(b2, False, False, 0)
        hbox.show_all()

        root_vbox.pack_end(hbox, False, False, 0)

    def toggle_advanced(self, button):
#      print("toggle advanced called: "+str(button.get_active()))
      if not button.get_active():
        self.name_frame.hide()
      else:
        self.name_frame.show_all()

    
      

     

 
    def on_run_clicked(self, button):
#      print("save was clicked")
#      print("my height: " + str(self.get_allocation().height))
#      print("my width: " + str(self.get_allocation().width))

#       log.debug("container_name: " + self.get_container_name())
#       log.debug('id selected: ' + self.flavor_box.get_active_id())

      self.response(Gtk.ResponseType.OK)

        

    def on_cancel_clicked(self, button):
      log.debug("cancel was clicked")
#      self.emit("response", Gtk.ResponseType.CANCEL)
      self.response(Gtk.ResponseType.CANCEL)

    def get_container_name(self):
      return self.container_name_entry.get_text()
    def get_gpus(self):
      gpus = []
      i = 0
      for b in self.get_gpu_check_buttons():
        if b.get_active():
          # these need to be strings for downstream consumption even though they are numbers
          gpus.append(str(i))
        i = i + 1
      return gpus

    def get_gpu_check_buttons(self):
      return self.gpu_check_buttons
    def get_volumes(self):
      volumes = []
      i = 0
      for fcb_local_volume in self.fcb_local_volumes:
        volumes.append(fcb_local_volume.get_current_folder() + ':' + self.ent_remote_volumes[i].get_text() + ':' + 'rw')
        i = i + 1

      return volumes


    def get_attrs(self):
      attrs = {}
      attrs['flavor_id'] = self.flavor_box.get_active_id()
      return attrs




# strictly for testing
if __name__ == '__main__':


# - data:/data:rw   
# - data:/workspace/data:rw 
  item = {'id': '1001', 'name': 'PyTorch 21.08', 'description': 'Pytorch v21.08'}
  flavors = {}
  flavors['10001'] = {'id': '10001', 'name': 'tall', 'description': 'small flavor'}
  flavors['10002'] = {'id': '10002', 'name': 'grande', 'description': 'medium flavor'}
  flavors['10003'] = {'id': '10003', 'name': 'venti', 'description': 'large flavor'}
  flavors['10004'] = {'id': '10004', 'name': 'ventissimo', 'description': 'extra large flavor'}

  win = NVAIELaunchDialog(
        title = 'Launching PyTorch 21.08', 
        menu_item = item,
        flavors = flavors,
        preset_flavor = flavors['10002'],
        icon_file = '../images/nvidia.png'
  )
  win.connect("destroy", Gtk.main_quit)

  print("before win run!")
  rc = win.run()
  print("done with win run!")
  if rc == Gtk.ResponseType.CANCEL:
    print("cancel was clicked!")

  if rc == Gtk.ResponseType.OK:
    print("ok was clicked")

  attrs = win.get_attrs()
  import json
  print(json.dumps(attrs, indent=4, sort_keys=True))

# win.show()

# Gtk.Entry.get_text()
# Gtk.ToggleButton.get_active()
# Gtk.main()


