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

log = logging.getLogger('claunch_dialogs')



DEFAULT_WINDOW_HEIGHT = 184
DEFAULT_WINDOW_WIDTH = 555

DOCKER_VALID_CONTAINER_REGEX = re.compile('^[a-zA-Z0-9][a-zA-Z0-9_.-]*$',re.I)

css = b"""

entry.non_editable {
  color: grey;
}


"""

style_provider = Gtk.CssProvider()
style_provider.load_from_data(css)
Gtk.StyleContext.add_provider_for_screen(
        Gdk.Screen.get_default(), style_provider,
        Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)

# log.setLevel(logging.DEBUG)
# log.addHandler(logging.StreamHandler())
# log.debug("starting..")

class CLaunchDialog(Gtk.Dialog):
    def __init__(self, parent, title, description, gpus, ports, volumes, browser, license_url, icon_file, settings, selected_tag = None):
        super().__init__(title=title,transient_for=parent, flags=0)

        self.settings = settings
        self.set_size_request(DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT)
        if icon_file is not None:
          icon = GdkPixbuf.Pixbuf.new_from_file(icon_file)
          super().set_default_icon(icon)
#         self.get_title_bar().set_show_close_button(False)
#        self.get_header_bar().set_show_close_button(False)
        self.set_border_width(10)
        self.set_resizable(False)
#         self.get_titlebar().set_show_close_button(False)
        self.gpus = gpus
#         self.volumes = volumes
        if ports is not None:
          self.default_ports = ports 
        else:
          self.default_ports = []

        if volumes is not None:
          self.default_volumes = self.clean_volumes(volumes, settings)
        else:
          self.default_volumes = []

        self.container_ports_entries = []

        self.fcb_local_volumes = []
        self.ent_remote_volumes = []
        self.selected_tag = selected_tag


        self.root_vbox = Gtk.Box.new(orientation = Gtk.Orientation.VERTICAL, spacing = 10)
        self.root_vbox.set_border_width(10)
        self.root_vbox.show()

        box = self.get_content_area()
        box.add(self.root_vbox)

#         descr_frame = Gtk.Frame(label = 'descr frame')
        descr_frame = Gtk.Frame(label = 'image details')

        description_box = Gtk.Box()
        description_box.set_border_width(10)
        dlabel = description
        if self.selected_tag is not None:
          dlabel += ' ' + selected_tag['tag']

        description_box.pack_start(Gtk.Label(label=dlabel), True, True, 0)
        
        descr_frame.add(description_box)
        descr_frame.show_all()

        self.root_vbox.pack_start(descr_frame, False, False, 0)


        b = Gtk.ToggleButton(label="...")
        b.set_active(False)
        b.set_relief(Gtk.ReliefStyle.NONE)
        b.connect("toggled", self.toggle_advanced)
        box = Gtk.Box()
        box.pack_start(b, True, False, 0)
        box.show_all()
        self.root_vbox.pack_start(box, True, False, 0)

        self.name_frame = Gtk.Frame(label = 'container name')
        name_box = Gtk.Box()
        name_box.set_border_width(10)
        self.container_name_entry = Gtk.Entry()
        self.container_name_entry.set_max_length(128)
        self.container_name_entry.set_text("auto-assigned")
        name_box.pack_start(self.container_name_entry, True, True, 0)
