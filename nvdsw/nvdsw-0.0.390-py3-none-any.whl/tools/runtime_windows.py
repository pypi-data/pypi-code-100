import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GLib, Pango
from gi.repository import GdkPixbuf

import logging
import os, pathlib
import configparser
import timeago
import datetime
import subprocess
import time
import threading
from functools import cmp_to_key
import copy

from nvdsw.tools.rtlaunch import NVAIELaunchDialog
from nvdsw.tools.claunch import CLaunchDialog

PKG_DIR = str(pathlib.Path(__file__).parent.absolute())

log = logging.getLogger('runtime_dialogs')





class RTWindow(Gtk.Window):
  def __init__(self, title, config, icon_file, settings, nvaie_rt, local_rt, gpus, icon_default):
    super().__init__(title=title)
    self.set_border_width(3)

    self.nvaie_rt = nvaie_rt
    self.local_rt = local_rt
    self.settings = settings

    self.icon_file = icon_file
    self.nvaie_fbox = None
    self.local_fbox = None
    
    self.icon_default = icon_default
    self.gpus = gpus

    self.loginoutbutton = None

####    self.set_events(Gdk.EventMask.BUTTON_PRESS_MASK)

    self.config = config
    if icon_file is not None:
      icon = GdkPixbuf.Pixbuf.new_from_file(icon_file)
      super().set_default_icon(icon)

    # these are inside the stack
    # key is the name of the tab (Running, NVIDIA AI Enterprise)
    self.listboxes = {}

    # these are the items to the left
    self.side_listbox_rows = {}


    root_hbox = Gtk.Box.new(orientation = Gtk.Orientation.HORIZONTAL, spacing = 10)

    self.set_default_size(int(config['MAIN']['LAUNCHER_DEFAULT_WIDTH']),int(config['MAIN']['LAUNCHER_DEFAULT_HEIGHT']))
  #   self.set_size_request(int(config['MAIN']['LAUNCHER_DEFAULT_WIDTH']),int(config['MAIN']['LAUNCHER_DEFAULT_HEIGHT']))
#     root_hbox.set_border_width(10)
    self.add(root_hbox)

    sidebar_vbox = Gtk.Box.new(orientation = Gtk.Orientation.VERTICAL, spacing = 10)
    sidebar_vbox.set_border_width(10)

    sidebar_vbox.set_size_request(220,200)

    root_hbox.pack_start(sidebar_vbox, False, False, 0)
    panel_separator = Gtk.Separator(orientation = Gtk.Orientation.VERTICAL)
    root_hbox.pack_start(panel_separator, False, False, 0)

    self.stack = Gtk.Stack()
    self.stack.set_vexpand(False)
    self.stack.set_hexpand(True)
#     self.stack.set_size_request(600,200)
    self.stack.set_transition_type(Gtk.StackTransitionType.CROSSFADE)
    self.stack.set_transition_duration(100)
    root_hbox.pack_start(self.stack, True, True, 0)

    scrolledwindow = Gtk.ScrolledWindow()
    # this is the left hand size area. Don't expand it horizontally.
    scrolledwindow.set_hexpand(False)
    # vertically is okay
    scrolledwindow.set_vexpand(True)

#     scrolledwindow.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

    sidebar_vbox.pack_start(scrolledwindow, True, True, 0)
#    sidebar_vbox.add(scrolledwindow)
    self.main_listbox = Gtk.ListBox()
    self.main_listbox.connect('row-activated', self.switchstack)
    scrolledwindow.add(self.main_listbox)

    # icons = ['ACCOUNT', 'LAUNCHER', 'RUNNING', 'DATA']
    icons = ['ACCOUNT', 'NVAIE', 'LOCALRT', 'CONTAINER', 'RUNNING', 'DATA']
#     image = Gtk.Image.new_from_file('/home/nvidia/Downloads/126472.png')
    i = 0
    for l in ['My Account', 'NVIDIA AI Enterprise', 'Local Runtime', 'Local Images', 'Running', 'Data']:
#      row = Gtk.ListBoxRow()
#      main_listbox.add(row)

#       row.   set_visible_child_name(l)
      grid = Gtk.Grid()
      self.side_listbox_rows[l] = grid

      self.main_listbox.add(grid)
      pagelabel = Gtk.Label()
      pagecontent = Gtk.Label()

      fname = os.path.abspath(PKG_DIR + "/../" + self.config['icons'][icons[i]])
      pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
        
      filename=fname, width=16, height=16, preserve_aspect_ratio=True)
      image = Gtk.Image.new_from_pixbuf(pixbuf)

      image.set_margin_top(10)
      image.set_margin_bottom(10)
      image.set_margin_left(6)
      image.set_margin_right(6)

      grid.add(image)
      grid.attach(pagelabel, 1,0,1,1)
      pagelabel.set_text(l)
      pagelabel.set_margin_top(10)
      pagelabel.set_margin_bottom(10)
      pagelabel.set_margin_left(10)
      pagelabel.set_margin_right(10)
      pagecontent.set_text('content: ' + l)

      

#      self.stack.add_named(sw, l)


      top_vbox = Gtk.Box.new(orientation = Gtk.Orientation.VERTICAL, spacing = 0)
      self.stack.add_named(top_vbox, l)
#      sw.add(top_vbox)


      title_hbox = Gtk.Box.new(orientation = Gtk.Orientation.HORIZONTAL, spacing = 10)
      title_hbox.set_margin_top(5)
      # title_hbox.set_margin_bottom(5)
      title_hbox.set_margin_right(20)
      title_hbox.set_margin_left(20)
      header_hbox = Gtk.Box.new(orientation = Gtk.Orientation.HORIZONTAL, spacing = 0)
      # header_hbox.set_margin_top(5)
      header_hbox.set_margin_bottom(5)
      header_hbox.set_margin_right(20)
      header_hbox.set_margin_left(20)

      label = Gtk.Label()
      label.set_markup('<big>' + l + '</big>')
      label.set_margin_top(16)
      label.set_margin_bottom(16)
      
      title_hbox.pack_start(label, False, False, 0)
      top_vbox.pack_start(title_hbox, False, False, 0)
      top_vbox.pack_start(header_hbox, False, False, 0)

      sw = Gtk.ScrolledWindow()
      # sw.set_vexpand(False)
      sw.set_vexpand(True)
      sw.set_hexpand(True)  
      # sw.set_min_content_width(800)
      top_vbox.pack_start(sw, True, True, 0)
      # top_vbox.pack_start(sw, False, False, 0)

      vb = Gtk.Box.new(orientation = Gtk.Orientation.VERTICAL, spacing = 0)
      frame = Gtk.Frame()
      vb.add(frame)
      sw.add(vb)
