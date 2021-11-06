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


import feedparser
import traceback
import sys
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk
from gi.repository import GdkPixbuf

from nvdsw.tools.settings_yaml import SpinButtonSetting, ComboBoxTextSetting, FileChooserButtonSetting, SwitchSetting
# , TextViewSetting


import logging
import os, pathlib

DEFAULT_TEXTVIEW_WINDOW_HEIGHT = 100
DEFAULT_TEXTVIEW_WINDOW_WIDTH = 650

PKG_DIR = str(pathlib.Path(__file__).parent.absolute())

log = logging.getLogger('preferences')


class TextBox(Gtk.Box):
  def set_title(self, title):
    self.title = title
  def get_title(self):
    return self.title
  def set_setting(self, setn):
    self.setting = setn
  def get_setting(self):
    return self.setting
  def set_val(self, val):
    self.setting['value'] = val
  def get_val(self):
    return self.setting['value'] 
  def set_num_label(self, label):
    self.label = label
  def get_num_label(self):
    return self.label

class SettingsWindow(Gtk.Window):
  def __init__(self, title, config, settings, icon_file):
    super().__init__(title=title)
    self.set_border_width(3)
    self.settings = settings

    self.config = config

    if icon_file is not None:
      icon = GdkPixbuf.Pixbuf.new_from_file(icon_file)
      super().set_default_icon(icon)

    root_hbox = Gtk.Box.new(orientation = Gtk.Orientation.HORIZONTAL, spacing = 10)
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
    self.stack.set_hexpand(False)
    self.stack.set_size_request(800,400)
    self.stack.set_transition_type(Gtk.StackTransitionType.CROSSFADE)
    self.stack.set_transition_duration(100)
    root_hbox.pack_start(self.stack, True, False, 0)

    scrolledwindow = Gtk.ScrolledWindow()
#     scrolledwindow.set_hexpand(True)
    scrolledwindow.set_vexpand(True)

    sidebar_vbox.pack_start(scrolledwindow, True, True, 0)
#    sidebar_vbox.add(scrolledwindow)
    main_listbox = Gtk.ListBox()
    main_listbox.connect('row-activated', self.switchstack)
    scrolledwindow.add(main_listbox)

#     icons = ['preferences-desktop', 'system-software-install', 'application-rss+xml', 'system-software-update']
#     image = Gtk.Image.new_from_file('/home/nvidia/Downloads/126472.png')
    i = 0
#     for l in ['General', 'Containers', 'News', 'Updates']:
    for l,v in settings.get_raw().items():
#      row = Gtk.ListBoxRow()
#      main_listbox.add(row)

#       row.   set_visible_child_name(l)
      grid = Gtk.Grid()
      main_listbox.add(grid)
      pagelabel = Gtk.Label()
      pagecontent = Gtk.Label()
      icon_type = v['icon']['type']
      icon_name = v['icon']['name']
      if icon_type == 'file':
#      if l == 'Containers':
        fname = os.path.abspath(PKG_DIR + "/../" + icon_name)
#        fname = os.path.abspath(PKG_DIR + "/../" + self.config['icons']['CONTAINER'])
#        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(filename=fname, width=16, height=16, preserve_aspect_ratio=True)
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(filename=fname, width=16, height=16, preserve_aspect_ratio=True)
        image = Gtk.Image.new_from_pixbuf(pixbuf)
      else:
#        image = Gtk.Image.new_from_icon_name(icons[i], Gtk.IconSize.MENU)
        image = Gtk.Image.new_from_icon_name(icon_name, Gtk.IconSize.MENU)
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
#       self.stack.add_named(pagecontent, l)
      
#       hbox = Gtk.Box.new(orientation = Gtk.Orientation.HORIZONTAL, spacing = 0)
#       self.stack.add_named(hbox, l)

      sw = Gtk.ScrolledWindow()
      sw.set_vexpand(False)
      sw.set_hexpand(True)
#       hbox.add(sw)
      self.stack.add_named(sw, l)
      vbox0 = Gtk.Box.new(orientation = Gtk.Orientation.VERTICAL, spacing = 0)
      sw.add(vbox0)

      vbox = Gtk.Box.new(orientation = Gtk.Orientation.VERTICAL, spacing = 0)
#       vbox.set_property('maximum-width', 600)
      vbox.set_size_request(220,200)
      vbox0.pack_start(vbox, False, False, 0)
#       sw.pack_start(vbox, True, False, 0)
##      sw.add(vbox)
#       vbox.add(Gtk.Label(label = l))

      label = Gtk.Label(label = l)
      label.set_margin_top(16)
      label.set_margin_bottom(16)

      vbox.pack_start(label, False, False, 0)
      frame = Gtk.Frame()
      vbox.pack_start(frame, False, False, 0)
#       vbox.add(frame)
      listbox = Gtk.ListBox()
      listbox.connect('row-activated', self.itempopup)
      frame.add(listbox)

      j=0
