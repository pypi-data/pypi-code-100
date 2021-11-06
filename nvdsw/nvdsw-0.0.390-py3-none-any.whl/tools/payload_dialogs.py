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
import json
import subprocess
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk as gtk, GLib
import time
import threading
import logging

log = logging.getLogger('payload_dialogs')


class PayloadDialog(gtk.Dialog):
  def __init__(self, title = '', label = '', cmd = None):
        gtk.Dialog.__init__(self, title=title, transient_for=None, flags=0)
        self.proc = None
        self.cmd = None
        self.timeout = None
        self.cmd_stdout = ''
        self.cmd_stderr = ''
        self.cmd_rc = 0
        self.payload_killed = False
        self.button1 = self.add_button(gtk.STOCK_CANCEL, gtk.ResponseType.CANCEL)
        self.button1.connect("clicked", self.stop_payload) 
        self.connect("delete-event", self.stop_payload_close)
        self.button2 = self.add_button(gtk.STOCK_OK, gtk.ResponseType.OK)

        self.set_default_size(300, 80)

        self.label = gtk.Label(label=label)
        
  #      self.label2 = gtk.Label(label='')
#        self.label.set_alignment(0.5,0)

        box = self.get_content_area()
        box.set_spacing(10)
        box.add(self.label)
  #      box.add(self.label2)
        self.show_all()

  # only the paranoid survive.
  def set_label(self, msg):
    GLib.idle_add(self._set_label, msg)

  def _set_label(self, msg):
    self.label.set_text(msg)

  def set_markup(self, msg):
    self.label.set_markup(msg)
#    self.label.set_alignment(0.5,0)

#  def set_label2(self, msg):
#    self.label2.set_text(msg)

#  def set_markup2(self, msg):
#    self.label2.set_markup(msg)
#    self.label2.set_alignment(0.5,0)    

#  def set_timeout(self, tm):
#    self.timeout = tm

  def set_cmd(self, payload):
    self.cmd = payload

  def get_cmd_out(self):
    return self.cmd_stdout

  def get_cmd_err(self):
    return self.cmd_stderr

  def get_cmd_rc(self):
    return self.cmd_rc

  def run(self):
    if self.cmd is not None:
      self.cmd_stderr = None
      self.cmd_stdout = None
      self.cmd_rc = 0
      self.start_payload()
    return gtk.Dialog.run(self)
    
  def stop_payload_close(self,button, x):
    log.debug("stop payload close")
    return self.stop_payload(button)

  def stop_payload(self, button):
    if self.cmd is None:
      log.debug("the cmd is not set")
      return
#    if self.payload_thread is None:
#      log.debug("no payload thread")
#      return

    if self.proc is None:
      log.debug("no proc to kill")
      return

    if self.proc.poll() is not None:
      log.debug("the proc is dead already, no need to kill it")
      return
    self.payload_killed = True
    self.proc.kill()

  def start_payload(self):
    log.debug("start_payload called")
    GLib.idle_add(self.payload_wrapper)
  #  self.payload_thread = threading.Thread(target=self.payload_wrapper, args=[])
#    self.payload_thread.daemon = True
  #  self.payload_thread.start()
  
  def destroy_cancel_button(self):
    log.debug("inside destroy cancel button")
    GLib.idle_add(self._destroy_cancel_button)

  def _destroy_cancel_button(self):
    log.debug("inside _destroy cancel button")
    self.button1.destroy()

  def destroy_ok_button(self):
    log.debug("inside destroy ok button")
    GLib.idle_add(self._destroy_ok_button)

  def _destroy_ok_button(self):
    log.debug("inside _destroy ok button")
    self.button2.destroy()    

  def on_timeout(self, user_data):
  #  log.debug("on_timeout")
    self.progressBar.pulse()
    if self.proc is not None:
     if self.proc.poll() is not None:
      log.debug("payload thread sees that the proc is dead")
      GLib.source_remove(self.timeout_id)
      self.cleanup_payload()
    return True


  def payload_wrapper(self):
    # scheduled via GLib
    log.debug("in payload wrapper")
    self.progressBar = gtk.ProgressBar()
    self.get_content_area().add(self.progressBar)
    self.progressBar.show()
    log.debug("starting actual payload")
    log.debug("cmd is " + self.cmd)
    self.proc = subprocess.Popen(self.cmd, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE) 
    self.timeout_id = GLib.timeout_add(100, self.on_timeout, None)

  def cleanup_payload(self):
    log.debug("in cleanup_payload")
    out = None
    err = None
    try:
      out, err = self.proc.communicate(timeout = 0.5)
    except subprocess.TimeoutExpired:
      log.debug("cleanup_payload sees that the pipes are still open.... looks like we've launched a grandchild and the parent died..")
      rc = self.proc.poll()
      if rc is None:
        log.error("rc is None, meaning we are still running.. this simply cannot be! let's whack the process just to be sure")
        self.proc.kill()
      else:
        log.info("rc is " + str(rc))

    if out is not None:
      self.cmd_stdout = out.decode('utf-8')
      log.debug(self.cmd_stdout)
    if err is not None:
      self.cmd_stderr = err.decode('utf-8')
      log.debug(self.cmd_stderr)