#      frame.set_size_request(1600,250)
#      top_vbox.pack_start(frame, False, False, 0)

   

      


      if l == 'NVIDIA AI Enterprise':
        flowbox = self.build_nvaie_flowbox()
        frame.add(flowbox)
      elif l == 'Local Runtime':
        flowbox = self.build_local_flowbox()
        frame.add(flowbox)
        refresh_button = Gtk.Button()
        refresh_button.set_relief(Gtk.ReliefStyle.NONE)
        refresh_button.set_image(Gtk.Image.new_from_icon_name('view-refresh', Gtk.IconSize.MENU))
        title_hbox.pack_start(refresh_button, False, False, 0)
        refresh_button.connect('clicked', self.build_local_flowbox_b)
        refresh_button.set_tooltip_text('refresh')
      elif l == 'My Account':

        listbox = Gtk.ListBox()
        self.listboxes[l] = listbox
        frame.add(listbox)

        rowb = Gtk.Box.new(orientation = Gtk.Orientation.HORIZONTAL, spacing = 0)
        name = 'Not Authenticated'
        company = 'Not Authenticated'
        user = nvaie_rt.get_user()
        if user is not None:
          name = user['name']
          company = user['company']
          # self.loginoutbutton =  Gtk.Button.new_with_label("Logout")
          self.loginoutbutton =  Gtk.Button()
          label = Gtk.Label()
          label.set_markup('<big>Logout</big>')
          self.loginoutbutton.add(label)
          self.loginoutbutton.set_relief(Gtk.ReliefStyle.NONE)
          self.loginoutbutton.connect("clicked", self.logout_clicked)
          title_hbox.pack_start(self.loginoutbutton, False, False, 0)
        else:
          # self.loginoutbutton =  Gtk.Button.new_with_label("Login")
          self.loginoutbutton =  Gtk.Button()
          label = Gtk.Label()
          label.set_markup('<big>Login</big>')
          self.loginoutbutton.add(label)
          self.loginoutbutton.set_relief(Gtk.ReliefStyle.NONE)
          self.loginoutbutton.connect("clicked", self.login_clicked)
          title_hbox.pack_start(self.loginoutbutton, False, False, 0)

        rowb.pack_start(Gtk.Label(label = name), False, False, 0)
        rowb.pack_end(Gtk.Label(label = company), False, False, 0)
        rowb.set_margin_top(16)
        rowb.set_margin_bottom(16)
        rowb.set_margin_right(20)
        rowb.set_margin_left(20)
        listbox.add(rowb)
        listbox.set_selection_mode(Gtk.SelectionMode.NONE)
      elif l == 'Local Images':

        refresh_button = Gtk.Button()
        refresh_button.set_relief(Gtk.ReliefStyle.NONE)
        refresh_button.set_image(Gtk.Image.new_from_icon_name('view-refresh', Gtk.IconSize.MENU))
        refresh_button.set_tooltip_text('refresh')
        # refresh_button.set_toolip
        title_hbox.pack_start(refresh_button, False, False, 0)

        self.show_queue_only_button = Gtk.CheckButton()
        self.show_queue_only_button.set_active(True)

        title_hbox.pack_end(Gtk.Label(label = 'Hide non-queued images'), False, False, 0)
        title_hbox.pack_end(self.show_queue_only_button, False, False, 0)
        

        self.populate_image_row_header(header_hbox)
        

        listbox = Gtk.ListBox()
        listbox.set_header_func(header_func, None)
        self.listboxes[l] = listbox
        frame.add(listbox)

        refresh_button.connect('clicked', self.refresh_local_images, listbox)
        self.show_queue_only_button.connect("toggled", self.refresh_local_images, listbox)

        self.load_local_images(listbox)
      elif l == 'Running':

        refresh_button = Gtk.Button()
        refresh_button.set_relief(Gtk.ReliefStyle.NONE)
        refresh_button.set_image(Gtk.Image.new_from_icon_name('view-refresh', Gtk.IconSize.MENU))
        refresh_button.set_tooltip_text('refresh')
        title_hbox.pack_start(refresh_button, False, False, 0)

        self.populate_running_row_header(header_hbox)

        listbox = Gtk.ListBox()
        listbox.set_header_func(header_func, None)
        self.listboxes[l] = listbox
        frame.add(listbox)
        # refresh_button was created just above
        # refresh_button.connect('clicked', self.refresh_nvaie_resources, listbox)
        refresh_button.connect('clicked', self.refresh_resources, listbox)
        self.load_resources(listbox)
      else:
        listbox = Gtk.ListBox()
        listbox.set_header_func(header_func, None)
        self.listboxes[l] = listbox
        frame.add(listbox)
        for j in range(0,5):
#           if j != 0:
#             separator = Gtk.Separator(orientation = Gtk.Orientation.VERTICAL)
#             listbox.add(separator)

          rowb = Gtk.Box.new(orientation = Gtk.Orientation.HORIZONTAL, spacing = 0)
          rowb.pack_start(Gtk.Label(label = 'key' + str(j)), False, False, 0)
          rowb.pack_end(Gtk.Label(label = "value" + str(j)), False, False, 0)
          rowb.set_margin_top(16)
          rowb.set_margin_bottom(16)
          rowb.set_margin_right(20)
          rowb.set_margin_left(20)
          listbox.add(rowb)
        




      i = i + 1

    root_hbox.show_all()
    # just in case nvaie is not enabled
    if not self.settings.get()['Experimental']['NVAIE_ENABLED']:
      if not self.settings.get()['Experimental']['LAUNCHER_ENABLED']:
        self.stack.set_visible_child_name('Running')
        # The Running tab is the next to last one.. 
        ind_tab = len(self.main_listbox.get_children()) - 2
      else:
        self.stack.set_visible_child_name('Local Runtime')
        # The Local Runtime tab is two up from the Running tab
        ind_tab = len(self.main_listbox.get_children()) - 4
      self.main_listbox.select_row(self.main_listbox.get_row_at_index(ind_tab))
      

  def show_all(self):
    super().show_all()
  

    # hide the data tab for now
    self.side_listbox_rows['Data'].hide()


    if not self.settings.get()['Experimental']['NVAIE_ENABLED']:
      self.side_listbox_rows['My Account'].hide()

    if not self.settings.get()['Experimental']['LAUNCHER_ENABLED']:
      self.side_listbox_rows['Local Runtime'].hide()
      self.side_listbox_rows['Local Images'].hide()

    if not self.nvaie_rt.authed():
      # hide the NVIDIA AI Enterprise tab
      self.side_listbox_rows['NVIDIA AI Enterprise'].hide()

  def build_nvaie_flowbox(self):
    if self.nvaie_fbox is None:
      self.nvaie_fbox = Gtk.FlowBox()
      self.nvaie_fbox.set_border_width(10)
      self.nvaie_fbox.set_max_children_per_line(100)
      self.nvaie_fbox.set_valign(Gtk.Align.START)
      self.nvaie_fbox.set_selection_mode(Gtk.SelectionMode.NONE)
    else:
      # clean it up
      for c in self.nvaie_fbox.get_children():
        c.destroy()

    if not self.nvaie_rt.authed():
      return self.nvaie_fbox
    else: 
      
#       fbox.set_max_children_per_line(30)
      menu_items = self.nvaie_rt.get_menu()['items']
    
      for k,v in menu_items.items():
#         log.debug('building flowbox for item: ' + v['name'])
        button = Gtk.Button()
        button.connect("clicked", self.on_nvaie_menu_item_clicked, v)
        button.set_label(v['name'])
        button.set_size_request(150, 150)
        self.nvaie_fbox.add(button)

#       self.nvaie_fbox.show_all()
      return self.nvaie_fbox

  def local_fbox_clicked(self, fbox, child):
#     log.debug('in foo')
#     print(child.menu_item)
    self.on_local_menu_item_clicked(child, child.menu_item_id)

  def foo(self, c):
    log.debug('in foo')

  def build_local_flowbox_b(self, button):
    return self.build_local_flowbox()
    
  def build_local_flowbox(self):
#    log.debug('in build local flowbox')
    if self.local_fbox is None:
      self.local_fbox = Gtk.FlowBox()
      self.local_fbox.set_border_width(10)
      self.local_fbox.set_max_children_per_line(100)
      self.local_fbox.set_valign(Gtk.Align.START)
      self.local_fbox.set_selection_mode(Gtk.SelectionMode.SINGLE)
      self.local_fbox.connect('child-activated', self.local_fbox_clicked)
    else:
      # clean it up
      for c in self.local_fbox.get_children():
        c.destroy()

    if not self.local_rt.authed():
      return self.local_fbox
    else: 
      
      # trying to prevent concurrency issues.. 
      menu_items = copy.deepcopy(self.local_rt.get_menu()['items'])
    
      for k,v in menu_items.items():
#        log.debug('building local flowbox for item: ' + v['name'])

        c = Gtk.FlowBoxChild()
        # c.menu_item = v
        c.menu_item_id = k
#         c.connect("activate", self.foo)

        # button = Gtk.Button()
        frame = Gtk.Frame()
        c.add(frame)
        # button.connect("clicked", self.on_local_menu_item_clicked, v)
        
#         button.connect("button-press-event", self.on_local_menu_item_clicked, v)


        
        label = Gtk.Label(label = v['name'])
        ldesc = Gtk.Label(label = v['description'])
        ldesc.set_line_wrap(True)
        ldesc.set_max_width_chars(20)
        ldesc.set_justify(Gtk.Justification.CENTER)

        #ldesc.set_size_request(160,5)
#         button.set_label(label)
        w = Gtk.ComboBoxText()
#        w.set_size_request(50,0)
#         print(v['tags'])
        sorted_tags = sorted(v['tags'].items(), key = cmp_to_key(self.compare_tags), reverse = True)
#         sorted_tags = sorted(v['tags'].items(), key = lambda kv: kv[1]['status'], reverse = True)
#        for tk, tv in v['tags'].items():
        for tk, tv in sorted_tags:
          if tv['status'] == 'pulled':
            w.append(tk, tv['tag'])
          elif tv['status'] == 'queued' or tv['status'] == 'pulling' or tv['status'] == 'paused':
            # w.append(tk, tv['tag'] + ' [' + tv['status'] + ']')
            w.append(tk, tv['tag'] + ' ' + tv['status'])
          else:
            # w.append(tk, tv['tag'] + ' [' + tv['status'] + ']')
            # w.append(tk, tv['tag'] + ' [not pulled]')
            w.append(tk, tv['tag'] + ' ' + tv['status'])
            # w.append(tk, tv['tag'] + ' [not pulled]')
        # w.set_active_id(list(v['tags'].keys())[0])
        w.set_active_id(sorted_tags[0][0])
        v = Gtk.Box.new(orientation = Gtk.Orientation.VERTICAL, spacing = 10)
        v.set_border_width(10)
        # v.set_size_request(75, 0)

        v.pack_start(label, False, False, 0)
        v.pack_start(ldesc, False, False, 0)
        v.pack_end(w, False, False, 0)
        frame.add(v)

        c.set_size_request(150, 150)
        self.local_fbox.add(c)