#      for k,value in v.items():
      for item in v['items']:
        k = item['key']
        setting_name = item['name']
        value = item['value']
        ktype = item['type']

#        print('processing: ' + k)

        if j != 0:
          separator = Gtk.Separator(orientation = Gtk.Orientation.VERTICAL)
          listbox.add(separator)

        rowb = Gtk.Box.new(orientation = Gtk.Orientation.HORIZONTAL, spacing = 0)

        rowb.pack_start(Gtk.Label(label = setting_name), False, False, 0)

        

        value_str = value
        if isinstance(value, int):
          value_str = str(value)
        elif isinstance(value, list):
          value_str = value[0]

        
        if ktype == 'SpinButton':
          min = item['min']
          max = item['max']
          step = item['step']
          # widj = Gtk.SpinButton.new_with_range(min, max, step)
          widj = SpinButtonSetting()
          widj.set_range(min, max)
          # not doing anything special for a two button press (second param)
          widj.set_increments(step,step)
          widj.set_numeric(True)
          widj.set_value(value)
          widj.set_setting(item)
          widj.connect("value-changed", self.on_spinbutton_changed)
        elif ktype == 'ComboBoxText':
          # widj = Gtk.ComboBoxText()
          widj = ComboBoxTextSetting()
          for option in item['options']:  
            widj.append(str(option['value']), option['name'])
          widj.set_active_id(str(value))
          widj.set_setting(item)
          widj.connect("changed", self.on_combo_changed)
        elif ktype == 'Switch':
          # widj = Gtk.Switch()
          widj = SwitchSetting()
          widj.set_active(value)
          widj.connect("state-set", self.on_switch_state_changed)
          widj.set_setting(item)
        elif ktype == 'FolderChooserButton':
          # widj = Gtk.FileChooserButton(title="Folder to mount inside container", action = Gtk.FileChooserAction.SELECT_FOLDER)
          widj = FileChooserButtonSetting()
          widj.set_title("Folder to mount inside container")
          
          widj.connect("file-set", self.on_filechooser_changed)
          if not value.startswith('/'):
            value = os.environ['HOME'] + '/' + value
          widj.set_current_folder(value)
          widj.set_action(Gtk.FileChooserAction.SELECT_FOLDER)
          widj.set_setting(item)
        elif ktype == 'TextView':
          widj = TextBox()
          widj.set_spacing(5)
#           widj = TextBox.new(orientation = Gtk.Orientation.HORIZONTAL, spacing = 5)
          label = Gtk.Label(label = str(len(value)))
          widj.set_num_label(label)
          widj.add(label)
#           widj.set_text(value)
          widj.set_title(setting_name)
          widj.set_setting(item)
          image = Gtk.Image.new_from_icon_name('go-next', Gtk.IconSize.MENU)
          widj.add(image)
        else:
          widj = Gtk.Label(label = value_str)

        
        rowb.pack_end(widj, False, False, 0)
        rowb.set_margin_top(16)
        rowb.set_margin_bottom(16)
        rowb.set_margin_right(20)
        rowb.set_margin_left(20)
        listbox.add(rowb)
        j = j + 1
        




      i = i + 1

    root_hbox.show_all()

  def on_filechooser_changed(self, fileChooserButton):
    log.debug('in on_filechooser_changed!')
    fileChooserButton.set_val(fileChooserButton.get_current_folder())
    log.debug('current folder set to: ' + fileChooserButton.get_val())
    self.settings.parse_and_save()


  def on_spinbutton_changed(self, spinbutton):
    log.debug('in on_spinbutton_changed!')
    spinbutton.set_val(spinbutton.get_value_as_int())
    log.debug('new spinbutton value is: ' + str(spinbutton.get_val()))
    self.settings.parse_and_save()

  def on_combo_changed(self, combo):
    log.debug('in on_combo_changed!')
    combo.set_val(int(combo.get_active_id()))
    log.debug('new combo value is: ' + str(combo.get_val()))
    self.settings.parse_and_save()

  def on_switch_state_changed(self, switch, new_state):
    log.debug('in on_switch_state_changed!')
#     log.debug(switch)
    # this is simpler than others
    log.debug('new switch state: ' + str(new_state))
    switch.set_val(new_state)
    
    self.settings.parse_and_save()

  def itempopup(self, box, row):
#     print('list item activated!')
    box = row.get_child()
    second_child = box.get_children()[1]
    if isinstance(second_child, TextBox):
      dialog = Gtk.Dialog(title = second_child.get_title(),transient_for=self, modal = True)
      dialog.set_size_request(DEFAULT_TEXTVIEW_WINDOW_WIDTH, DEFAULT_TEXTVIEW_WINDOW_HEIGHT)
      dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, 'Save', Gtk.ResponseType.OK)
      ca = dialog.get_content_area()
      vbox = Gtk.Box.new(orientation = Gtk.Orientation.VERTICAL, spacing = 10)
      vbox.set_border_width(10)
      frame = Gtk.Frame()
      vbox.add(frame)
      ca.add(vbox)


      scrolledwindow = Gtk.ScrolledWindow()
      scrolledwindow.set_hexpand(True)
      scrolledwindow.set_vexpand(True)
      frame.add(scrolledwindow)

      textview = Gtk.TextView()
