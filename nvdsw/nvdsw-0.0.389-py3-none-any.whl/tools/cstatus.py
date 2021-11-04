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
import subprocess

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GdkPixbuf

import logging

log = logging.getLogger('cstatus_dialogs')

# DEFAULT_WINDOW_HEIGHT = 184
DEFAULT_WINDOW_HEIGHT = 150
DEFAULT_WINDOW_WIDTH = 555

css = b"""

entry.non_editable {
  color: grey;
}
entry.clickable {
  text-decoration-line: underline;

}



.cstatusdialog.background {
  border-bottom-left-radius: 8px;
  border-bottom-right-radius: 8px;
}


"""

#   cursor: pointer;

# .cstatusdialog,
# .cstatusdialog .background {
#   border-top-left-radius: 8px;
#   border-top-right-radius: 8px;


style_provider = Gtk.CssProvider()
style_provider.load_from_data(css)
Gtk.StyleContext.add_provider_for_screen(
        Gdk.Screen.get_default(), style_provider,
        Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)

class CStatusDialog(Gtk.Dialog):
    def __init__(self, title, description, cstatus, cattrs, browser, gpunames, icon_file):
        super().__init__(
          title=title,
          transient_for=None, 
          flags=0, 

        )
        self.set_size_request(DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT)
        self.set_resizable(False)
        self.get_style_context().add_class("cstatusdialog")
        if icon_file is not None:
          icon = GdkPixbuf.Pixbuf.new_from_file(icon_file)
          super().set_default_icon(icon)

#           message_type=Gtk.MessageType.OTHER,
# text = text,
#           buttons = Gtk.ButtonsType.NONE
#         if buttons is not None:
#           for k,v in buttons.items():
 #            self.add_buttons(k,v)

        raw_ports = cattrs['NetworkSettings']['Ports']
        raw_volumes = cattrs['HostConfig']['Binds']
        labels = cattrs['Config']['Labels']
        browser_port = labels['browser_port']

        gpu_nums = self.parse_gpu_nums(cattrs['HostConfig']['DeviceRequests'])

        # the above gies us a list of integers
#         ports = []
#         ports.append('8888/tcp')
#         ports.append('8080/tcp')
#         browser = 'y'
        gpus = []
        for gn in gpu_nums:
          gpu = gpunames[gn] + ' [' + str(gn) + ']'
          gpus.append(gpu)

#        gpus.append('NVIDIA GeForce RTX 3090 Laptop GPU')
#        gpus.append('NVIDIA GeForce RTX 3091 Laptop GPU')

#         volumes = []
#         volumes.append('/home/nvidia/data:/data:rw')
#         volumes.append('/home/nvidia/data:/workspace/data:rw')
        ## testing

        root_vbox = Gtk.Box.new(orientation = Gtk.Orientation.VERTICAL, spacing = 10)
        root_vbox.set_border_width(10)
        root_vbox.show()

        box = self.get_content_area()
        box.add(root_vbox)

        descr_frame = Gtk.Frame(label = 'image details')

        description_box = Gtk.Box()
        description_box.set_border_width(10)
        description_box.pack_start(Gtk.Label(label=description), True, True, 0)
        
        descr_frame.add(description_box)

        descr_frame.show_all()

        root_vbox.pack_start(descr_frame, False, False, 0)        

#        self.props.image = None
#        self.set_decorated(False)
#         self.props.skip_taskbar_hint = False


        b = Gtk.ToggleButton(label="...")
        b.set_active(False)
        b.set_relief(Gtk.ReliefStyle.NONE)
        b.connect("toggled", self.toggle_advanced)
        box = Gtk.Box()
        box.pack_start(b, True, False, 0)
        box.show_all()
        root_vbox.pack_start(box, True, False, 0)

        self.name_frame = Gtk.Frame(label = 'container name')

        cname = cattrs['Name'].split('/')[1]
        name_box = Gtk.Box()
        name_box.set_border_width(10)
        name_box.pack_start(Gtk.Label(label = cname), True, True, 0)
        
        self.name_frame.add(name_box)
        root_vbox.pack_start(self.name_frame, False, False, 0)

        self.status_frame = Gtk.Frame(label = 'container status')

        status_box = Gtk.Box()
        status_box.set_border_width(10)
        status_box.pack_start(Gtk.Label(label=cstatus), True, True, 0)
        
        self.status_frame.add(status_box)