#       self.nvaie_fbox.show_all()
      self.local_fbox.show_all()
      return self.local_fbox

  def compare_tags(self, kvtag1,kvtag2):
    tag1 = kvtag1[1]
    tag2 = kvtag2[1]
    if tag1['status'] == 'pulled' and tag1['status'] == 'pulled':
      if tag1['tag'] > tag2['tag']:
        return 1
      elif tag1['tag'] < tag2['tag']:
        return -1
      else:
        return 0
    else:
      if tag1['status'] == 'pulled':
        return 1
      elif tag2['status'] == 'pulled':
        return -1
      else:
        if tag1['tag'] > tag2['tag']:
          return 1
        elif tag1['tag'] < tag2['tag']:
          return -1
        else:
          return 0  

  def update_local_asset_combo(self, comboboxtext, tags):
    # GLib.idle_add(self.update_local_asset_combo, comboboxtext, menu_item['tags'])
    comboboxtext.remove_all()
    for tk, tv in tags.items():
      if tv['status'] == 'pulled':
        comboboxtext.append(tk, tv['tag'])
      else:
        comboboxtext.append(tk, tv['tag'] + ' ' + tv['status'])
    
    # there needs to be some sorting here for sure
    comboboxtext.set_active_id(list(tags.keys())[0])

    comboboxtext.show_all()


  def login_clicked(self, _):
    log.debug('login clicked')
    dialog = Gtk.MessageDialog(parent = self, message_type = Gtk.MessageType.OTHER, buttons = Gtk.ButtonsType.OK_CANCEL, text = 'login')

    box = dialog.get_content_area()
    box.set_spacing(5)
    root_vbox = Gtk.Box.new(orientation = Gtk.Orientation.VERTICAL, spacing = 5)
    box.add(root_vbox)
    root_vbox.set_border_width(5)
    userid = Gtk.Entry()
    userid.set_max_length(24)
    userid.set_text('userid')
    root_vbox.pack_start(userid, False, False, 0)

    passwd = Gtk.Entry()
    passwd.set_max_length(12)
    passwd.set_text('passwd')
    root_vbox.pack_start(passwd, False, False, 0)
    root_vbox.show_all()

    while True:
      rc = dialog.run()
      if rc  == Gtk.ResponseType.CANCEL:
#        nvaie_win.destroy()
        dialog.destroy()
        return
    
      creds = {}
      creds['userid'] = userid.get_text()
      creds['passwd'] = passwd.get_text()
      rc = self.nvaie_rt.auth(creds)
      if not rc:
        d = Gtk.MessageDialog(parent = dialog, message_type = Gtk.MessageType.ERROR, buttons = Gtk.ButtonsType.OK, text = 'incorrect login')
        d.run()
        d.destroy()
        continue
      else:
        break

    # the nvaie menu item should not be even displayed unless the person is logged in

    b = self.listboxes['My Account'].get_row_at_index(0).get_children()[0]
    label1 = b.get_children()[0]
    label2 = b.get_children()[1]
    user = self.nvaie_rt.get_user()
    label1.set_text(user['name'])
    label2.set_text(user['company'])
  #   b.show_all()
    self.build_nvaie_flowbox()

    # Need to refresh the list of resources
    # self.refresh_nvaie_resources(None, self.listboxes['Running'])
    self.refresh_resources(None, self.listboxes['Running'])

    # the login button becomes logout button
    ## self.loginoutbutton.set_label('Logout')
    label = self.loginoutbutton.get_children()[0]
    label.set_markup('<big>Logout</big>')
    self.loginoutbutton.disconnect_by_func(self.login_clicked)
    self.loginoutbutton.connect("clicked", self.logout_clicked)
    self.show_all()
    dialog.destroy()


  def logout_clicked(self, _):
    d = Gtk.MessageDialog(parent = self, message_type = Gtk.MessageType.INFO, buttons = Gtk.ButtonsType.OK_CANCEL, text = 'Log out?')
    rc = d.run()
    if rc == Gtk.ResponseType.OK:
      log.debug("logging out of NVAIE")
      self.nvaie_rt.logout()
      # the logout button becomes login button
      # self.loginoutbutton.set_label('Login')
      label = self.loginoutbutton.get_children()[0]
      label.set_markup('<big>Login</big>')
      self.loginoutbutton.disconnect_by_func(self.logout_clicked)
      self.loginoutbutton.connect("clicked", self.login_clicked)
      # need to hide the NVAIE launcher.  
      self.build_nvaie_flowbox()
      
      # Need to refresh the list of resources
      # self.refresh_nvaie_resources(None, self.listboxes['Running'])
      self.refresh_resources(None, self.listboxes['Running'])


      # remove user information from the login tab
      b = self.listboxes['My Account'].get_row_at_index(0).get_children()[0]
      label1 = b.get_children()[0]
      label2 = b.get_children()[1]
      user = self.nvaie_rt.get_user()
      name = 'Not Authenticated'
      company = 'Not Authenticated'
      label1.set_text(name)
      label2.set_text(company)



      self.show_all()
    d.destroy()

  def on_delete_clicked(self, button, rt, resource_id):
    d = Gtk.MessageDialog(parent = self, message_type = Gtk.MessageType.INFO, buttons = Gtk.ButtonsType.OK_CANCEL, text = 'Remove resource?')
    rc = d.run()
    if rc == Gtk.ResponseType.OK:
      log.debug("deleting resource with id: " + resource_id)
#       res_id = rt.delete_resource(resource_id)
      md = Gtk.MessageDialog(parent = self, message_type=Gtk.MessageType.OTHER, text = "deleting")
      spinner = Gtk.Spinner()
      spinner.show()
      spinner.start()
      md.get_message_area().add(spinner)
      md.show()
      th = threading.Thread(target=self.async_rt_api_local_thread, args = ('delete', rt, resource_id, button, md))
      th.daemon = True
      th.start()
    d.destroy()

#     updated_resource = rt.get_resource(resource_id)
#     updated_box = None
#     if updated_resource is not None:
#       # what if it didn't get deleted or get deleted yet?
#        updated_box = self.create_running_row_local(updated_resource)
#     current_listbox_row = button.get_parent().get_parent()
#     GLib.idle_add(self.update_listbox_row, current_listbox_row, updated_box)

  def on_stop_clicked(self, button, rt, resource_id):
    d = Gtk.MessageDialog(parent = self, message_type = Gtk.MessageType.INFO, buttons = Gtk.ButtonsType.OK_CANCEL, text = 'Stop resource?')
    rc = d.run()
    if rc == Gtk.ResponseType.OK:
      log.debug("stopping resource with id: " + resource_id)
  #     res_id = rt.stop_resource(resource_id)
      md = Gtk.MessageDialog(parent = self, message_type=Gtk.MessageType.OTHER, text = "stopping")
      spinner = Gtk.Spinner()
      spinner.show()
      spinner.start()
      md.get_message_area().add(spinner)
      md.show()
      th = threading.Thread(target=self.async_rt_api_local_thread, args = ('stop', rt, resource_id, button, md))
      th.daemon = True
      th.start()
    d.destroy()

  #   # get the updated resource
  #   updated_resource = rt.get_resource(resource_id)
  #   updated_box = self.create_running_row_local(updated_resource)

    # the clicked button belongs to a horizontal box which is the sole chid of a listbox row.
    # we need to unlink that box and replace it with the new one.. 
  #   current_listbox_row = button.get_parent().get_parent()
    # thread carefully.. 
  #   GLib.idle_add(self.update_listbox_row, current_listbox_row, updated_box)