#         name_box.pack_start(Gtk.Label(label='some container name'), False, False, 0)
        self.name_frame.add(name_box)
        self.root_vbox.pack_start(self.name_frame, False, False, 0)

        self.gpu_frame = Gtk.Frame(label = 'gpus to pass through')
        gpu_vbox = Gtk.Box.new(orientation = Gtk.Orientation.VERTICAL, spacing = 5)
        gpu_vbox.set_border_width(10)
        self.gpu_frame.add(gpu_vbox)

        self.gpu_check_buttons = []
        i=0
        for gpu in gpus:
          gpu_box = Gtk.Box(spacing = 10)
          gpu_check_button = Gtk.CheckButton()
          gpu_check_button.set_active(True)
          self.gpu_check_buttons.append(gpu_check_button)
          gpu_box.pack_start(gpu_check_button, False, False, 0)
          gpu_box.pack_start(Gtk.Label(label = gpu + ' [' + str(i) + ']'), False, False, 0)
          gpu_vbox.pack_start(gpu_box, False, False, 0)
          i = i + 1
    

        self.root_vbox.pack_start(self.gpu_frame, False, False, 0)

        self.ports_frame = Gtk.Frame(label = 'ports to expose')
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

        for p in self.default_ports:
          entry_container_port = Gtk.Entry()
          entry_container_port.set_max_length(10)
          entry_container_port.set_text(p)
          self.container_ports_entries.append(entry_container_port)
          self.remote_vbox_ports.pack_start(entry_container_port, False, False, 0)
     

          entry_local_port = Gtk.Entry()
          entry_local_port.set_text("auto-assigned")
          entry_local_port.set_editable(False) 
          entry_local_port.get_style_context().add_class("non_editable")
          self.local_vbox_ports.pack_start(entry_local_port, False, False, 0)


        
        browser_vbox_ = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 5)
        b = Gtk.Box()
        b.pack_start(Gtk.Label(label='open'), False, False, 0)
        browser_vbox_.pack_start(b, False, False, 0)

        b_is_browser_port = Gtk.Box(spacing = 0)
        b_is_browser_port.set_border_width(8)
        self.is_browser = Gtk.CheckButton()
        if browser == 'y':
          self.is_browser.set_active(True)
        else:
          self.is_browser.set_active(False)   
        b_is_browser_port.pack_start(self.is_browser, False, False, 0)
        browser_vbox_.pack_start(b_is_browser_port, False, False, 0)

        ports_box.pack_start(browser_vbox_, False, False, 0)


        add_vbox_ports = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 5)
        b = Gtk.Box()
        b.pack_start(Gtk.Label(label='browser'), False, False, 0)
        add_vbox_ports.pack_start(b, False, False, 0)

        b_add_ports = Gtk.Box(spacing = 5)
        b = Gtk.Button(label='+')
        b.connect('clicked', self.on_add_ports)
        b_add_ports.pack_start(b, False, False, 0)

        b = Gtk.Button(label='-')
        b.connect('clicked', self.on_remove_ports)
        b_add_ports.pack_start(b, False, False, 0)
        add_vbox_ports.pack_end(b_add_ports, False, False, 0)
        ports_box.pack_start(add_vbox_ports, False, False, 0)

        self.root_vbox.pack_start(self.ports_frame, False, False, 0)

        self.volumes_frame = Gtk.Frame(label = 'volumes to mount')
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

        for v in self.default_volumes:
          s = v.split(':')
          local_mnt = s[0]
          remote_mnt = s[1]
          mode = s[2]


          fcb_local_volume = Gtk.FileChooserButton(title="Folder to mount inside container", action = Gtk.FileChooserAction.SELECT_FOLDER)
          fcb_local_volume.set_current_folder(local_mnt)
          self.fcb_local_volumes.append(fcb_local_volume)
          self.local_vbox_volumes.pack_start(fcb_local_volume, False, False, 0)

          entry_remote_volume = Gtk.Entry()
          entry_remote_volume.set_max_length(128)
          entry_remote_volume.set_text(remote_mnt)
          self.ent_remote_volumes.append(entry_remote_volume)
          self.remote_vbox_volumes.pack_start(entry_remote_volume, False, False, 0)


        add_vbox_volumes = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 5)
        b = Gtk.Box()
        b.pack_start(Gtk.Label(label=' '), False, False, 0)
        add_vbox_volumes.pack_start(b, False, False, 0)

        b_add_volumes = Gtk.Box(spacing = 5)
        b = Gtk.Button(label='+')
        b.connect('clicked', self.on_add_volumes)
        b_add_volumes.pack_start(b, False, False, 0)
        
        b = Gtk.Button(label='-')
        b.connect('clicked', self.on_remove_volumes)
        b_add_volumes.pack_start(b, False, False, 0)
        add_vbox_volumes.pack_end(b_add_volumes, False, False, 0)
        volumes_box.pack_start(add_vbox_volumes, False, False, 0)



        self.root_vbox.pack_start(self.volumes_frame, False, False, 0)



        hbox = Gtk.Box(spacing=10)
        hbox.set_homogeneous(False)
        label = Gtk.Label()
        label.set_markup('By launching, you accept the <a href="' + license_url + '">License Agreement</a>')
        hbox.pack_start(label, False, False, 0)

        b1 = Gtk.Button(label = "Run")
        b1.connect("clicked", self.on_run_clicked)
        b2 = Gtk.Button(label = "Cancel")
        b2.connect("clicked", self.on_cancel_clicked)
        
        hbox.pack_end(b1, False, False, 0)
        hbox.pack_end(b2, False, False, 0)
        hbox.show_all()

        self.root_vbox.pack_end(hbox, False, False, 0)

    def toggle_advanced(self, button):