#         descr_frame.show_all()

        root_vbox.pack_start(self.status_frame, False, False, 0) 



        self.gpu_frame = Gtk.Frame(label = 'assigned gpus')
        gpu_vbox = Gtk.Box.new(orientation = Gtk.Orientation.VERTICAL, spacing = 5)
        gpu_vbox.set_border_width(10)
        self.gpu_frame.add(gpu_vbox)

        self.gpu_check_buttons = []
        for gpu in gpus:
          gpu_box = Gtk.Box(spacing = 10)
#           gpu_check_button = Gtk.CheckButton()
#           gpu_check_button.set_active(True)
#           gpu_check_button.set_editable(False)
#           self.gpu_check_buttons.append(gpu_check_button)
#           gpu_box.pack_start(gpu_check_button, False, False, 0)
          gpu_box.pack_start(Gtk.Label(label = gpu ), False, False, 0)
          gpu_vbox.pack_start(gpu_box, False, False, 0)
    

        root_vbox.pack_start(self.gpu_frame, False, False, 0)   



        self.ports_frame = Gtk.Frame(label = 'exposed ports')
        ports_box = Gtk.Box.new(orientation = Gtk.Orientation.HORIZONTAL, spacing = 5)
        ports_box.set_border_width(10)
        self.ports_frame.add(ports_box)

        self.remote_vbox_ports = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 5)
        b_remote_ports = Gtk.Box()
        b_remote_ports.pack_start(Gtk.Label(label='container port                        '), False, False, 0)
        self.remote_vbox_ports.pack_start(b_remote_ports, False, False, 0)

        ports_box.pack_start(self.remote_vbox_ports, False, False, 0)

        self.local_vbox_ports = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 5)
        b_host_ports = Gtk.Box()
        b_host_ports.pack_start(Gtk.Label(label='local host port                        '), False, False, 0)
        self.local_vbox_ports.pack_start(b_host_ports, False, False, 0)

        ports_box.pack_start(self.local_vbox_ports, False, False, 0)

        # the browser port should be elevated to #1 position in the list
        processed_ports = {}
        for k,v in raw_ports.items():
          if k == browser_port:
            processed_ports[browser_port] = v
        
        for k,v in raw_ports.items():
          if k == browser_port:
            continue
          processed_ports[k] = v


        for k,v in processed_ports.items():
# >> c.attrs['NetworkSettings']['Ports']
# {'6006/tcp': None, '8888/tcp': [{'HostIp': '0.0.0.0', 'HostPort': '49168'}, {'HostIp': '::', 'HostPort': '49168'}]}
          if v is None:
            continue
          container_port = k
          local_port = v[0]['HostPort']

          entry_container_port = Gtk.Entry()
          entry_container_port.set_max_length(10)
          entry_container_port.set_text(container_port)
          entry_container_port.set_editable(False) 
          entry_container_port.get_style_context().add_class("non_editable")
#          self.container_ports_entries.append(entry_container_port)
          self.remote_vbox_ports.pack_start(entry_container_port, False, False, 0)
     

          entry_local_port = Gtk.Entry()
          entry_local_port.set_text(local_port)
          entry_local_port.set_editable(False) 
          entry_local_port.get_style_context().add_class("clickable")
          entry_local_port.connect('button-press-event', self.open_local_port)
          self.local_vbox_ports.pack_start(entry_local_port, False, False, 0)


        
        browser_vbox_ = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 5)
        b = Gtk.Box()
        b.pack_start(Gtk.Label(label='open browser'), False, False, 0)
        browser_vbox_.pack_start(b, False, False, 0)

        b_is_browser_port = Gtk.Entry()
        b_is_browser_port.set_editable(False) 
        b_is_browser_port.get_style_context().add_class("non_editable")
        if browser:
          b_is_browser_port.set_text("Yes")
        else:
          b_is_browser_port.set_text('No')  
        browser_vbox_.pack_start(b_is_browser_port, False, False, 0)

        ports_box.pack_start(browser_vbox_, False, False, 0)


        root_vbox.pack_start(self.ports_frame, False, False, 0)            


        self.volumes_frame = Gtk.Frame(label = 'mounted volumes')
        volumes_box = Gtk.Box.new(orientation = Gtk.Orientation.HORIZONTAL, spacing = 5)
        volumes_box.set_border_width(10)
        self.volumes_frame.add(volumes_box)

        self.local_vbox_volumes = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 5)
        b_host_volumes = Gtk.Box()
        b_host_volumes.pack_start(Gtk.Label(label='local host                                 '), False, False, 0)
        self.local_vbox_volumes.pack_start(b_host_volumes, False, False, 0)

        volumes_box.pack_start(self.local_vbox_volumes, False, False, 0)

        self.remote_vbox_volumes = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 5)
        b_remote_volumes = Gtk.Box()
        b_remote_volumes.pack_start(Gtk.Label(label='container                                   '), False, False, 0)
        self.remote_vbox_volumes.pack_start(b_remote_volumes, False, False, 0)

        volumes_box.pack_start(self.remote_vbox_volumes, False, False, 0)

        for v in raw_volumes:
# >>> c.attrs['HostConfig']['Binds']
# ['/home/nvidia/data:/data:rw', '/home/nvidia/data:/workspace/data:rw']
          
          s = v.split(':')
          local_mnt = s[0]
          remote_mnt = s[1]
          mode = s[2]


          entry_local_volume = Gtk.Entry()
          entry_local_volume.set_max_length(128)
          entry_local_volume.set_text(local_mnt)
          entry_local_volume.set_editable(False) 
          entry_local_volume.get_style_context().add_class("non_editable")
#           self.fcb_local_volumes.append(fcb_local_volume)
          self.local_vbox_volumes.pack_start(entry_local_volume, False, False, 0)

          entry_remote_volume = Gtk.Entry()
          entry_remote_volume.set_max_length(128)
          entry_remote_volume.set_text(remote_mnt)
          entry_remote_volume.set_editable(False) 
          entry_remote_volume.get_style_context().add_class("non_editable")
#           self.ent_remote_volumes.append(entry_remote_volume)
          self.remote_vbox_volumes.pack_start(entry_remote_volume, False, False, 0)


        root_vbox.pack_start(self.volumes_frame, False, False, 0)

        hbox = Gtk.Box(spacing=10)
        hbox.set_homogeneous(False)

        b1 = Gtk.Button(label = "STOP AND REMOVE")
        b1.connect("clicked", self.on_stop_clicked)
        b2 = Gtk.Button(label = "CANCEL")
        b2.connect("clicked", self.on_cancel_clicked)
        
        hbox.pack_end(b1, False, False, 0)
        hbox.pack_end(b2, False, False, 0)
        hbox.show_all()

        root_vbox.pack_end(hbox, False, False, 0)


    def on_cancel_clicked(self, button):
      log.debug("cancel was clicked")
      self.response(Gtk.ResponseType.CANCEL)

    def on_stop_clicked(self, button):
      log.debug("stop was clicked")
      self.response(Gtk.ResponseType.OK)


    def toggle_advanced(self, button):
      log.debug("toggle advanced was clicked")
#      print("toggle advanced called: "+str(button.get_active()))
      if not button.get_active():
        self.name_frame.hide()
        self.status_frame.hide()
        self.gpu_frame.hide()
        self.ports_frame.hide()
        self.volumes_frame.hide()
      else:
        self.name_frame.show_all()
        self.status_frame.show_all()
        self.gpu_frame.show_all()
        self.ports_frame.show_all()
        self.volumes_frame.show_all() 

    def open_local_port(self, entry, ev):
      bp = entry.get_text()
      log.debug("open_local_port was clicked: " + entry.get_text())
      self.open_url("http://localhost:" + bp + "/lab")

    def open_url(self,url):
      cmd = ["/usr/bin/x-www-browser", url]
      subprocess.Popen(cmd)

    def parse_gpu_nums(self, device_str):
      log.debug("in parse_gpu_nums")
 # >>> c.attrs['HostConfig']['DeviceRequests']
 # [{'Driver': '', 'Count': 0, 'DeviceIDs': ['0'], 'Capabilities': [['gpu']], 'Options': {}}]
      gpunums = []
      for ds in device_str:
        gpu_capable = False
        for i in ds['Capabilities']:

          for j in i:
            if j == 'gpu':
              gpu_capable = True
              break
          
          if gpu_capable:  # flatten this list
            for dev_id in ds['DeviceIDs']:
              gpunums.append(int(dev_id))
      for g in gpunums:
        log.debug("parse_gpu_nums: found gpu " + str(g))
      return gpunums