#     print('new status:' + new_stat)
#     statLabel = button.get_parent().get_children()[1]
#     print(statLabel.get_text())

  def update_listbox_row(self, current_listbox_row, new_child):
    # a listbox row only has one child, which makes this so much easier
    current_listbox_row.get_child().destroy()

    # trying to handle the delete case
    # a childless listbox row is dead.. 
    if new_child is not None:
      current_listbox_row.add(new_child)
    else:
      current_listbox_row.destroy()

    current_listbox_row.show_all()

  def async_rt_api_local_thread(self, op_string, rt, resource_id, button, popup):
    rc = 0
    if op_string == 'start':
      rc = rt.start_resource(resource_id)
    elif op_string == 'stop':
      rc = rt.stop_resource(resource_id)
    elif op_string == 'restart':
      rc = rt.restart_resource(resource_id)
    elif op_string == 'delete':
      rc = rt.delete_resource(resource_id)
    else:
      log.error('unrecognized operation attempted: ' + op_string)
      popup.destroy()
      return

    GLib.idle_add(self.async_rt_api_local_thread_gtk, op_string, rt, resource_id, rc, button, popup)


  def async_rt_api_local_thread_gtk(self, op_string, rt, resource_id, rc, button, popup):

    # remove the spinning popup
    popup.destroy()

    if not rc:
      self.show_dialog(Gtk.MessageType.ERROR, 'asset ' + op_string + ' error', "asset failed to " + op_string + ". Please see logs", Gtk.ButtonsType.OK,"Error", None)
      return

    updated_resource = rt.get_resource(resource_id)
    updated_box = None
    if updated_resource is not None:
      # e.g. if the resource was deleted as part of the delete operation
      if rt == self.local_rt:
        updated_box = self.create_running_row_local(updated_resource)
      else:
        updated_box = self.create_running_row_nvaie(updated_resource)

    current_listbox_row = button.get_parent().get_parent()
    GLib.idle_add(self.update_listbox_row, current_listbox_row, updated_box)


  def on_start_clicked(self, button, rt, resource_id):
    d = Gtk.MessageDialog(parent = self, message_type = Gtk.MessageType.INFO, buttons = Gtk.ButtonsType.OK_CANCEL, text = 'Start resource?')
    rc = d.run()
    if rc == Gtk.ResponseType.OK:
      log.debug("starting resource with id: " + resource_id)
      md = Gtk.MessageDialog(parent = self, message_type=Gtk.MessageType.OTHER, text = "starting")
      spinner = Gtk.Spinner()
      spinner.show()
      spinner.start()
      md.get_message_area().add(spinner)
      md.show()
      th = threading.Thread(target=self.async_rt_api_local_thread, args = ('start', rt, resource_id, button, md))
      th.daemon = True
      th.start()
 
    d.destroy()


  def on_restart_clicked(self, button, rt, resource_id):
    d = Gtk.MessageDialog(parent = self, message_type = Gtk.MessageType.INFO, buttons = Gtk.ButtonsType.OK_CANCEL, text = 'Restart resource?')
    rc = d.run()
    if rc == Gtk.ResponseType.OK:
      log.debug("restarting resource with id: " + resource_id)
      md = Gtk.MessageDialog(parent = self, message_type=Gtk.MessageType.OTHER, text = "restarting")
      spinner = Gtk.Spinner()
      spinner.show()
      spinner.start()
      md.get_message_area().add(spinner)
      md.show()
      th = threading.Thread(target=self.async_rt_api_local_thread, args = ('restart', rt, resource_id, button, md))
      th.daemon = True
      th.start()
#       res_id = rt.restart_resource(resource_id)    
    d.destroy()
#     updated_resource = rt.get_resource(resource_id)
#     updated_box = self.create_running_row_local(updated_resource)
#     current_listbox_row = button.get_parent().get_parent()
#     GLib.idle_add(self.update_listbox_row, current_listbox_row, updated_box)

  def on_image_delete_clicked(self, button, rt, local_image, tag):

    d = Gtk.MessageDialog(parent = self, message_type = Gtk.MessageType.INFO, buttons = Gtk.ButtonsType.OK_CANCEL, text = 'Delete image?')
    rc = d.run()
    if rc == Gtk.ResponseType.OK:
#       rt.uncache_menu_item_tag(local_image['id'], tag['tag']) 
      log.debug("deleting image with id: " + local_image['id'])
      md = Gtk.MessageDialog(parent = self, message_type=Gtk.MessageType.OTHER, text = "deleting")
      spinner = Gtk.Spinner()
      spinner.show()
      spinner.start()
      md.get_message_area().add(spinner)
      md.show()
      th = threading.Thread(target=self.async_docker_img_del_local_thread, args = (local_image, tag, button, md))
      th.daemon = True
      th.start()

    d.destroy()
    
#     updated_mi = rt.get_menu_item(local_image['id'])
#     updated_tag = updated_mi['tags'][tag['tag']]
#     updated_box = self.create_image_row(updated_mi, updated_tag)
#     current_listbox_row = button.get_parent().get_parent()
#     GLib.idle_add(self.update_listbox_row, current_listbox_row, updated_box)
    return 

  def async_docker_img_del_local_thread(self, local_image, tag, button, popup):
    rc = self.local_rt.uncache_menu_item_tag(local_image['id'], tag['tag']) 
    GLib.idle_add(self.async_docker_img_del_local_thread_gtk, local_image, tag, rc, button, popup)  
  
  def async_docker_img_del_local_thread_gtk(self, local_image, tag, rc, button, popup):
    popup.destroy()
    if not rc:
      self.show_dialog(Gtk.MessageType.ERROR, 'image delete error', "image " + local_image['id'] + " could not be deleted. Please see logs", Gtk.ButtonsType.OK,"Error", None)
      return

    updated_mi = self.local_rt.get_menu_item(local_image['id'])
    updated_tag = updated_mi['tags'][tag['tag']]
    updated_box = self.create_image_row(updated_mi, updated_tag)
    current_listbox_row = button.get_parent().get_parent()
    GLib.idle_add(self.update_listbox_row, current_listbox_row, updated_box)


  def on_image_download_clicked(self, button, rt, local_image, tag):
    d = Gtk.MessageDialog(parent = self, message_type = Gtk.MessageType.INFO, buttons = Gtk.ButtonsType.OK_CANCEL, text = 'Download image?')
    rc = d.run()
    if rc == Gtk.ResponseType.OK:
      rt.cache_menu_item_tag(local_image['id'], tag['tag'])   
    d.destroy()

    updated_mi = rt.get_menu_item(local_image['id'])
    updated_tag = updated_mi['tags'][tag['tag']]
    updated_box = self.create_image_row(updated_mi, updated_tag)
    current_listbox_row = button.get_parent().get_parent()
    GLib.idle_add(self.update_listbox_row, current_listbox_row, updated_box)

    return 


  def on_image_pause_clicked(self, button, rt, local_image, tag):
    d = Gtk.MessageDialog(parent = self, message_type = Gtk.MessageType.INFO, buttons = Gtk.ButtonsType.OK_CANCEL, text = 'Pause image download?')
    rc = d.run()
    if rc == Gtk.ResponseType.OK:
      rt.pause_caching_menu_item_tag(local_image['id'], tag['tag'])   
    d.destroy()   

    updated_mi = rt.get_menu_item(local_image['id'])
    updated_tag = updated_mi['tags'][tag['tag']]
    updated_box = self.create_image_row(updated_mi, updated_tag)
    current_listbox_row = button.get_parent().get_parent()
    GLib.idle_add(self.update_listbox_row, current_listbox_row, updated_box) 
    
    return 
  
  def on_image_unpause_clicked(self, button, rt, local_image, tag):
    d = Gtk.MessageDialog(parent = self, message_type = Gtk.MessageType.INFO, buttons = Gtk.ButtonsType.OK_CANCEL, text = 'Resume image download?')
    rc = d.run()
    if rc == Gtk.ResponseType.OK:
      rt.unpause_caching_menu_item_tag(local_image['id'], tag['tag'])  
    d.destroy()  

    updated_mi = rt.get_menu_item(local_image['id'])
    updated_tag = updated_mi['tags'][tag['tag']]
    updated_box = self.create_image_row(updated_mi, updated_tag)
    current_listbox_row = button.get_parent().get_parent()
    GLib.idle_add(self.update_listbox_row, current_listbox_row, updated_box)
    
    return 

  def on_local_menu_item_clicked(self, flowboxchild, menu_item_id):

    frame = flowboxchild.get_children()[0]
    vbox = frame.get_children()[0]
    comboboxtext = vbox.get_children()[2]
    selected_tag_id = comboboxtext.get_active_id()
    log.debug('selected tag id is: ' + selected_tag_id)

    menu_item = self.local_rt.get_menu_item(menu_item_id)
    
    selected_tag = menu_item['tags'][selected_tag_id] 
    stat = selected_tag['status']
    if stat == 'pulling' or stat == 'queued':
      md = Gtk.MessageDialog(parent = self, 
      message_type=Gtk.MessageType.OTHER, 
      buttons = Gtk.ButtonsType.OK,
      text = "image is " + stat + ', please wait for it')
      md.run()
      md.destroy()
      # need to thread safely update the comboboxtext with the latest status
      GLib.idle_add(self.update_local_asset_combo, comboboxtext, menu_item['tags'])
      return 

    # right here we need to check if the asset is not pulled and offer to pull it.  then go to it in the images tab
    elif stat == 'not pulled' or stat == 'paused':

      txt = 'Pull this image?'
      if stat == 'paused':
        txt = 'Resume pull of this image?'

      md = Gtk.MessageDialog(parent = self, 
      message_type=Gtk.MessageType.OTHER, 
      buttons = Gtk.ButtonsType.OK_CANCEL,
      text = txt)
      if md.run() == Gtk.ResponseType.OK:
        # pull it!
        self.local_rt.cache_menu_item_tag(menu_item_id, selected_tag_id)
        # The images tab is the second one from the bottom
        ind_img_tab = len(self.main_listbox.get_children()) - 3
        self.main_listbox.select_row(self.main_listbox.get_row_at_index(ind_img_tab))

        # update the images tab
        lb = self.listboxes['Local Images']
        # the first param is button which we don't have
        self.refresh_local_images(None, lb)

        # find the row we just pulled
        for c in lb.get_children():
          c0 = c.get_children()[0]
          if isinstance(c0, Gtk.Box):
            cs = c0.get_children()
            # the first label is the image name
            # the second one is the tag
            l1 = cs[0].get_label()
            l2= cs[1].get_label()