#      print("toggle advanced called: "+str(button.get_active()))
      if not button.get_active():
        self.name_frame.hide()
        self.gpu_frame.hide()
        self.ports_frame.hide()
        self.volumes_frame.hide()
      else:
        self.name_frame.show_all()
        self.gpu_frame.show_all()
        self.ports_frame.show_all()
        self.volumes_frame.show_all()

    def on_add_ports(self, button):
      log.debug("add ports clicked")
      entry_container_port = Gtk.Entry()
      entry_container_port.set_max_length(10)

      n_children = len(self.local_vbox_ports.get_children()) - 1
      if n_children < len(self.default_ports):
        entry_container_port.set_text(self.default_ports[n_children])
      else:
        entry_container_port.set_text('0000/tcp')

      self.container_ports_entries.append(entry_container_port)
      self.remote_vbox_ports.pack_start(entry_container_port, False, False, 0)
     
      entry_local_port = Gtk.Entry()
      entry_local_port.set_text("auto-assigned")
      entry_local_port.set_editable(False) 
      entry_local_port.get_style_context().add_class("non_editable")
      self.local_vbox_ports.pack_start(entry_local_port, False, False, 0)

      self.ports_frame.show_all()

    def on_remove_ports(self, button):
      log.debug("remove ports clicked")
      self.container_ports_entries.pop()
      cs = self.remote_vbox_ports.get_children()
      self.remote_vbox_ports.remove(cs[-1])

      cs = self.local_vbox_ports.get_children()
      self.local_vbox_ports.remove(cs[-1])

      self.ports_frame.show_all()


    def on_add_volumes(self, button):
      log.debug("add volumes clicked")

      

      n_children = len(self.local_vbox_volumes.get_children()) - 1
      if n_children < len(self.default_volumes):
        dpe = self.default_volumes[n_children].split(':')
        local_mnt = dpe[0]
        remote_mnt = dpe[1]
      else:
        local_mnt = os.environ['HOME']
        remote_mnt = ''

      fcb_local_volume = Gtk.FileChooserButton(title="Folder to mount inside container", action = Gtk.FileChooserAction.SELECT_FOLDER)
      fcb_local_volume.set_current_folder(local_mnt)
      self.fcb_local_volumes.append(fcb_local_volume)
      self.local_vbox_volumes.pack_start(fcb_local_volume, False, False, 0)

      
      entry_remote_volume = Gtk.Entry()
      entry_remote_volume.set_max_length(128)
      entry_remote_volume.set_text(remote_mnt)
      self.ent_remote_volumes.append(entry_remote_volume)
      self.remote_vbox_volumes.pack_start(entry_remote_volume, False, False, 0)

      self.volumes_frame.show_all()      

    def on_remove_volumes(self, button):
      log.debug("remove volumes clicked")
      self.fcb_local_volumes.pop()
      self.ent_remote_volumes.pop()
      cs = self.local_vbox_volumes.get_children()
      self.local_vbox_volumes.remove(cs[-1])

      cs = self.remote_vbox_volumes.get_children()
      self.remote_vbox_volumes.remove(cs[-1])

      self.volumes_frame.show_all() 

    def detect_duplicates_in_volumes(self, volumes):
      err_msg = ''
      rc = True

      # looking for duplicates in container volumes only; 
      # since host mountpoints can be passed through more than once
      cvs = []
      for v in volumes:
        sv = v.split(':')
        cvs.append(sv[1])

      for item, count in collections.Counter(cvs).items():
        if count > 1:
          rc = False
          err_msg += 'path ' + item + ' was specified ' + str(count) + ' times\n'

      return rc, err_msg

    def validate_volume(self, vol):
      err_msg = ''
      rc = True

      vs = vol.split(':')
      if len(vs) < 3:
        return False, "invalid volume format: " + vol

      for v in vs[:2]:
        rcc, msg = self.validate_path(v)
        if not rcc:
          rc = False
          err_msg += msg + '\n'

      return rc, err_msg

    def validate_port(self, port):
      err_msg = ''
      rc = True
      ps = port.split('/')
      if len(ps) < 2:
        return False, "invalid port format: " + port



      try:
        i = int(ps[0])
        if i < 1 or i > 65535:
          raise ValueError

      except ValueError as ve:
        err_msg += 'invalid port number: ' + ps[0] + '\n'
        rc = False

      if ps[1] != 'tcp' and ps[1] != 'udp' and ps[1] != 'sctp':
        err_msg += 'invalid protocol: ' + ps[1]
        rc = False

      return rc, err_msg

    def validate_container_name(self, cname):
      if DOCKER_VALID_CONTAINER_REGEX.match(cname):
        return True, ''
      else:
        return False, 'invalid container name: ' + cname

    def validate_path(self, path):