#       textview = TextViewSetting()
      textview.set_left_margin(10)
      textview.set_top_margin(10)
      textbuffer = textview.get_buffer()
      textbuffer.set_text('\n'.join(second_child.get_val()))
      scrolledwindow.add(textview)
      dialog.show_all()
      while True:
        rc = dialog.run()
        if rc == Gtk.ResponseType.CANCEL:
          log.debug('user chose to cancel')
          dialog.destroy()
          return
        else:
          log.debug('user chose ok')
          start_iter = textbuffer.get_start_iter()
          end_iter = textbuffer.get_end_iter()
          text = textbuffer.get_text(start_iter, end_iter, False) 

          new_val = text.split('\n')
          valmsg = self.validate_news_urls(new_val)
          if valmsg == '':
            second_child.set_val(new_val)
            self.settings.parse_and_save()
            l = second_child.get_num_label()
            l.set_text(str(len(new_val)))
            # some magic here to modify that label !
            dialog.destroy()
            return
          else:
            d = Gtk.MessageDialog(parent = dialog, message_type = Gtk.MessageType.ERROR, buttons = Gtk.ButtonsType.OK, text = valmsg)
            d.run()
            d.destroy()
#       print(second_child.get_text())
#    for c in box.get_children():
#       print(c)

  def validate_news_urls(self, urllist):
    msg = ''
    for f in urllist:
      try:
       log.debug('validating url: ' + f)
       fs = feedparser.parse(f)
       log.debug("num of feed items parsed: " + str(len(fs)))
      except Exception:
        log.warning("unable to parse feed " + f)
        exc_type, exc_value, exc_tb = sys.exc_info()
        log.warning(traceback.format_exception(exc_type, exc_value, exc_tb)) 
        if (msg != ''):
          msg += '\n'
        msg += "unable to parse feed " + f
        

    return msg

  def switchstack(self, box, row):
#    log.debug('switchstack')
    grid = row.get_child()
#    print(dir(grid))
    label = grid.get_children()[0]
    name = label.get_text()
    self.stack.set_visible_child_name(name)
#    print(txt)
    
#        root_vbox.show()

class PreferencesWindow(Gtk.Window):
    def __init__(self, title):
        super().__init__(title=title)
        self.set_border_width(3)

        self.notebook = Gtk.Notebook()
# run it vertically?
#        self.notebook.set_tab_pos(0)
        self.notebook.set_scrollable(True)
        self.notebook.set_show_border(True)
        self.notebook.set_border_width(10)

        self.add(self.notebook)

        self.page1 = Gtk.Box()
        self.page1.set_border_width(10)
#        self.page1.set_show_border(True)
        self.page1.add(Gtk.Label(label="General"))
#        self.page1.add(Gtk.Label(label="Hello World", angle=25, halign=Gtk.Align.END))
        self.notebook.append_page(self.page1, Gtk.Label(label="General"))

        self.page2 = Gtk.Box()
        self.page2.set_border_width(10)
        self.page2.add(Gtk.Label(label="Prefetch latest images toggle"))
        self.page2.add(Gtk.Label(label="Download only during a certain window"))
        self.notebook.append_page(self.page2, Gtk.Label(label="Tools"))

        self.page3 = Gtk.Box()
        self.page3.set_border_width(10)
        self.page3.add(Gtk.Label(label="News"))
        self.notebook.append_page(self.page3, Gtk.Label(label="News"))

        self.page3 = Gtk.Box()
        self.page3.set_border_width(10)
        self.page3.add(Gtk.Label(label="Updates"))
        self.notebook.append_page(self.page3, Gtk.Label(label="Updates"))

#        self.page4 = Gtk.Box()
#        self.page4.set_border_width(10)
#        self.page4.add(Gtk.Label(label="A page with an image for a Title."))

#         button = Gtk.Button.new_with_label("Mama")
#         c1  = Gtk.Widget.get_style_context(button);
#         Gtk.StyleContext.add_class(c1, "e_button")
#         self.page4.add(button)
#         self.notebook.append_page(
#             self.page4, Gtk.Image.new_from_icon_name("help-about", Gtk.IconSize.MENU)
#       )



# strictly for testing
if __name__ == '__main__':

  log.setLevel(logging.DEBUG)
  log.addHandler(logging.StreamHandler())
  log.debug("starting..")

  win = SettingsWindow(title = 'nvdsw preferences')
  win.set_position(Gtk.WindowPosition.CENTER)
  win.show_all()
  win.connect("destroy", Gtk.main_quit)

  Gtk.main()