#            print('l1: ' + l1 + ' vs: '+ menu_item['name'])
#            print('l2: ' + l2 + ' vs: '+ selected_tag_id)
            if l1 == menu_item['name'] and l2 == selected_tag_id:
#              print('we have a hit!')
              lb.select_row(c)
#              lb.show_all()
              break

            
        
        # switch to the images tab...
        self.stack.set_visible_child_name('Local Images')
        md.destroy()
        return
      else:
        # user chose to cancel
        md.destroy()
        return
      

    win = CLaunchDialog(
        parent = self,
        title = 'Launching Asset', 
        description = menu_item['description'],
        license_url = menu_item['license_url'],
        ports = menu_item['ports'],
        volumes = menu_item['volumes'],
        browser = menu_item['browser'],
        gpus = self.gpus,
        icon_file = self.icon_default,
        settings = self.settings, 
        selected_tag = selected_tag
    ) 
    rc = win.run()
    if rc == Gtk.ResponseType.OK:
      log.debug('okay was clicked')
      attrs = win.get_attrs().copy()
#       win.destroy()

      md = Gtk.MessageDialog(parent = self, message_type=Gtk.MessageType.OTHER, text = "launching")
      spinner = Gtk.Spinner()
      spinner.show()
      spinner.start()
      md.get_message_area().add(spinner)
      md.show()
#      log.debug("showed!")
      th = threading.Thread(target=self.async_launch_local_thread, args = (attrs, menu_item, md, selected_tag_id))
      th.daemon = True
      th.start()

    win.destroy()

    
  def async_launch_local_thread(self, attrs, menu_item, md, selected_tag_id):  
    # this is not a GTk safe method. 
    log.debug(' in async launch local')
#     time.sleep(10)
    # this is but a hack.  Need to display a pull down and select the right tag
#     latest_tag = list(menu_item['tags'].keys())[0]
    res_id = self.local_rt.create_resource(menu_item['id'], flavor_id = None, tag = selected_tag_id, attrs = attrs)
        
    GLib.idle_add(self.async_launch_local_gtk, attrs, menu_item, md, res_id)

  def async_launch_local_gtk(self, attrs, menu_item, md, res_id):

    # remove the spinning popup
    md.destroy()

    if res_id is None:
      self.show_dialog(Gtk.MessageType.ERROR, 'asset launch error', "asset failed to start. Please see logs", Gtk.ButtonsType.OK,"Launch Error", None)
      return

    log.debug('created resource with id: ' + res_id)
    local_resource = self.local_rt.get_resource(res_id)
    self.stack.set_visible_child_name('Running')
    
# The Running tab is the next to last one.. 
    ind_run_tab = len(self.main_listbox.get_children()) - 2
    self.main_listbox.select_row(self.main_listbox.get_row_at_index(ind_run_tab))

    lb = self.listboxes['Running']
    n_children = len(lb.get_children())
#    if n_children > 0:
#      separator = Gtk.Separator(orientation = Gtk.Orientation.VERTICAL)
#      lb.add(separator)

    rowb = self.create_running_row_local(local_resource)
    # lb.add(rowb)
    # insert as the first row since it's the freshest
    lb.insert(rowb, 0)
      
    lb.select_row(lb.get_row_at_index(0))
    # lb.select_row(lb.get_row_at_index(n_children - 1))
    lb.show_all()


  def on_nvaie_menu_item_clicked(self, button, menu_item):
    flavors = self.nvaie_rt.get_flavors()['items']
    win = NVAIELaunchDialog(
        parent = self,
        title = 'Launching Asset', 
        menu_item = menu_item,
        flavors = flavors,
        preset_flavor = flavors['10002'],
        icon_file = self.icon_file
    )
    rc = win.run()
    if rc == Gtk.ResponseType.OK:
      res_id = self.nvaie_rt.create_resource(menu_item['id'], win.flavor_box.get_active_id())
      log.debug('created resource with id: ' + res_id)

      nvaie_resource = self.nvaie_rt.get_resource(res_id)
      
      log.debug('user chose to launch: ')
      log.debug("menu_item id: " + menu_item['id'] + ', name: '+ menu_item['name'])
      log.debug('id selected: ' + win.flavor_box.get_active_id())
      self.stack.set_visible_child_name('Running')
      
      # self.main_listbox.select_row(self.main_listbox.get_row_at_index(2))
      # The Running tab is the next to last one.. 
      ind_run_tab = len(self.main_listbox.get_children()) - 2
      self.main_listbox.select_row(self.main_listbox.get_row_at_index(ind_run_tab))

      lb = self.listboxes['Running']
      n_children = len(lb.get_children())
#      if n_children > 0:
#        separator = Gtk.Separator(orientation = Gtk.Orientation.VERTICAL)
#        lb.add(separator)

      rowb = self.create_running_row_nvaie(nvaie_resource)
      # lb.add(rowb)
      # insert as the first row since it's the freshest
      lb.insert(rowb, 0)
      
      lb.select_row(lb.get_row_at_index(0))
      # lb.select_row(lb.get_row_at_index(n_children - 1))
      lb.show_all()


    win.destroy()

  def switchstack(self, box, row):
  #   log.debug('switchstack')
    grid = row.get_child()
    label = grid.get_children()[0]
    name = label.get_text()

    lbox = self.listboxes.get(name)
    if name == 'Running':
      # the first param is button which we obviously don't have here.. 
      self.refresh_resources(None, lbox)
    elif name == 'Local Runtime':
      # this one does not have a listbox
      self.build_local_flowbox()
    elif name == 'Local Images':
      self.refresh_local_images(None, lbox)

    self.stack.set_visible_child_name(name)


  def refresh_resources(self, _, listbox):
    for c in listbox.get_children():
      c.destroy()
    self.load_resources(listbox)
    listbox.show_all()
    return 

  def refresh_nvaie_resources(self, _, listbox):
    for c in listbox.get_children():
      c.destroy()
    self.load_nvaie_resources(listbox)
    listbox.show_all()
    return 

  def load_local_images(self, listbox):
    log.debug('load_local_images called')
    local_images = []
    if self.settings.get()['Experimental']['LAUNCHER_ENABLED']:
      local_images = self.local_rt.get_menu(active_only = self.show_queue_only_button.get_active())['items'].items()

# not quite sure how to sort this yet
#     all_unsorted = list(local_images) 
#     images = sorted(all_unsorted, key = lambda i: i['created'], reverse = True )
    images = local_images

    j = 0
    for _, i in images:
#       print(i['tags'])
      for _,t in i['tags'].items():
#        print(t)

        # this is now redundant because we don't pull inactive stuff if this flag is set
        # keeping it around due to paranoia
        if self.show_queue_only_button.get_active() == True and (t['status'] == 'pulled' or t['status'] == 'not pulled'):
          continue
        row = Gtk.ListBoxRow()
        hbox = self.create_image_row(i,t)
        row.add(hbox)
#         if j > 0:
#          row.set_header(Gtk.Separator(orientation = Gtk.Orientation.VERTICAL))
        listbox.add(row)
        j = j + 1


  def refresh_local_images(self, _, listbox):
    log.debug('refresh_local_images called')
    for c in listbox.get_children():
      c.destroy()
    self.load_local_images(listbox)
    listbox.show_all()
    return

  def refresh_local_resources(self, _, listbox):
    for c in listbox.get_children():
      c.destroy()
    self.load_local_resources(listbox)
    listbox.show_all()
    return 

  def load_resources(self, listbox):
    local_resources = []
    nvaie_resources = self.nvaie_rt.get_resources().values()
    if self.settings.get()['Experimental']['LAUNCHER_ENABLED']:
      local_resources = self.local_rt.get_resources().values()
    all_unsorted = list(local_resources) + list(nvaie_resources)
    resources = sorted(all_unsorted, key = lambda r: r['created'], reverse = True )

    # sort
    i = 0
    for r in resources:
#      if i > 0:
#        separator = Gtk.Separator(orientation = Gtk.Orientation.VERTICAL)
#        listbox.add(separator)
      
      if r['rtype'] == 'remote':
        listbox.add(self.create_running_row_nvaie(r))
      else:
        listbox.add(self.create_running_row_local(r))

      i = i + 1

  def load_nvaie_resources(self, listbox):
    resource_ids = self.nvaie_rt.get_resource_ids()
    i = 0
    for rid in resource_ids:
      log.debug('processing resoruce id: ' + rid)
      res = self.nvaie_rt.get_resource(rid)