#      print('validaing path: '+ path)
      if not os.path.isabs(path):
        return False, "invalid absolute path: " + path    

      return True, ''  

    def validate(self):
      err_msg = ''
      rc = True

      rcc, msg = self.validate_container_name(self.get_container_name())        
      if not rcc:
        rc = False
        err_msg += msg + '\n'

      ports = self.get_ports()
      # find duplicates
      for item, count in collections.Counter(ports).items():
        if count > 1:
          rc = False
          err_msg += 'port ' + item + ' was specified ' + str(count) + ' times\n'


      for p in ports:
#        print('port: ' + p)
        rcc, msg = self.validate_port(p)
        if not rcc:
          rc = False
          err_msg += msg + '\n'

      volumes = self.get_volumes()


      for v in volumes:
        rcc, msg = self.validate_volume(v)
        if not rcc:
          rc = False
          err_msg += msg + '\n'    

      rcc, msg = self.detect_duplicates_in_volumes(volumes)
      if not rcc:
        rc = False
        err_msg += msg + '\n'

      return rc, err_msg   

    def on_run_clicked(self, button):
#      print("save was clicked")
#      print("my height: " + str(self.get_allocation().height))
#      print("my width: " + str(self.get_allocation().width))

      log.debug("container_name: " + self.get_container_name())
      for b in self.get_gpu_check_buttons():
        log.debug("gpu enabled: " + str(b.get_active()))

      for p in self.get_ports():
        log.debug("ports: " + p)

      log.debug("the first port is browser port: " + str(self.is_browser.get_active()))

      for v in self.get_volumes():
        log.debug("volumes: " + v)

      rc, msg = self.validate()
      if rc:
        log.debug("validation passed,not displaying anything for now.")
#         dialog = Gtk.MessageDialog(parent = self, message_type = Gtk.MessageType.INFO, buttons = Gtk.ButtonsType.OK, text = 'message')
      else:
        dialog = Gtk.MessageDialog(parent = self, message_type = Gtk.MessageType.ERROR, buttons = Gtk.ButtonsType.OK, text = msg)
        dialog.run()
        dialog.destroy()

      if rc:
        self.response(Gtk.ResponseType.OK)
      # otherwise, we just chill.  they need to correct the mistakes and try again or click 'cancel'
        

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

    def get_ports(self):
      ports = []
      for i in self.container_ports_entries:
        ports.append(i.get_text())            
      return ports

    def convert_ports_to_dict(self, ports):
      dict_ports = {}
      for p in ports:
        dict_ports[p] = ''

      return dict_ports

    def get_attrs(self):
      attrs = {}
      attrs['ports'] = self.convert_ports_to_dict(self.get_ports())
      attrs['volumes'] = self.get_volumes()
      attrs['name'] = self.get_container_name()
      attrs['gpus'] = self.get_gpus()
      attrs['browser'] = self.is_browser.get_active()
      return attrs

    def clean_volumes(self, raw_volumes, settings):
      volumes = []
      for vv in raw_volumes:
        log.debug('processing: '+ vv)
        vaa = vv.split(':')
        v = vaa[0]
        rest = vaa[1:]
        # if v.startswith('/'):
        if v != 'DOCKER_SOURCE_MOUNT':
          # absolute path
          volumes.append(vv)
        else:
          # volumes.append(os.environ['HOME'] + '/' + v + ':' + ':'.join(rest))
          value = settings.get()['Containers']['DOCKER_SOURCE_MOUNT']
          if not value.startswith('/'):
            value = os.environ['HOME'] + '/' + value
          log.debug('DOCKER_SOURCE_MOUNT: ' + value )
          volumes.append(value + ':' + ':'.join(rest))
      return volumes


# strictly for testing
if __name__ == '__main__':
  gpus = []
  gpus.append('NVIDIA GeForce RTX 3090 Laptop GPU')
  gpus.append('NVIDIA GeForce RTX 3091 Laptop GPU')

  ports = []
  ports.append('8888/tcp')
  ports.append('8080/tcp')

  raw_volumes = []
  raw_volumes.append('data:/data:rw')
  raw_volumes.append('data:/workspace/data:rw')

  volumes = []

  for v in raw_volumes:
    if v.startswith('/'):
      # absolute path
      volumes.append(v)
    else:
      volumes.append(os.environ['HOME'] + '/' + v)

# - data:/data:rw   
# - data:/workspace/data:rw 

  win = CLaunchDialog(
        title = 'Launching PyTorch 21.08', 
        description = 'GPU Accelerated PyTorch 1.11',
        license_url = 'http://www.nvidia.com',
        ports = ports,
        volumes = volumes,
        gpus = gpus,

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