#    log.debug("after communicate")
    self.cmd_rc = self.proc.returncode
    if self.get_content_area() is not None:
      self.get_content_area().remove(self.progressBar)
    log.debug("cleanup_payload done")
    self.response(gtk.ResponseType.NONE)

  def payload_wrapper_classic(self):
    log.debug("in payload wrapper")
#    spinner = gtk.Spinner()
#     self.get_content_area().add(spinner)
#    spinner.show()
#     spinner.start()
    self.progressBar = gtk.ProgressBar()
    self.get_content_area().add(self.progressBar)
    self.progressBar.show()
    self.timeout_id = GLib.timeout_add(100, self.on_timeout, None)
    log.debug("starting actual payload")
    log.debug("cmd is " + self.cmd)

    self.proc = subprocess.Popen(self.cmd, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    rc = self.proc.poll()
    while rc is None:
      # still running
      try:
#        log.debug("before communicate")
        out, err = self.proc.communicate(timeout = 0.5)
#        log.debug("after communicate")
        if out is not None:
          if self.cmd_stdout is None:
            self.cmd_stdout = out.decode('utf-8')
          else:
            self.cmd_stdout += out.decode('utf-8')
        if err is not None:
          if self.cmd_stderr is None:
            self.cmd_stderr = err.decode('utf-8')
          else:
            self.cmd_stderr += err.decode('utf-8')

        rc = self.proc.poll()
      except subprocess.TimeoutExpired:
        rc = self.proc.poll()
        log.debug("payload still running.. ")
  


    self.cmd_rc = rc
#     try:
#       self.cmd_stdout, self.cmd_stderr = self.proc.communicate(timeout = self.timeout)
#     except subprocess.TimeoutExpired:
#       log.debug("timeout expired")

#     rc = self.proc.poll()
#     if rc is None:
#       log.error("the process is still alive.. killing..")
#       self.proc.kill()
#       self.cmd_rc = -1
#     else:
#       log.debug("the process terminated normally with rc: " + str(self.proc.returncode))
#       self.cmd_rc = self.proc.returncode

    
#    rc = None
#    while rc is None:
#      rc = self.proc.poll()
#      print("the process is still alive")
#      time.sleep(1)
    log.debug("payload wrapper: payload done with rc: " + str(self.cmd_rc))
    GLib.source_remove(self.timeout_id)
    self.get_content_area().remove(self.progressBar)
#    spinner.stop()

    # the idea is to return to the caller here... since we are done
    if self.payload_killed:
      return
#       self.response(gtk.ResponseType.CANCEL)
    self.response(gtk.ResponseType.NONE)


  

# strictly for testing
if __name__ == '__main__':

  log.setLevel(logging.DEBUG)
  log.addHandler(logging.StreamHandler())
  log.debug("starting..")
  dialog = PayloadDialog(title = "Data Science Workbench", label = None, cmd = None)
  dialog.set_label("Check for updates?")
  response = dialog.run()
  log.debug(response)
  if response == gtk.ResponseType.CANCEL or response == gtk.ResponseType.DELETE_EVENT:
    log.debug("user chose to cancel")
    sys.exit()

  log.debug("proceeding")
#   print("second dialog")
  # dialog.set_label("Checking for updates")
  dialog.set_label("Checking for updates")
#  dialog.set_markup2("<a href='https://github.com/NVIDIA/data-science-stack/releases'>Release notes</a>")
  dialog.destroy_ok_button()
#  dialog.set_cmd("pip3 list -o --format json")
  dialog.set_cmd("/home/dima/.local/bin/nvdswd")
#  dialog.set_timeout(6)
  response = dialog.run()
#   print(response)
  if response == gtk.ResponseType.CANCEL:
    log.debug("user chose to cancel the workload while it was running")

  if response == gtk.ResponseType.NONE:
    log.debug("workload completed normally")

  if response == gtk.ResponseType.DELETE_EVENT:
    log.debug("user chose to close the dialog")

  # print("chilling before quitting")
  # time.sleep(10)

  out = dialog.get_cmd_out()
  if out is not None:
   for j in json.loads(out):
    if j['name'] == 'nvdsw':
      log.debug("latest version: " + j['latest_version'])

  log.debug("all done")