#      if i > 0:
#        separator = Gtk.Separator(orientation = Gtk.Orientation.VERTICAL)
#        listbox.add(separator)
      listbox.add(self.create_running_row_nvaie(res))
      i = i + 1

  def load_local_resources(self, listbox):
    resource_ids = self.local_rt.get_resource_ids()
    i = 0
    for rid in resource_ids:
      log.debug('processing resoruce id: ' + rid)
      res = self.local_rt.get_resource(rid)
#      if i > 0:
#        separator = Gtk.Separator(orientation = Gtk.Orientation.VERTICAL)
#        listbox.add(separator)
      listbox.add(self.create_running_row_local(res))
      i = i + 1

  def open_url(self,_, url):
    cmd = ["/usr/bin/x-www-browser", url]
    subprocess.Popen(cmd)

  def create_image_row(self, local_image,tag):
    # print(tag)
    rowb = Gtk.Box.new(orientation = Gtk.Orientation.HORIZONTAL, spacing = 0)

    l = Gtk.Label(label = local_image['name'])
#    l.set_selectable(True)
    l.set_width_chars(30)
    l.set_max_width_chars(30)
    l.set_xalign(0)
#     l.set_justify(Gtk.Justification.LEFT)
    rowb.pack_start(l, False, False, 0)

    l = Gtk.Label(label = tag['tag'])
    l.set_width_chars(10)
    l.set_max_width_chars(10)
    l.set_xalign(0)
#     l.set_justify(Gtk.Justification.LEFT)
    rowb.pack_start(l, False, False, 0)

    l = Gtk.Label(label = tag['status'])
    l.set_width_chars(10)
    l.set_max_width_chars(10)
    l.set_xalign(0)
#     l.set_justify(Gtk.Justification.LEFT)
    rowb.pack_start(l, False, False, 0)
    if tag.get('created') is not None:
      l = Gtk.Label(label = timeago.format(float(tag['created']), datetime.datetime.now()))
    else:
      l = Gtk.Label(label = 'None')
    l.set_width_chars(20)
    l.set_max_width_chars(10)
    l.set_xalign(0)
#     l.set_justify(Gtk.Justification.LEFT)
    rowb.pack_start(l, False, False, 0)

    if tag.get('size') is not None:
      # size in GB
      sl = "{:.1f}".format(tag['size'] / 1024 / 1024 / 1024)
      l = Gtk.Label(label = sl)
    else:
      l = Gtk.Label(label = 'None')
    l.set_width_chars(10)
    l.set_max_width_chars(10)
    l.set_xalign(0)
#     l.set_justify(Gtk.Justification.LEFT)
    rowb.pack_start(l, False, False, 0)

    if tag['status'] == 'pulled':
      b = Gtk.Button()
      b.set_relief(Gtk.ReliefStyle.NONE)
      b.set_image(Gtk.Image.new_from_icon_name('edit-delete', Gtk.IconSize.MENU))
      b.connect('clicked', self.on_image_delete_clicked, self.local_rt, local_image, tag)
      b.set_tooltip_text('delete image')
      rowb.pack_end(b, False, False, 0)

    elif tag ['status'] == 'pulling' or tag ['status'] == 'queued':
      b = Gtk.Button()
      b.set_relief(Gtk.ReliefStyle.NONE)
      b.set_image(Gtk.Image.new_from_icon_name('media-playback-pause', Gtk.IconSize.MENU))
      b.connect('clicked', self.on_image_pause_clicked, self.local_rt, local_image, tag)
      b.set_tooltip_text('pause pull')
      rowb.pack_end(b, False, False, 0)

    elif tag ['status'] == 'paused':
      b = Gtk.Button()
      b.set_relief(Gtk.ReliefStyle.NONE)
      b.set_image(Gtk.Image.new_from_icon_name('media-playback-start', Gtk.IconSize.MENU))
      b.connect('clicked', self.on_image_unpause_clicked, self.local_rt, local_image, tag)
      b.set_tooltip_text('resume pull')
      rowb.pack_end(b, False, False, 0)

    elif tag ['status'] == 'not pulled':
      b = Gtk.Button()
      b.set_relief(Gtk.ReliefStyle.NONE)
      fname = os.path.abspath(PKG_DIR + "/../" + self.config['icons']['DOWNLOAD'])
      pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(filename=fname, width=16, height=16, preserve_aspect_ratio=True)
      b.set_image(Gtk.Image.new_from_pixbuf(pixbuf))
      b.set_tooltip_text('pull image')

      # b.set_image(Gtk.Image.new_from_icon_name('emblem-downloads', Gtk.IconSize.MENU))
      b.connect('clicked', self.on_image_download_clicked, self.local_rt, local_image, tag)
      rowb.pack_end(b, False, False, 0)

    if tag ['status'] == 'pulling':
      b = Gtk.Button()
      b.set_relief(Gtk.ReliefStyle.NONE)
      b.set_image(Gtk.Image.new_from_icon_name('video-display', Gtk.IconSize.MENU))
      b.set_tooltip_text('build output')
      b.connect('clicked', self.on_image_build_log_clicked, local_image, tag)
      rowb.pack_end(b, False, False, 0)

    rowb.set_margin_top(16)
    rowb.set_margin_bottom(16)
    rowb.set_margin_right(20)
    rowb.set_margin_left(20)

    return rowb

  def on_image_build_log_clicked(self, button, local_image, tag):
    log.debug('on_image_build_log_clicked')
    img_name = local_image['image'] + ':' + tag['tag']
    # if we got here, we were in status pulling when the button was shown to the user
    # but, is the GUI stale at this point?
    new_status = self.local_rt.get_ephem_img_status(img_name)
    if new_status != 'pulling':
      # the image status changed from under us.. don't make a fuss,
      # just refresh the row and exit
      updated_mi = self.local_rt.get_menu_item(local_image['id'])
      updated_tag = updated_mi['tags'][tag['tag']]
      updated_box = self.create_image_row(updated_mi, updated_tag)
      current_listbox_row = button.get_parent().get_parent()
      GLib.idle_add(self.update_listbox_row, current_listbox_row, updated_box)
      return

    d = Gtk.Dialog(title = 'image build output',parent=self, modal = False)
    d.set_size_request(350, 150)
    # d.get_header_bar().set_show_close_button(False)
    d.add_button(Gtk.STOCK_OK, Gtk.ResponseType.OK)
    ca = d.get_content_area()
    vbox = Gtk.Box.new(orientation = Gtk.Orientation.VERTICAL, spacing = 10)
    vbox.set_border_width(10)
    f = Gtk.Frame()
    vbox.add(f)
    ca.add(vbox)

    sw = Gtk.ScrolledWindow()
    sw.set_hexpand(True)
    sw.set_vexpand(True)
    f.add(sw)

    textview = Gtk.TextView()
    textview.set_editable(False)
    textview.set_left_margin(10)
    textview.set_top_margin(10)
    # textbuffer = textview.get_buffer()
    # textbuffer.set_text('old mcdonald had a farm')
    sw.add(textview)
    
    d.show_all()
    self.local_rt.attach_widget_menu_item_tag_caching(textview, local_image, tag)
    rc = d.run()
    log.debug('popup gone')
    self.local_rt.remove_widget_menu_item_tag_caching(local_image, tag)

    new_new_status = self.local_rt.get_ephem_img_status(img_name)
    if new_status != new_new_status:
      # the status has changed.  Need to update the GUI
      updated_mi = self.local_rt.get_menu_item(local_image['id'])
      updated_tag = updated_mi['tags'][tag['tag']]
      updated_box = self.create_image_row(updated_mi, updated_tag)
      current_listbox_row = button.get_parent().get_parent()
      GLib.idle_add(self.update_listbox_row, current_listbox_row, updated_box)

    d.destroy()

#  def image_header_sorter(self, widget):
#    print('clicked')
#    print(widget)

  def populate_image_row_header(self, rowb):

#    b = Gtk.Button()
#    b.set_relief(Gtk.ReliefStyle.NONE)
#    b.set_focus_on_click(False)
    l = Gtk.Label(label = 'Name')
    l.set_width_chars(30)
    l.set_max_width_chars(30)
    l.set_xalign(0)
    rowb.pack_start(l, False, False, 0)
#    b.add(l)
#    b.connect('clicked', self.image_header_sorter)

    l = Gtk.Label(label = 'Tag')
    l.set_width_chars(10)
    l.set_max_width_chars(10)
    l.set_xalign(0)
    rowb.pack_start(l, False, False, 0)

    l = Gtk.Label(label = 'Status')
    l.set_width_chars(10)
    l.set_max_width_chars(10)
    l.set_xalign(0)
    rowb.pack_start(l, False, False, 0)

    l = Gtk.Label(label = 'Created')
    l.set_width_chars(20)
    l.set_max_width_chars(10)
    l.set_xalign(0)
    rowb.pack_start(l, False, False, 0)


    l = Gtk.Label(label = 'Size, GB')
    l.set_width_chars(10)
    l.set_max_width_chars(10)
    l.set_xalign(0)
    rowb.pack_start(l, False, False, 0)


    l = Gtk.Label(label = 'Actions')
    l.set_width_chars(10)
    l.set_max_width_chars(10)
    l.set_xalign(0)
    rowb.pack_end(l, False, False, 0)


  def create_running_row_local(self,local_resource):

    rowb = Gtk.Box.new(orientation = Gtk.Orientation.HORIZONTAL, spacing = 0)
    mi = self.local_rt.get_menu_item(local_resource['menu_item_id'], pull_tag_status = False)
#     fl = self.nvaie_rt.get_flavor(local_resource['flavor_id'])

    l = Gtk.Label(label = local_resource['name'])
#    l.set_selectable(True)
    l.set_width_chars(30)
    l.set_max_width_chars(30)
    l.set_xalign(0)
#     l.set_justify(Gtk.Justification.LEFT)
    rowb.pack_start(l, False, False, 0)

    l = Gtk.Label(label = local_resource['status'])
    l.set_width_chars(10)
    l.set_max_width_chars(10)
    l.set_xalign(0)
#     l.set_justify(Gtk.Justification.LEFT)
    rowb.pack_start(l, False, False, 0)

    l = Gtk.Label(label = local_resource['rtype'])
    l.set_width_chars(8)
    l.set_max_width_chars(8)
    l.set_xalign(0)
#     l.set_justify(Gtk.Justification.LEFT)
    rowb.pack_start(l, False, False, 0)

    l = Gtk.Label(label = mi['name'])
    l.set_width_chars(20)
    l.set_max_width_chars(20)
    l.set_xalign(0)
#     l.set_justify(Gtk.Justification.LEFT)
    rowb.pack_start(l, False, False, 0)    

    # flavor.. there's no flavor.. but there's tag
    l = Gtk.Label(label = local_resource['tag'])
    l.set_width_chars(10)
    l.set_max_width_chars(10)
    l.set_xalign(0)
#     l.set_justify(Gtk.Justification.LEFT)
    rowb.pack_start(l, False, False, 0)

    # gpus
    gpu_row = self.make_gpu_row(local_resource['gpus'])
    rowb.pack_start(gpu_row, False, False, 0) 

#     print(local_resource['ports']) 
    if len(local_resource['ports']) == 0 or len(local_resource['ports']) == 1:
      if len(local_resource['ports']) == 1:
        port = list(local_resource['ports'].items())[0]
        ports_label = "<a href='http://localhost:" + port[1] + "/lab'>" + self.ports2str(port) + "</a>"
        l = Gtk.Label()
        l.set_markup(ports_label)
      else:
        l = Gtk.Label(label = '')
      l.set_width_chars(15)
      l.set_max_width_chars(15)
      l.set_xalign(0)
      rowb.pack_start(l, False, False, 0)
    else:
      row = Gtk.Box.new(orientation = Gtk.Orientation.VERTICAL, spacing = 5)
      for port in local_resource['ports'].items():
        ports_label = "<a href='http://localhost:" + port[1] + "/lab'>" + self.ports2str(port) + "</a>"
        l = Gtk.Label()
        l.set_markup(ports_label)
        l.set_width_chars(15)
        l.set_max_width_chars(15)
        l.set_xalign(0)
        row.pack_start(l, False, False, 0) 
#     l.set_justify(Gtk.Justification.LEFT)
      rowb.pack_start(row, False, False, 0) 

#     print(local_resource['volumes'])
    # ['/home/nvidia/data:/data:rw', '/home/nvidia/data:/workspace/data:rw']
    volumes_row = self.make_volumes_row(local_resource['volumes'])
    rowb.pack_start(volumes_row, False, False, 0) 


    l = Gtk.Label(label = timeago.format(float(local_resource['created']), datetime.datetime.now()))
    l.set_width_chars(20)
    l.set_max_width_chars(10)
    l.set_xalign(0)
#     l.set_justify(Gtk.Justification.LEFT)
    rowb.pack_start(l, False, False, 0)

    b = Gtk.Button()
    b.set_relief(Gtk.ReliefStyle.NONE)
    b.set_image(Gtk.Image.new_from_icon_name('edit-delete', Gtk.IconSize.MENU))
    b.connect('clicked', self.on_delete_clicked, self.local_rt, local_resource['id'])
    b.set_tooltip_text('delete')
#     l = Gtk.Label(label = 'actions')
#     l.set_width_chars(10)
#     l.set_max_width_chars(10)
#     l.set_xalign(0)
# #   l.set_justify(Gtk.Justification.LEFT)
    rowb.pack_end(b, False, False, 0)
    b = Gtk.Button()
    b.set_relief(Gtk.ReliefStyle.NONE)
    b.set_image(Gtk.Image.new_from_icon_name('view-refresh', Gtk.IconSize.MENU))
    b.connect('clicked', self.on_restart_clicked, self.local_rt, local_resource['id'])
    b.set_tooltip_text('restart')
    rowb.pack_end(b, False, False, 0)   

    if local_resource['status'] == 'running':
      b = Gtk.Button()
      b.set_relief(Gtk.ReliefStyle.NONE)
      b.set_image(Gtk.Image.new_from_icon_name('media-playback-stop', Gtk.IconSize.MENU))
      b.connect('clicked', self.on_stop_clicked, self.local_rt, local_resource['id'])
      b.set_tooltip_text('stop')
      rowb.pack_end(b, False, False, 0)  
    elif local_resource['status'] == 'exited':
      b = Gtk.Button()
      b.set_relief(Gtk.ReliefStyle.NONE)
      b.set_image(Gtk.Image.new_from_icon_name('media-playback-start', Gtk.IconSize.MENU))
      b.connect('clicked', self.on_start_clicked, self.local_rt, local_resource['id'])
      b.set_tooltip_text('start')
      rowb.pack_end(b, False, False, 0)        

    if local_resource['status'] == 'running':
      b = Gtk.Button()
      b.set_relief(Gtk.ReliefStyle.NONE)
      b.set_image(Gtk.Image.new_from_icon_name('computer', Gtk.IconSize.MENU))
      b.connect('clicked', self.open_url, local_resource['url'])
      b.set_tooltip_text('open in browser')
      rowb.pack_end(b, False, False, 0)

    rowb.set_margin_top(16)
    rowb.set_margin_bottom(16)
    rowb.set_margin_right(20)
    rowb.set_margin_left(20)


    return rowb


  def populate_running_row_header(self, rowb):

#     rowb = Gtk.Box.new(orientation = Gtk.Orientation.HORIZONTAL, spacing = 0)

    l = Gtk.Label(label = 'Name')
    l.set_width_chars(30)
    l.set_max_width_chars(30)
    l.set_xalign(0)
    rowb.pack_start(l, False, False, 0)

    l = Gtk.Label(label = 'Status')
    l.set_width_chars(10)
    l.set_max_width_chars(10)
    l.set_xalign(0)
    rowb.pack_start(l, False, False, 0)

    l = Gtk.Label(label = 'Type')
    l.set_width_chars(8)
    l.set_max_width_chars(8)
    l.set_xalign(0)
    rowb.pack_start(l, False, False, 0)

    l = Gtk.Label(label = 'Image name')
    l.set_width_chars(20)
    l.set_max_width_chars(20)
    l.set_xalign(0)
    rowb.pack_start(l, False, False, 0)    

    # flavor.. there's no flavor.. but there's tag
    l = Gtk.Label(label = 'Tag')
    l.set_width_chars(10)
    l.set_max_width_chars(10)
    l.set_xalign(0)
    rowb.pack_start(l, False, False, 0)

    l = Gtk.Label(label = 'GPUs')
    l.set_width_chars(10)
    l.set_max_width_chars(10)
    l.set_xalign(0)
    rowb.pack_start(l, False, False, 0) 

    l = Gtk.Label(label = 'Ports')
    l.set_width_chars(15)
    l.set_max_width_chars(15)
    l.set_xalign(0)
    rowb.pack_start(l, False, False, 0)

    l = Gtk.Label(label = 'Volumes')
    l.set_width_chars(60)
    l.set_max_width_chars(60)
    l.set_xalign(0)
    rowb.pack_start(l, False, False, 0) 

    l = Gtk.Label(label = 'Created')
    l.set_width_chars(20)
    l.set_max_width_chars(10)
    l.set_xalign(0)
    rowb.pack_start(l, False, False, 0)

    l = Gtk.Label(label = 'Actions')
    l.set_width_chars(10)
    l.set_max_width_chars(10)
    l.set_xalign(0)
    rowb.pack_end(l, False, False, 0) 

    return rowb
  

  # ['/home/nvidia/data:/data:rw', '/home/nvidia/data:/workspace/data:rw']
  def make_volumes_row(self, volumes):
    if len(volumes) == 0 or len(volumes) == 1:
      if len(volumes) == 1:
        v = ':'.join(volumes[0].split(':')[:2])
        l = Gtk.Label(label = v)
      else:
        l = Gtk.Label(label = '')
      l.set_width_chars(60)
      l.set_max_width_chars(60)
      l.set_xalign(0)
      return l

    row = Gtk.Box.new(orientation = Gtk.Orientation.VERTICAL, spacing = 5)
    for v in volumes:
      v = ':'.join(v.split(':')[:2])
      l = Gtk.Label(label = v)
      l.set_width_chars(60)
      l.set_max_width_chars(60)
      l.set_xalign(0)
#     l.set_justify(Gtk.Justification.LEFT)
      row.pack_start(l, False, False, 0)   

    return row

  def make_gpu_row(self, gpus):
    if len(gpus) == 0 or len(gpus) == 1:
      if len(gpus) == 1:
        l = Gtk.Label(label = gpus[0])
      else:
        l = Gtk.Label(label = '')
      l.set_width_chars(10)
      l.set_max_width_chars(10)
      l.set_xalign(0)
      return l

    row = Gtk.Box.new(orientation = Gtk.Orientation.VERTICAL, spacing = 5)
    for gpu in gpus:
      l = Gtk.Label(label = gpu)
      l.set_width_chars(10)
      l.set_max_width_chars(10)
      l.set_xalign(0)
#     l.set_justify(Gtk.Justification.LEFT)
      row.pack_start(l, False, False, 0)   

    return row


  def ports2str(self, port_tuple):
    c = port_tuple[0]
    h = port_tuple[1]
    pstr = c.split('/')[0] + ':' + h
    return pstr

    return str(ports)

  def create_running_row_nvaie(self,nvaie_resource):
#     grid = Gtk.Grid()
#     grid.set_column_spacing(5)
    rowb = Gtk.Box.new(orientation = Gtk.Orientation.HORIZONTAL, spacing = 0)
    mi = self.nvaie_rt.get_menu_item(nvaie_resource['menu_item_id'])
    fl = self.nvaie_rt.get_flavor(nvaie_resource['flavor_id'])
#     grid.attach(Gtk.Label(label = mi['name']), 0, 0, 1, 1)
#     grid.attach(Gtk.Label(label = fl['name']), 1, 0, 1, 1)
    l = Gtk.Label(label = nvaie_resource['id'])
#    l.set_selectable(True)
    l.set_width_chars(30)
    l.set_max_width_chars(30)
    l.set_ellipsize(Pango.EllipsizeMode.END)
    l.set_xalign(0)
#     l.set_justify(Gtk.Justification.LEFT)
    rowb.pack_start(l, False, False, 0)

    l = Gtk.Label(label = nvaie_resource['status'])
    l.set_width_chars(10)
    l.set_max_width_chars(10)
    l.set_xalign(0)
#     l.set_justify(Gtk.Justification.LEFT)
    rowb.pack_start(l, False, False, 0)

    l = Gtk.Label(label = nvaie_resource['rtype'])
    l.set_width_chars(8)
    l.set_max_width_chars(8)
    l.set_xalign(0)
#     l.set_justify(Gtk.Justification.LEFT)
    rowb.pack_start(l, False, False, 0)

    l = Gtk.Label(label = mi['name'])
    l.set_width_chars(20)
    l.set_max_width_chars(20)
    l.set_xalign(0)
#     l.set_justify(Gtk.Justification.LEFT)
    rowb.pack_start(l, False, False, 0)    


    l = Gtk.Label(label = fl['name'])
    l.set_width_chars(10)
    l.set_max_width_chars(10)
    l.set_xalign(0)
#     l.set_justify(Gtk.Justification.LEFT)
    rowb.pack_start(l, False, False, 0)

    # gpus 10
    l = Gtk.Label(label = '')
    l.set_width_chars(10)
    l.set_max_width_chars(10)
    l.set_xalign(0)
    rowb.pack_start(l, False, False, 0)
    # pots 15
    l = Gtk.Label(label = '')
    l.set_width_chars(15)
    l.set_max_width_chars(15)
    l.set_xalign(0)
    rowb.pack_start(l, False, False, 0)

    # volumes 60
    l = Gtk.Label(label = '')
    l.set_width_chars(60)
    l.set_max_width_chars(60)
    l.set_xalign(0)
    rowb.pack_start(l, False, False, 0)

    l = Gtk.Label(label = timeago.format(float(nvaie_resource['created']), datetime.datetime.now()))
    l.set_width_chars(20)
    l.set_max_width_chars(20)
    l.set_xalign(0)
#     l.set_justify(Gtk.Justification.LEFT)
    rowb.pack_start(l, False, False, 0)

    b = Gtk.Button()
    b.set_relief(Gtk.ReliefStyle.NONE)
    b.set_image(Gtk.Image.new_from_icon_name('edit-delete', Gtk.IconSize.MENU))
    b.connect('clicked', self.on_delete_clicked, self.nvaie_rt, nvaie_resource['id'])
    b.set_tooltip_text('delete')
#     l = Gtk.Label(label = 'actions')
#     l.set_width_chars(10)
#     l.set_max_width_chars(10)
#     l.set_xalign(0)
# #   l.set_justify(Gtk.Justification.LEFT)
    rowb.pack_end(b, False, False, 0)
    b = Gtk.Button()
    b.set_relief(Gtk.ReliefStyle.NONE)
    b.set_image(Gtk.Image.new_from_icon_name('view-refresh', Gtk.IconSize.MENU))
    b.connect('clicked', self.on_restart_clicked, self.nvaie_rt, nvaie_resource['id'])
    b.set_tooltip_text('restart')
    rowb.pack_end(b, False, False, 0)   

    if nvaie_resource['status'] == 'active':
      b = Gtk.Button()
      b.set_relief(Gtk.ReliefStyle.NONE)
      b.set_image(Gtk.Image.new_from_icon_name('media-playback-stop', Gtk.IconSize.MENU))
      b.connect('clicked', self.on_stop_clicked, self.nvaie_rt, nvaie_resource['id'])
      b.set_tooltip_text('stop')
      rowb.pack_end(b, False, False, 0)  
    elif nvaie_resource['status'] == 'stopped':
      b = Gtk.Button()
      b.set_relief(Gtk.ReliefStyle.NONE)
      b.set_image(Gtk.Image.new_from_icon_name('media-playback-start', Gtk.IconSize.MENU))
      b.connect('clicked', self.on_start_clicked, self.nvaie_rt, nvaie_resource['id'])
      b.set_tooltip_text('start')
      rowb.pack_end(b, False, False, 0)        

    b = Gtk.Button()
    b.set_relief(Gtk.ReliefStyle.NONE)
    b.set_image(Gtk.Image.new_from_icon_name('computer', Gtk.IconSize.MENU))
    b.connect('clicked', self.open_url, nvaie_resource['url'])
    b.set_tooltip_text('open in browser')
    rowb.pack_end(b, False, False, 0)

    rowb.set_margin_top(16)
    rowb.set_margin_bottom(16)
    rowb.set_margin_right(20)
    rowb.set_margin_left(20)
#     grid.set_margin_top(16)
#     grid.set_margin_bottom(16)
#     grid.set_margin_right(20)
#     grid.set_margin_left(20)

    return rowb

  def show_dialog(self, type, title, sec_txt, btn_type, primary_txt, buttons):
#   app = gtk.Application()
    dialog = Gtk.MessageDialog(None, 0, type, btn_type, primary_txt)
#  dialog = gtk.MessageDialog(application = app, transient_for = none, 0, type, btn_type, primary_txt)
    dialog.set_title(title)
    dialog.format_secondary_markup(sec_txt)
    dialog.set_icon_from_file(self.icon_default)
    if buttons is not None:
      for k,v in buttons.items():
        dialog.add_buttons(k,v)

    dialog.set_position(Gtk.WindowPosition.CENTER)
    dialog.show()
    response = dialog.run()
    dialog.destroy()
    return response == Gtk.ResponseType.OK  


def header_func(row, row_before, data):
  if row_before is not None:
    row.set_header(Gtk.Separator(orientation = Gtk.Orientation.VERTICAL))

# strictly for testing
if __name__ == '__main__':

  log.setLevel(logging.DEBUG)
  log.addHandler(logging.StreamHandler())
  log.debug("starting..")


  PKG_DIR = str(pathlib.Path(__file__).parent.absolute())

  config = configparser.ConfigParser()
  # case-sensitive
  config.optionxform = str
  # config.read(HOME_DIR + 'config/config.ini')
  config.read(PKG_DIR + '/../config/config.ini')

  win = RTWindow(title = 'NVIDIA AI Enterprise', config = config)
  win.set_position(Gtk.WindowPosition.CENTER)
  win.show_all()
  win.connect("destroy", Gtk.main_quit)

  Gtk.main()