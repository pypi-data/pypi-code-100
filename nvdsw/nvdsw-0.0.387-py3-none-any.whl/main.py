#!/usr/bin/env python3
#
# coding: utf-8

# Copyright (c) 2019-2020, vVIDIA CORPORATION.  All Rights Reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.
#



import os
import signal
# import socket
import urllib.request
import gi
import subprocess
import time
import threading, queue
import re
import sys
import traceback
import datetime
import argparse
import logging
from logging.handlers import TimedRotatingFileHandler
import pathlib

import feedparser
import configparser
import yaml

import semver

import nvdsw
from nvdsw.tools.runner import DockerRunner
from nvdsw.tools.versions import VersionChecker
from nvdsw.tools.hardware import HWStats
from nvdsw.tools.payload_dialogs import PayloadDialog
from nvdsw.tools.license_dialogs import LicenseDialog
from nvdsw.tools.winraise import winraise
from nvdsw.tools.preferences import SettingsWindow
from nvdsw.tools.claunch import CLaunchDialog
from nvdsw.tools.cstatus import CStatusDialog

from nvdsw.tools.runtime_windows import RTWindow
from nvdsw.runtimes.nvaie import nvaie
from nvdsw.runtimes.dockerrt import dockerrt

from nvdsw.tools.settings_yaml import SettingsYaml
from nvdsw.tools.news_processor import NewsProcessor, NewsItem



# print("script running under: " + pathlib.Path(__file__).parent.absolute())

PKG_DIR = str(pathlib.Path(__file__).parent.absolute())
# print(PKG_DIR)
HOME_DIR = os.environ['HOME']
config = configparser.ConfigParser()
# case-sensitive
config.optionxform = str
# config.read(HOME_DIR + 'config/config.ini')
config.read(PKG_DIR + '/config/config.ini')

# this is our app name 
APP_ID = config['MAIN']['APP_ID']
APP_DIR = HOME_DIR + "/.config" + '/' + APP_ID 

SETUP_SUCCEEDED_FILE = APP_DIR + '/' + config['MAIN']['SETUP_SUCCEEDED_FILE']
LICENSE_ACCEPTED_FILE = APP_DIR + '/' + config['MAIN']['LICENSE_ACCEPTED_FILE']
# APP_DIR = HOME_DIR + '/' + APP_ID 

img_pull_queue = queue.Queue()
try:
    os.stat(APP_DIR)
except:
    os.makedirs(APP_DIR)  

LOG_DIR = APP_DIR + '/' + config['MAIN']['LOG_DIR']
LOG_FILE = LOG_DIR + '/' + APP_ID + '.log'
LOG = logging.getLogger(APP_ID)
# LOG_FORMAT = config['MAIN']['LOG_FORMAT']
LOG_FORMAT = ('%(asctime)s - %(threadName)s - %(name)s - %(levelname)s - %(message)s')

try:
    os.stat(LOG_DIR)
except:
    os.mkdir(LOG_DIR)  

# logger.setLevel(logging.DEBUG)

# logging.basicConfig(filename = LOG_FILE, level=logging.DEBUG, format = LOG_FORMAT)
handler = TimedRotatingFileHandler(LOG_FILE, when="d", interval=int(config['MAIN']['LOG_ROLL_DAYS']), backupCount=int(config['MAIN']['LOG_BACKUPS']))
# logger.addHandler(handler)
logging.basicConfig(level=logging.DEBUG, format = LOG_FORMAT, handlers = [handler])

try:
    os.stat(SETUP_SUCCEEDED_FILE)
except:
    LOG.error("setup hasn't run, exiting")
    print("please run nvdsw-setup first")
    sys.exit(1)

uuid = ""
UUID_FILE = APP_DIR + '/' + config['MAIN']['UUID_FILE']
try:
    os.stat(UUID_FILE)
    with open(UUID_FILE, "r") as uuidf:
      uuid = uuidf.readline()
    LOG.debug("uuid is: " + uuid)

except:
    LOG.error("setup hasn't generated the UUID file, exiting")
    print("please run nvdsw-setup first to generate the UUID file")
    sys.exit(1)

menus_fname = PKG_DIR + "/" + config['MAIN']['MENUS_YAML']
try:
  ymenus = yaml.load(open(menus_fname, 'r'), Loader=yaml.SafeLoader) 
except FileNotFoundError:
  LOG.error("menus file not found " + menus_fname)


settings = SettingsYaml(PKG_DIR + "/" + config['MAIN']['USERSETTINGS_YAML'])
try:
  settings.load() 
except FileNotFoundError:
  LOG.error("settings file not found " + config['MAIN']['USERSETTINGS_YAML'])  

# settings.get() = settings.get_settings()

DOCKERFILE_DIR = PKG_DIR + '/' + config['MAIN']['DOCKERFILE_DIR']

# these will explode if not installed or if you are not on a laptop / desktop
gi.require_version("Gtk", "3.0")
gi.require_version('AppIndicator3', '0.1')
gi.require_version('Notify', '0.7')

from gi.repository import GLib
from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator
from gi.repository import Notify as notify
from gi.repository import GObject
from gi.repository import GdkPixbuf

LICENSE = None

# with open (APP_DIR + "/LICENSE", "r") as lfile:
with open (PKG_DIR + "/LICENSE", "r") as lfile:  
    LICENSE = lfile.readlines()

# ICON_DEFAULT = os.path.abspath(APP_DIR + '/' + config['MAIN']['ICON_FILE'])
ICON_DEFAULT = os.path.abspath(PKG_DIR + "/" + config['icons']['ICON_FILE'])
# ICON_WARNING = 'dialog-warning'
ICON_WARNING = os.path.abspath(PKG_DIR + "/" + config['icons']['UPDATE_ICON_FILE']) 

DOUBLE_LOOP_SLEEP_INTERVAL = int(config['MAIN']['DOUBLE_LOOP_SLEEP_INTERVAL'])



newest_item_timestamp = -1
notifs = []

DISPLAY_CONTAINER_INFO = config.getboolean('MAIN','DISPLAY_CONTAINER_INFO')

IMG_CHECK_INTERVAL = int(config['MAIN']['IMG_CHECK_INTERVAL'])

# this is supposed to be $HOME/.local/bin  except if there conda or venv
SCRIPT_DIR = ""
# the terms dialog window
# the idea is to prevent too many windows
about = None

# the prefs window
prefs_win = None
# the nvaie window
launcher_win = None
child_procs = {}


GPUs = HWStats(config).get_gpus()

v = None
# moving this to main
# v = VersionChecker(config, SCRIPT_DIR)
# v.check_local()



# DSS_VER = "2.7.0"

LATEST_DSS_VER = config['MAIN']['LATEST_DSS_VERSION']

# DSS_UP_TO_DATE = False
# if semver.compare(v.local['dss'],config['MAIN']['LATEST_DSS_VERSION']) >= 0:
DSS_UP_TO_DATE = True



NVDSW_UP_TO_DATE = True
ALREADY_NOTIFIED_TO_UPGRADE = False
ALREADY_UPGRADED = False
# what happens when you click on the the menu item for the data science workbench?
NVDSW_MENU_ITEM_ACTION_HANDLER_ID = None

# what happens when you click on the the menu item for the data science stack?
DSS_MENU_ITEM_ACTION_HANDLER_ID = None


nvaie_rt = nvaie()
local_rt = dockerrt(config,ymenus, settings)

# should we disable notifications?

# notify_disable = usersettings['General']['NOTIFY_DISABLE']
# we will be updating this periodically
# news_item = gtk.MenuItem.new_with_label('News' )
news_menu = gtk.Menu.new()
# sw_menu = gtk.Menu.new()
sw_menu_client = gtk.MenuItem()
sw_menu_stack = gtk.MenuItem()

def open_url(_,url):
#   cmd = ["/opt/google/chrome/chrome", url]
  cmd = ["/usr/bin/x-www-browser", url]
  subprocess.Popen(cmd)
#  subprocess.call(cmd)

def do_dss_cli(m):
  cmd = ["/usr/bin/gnome-terminal","--working-directory="+os.environ['HOME']+"/data-science-stack", "--", "sh",  "-c", "./data-science-stack;bash"]
  subprocess.call(cmd)

def do_kaggle_cli(m):
  cmd = ["/usr/bin/gnome-terminal","--working-directory="+os.environ['HOME'], "--", "sh",  "-c", "kaggle -v;bash"]
  subprocess.call(cmd)

def do_ngc_cli(m):
  cmd = ["/usr/bin/gnome-terminal","--working-directory="+os.environ['HOME'], "--", "sh",  "-c", "ngc --version;bash"]
  subprocess.call(cmd)    


def do_aws_cli_wrapper(m,r):
  if do_aws_cli(m,r):
    LOG.debug("cli launched")
  else:
    LOG.error("could not launch CLI")
    show_dialog(gtk.MessageType.ERROR, 'nvdsw awscli start error', "AWS CLI failed to start. Please see logs", gtk.ButtonsType.OK,"Launch Error", None)
    
def do_aws_cli(m, r):
  # AWS CLI runs inside a container. So, does it exist?
  container_exists = False
  try:
    import docker
    client = r.docker.DockerClient()
    c = client.containers.get(config['MAIN']['AWS_CLI_CONTAINER_NAME'])
    num_tries = 0
    while c.status != 'running':
      if num_tries > 4:
        LOG.error("unable to start the container.")
        client.close()
        return False
      LOG.warning("the AWS CLI container exists but it is in non-running status " + c.status)
      LOG.debug("attempting to start... try " + str(num_tries))
      c.start()
      time.sleep(1)
      c.reload()
      num_tries = num_tries + 1

    client.close()
    container_exists =  True
  except docker.errors.NotFound:
    container_exists = False
  except docker.errors.APIError:
    LOG.warning("Unable to start AWS CLI: Docker API error")
    exc_type, exc_value, exc_tb = sys.exc_info()
    LOG.warning(traceback.format_exception(exc_type, exc_value, exc_tb))  
    return False
  except Exception:
    LOG.warning("Unable to start AWS CLI: Docker API error")
    exc_type, exc_value, exc_tb = sys.exc_info()
    LOG.warning(traceback.format_exception(exc_type, exc_value, exc_tb))  
    return False    
  
  
  if container_exists:
    cmd = ["/usr/bin/gnome-terminal","--working-directory="+os.environ['HOME'], "--", "sh",  "-c", "docker attach " + config['MAIN']['AWS_CLI_CONTAINER_NAME']]
  else:
    mount_str = "-v " + os.environ['HOME'] + '/' + config['MAIN']['AWS_DOCKER_SOURCE_MOUNT'] + ':' + config['MAIN']['AWS_DOCKER_TARGET_MOUNT']

    cmd = ["/usr/bin/gnome-terminal","--working-directory="+os.environ['HOME'], "--", "sh",  "-c", "docker run --name " + 
      config['MAIN']['AWS_CLI_CONTAINER_NAME'] + ' --entrypoint /bin/bash ' + mount_str + ' -ti ' + config['MAIN']['AWS_DOCKER_IMAGE'] + ' -c "aws;bash"']

  LOG.debug("aws docker cmd: " + ' '.join(cmd))
  subprocess.call(cmd)
  return True
  

def do_spyder(m):
    global child_procs
#    if m.get_active():
#      cmd = ["/bin/bash", "-c", "/home/dima/conda/envs/data-science-stack-2.7.0/bin/spyder &"]
    if 'spyder' in child_procs:
      LOG.info("spyder was previously launched. Checking to see if it's alive")
      if child_procs['spyder'].poll() is None:
        LOG.info("another process still running. No need to start a new one")
        return
      else:
        LOG.info("the old process died. Starting a new one.")
    else:
      LOG.info("starting a new spyder")
    child_procs['spyder'] = subprocess.Popen("/usr/bin/spyder3")
#    else:
#      LOG.debug("attempted murder of Spyder but we don't support it.  For obvious reasons.")
#      child_procs['spyder'].terminate()
#      cmd = ["pkill", "spyder"]

#    subprocess.call(cmd)

def do_code(m):
    global child_procs
    CODE_EXEC = "/snap/bin/code"
    # CODE_EXEC = "/usr/bin/code"
#    if m.get_active():
#      cmd = ["/bin/bash", "-c", "/snap/bin/code &"]
    if 'code' in child_procs:
      LOG.info("code was previously launched. Checking to see if it's alive")
      if child_procs['code'].poll() is None:
        LOG.info("another process still running. No need to start a new one")
        return
      else:
        LOG.info("the old process died. Starting a new one.")
    else:
      LOG.info("starting a new code")
    child_procs['code'] = subprocess.Popen(CODE_EXEC)
     # you can't just kill the process :(
#      child_procs['code'].kill()
#      cmd = ["pkill", "code"]
#      subprocess.call(cmd)


# def disable_notification(self):
#     global notify_disable
#     notify_disable = self.get_active()
#     if notify_disable and indicator.get_icon() == ICON_WARNING:
#        clear_warning()

def do_upgrade_dss(m):
  global DSS_UP_TO_DATE
  LOG.info("do_upgrade_dss called")
  driver_before_upgrade = v.local['driver']
  DRIVER_VER_CHANGED = False

  title = "nvdsw dss upgrade"
  dialog = PayloadDialog(title = title, label = None, cmd = None)
  dialog.set_label("Upgrading DS Stack to ver " + LATEST_DSS_VER)
  dialog.set_icon_from_file(ICON_DEFAULT)
  release_label = gtk.Label()
  release_label.set_markup("<a href='https://github.com/NVIDIA/data-science-stack/releases'>Release notes</a>")
  release_label.show()
  dialog.get_content_area().add(release_label)

  dialog.set_position(gtk.WindowPosition.CENTER)
  dialog.show()
  GLib.idle_add(winraise, title)  

  response = dialog.run()
  if response == gtk.ResponseType.CANCEL or response == gtk.ResponseType.DELETE_EVENT:
    LOG.info("the user chose to cancel the DSS upgrade") 
    dialog.destroy()
    return
  LOG.info("do_upgrade_dss confirmed")
  dialog.set_label("DSS upgrade in progress")
  dialog.button2.hide()
  # need to put this into a conf file?
  # rc = os.system(SCRIPT_DIR + '/iudss.sh') + LATEST_DSS_VER
  # the last 1 is a flag to use pkexec
  dialog.set_cmd(SCRIPT_DIR + '/iudss.sh ' + LATEST_DSS_VER + " 1")
  response = dialog.run()

  if response == gtk.ResponseType.CANCEL:
    LOG.debug("user chose to cancel the upgrade while it was running")
    dialog.destroy()
    return
  if response == gtk.ResponseType.DELETE_EVENT:
    LOG.debug("user chose to close the dialog while it was running")
    dialog.destroy()
    return
  if response == gtk.ResponseType.NONE:
    LOG.debug("dss upgrade completed normally")

#   v.local['dss']
  
  v.check_driver_local()
  if driver_before_upgrade != v.local['driver']:
    DRIVER_VER_CHANGED = True
  
  # we are only updating the driver and the dss. No other versions should change.
  v.check_dss_local()
 

  out = dialog.get_cmd_out()
  err = dialog.get_cmd_err()
  rc = dialog.get_cmd_rc()
  if rc == 0:
      LOG.info("DS Stack Upgrade successful")
      if out is not None:
        LOG.debug("stdout: " + out)
      if err is not None:
        LOG.debug("stderr: " + err) 

      if v.local['dss'] == LATEST_DSS_VER:
        DSS_UP_TO_DATE = True
        GLib.idle_add(update_sw_menu_dss_item, sw_menu_stack, ' DS Stack: '+ v.local['dss'])
        # flip the icon to normal if nvdsw is up to date
        if NVDSW_UP_TO_DATE:
          indicator.set_icon(ICON_DEFAULT)
      else:
        DSS_UP_TO_DATE = False
        LOG.error("the dss upgrade script completed fine, but the DSS version did not change. weird.")

    
      dialog.set_label("DS Stack Upgrade successful")
      dialog.set_cmd(None)

      if DRIVER_VER_CHANGED:
        release_label.set_markup("The driver was updated. Please reboot")
      else:
        release_label.set_markup("No reboot required.")

      dialog.button1.hide() # the cancel button we don't need
      dialog.button2.show()
      dialog.run()
      dialog.destroy()
      

  else:
      LOG.error("dss upgrade failed with rc: " + str(rc))
      LOG.error("stdout: " + out)
      LOG.error("stderr: " + err)
      dialog.set_label("DS Stack Upgrade failed")
      dialog.set_cmd(None)
      release_label.set_markup("Please see logs.")
#      dialog.get_content_area().remove(release_label)
#      release_label.destroy()
      dialog.button1.hide() # the cancel button we don't need
      # dialog.button2 = dialog.add_button(gtk.STOCK_OK, gtk.ResponseType.OK)
      dialog.button2.show()
      dialog.run()
      dialog.destroy()
      return  

def do_upgrade(m):
  global ALREADY_UPGRADED
  if ALREADY_UPGRADED:
    LOG.info("do_upgraded called but we already upgraded, so..")
    return

  title = "nvdsw upgrade"
  dialog = PayloadDialog(title = title, label = None, cmd = None)
  dialog.set_label("Upgrading to ver " + v.remote[APP_ID])
  dialog.set_icon_from_file(ICON_DEFAULT)
  release_label = gtk.Label()
  release_label.set_markup("<a href='https://github.com/NVIDIA/data-science-stack/releases'>Release notes</a>")
  release_label.show()
  dialog.get_content_area().add(release_label)

  dialog.set_position(gtk.WindowPosition.CENTER)
  dialog.set_modal(False)
  dialog.show()
  GLib.idle_add(winraise, title)

  response = dialog.run()
  if response == gtk.ResponseType.CANCEL or response == gtk.ResponseType.DELETE_EVENT:
    LOG.info("the user chose to cancel the upgrade") 
    dialog.destroy()
    return

  LOG.info("do_upgrade confirmed")
  dialog.set_label("Upgrade in progress")
  dialog.button2.hide()
  dialog.set_cmd(VersionChecker.PIP_NVDSW_UPGRADE_CMD)
  response = dialog.run()

  if response == gtk.ResponseType.CANCEL:
    LOG.debug("user chose to cancel the upgrade while it was running")
    dialog.destroy()
    return
  if response == gtk.ResponseType.DELETE_EVENT:
    LOG.debug("user chose to close the dialog while it was running")
    dialog.destroy()
    return

  if response == gtk.ResponseType.NONE:
    LOG.debug("upgrade completed normally")

  out = dialog.get_cmd_out()
#  if out is not None:
#    out = out.decode('utf-8')
  err = dialog.get_cmd_err()
#  if err is not None:
#    err = err.decode('utf-8')

  rc = dialog.get_cmd_rc()
  if rc == 0:
      LOG.info("Upgrade successful")
      if out is not None:
        LOG.debug("stdout: " + out)
      if err is not None:
        LOG.debug("stderr: " + err) 
      ALREADY_UPGRADED = True  
      dialog.destroy()     
      do_restart(m)
      # if we are here, the user did not want to restart yet. so, we just update the menu and chill
      GLib.idle_add(update_sw_menu_client_item, sw_menu_client, "restart")
      

  else:
      LOG.error("upgrade failed with rc: " + str(rc))
      LOG.error("stdout: " + out)
      LOG.error("stderr: " + err)
      dialog.set_label("Upgrade failed, please see logs")
      dialog.set_cmd(None)
      dialog.button1.hide() # the cancel button we don't need
      # dialog.button2 = dialog.add_button(gtk.STOCK_OK, gtk.ResponseType.OK)
      dialog.button2.show()
      dialog.run()
      dialog.destroy()
      return

def do_restart(m):
  title = "nvdsw restart"
  dialog = PayloadDialog(title = title, label = None, cmd = None)
  dialog.set_label("Restart Client now?")
  dialog.set_icon_from_file(ICON_DEFAULT)

  dialog.set_position(gtk.WindowPosition.CENTER)
  dialog.show()
  GLib.idle_add(winraise, title)

  response = dialog.run()
  if response == gtk.ResponseType.CANCEL or response == gtk.ResponseType.DELETE_EVENT:
    LOG.info("the user chose not to restart") 
    dialog.destroy()
    return

  LOG.info("do_restart confirmed")
  dialog.set_label("Restart in progress")
  dialog.button2.hide()
  dialog.set_cmd(v.get_nvdswd_start_cmd())
  response = dialog.run()

  if response == gtk.ResponseType.CANCEL:
    LOG.debug("user chose to cancel the restart while it was running")
    dialog.destroy()
    return
  if response == gtk.ResponseType.DELETE_EVENT:
    LOG.debug("user chose to close the dialog while it was running")
    dialog.destroy()
    return

  if response == gtk.ResponseType.NONE:
    LOG.debug("restart completed normally")

  out = dialog.get_cmd_out()
#  if out is not None:
#    out = out.decode('utf-8')
  err = dialog.get_cmd_err()
#  if err is not None:
#    err = err.decode('utf-8')
  rc = dialog.get_cmd_rc()
  if rc == 0:
    LOG.info("the new instance is running so exiting")
    dialog.destroy()
    quit(m)
  else:
    LOG.error("Failed to launch. Please restart manually")
    dialog.set_label("Restart failed. Please try manually")
    dialog.set_cmd(None)
    dialog.button1.hide() # the cancel button we don't need
    dialog.button2.show() # the ok button we need
  #   dialog.button2 = dialog.add_button(gtk.STOCK_OK, gtk.ResponseType.OK)
    dialog.run()
    dialog.destroy()  


  if confirm_upgrade():
    LOG.info("do_upgrade confirmed")
    out,err, rc = v.update_nvdsw()
    if rc == 0:
      LOG.info("upgrade successful")
      LOG.debug("stdout: " + out)
      LOG.debug("stderr: " + err) 
      ALREADY_UPGRADED = True       
      do_restart(m)
      # if we are here, the user did not want to restart yet. so, we just update the menu and chill
      GLib.idle_add(update_sw_menu_client_item, sw_menu_client, "Restart Client")

    else:
      LOG.error("upgrade failed with rc: " + str(rc))
      LOG.error("stdout: " + out)
      LOG.error("stderr: " + err)
  else:
    LOG.info("the user chose to cancel the upgrade")    


def warn_couldnt_restart(*args):
    dialog = gtk.MessageDialog(None, 0, gtk.MessageType.WARNING,
        gtk.ButtonsType.OK, "Please restart the client manually")

    title = "nvdsw failed to restart"
    dialog.set_title(title)
    dialog.format_secondary_text("Upgrading to " + v.remote[APP_ID] + " failed")
    dialog.set_icon_from_file(ICON_DEFAULT)

    dialog.set_position(gtk.WindowPosition.CENTER)
    dialog.show()
    GLib.idle_add(winraise, title)

    response = dialog.run()
    dialog.destroy()
    return response == gtk.ResponseType.OK    


def confirm_upgrade(*args):
    dialog = gtk.MessageDialog(None, 0, gtk.MessageType.WARNING,
        gtk.ButtonsType.OK_CANCEL, "Upgrading to " + v.remote[APP_ID])
    title = "nvdsw upgrade"
    dialog.set_title(title)
#    dialog.set_logo(icon)
    dialog.set_icon_from_file(ICON_DEFAULT)
    dialog.format_secondary_text("Are you sure?")

    dialog.set_position(gtk.WindowPosition.CENTER)
    dialog.show()
    GLib.idle_add(winraise, title)
    
    response = dialog.run()
    dialog.destroy()
    return response == gtk.ResponseType.OK  



def confirm_restart(*args):
    title = "nvdsw restart"
    dialog = gtk.MessageDialog(None, 0, gtk.MessageType.INFO,
        gtk.ButtonsType.OK_CANCEL, "Upgrade successful")
    dialog.set_title(title)
    dialog.set_icon_from_file(ICON_DEFAULT)
#    about.set_logo(icon)
    dialog.format_secondary_text("Would you like to restart now?")

    dialog.set_position(gtk.WindowPosition.CENTER)
    dialog.show()
    GLib.idle_add(winraise, title)
    
    response = dialog.run()
    dialog.destroy()
    return response == gtk.ResponseType.OK 

def do_forced_ver_check(m):
  global NVDSW_UP_TO_DATE
  title = "nvdsw version check"
  dialog = PayloadDialog(title = title, label = None, cmd = None)
  dialog.set_label("Check for updates?")
  dialog.set_icon_from_file(ICON_DEFAULT)

  dialog.set_position(gtk.WindowPosition.CENTER)
  dialog.set_modal(False)
  dialog.show()
  GLib.idle_add(winraise, title)

  response = dialog.run()
  if response == gtk.ResponseType.CANCEL or response == gtk.ResponseType.DELETE_EVENT:
    LOG.info("the user canceled a forced version check") 
    dialog.destroy()
    return

  dialog.set_label("Checking for updates")
  # dialog.button2.destroy()
#  dialog.button2.hide()
  dialog.destroy_ok_button()
  dialog.set_cmd(VersionChecker.PIP_VER_CHECK_CMD)
  response = dialog.run()

  if response == gtk.ResponseType.CANCEL:
    LOG.debug("user chose to cancel the workload while it was running")
    dialog.destroy()
    return
  if response == gtk.ResponseType.DELETE_EVENT:
    LOG.debug("user chose to close the dialog")
    dialog.destroy()
    return

  if response == gtk.ResponseType.NONE:
    LOG.debug("workload completed normally")

  out = dialog.get_cmd_out()
  err = dialog.get_cmd_err()
  if err is not None:
    LOG.debug(" err: " +  err)
#    LOG.debug(" err: " +  err.decode('utf-8'))
#   LOG.debug("pip out: " + out.decode('utf-8') + " err: " +  err.decode('utf-8'))
  new_ver = check_ver_dyn(v, out)
  if new_ver is not None:
    LOG.warning("new version detected: " + new_ver)
    NVDSW_UP_TO_DATE = False
    indicator.set_icon(ICON_WARNING)
    GLib.idle_add(update_sw_menu_client_item, sw_menu_client, "upgrade")
#       notify_upgrade()
    
  else:
    NVDSW_UP_TO_DATE = True 
    dialog.set_label("No upgrades available")
    dialog.set_cmd(None)
    # dialog.button1.destroy() # the cancel button we don't need
    # dialog.button1.hide()
    dialog.destroy_cancel_button()
    dialog.button2 = dialog.add_button(gtk.STOCK_OK, gtk.ResponseType.OK)
    #dialog.button2.show()
    dialog.run()
    dialog.destroy()
    return
#    show_noupgrades()

  # upgrade
  dialog.destroy()
  do_upgrade(m)

def check_ver_dyn(versions, out):  
    LOG.info('version check running')
    versions.parse_pip_output(out)
    if APP_ID in versions.remote:
      if semver.compare(nvdsw.__version__, versions.remote[APP_ID]) >=0:
        LOG.info("up to date: local: " + nvdsw.__version__ + ", remote: " + versions.remote[APP_ID])
        return None
      else:
        LOG.info("NOT up to date: local: " + nvdsw.__version__ + ", remote: " + versions.remote[APP_ID])
        return versions.remote[APP_ID]
    else:
      LOG.info(APP_ID + ' not in list of obsolete packages')
      return None
        

def show_dialog(type, title, sec_txt, btn_type, primary_txt, buttons):
#   app = gtk.Application()
  dialog = gtk.MessageDialog(None, 0, type, btn_type, primary_txt)
#  dialog = gtk.MessageDialog(application = app, transient_for = none, 0, type, btn_type, primary_txt)
  dialog.set_title(title)
  dialog.format_secondary_markup(sec_txt)
  dialog.set_icon_from_file(ICON_DEFAULT)
  if buttons is not None:
    for k,v in buttons.items():
      dialog.add_buttons(k,v)

  dialog.set_position(gtk.WindowPosition.CENTER)
  dialog.show()
  GLib.idle_add(winraise, title)
  response = dialog.run()
  dialog.destroy()
  return response == gtk.ResponseType.OK  


def show_launch_dialog(title, description, license, ports, volumes, browser, gpus, icon_file, settings):
  dialog = CLaunchDialog(
        parent = None,
        title = title, 
        description = description,
        license_url = license,
        ports = ports,
        volumes = volumes,
        browser = browser,
        gpus = gpus,
        icon_file = icon_file,
        settings = settings
  ) 
  
  dialog.set_position(gtk.WindowPosition.CENTER)
  dialog.show()
  GLib.idle_add(winraise, title)
  rc = dialog.run()
  attrs = dialog.get_attrs()
  dialog.destroy()

  return rc == gtk.ResponseType.OK, attrs

def show_status_dialog(title, description, cstatus, cattrs, browser, gpunames, icon_file):
  dialog = CStatusDialog(
        title = title, 
        description = description,
        cstatus = cstatus,
        cattrs = cattrs, 
        browser = browser,
        gpunames = gpunames,
        icon_file = icon_file
  ) 
  
  dialog.set_position(gtk.WindowPosition.CENTER)
  dialog.show()
  GLib.idle_add(winraise, title)
  rc = dialog.run()
  dialog.destroy()

  return rc == gtk.ResponseType.OK


def show_info_dialog(type, title, sec_txt, btn_type, primary_txt, license_url):
  dialog = gtk.MessageDialog(None, 0, type,
        btn_type, primary_txt)
  dialog.set_title(title)
  dialog.format_secondary_text(sec_txt)
  dialog.set_icon_from_file(ICON_DEFAULT)
  label = gtk.Label()
  label.set_markup('By launching, you accept the <a href="' + license_url + '">License Agreement</a>')
  label.show()
  vbox = dialog.get_message_area()
  vbox.set_spacing(4)
  vbox.pack_end(label, True, True, 0)

  dialog.set_position(gtk.WindowPosition.CENTER)
  dialog.show()
  GLib.idle_add(winraise, title)
  response = dialog.run()
  dialog.destroy()
  return response == gtk.ResponseType.OK   

def do_about(_):
  global about
  winname = 'About NVIDIA Data Science Workbench'
  
  # cleanup
  if about is not None:
    about.destroy()
    about = None

  about = gtk.AboutDialog()
  about.set_program_name("NVIDIA Data Science Workbench")
  about.set_title(winname)
  about.set_version("ver: " + nvdsw.__version__)
  about.set_icon_from_file(ICON_DEFAULT)
  about.set_resizable(True)
  icon = GdkPixbuf.Pixbuf.new_from_file(ICON_DEFAULT)
#  GdkPixbuf *example_logo = gdk_pixbuf_new_from_file ("./logo.png", NULL);
  about.set_logo(icon)
#  about.set_authors("Nvidia Corp.")
  about.set_copyright("(c) NVIDIA")
  about.set_comments("Driver: " + v.local['driver'] + "\nCUDA: " + v.local['cuda'] + "\nDocker: " + v.local['docker'] + "\nNVIDIA Container Toolkit: " + v.local['nvdocker'] + 
   "\nNGC CLI: " + v.local['ngc'] + "\nKaggle CLI: " + v.local['kaggle'] + "\nAWS CLI: " + v.local['aws'] + 
   "\nData Science Stack: " + v.local['dss'])
#  about.set_license_type(gtk.License.GPL_3_0)
  about.set_license(' '.join(LICENSE))
  # about.set_website(config['links']['Forums'])
  about.set_website('http://www.nvidia.com/workbench')
  about.set_website_label("Product Web Page")
  about.set_position(gtk.WindowPosition.CENTER)
  about.set_modal(False)
  
  about.show()
  
  GLib.idle_add(winraise, winname)

#   about.run()
 #  about.destroy()
 #  about = None


def quit_warn(m):
  if not show_dialog(gtk.MessageType.INFO, 'quit nvdsw', "All running containers will be removed", gtk.ButtonsType.OK_CANCEL,"Quitting", None):
    LOG.debug('the user chose not to quit')
    return

  quit(m)

def quit(_):
  LOG.debug("exiting")
  runner = DockerRunner(config)
#  subprocess.call(["xhost", "-local:"])
  subprocess.run(["xhost", "-local:"], stdout=subprocess.PIPE)
  runner.stop_all()
  global notifs
  for n in notifs:
    LOG.debug("removing " + n.props.summary +  " " + str(n.props.closed_reason))
    notifs.remove(n)

  notify.uninit()
  gtk.main_quit()
  LOG.debug("after gtk quit")
  sys.exit(0)


def async_docker_stoprm(m, runner, ydict):
  start_time = time.time()
  runner.stop(ydict)
  m._browser_port = None
  m._ports = None
  m._container_launched = False
  end_time = time.time()
  LOG.debug("the container was fully stopped with label " + ydict['container_label'] + " in " + str(end_time-start_time) + " s")

def async_docker_run(m, runner, ydict, attrs):
  if runner.run(ydict, attrs):
    start_time = time.time()
    LOG.debug("the container successfully launched... now checking ports")
#    if ydict['browser'] == 'y':
    if attrs['browser'] == True:
      c = runner.running_cs[ydict['container_label']]
      p = c.attrs['NetworkSettings']['Ports']
      LOG.debug("network settings of the new container: " + str(p))
      # we used to be mapping the first listed port 
      # browser_port = list(ydict['ports'].keys())[0]
      browser_port = list(attrs['ports'].keys())[0]
#      browser_port = ydict['browser_port']
      LOG.debug("the internal port is: " + browser_port)
      # we are assuming that these containers have only one port exposed; or if the have multiple, it is the first one listed that is mapped to the browser. So,
      # >>> c.attrs['NetworkSettings']['Ports']
      # {'6006/tcp': None, '6064/tcp': None, '8888/tcp': [{'HostIp': '0.0.0.0', 'HostPort': '49154'}]}    
      bp = p[browser_port][0]['HostPort']
      m._ports = {}
      for pk in p.keys():
        pv = p[pk]
        if pv is not None:
          m._ports[pk] = pv[0]['HostIp'] + ':' + pv[0]['HostPort']

      LOG.debug("docker assigned random port " + bp)
      m._volumes = c.attrs['Mounts']
      # the runner has made sure the container is up. But, is the port ready?
 #     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      ntries = 0
      clen = 0
#      while s.connect_ex(("127.0.0.1", int(bp))) != 0:
#        time.sleep(0.1)
#        ntries = ntries + 1
#        if ntries > 200:
#          raise Exception("timed out while waiting for container port to become available")
#      s.close()
      while clen == 0:
        try:
          with urllib.request.urlopen("http://localhost:" + bp + "/lab") as response:
            html = response.read()
            clen = len(html)
            if clen > 100:
              break
        except Exception:
          LOG.debug("connection refused")
        ntries = ntries + 1
        if ntries > 200:
          break
        time.sleep(0.1)

      if clen == 0:
        # the container came up, but the port is not working.. hmm
        LOG.error("launched container, but the port never became available")
        show_dialog(gtk.MessageType.ERROR, 'nvdsw docker start error', "docker container failed to start. Please see logs", gtk.ButtonsType.OK,"Launch Error", None)
        m._container_launched = False
        m._browser_port = None
        m.set_active(False)  
        # clean up
        runner.stop(ydict)   
        return   

      open_url(m, "http://localhost:" + bp + "/lab")
      m._browser_port = bp
    m._container_launched = True
    end_time = time.time()
    LOG.debug("the container is fully running with label " + ydict['container_label'] + " in " + str(end_time-start_time) + " s")
    
  else:
    LOG.error("could not launch container")
    show_dialog(gtk.MessageType.ERROR, 'nvdsw docker start error', "docker container failed to start. Please see logs", gtk.ButtonsType.OK,"Launch Error", None)
    m._container_launched = False
    m._browser_port = None
    m.set_active(False)

def launch_rt(m):
  global launcher_win
  LOG.debug("launch_rt clicked")

  
  title = 'The Launcher'
  # cleanup
  if launcher_win is not None:
    launcher_win.destroy()
    launcher_win = None

  launcher_win = RTWindow(title = title, config = config, icon_file = ICON_DEFAULT, settings = settings, 
    nvaie_rt = nvaie_rt, local_rt = local_rt, gpus = GPUs, icon_default = ICON_DEFAULT)
  launcher_win.set_position(gtk.WindowPosition.CENTER)
  launcher_win.show_all()
  GLib.idle_add(winraise, title)

  



def do_docker(m, conf, ydict, settings):
  runner = DockerRunner(conf)
  if m.get_active():
    if m._container_launched: # already running?
      LOG.debug("active clicked but the container is already launched")
      return

# make sure vars are named the same way as in ydict
# add gpus too
    if DISPLAY_CONTAINER_INFO:
#       if not show_info_dialog(gtk.MessageType.INFO, 'nvdsw start ' + ydict['name'], ydict['description'], gtk.ButtonsType.OK_CANCEL,"Launching " + ydict['name'], ydict['license_url']):
      rc, attrs = show_launch_dialog(
          title = 'nvdsw ' + ydict['name'] + " launch",
          description = ydict['description'],
          license = ydict['license_url'],
          ports = ydict['ports'],
          volumes = ydict['volumes'],
          browser = ydict['browser'],
          gpus = GPUs,
          icon_file = ICON_DEFAULT,
          settings = settings
      )

      if not rc:
        LOG.debug('the user chose not to launch')
        m._container_launched = False
        m.set_active(False)
        return
    # need to merge with the fetched params here.. 
    GLib.idle_add(async_docker_run, m, runner, ydict, attrs)

  else:
    if not m._container_launched: # already not running?
      LOG.debug("de-activate clicked but the container is not running")
      return
    vstr = ""
    if hasattr(m, '_volumes') and m._volumes is not None:
      # m._volumes = c.attr['Mounts']
      # [{'Type': 'bind', 'Source': '/home/dima/data', 'Destination': '/workspace/data', 'Mode': 'rw', 'RW': True, 'Propagation': 'rprivate'}]
      for v in m._volumes:
        if v['Type'] != 'bind':
          continue

        if vstr == "":
          vstr = "Mounted volumes:\n"
        vstr = vstr + v['Destination'] + "\t" + v['Source'] + "\n"
    pstr = "" 
    if hasattr(m, '_ports') and m._ports is not None:
      for pk in m._ports.keys():
        pv = m._ports[pk]
        # 0.0.0.0:49154
        if pstr == "":
          pstr = "Exposed Ports:\n"
        pstr = pstr + pk + "\t" + "<a href = 'http://localhost:" + pv.split(':')[1] + "'>" + pv + "</a>" + "\n"

    browser = True
    if m._browser_port is None: 
      browser = False

    c = runner.running_cs[ydict['container_label']]
    c.reload()
#    cs = c.status
#    cattrs = c.attrs
#    cdiag = CStatusDialog(title = 'nvdsw ' + ydict['name'], description = ydict['description'], cstatus = c.status, cattrs = cattrs, buttons = buttons)
#    cdiag.show_all()
#    cdiag.run()
    # if not cdiag.run() == gtk.ResponseType.OK:
    
#    if not show_dialog(gtk.MessageType.INFO, 'nvdsw stop ' + ydict['name'], pstr + vstr, gtk.ButtonsType.NONE, ydict['name'] + " is running", buttons):
    if not show_status_dialog(
      title = 'nvdsw ' + ydict['name'] + " stop", 
      description = ydict['description'], 
      cstatus = c.status, 
      cattrs = c.attrs, 
      browser = browser, gpunames = GPUs, icon_file = ICON_DEFAULT):
      LOG.debug('the user chose not to stop')
      m.set_active(True)
      return
    GLib.idle_add(async_docker_stoprm, m, runner, ydict)

def build_menu(config, ymenus, settings):
    global newest_item_timestamp
    global NVDSW_MENU_ITEM_ACTION_HANDLER_ID
    global DSS_MENU_ITEM_ACTION_HANDLER_ID
    global img_pull_queue
    runner = DockerRunner(config)


    menu = gtk.Menu()

    if settings.get()['Experimental']['LAUNCHER_ENABLED']:
      item = make_label_img('Launcher', 'LAUNCHER')
      item.connect('activate', launch_rt)
      menu.append(item)

    item = gtk.MenuItem.new_with_label('Tools' )
    menu.append(item)

    tools_menu = gtk.Menu.new()
    item.set_submenu(tools_menu)

    

    if not settings.get()['Experimental']['LAUNCHER_ENABLED']:
      # local items
      mi_local = gtk.MenuItem.new_with_label(' Local')
      tools_menu.append(mi_local)
      # the tools menu has local submenu if the launcher is not enabled
      local_menu = gtk.Menu.new()
      mi_local.set_submenu(local_menu)

      # remote items only if nvaie is enabled
      if settings.get()['Experimental']['NVAIE_ENABLED']:
        mi_remote = gtk.MenuItem.new_with_label(' Remote')
        m = gtk.Menu.new()
        mi_remote.set_submenu(m)
        mi_nvaie = make_label_img('   NVIDIA AI Enterprise', 'NVAIE')
        mi_nvaie.connect('activate', launch_rt)
        m.append(mi_nvaie)
        tools_menu.append(mi_remote)

    
    ji = gtk.MenuItem.new_with_label('  Jupyter Lab')
    if not settings.get()['Experimental']['LAUNCHER_ENABLED']:
      local_menu.append(ji)
    else:
      LOG.debug('temporarily disabling the jupyter menu when the launcher is enabled')
#       tools_menu.append(ji)

    

    jupyters = ymenus['jupyter']
    jm = gtk.Menu.new()
    
    for j in jupyters:

      if config['MAIN']['REMOVE_CONTAINERS_ON_STARTUP'] == 'True' and not settings.get()['Experimental']['LAUNCHER_ENABLED']:
#         runner.remove_container_if_exists(j['container_label'])
        runner.remove_container_by_label(j['container_label'])

      # For now, only handle the freshest tag..
      latest_tag = j['tags'][0]
      
      if runner.image_exists_locally(j['image'] + ':' + latest_tag):
        i = gtk.CheckMenuItem(label = '    ' + j['name'])
        i._container_launched = False
        i.connect('activate', do_docker, config, j, settings)
      else:
        i = gtk.MenuItem(label = '    ' + j['name'] + " [pulling]")
        fj = yaml.dump(j)
        img_pull_queue.put({i,fj})
      jm.append(i)


    ji.set_submenu(jm)
    
 
    item_code = gtk.MenuItem(label = '  VS Code')
    item_code.connect('activate', do_code)
    if not settings.get()['Experimental']['LAUNCHER_ENABLED']:
      local_menu.append(item_code)
    else:
      tools_menu.append(item_code)

    item_spyder = gtk.MenuItem(label = '  Spyder')
    item_spyder.connect('activate', do_spyder)

    if not settings.get()['Experimental']['LAUNCHER_ENABLED']:
      local_menu.append(item_spyder)
    else:
      tools_menu.append(item_spyder)  


    cli_menu_item = gtk.MenuItem(label = '  CLI')
    if not settings.get()['Experimental']['LAUNCHER_ENABLED']:
      local_menu.append(cli_menu_item)
    else:
      tools_menu.append(cli_menu_item) 

    cli_menu = gtk.Menu.new()
    cli_menu_item.set_submenu(cli_menu)
    

    item_dss_cli = gtk.MenuItem(label = '  DSS')
    item_dss_cli.connect('activate', do_dss_cli)
    cli_menu.append(item_dss_cli)

    item_ngc_cli = gtk.MenuItem(label = '  NGC')
    item_ngc_cli.connect('activate', do_ngc_cli)
    cli_menu.append(item_ngc_cli)

    item_kaggle_cli = gtk.MenuItem(label = '  Kaggle')
    item_kaggle_cli.connect('activate', do_kaggle_cli)    
    cli_menu.append(item_kaggle_cli)

    item_aws_cli = gtk.MenuItem(label = '  AWS')
    item_aws_cli.connect('activate', do_aws_cli_wrapper, runner)    
    cli_menu.append(item_aws_cli)    

#  #  m.append(cli_menu)
    
    item = gtk.MenuItem.new_with_label('Demos' )
#     item = gtk.MenuItem()
#     add_label_img(item, 'Demos', 'SETTINGS')
    m = gtk.Menu.new()
    demos = ymenus['demos']
    for j in demos:
      # For now, only handle the freshest tag..
      latest_tag = j['tags'][0]
      if runner.image_exists_locally(j['image'] + ':' + latest_tag):
        i = gtk.CheckMenuItem(label = '  ' + j['name'])
        i._container_launched = False
        i.connect('activate', do_docker, config, j)
      else:
        i = gtk.MenuItem(label = '  ' + j['name'] + " [pulling]")
        fj = yaml.dump(j)
        img_pull_queue.put({i,fj})
      m.append(i)




    item.set_submenu(m)

    if not settings.get()['Experimental']['LAUNCHER_ENABLED']:
      menu.append(item)
    else:
      LOG.debug('temporarily disabling the demo menu since the launcher is enabled')


#     menu.append(gtk.SeparatorMenuItem())
    item = gtk.MenuItem.new_with_label('Links' )
    m = gtk.Menu.new()

    for name in config['links']:
      i = gtk.MenuItem.new_with_label(' ' + name)
      u = config['links'][name]
      i.connect('activate', open_url, u)
      m.append(i)

    item.set_submenu(m)
    menu.append(item)

    menu.append(gtk.SeparatorMenuItem())
# news_menu is defined globally
    item = gtk.MenuItem.new_with_label('News' )


# news_menu is defined globally
    item.set_submenu(news_menu)
    menu.append(item)

    item = gtk.MenuItem.new_with_label('Hardware')
    m1 = gtk.Menu.new()
    item1 = gtk.MenuItem.new_with_label(' GPU (' + str(len(GPUs)) + ')' )
    m = gtk.Menu.new()
    for g in GPUs:
      i = gtk.MenuItem.new_with_label('  ' + g)
      m.append(i)

    item1.set_submenu(m)
    m1.append(item1)
    item.set_submenu(m1)
    menu.append(item)

#    menu.append(gtk.SeparatorMenuItem())
    item = gtk.MenuItem.new_with_label('Updates')
#     item = make_label_img('Updates', 'ABOUT')
    sw_menu = gtk.Menu.new()

    # sw_menu_client is externally defined
    if NVDSW_UP_TO_DATE:
#      sw_menu_client = gtk.MenuItem.new_with_label(' DS Workbench: '+ nvdsW.__version__)
#       sw_menu_client.set_label(' nvdsw: '+ nvdsw.__version__)
      sw_menu_client = make_label_img(' nvdsw: '+ nvdsw.__version__, 'SYNC')
      NVDSW_MENU_ITEM_ACTION_HANDLER_ID = sw_menu_client.connect('activate', do_forced_ver_check)
    else:
#      sw_menu_client = gtk.MenuItem.new_with_label(' Upgrade Client to: '+ v.remote[APP_ID])
      sw_menu_client.set_label(' Upgrade nvdsw to: '+ v.remote[APP_ID])
      NVDSW_MENU_ITEM_ACTION_HANDLER_ID = sw_menu_client.connect('activate', do_upgrade)
    sw_menu.append(sw_menu_client)

    # sw_menu_stack is externally defined
    # there is no need to check for the latest remote DSS version in a loop or on demand because we read it from the config file
    if DSS_UP_TO_DATE:
#      sw_menu_stack = gtk.MenuItem.new_with_label(' DS Stack: '+ v.local['dss'])
      sw_menu_stack.set_label(' Stack: '+ v.local['dss'] + ' [latest]')
      # disable this check. we want to control this by the version of the client.
#      DSS_MENU_ITEM_ACTION_HANDLER_ID = i.connect('activate', do_forced_ver_check_dss)
    else:
#      sw_menu_stack = gtk.MenuItem.new_with_label(' Upgrade Stack to: '+ LATEST_DSS_VER)
      sw_menu_stack.set_label(' Upgrade Stack to: '+ LATEST_DSS_VER)
      DSS_MENU_ITEM_ACTION_HANDLER_ID = sw_menu_stack.connect('activate', do_upgrade_dss)  
    sw_menu.append(sw_menu_stack)

    item.set_submenu(sw_menu)
    menu.append(item)

  #   i = gtk.ImageMenuItem.new_with_label('About')
#     i = gtk.MenuItem()
#     add_label_img(i, 'About', 'ABOUT')
    i = make_label_img('About', 'ABOUT')
    i.connect('activate', do_about)
    menu.append(i)

    menu.append(gtk.SeparatorMenuItem())
#     item_prefs = gtk.MenuItem.new_with_label('Settings')
    item_prefs = gtk.MenuItem()

# D.R. this madness below documents attempts to add icons to menu items.
# we know from the ubuntu menu items that this could be done
# However, with the Indicator library, the icons only show on the far right AND only if the menu item is not a submenu.


#     item_prefs.get_settings().set_property('gtk-menu-images', True)
#    print(settings.get_property('gtk-menu-images'))
#    settings.set_property('gtk-menu-images', True)
#     LOG.debug("settings: " + item_prefs.get_settings('gtk-menu-images'))
#     b = gtk.Box.new(orientation = gtk.Orientation.HORIZONTAL, spacing = 10)
#     fname = os.path.abspath(PKG_DIR + "/" + config['icons']['SETTINGS'])
#     img = load_img(fname,16,16)
#    img = gtk.Image.new_from_icon_name('preferences-desktop', gtk.IconSize.MENU)
#     LOG.debug('icon fname: ' + fname)
#     b.add(img)
#     b.add(gtk.Label(label = 'Settings'))
#    item_prefs.add(b)
#    b1.pack_start(img, True, True, 0)
#     b.pack_start(img, True, True, 0)
#     b.pack_start(img, True, True, 0)
#     b.pack_start(img, True, True, 0)
#    b1.pack_end(gtk.Label(label = 'dd'), False, False, 0)
#    b1.pack_start(gtk.Label(label = 'dd11'), False, False, 0)
#    b1.pack_end(gtk.Label(label = 'Settifngs'), False, False, 0)
#     b.pack_start(img, True, True, 0)
#     b.pack_end(img, True, True, 0)
#     b.pack_end(gtk.Label(label = 'Sengs'), True, True, 0)
#     item_prefs.add(b)
   
#    item_prefs.show_all()


#     item_prefs = gtk.ImageMenuItem()
#     item_prefs.set_image(img)
#    item_prefs.set_label(label = 'Settings')
#    item_prefs.set_always_show_image(True)

    add_label_img(item_prefs, 'Settings', 'SETTINGS')
    item_prefs.connect('activate', do_prefs)
    menu.append(item_prefs)

  #   item_quit = gtk.MenuItem.new_with_label('Quit')

    item_quit = gtk.ImageMenuItem()
    item_quit.set_label(label = 'Quit')
    image = gtk.Image.new_from_icon_name('application-exit', gtk.IconSize.MENU)
    item_quit.set_image(image)
    item_quit.set_always_show_image(True)


    item_quit.connect('activate', quit_warn)
    menu.append(item_quit)

    menu.show_all()
    return menu    


def notify_upgrade_dss():


    indicator.set_icon(ICON_WARNING)


    if not settings.get()['General']['NOTIFY_DISABLE']:
      warning_dss.update("DS Stack version " + LATEST_DSS_VER + " available")
      warning_dss.add_action('default', 'Action', do_notify_upgrade_dss)
      warning_dss.show()
    else:
      LOG.debug('notifications off, not notifying about new DSS version')

def do_prefs(m):
  global prefs_win
  LOG.debug('do_prefs invoked')
  title = "nvdsw settings"
  
  # cleanup
  if prefs_win is not None:
    prefs_win.destroy()
    prefs_win = None

  prefs_win = SettingsWindow(title = title, config = config, settings = settings, icon_file = ICON_DEFAULT)
  prefs_win.set_position(gtk.WindowPosition.CENTER)
  prefs_win.show_all()
  GLib.idle_add(winraise, title)

def notify_upgrade():
    global ALREADY_NOTIFIED_TO_UPGRADE

    if ALREADY_NOTIFIED_TO_UPGRADE:
      return 

    indicator.set_icon(ICON_WARNING)

    if not settings.get()['General']['NOTIFY_DISABLE']:
      warning.update("Nvidia Data Science Workbench version " + v.remote[APP_ID] + " available")
      warning.add_action('default', 'Action', do_notify_upgrade)
      warning.show()
      ALREADY_NOTIFIED_TO_UPGRADE = True
    else:
      LOG.debug('notifications off, not notifying about upgrade')

def do_notify_upgrade(x,y):
  return do_upgrade(x)

def do_notify_upgrade_dss(x,y):
  return do_upgrade_dss(x)  

def action_open_url(a,b,c):
  global notifs
  # this notification will become invisible, so remove it
  notifs.remove(a)
  LOG.debug("length of remaining notifs: " + str(len(notifs)))
  open_url(b,c)


def make_label_img(label, img_str):
  item = gtk.ImageMenuItem()
  fname = os.path.abspath(PKG_DIR + "/" + config['icons'][img_str])
  img = load_img(fname,16,16)
  item.set_image(img)
  item.set_label(label = label)
  item.set_always_show_image(True)
  return item


def add_label_img(menu_item, label, img_str):
  menu_item.get_settings().set_property('gtk-menu-images', True)
  b = gtk.Box.new(orientation = gtk.Orientation.HORIZONTAL, spacing = 10)
  fname = os.path.abspath(PKG_DIR + "/" + config['icons'][img_str])
  img = load_img(fname,16,16)
  b.add(img)
  b.add(gtk.Label(label = label))
  menu_item.add(b)

# def do_notify_rss_item(title, desc, href):
#     global notifs
#     if settings.get()['General']['NOTIFY_DISABLE']:
#       LOG.debug('notifications off so not notifying on new rss item')
#       return

#     info = notify.Notification.new(title, None)
#     info.set_timeout(settings.get()['News']['NOTIFICATION_VISIBILITY_TIMEOUT'] * 1000)

#     info.add_action('default', 'Action', action_open_url, href)
# 
#     info.show()
#     notifs.append(info)

def do_notify_news_items(news_items):
    global notifs
    if settings.get()['General']['NOTIFY_DISABLE']:
      LOG.debug('notifications off so not notifying on new rss item')
      return

    for item in news_items:
      info = notify.Notification.new(item.get_title(), None)
      info.set_timeout(settings.get()['News']['NOTIFICATION_VISIBILITY_TIMEOUT'] * 1000)
      info.add_action('default', 'Action', action_open_url, item.get_href())
      info.show()
      notifs.append(info)    




def wait_event(queue, event):
    while True:
        queue.put(event.wait_event())


def clean_notifs():
  global notifs
  # do some cleaning just in case we have exceeded the limit that the desktop has and some have become invisible
  LOG.debug("clean notifs running.. notifs: " + str(len(notifs)))
  for n in notifs:
    if n.props.closed_reason > -1:
      LOG.debug("removing " + n.props.summary +  " " + str(n.props.closed_reason))
      notifs.remove(n)

def news_update_loop(n_menu):
  
  # simple number of our run
  run_num = 0
  # we have to pull the feed the first time we run.
  last_successful_pull_time = -1
  newsProcessor = NewsProcessor(settings)

  while True:
    # the idea of this loop is, the settings on the update frequency take immediate effect  
    # also, if the feed is stale and there are connectivity errors, we'll keep retrying quickly rather then sleep forever
    settings_pulled_ts = settings.get_lastupdated()
    clean_notifs()

    while time.time() - last_successful_pull_time < settings.get()['News']['FEED_UPDATE_INTERVAL'] or settings.get()['News']['FEED_UPDATE_INTERVAL'] == -1:
  #     LOG.debug('news update double loop sleeping for ' + str(DOUBLE_LOOP_SLEEP_INTERVAL))
      time.sleep(DOUBLE_LOOP_SLEEP_INTERVAL)
  #     LOG.debug('news update double loop waking up')
      if settings.get_lastupdated() > settings_pulled_ts:
          # in the future, need to be more granular
          LOG.debug("news update double loop: settings changes, re-pulling")
          # a little aggressive here.. close any gaps
          settings_pulled_ts = settings.get_lastupdated()
          break

    run_num = run_num + 1
    LOG.debug("updater run num " + str(run_num))

    current_items, new_items = newsProcessor.parseFeeds()
    if current_items is not None:
      last_successful_pull_time = time.time()
      GLib.idle_add(update_menu, n_menu, current_items) 
      if new_items is not None and len(new_items) > 0:
        do_notify_news_items(new_items)
    else:
      # let the double loop force a quick retry
      continue




# def news_update_loop(n_menu):
#     i1 = 0
#     # we'll overwrite it below
#     global newest_item_timestamp
#     
#  
#     while True:
# 
# 
#       start_sleep_time = time.time()    
#       while time.time() - start_sleep_time < settings.get()['News']['FEED_UPDATE_INTERVAL'] or settings.get()['News']['FEED_UPDATE_INTERVAL'] == -1:
#         LOG.debug('news update double loop sleeping for ' + str(DOUBLE_LOOP_SLEEP_INTERVAL))
#         time.sleep(DOUBLE_LOOP_SLEEP_INTERVAL)
#         LOG.debug('news update double loop waking up')
#   
# 
#       i1 = i1 + 1
#       LOG.debug("updater run " + str(i1))
#       try: 
#         feed = feedparser.parse(settings.get()['News']['RSS_FEED_URLS'][0])
#       except Exception:
#         LOG.warning("unable to parse feed")
#         exc_type, exc_value, exc_tb = sys.exc_info()
#         LOG.warning(traceback.format_exception(exc_type, exc_value, exc_tb)) 
#         continue

#       # we assume that the first item in the feed is the newest
#       pubdate = feed['entries'][0].published
#       pubDate = "-".join(pubdate.split()[1:5])
#       n0 = datetime.datetime.strptime(pubDate , "%d-%b-%Y-%H:%M:%S").timestamp()      
#       titles = []
#       hrefs = []
##       print(n)
##       print(newest_item_timestamp)
#       if n0 > newest_item_timestamp:
#         LOG.debug("new news items detected!")          
##       if True:
        
#         # the most recent item goes on top
#         for i in reversed(range(settings.get()['News']['MAX_DISPLAY_ITEMS'])):
#            pubdate = feed['entries'][0].published
#           pubDate = "-".join(pubdate.split()[1:5])
#           n = datetime.datetime.strptime(pubDate , "%d-%b-%Y-%H:%M:%S").timestamp()
#           if n > newest_item_timestamp:
#             titles.append(feed['entries'][i]['title'][:settings.get()['News']['MAX_ITEM_TITLE_LEN']])
##             description.append(feed['description'][i]['link'])
#             hrefs.append(feed['entries'][i]['link'])

#            time.sleep(2)

#         newest_item_timestamp = n0
#         LOG.debug("adding " + str(len(titles)) + " new items to menu")

        # notifications
        # the most recent item goes last (on top)
#         for i in range(len(titles) - settings.get()['News']['MAX_ITEM_NOTIFICATIONS'], len(titles)):
#             do_notify_rss_item(titles[i], None, hrefs[i])


#         GLib.idle_add(update_menu, n_menu, titles, hrefs)

#       clean_notifs()

def update_sw_menu_dss_item(dss_item, msg):
  global DSS_MENU_ITEM_ACTION_HANDLER_ID
  LOG.debug("update_sw_menu_dss_item is called with: " + msg)
  # there is only one operation here, the normal
  dss_item.set_label(msg)
  dss_item.disconnect(DSS_MENU_ITEM_ACTION_HANDLER_ID)

def update_sw_menu_client_item(nvdsw_item, msg):
  global NVDSW_MENU_ITEM_ACTION_HANDLER_ID
  LOG.debug("update_sw_menu_client_item is called with: " + msg)
  if msg == "upgrade":
    nvdsw_item.set_label(' Upgrade to: ' + v.remote[APP_ID])
    if NVDSW_MENU_ITEM_ACTION_HANDLER_ID is not None:
      nvdsw_item.disconnect(NVDSW_MENU_ITEM_ACTION_HANDLER_ID)
    NVDSW_MENU_ITEM_ACTION_HANDLER_ID = nvdsw_item.connect('activate', do_upgrade)
  else: # restart
    nvdsw_item.set_label(' Restart required')
    if NVDSW_MENU_ITEM_ACTION_HANDLER_ID is not None:
      nvdsw_item.disconnect(NVDSW_MENU_ITEM_ACTION_HANDLER_ID)
    NVDSW_MENU_ITEM_ACTION_HANDLER_ID = nvdsw_item.connect('activate', do_restart)


def update_menu(n_menu, newsItems):
  # just refresh everything
  for c in n_menu.get_children():
    n_menu.remove(c)

  for newsItem in newsItems:
    # the space below is an indent showing that these items are nested
    news_menu_item = gtk.MenuItem(label = ' ' + newsItem.get_title())
    news_menu_item.connect('activate', open_url, newsItem.get_href())
    news_menu_item.show()
    n_menu.append(news_menu_item)


# def update_menu(n_menu, titles, hrefs):
# 
#   for i in range(len(titles)):
#     item_news = gtk.MenuItem(label = ' ' + titles[i])
#     item_news.connect('activate', open_url, hrefs[i])
#     item_news.show()
#     #  upstream in reversed order
#     # we're pushing the existing elements down
##     n_menu.insert(item_news,i)
#     n_menu.append(item_news)
#   
#   # now we just need to remove elements at the end since we got too many
#   i=0
#   for c in n_menu.get_children():
#     if i >= settings.get()['News']['MAX_DISPLAY_ITEMS']:
#       n_menu.remove(c)
#     i = i + 1

##   n_menu.show_all()


# AppIndicator3 doesn't handle SIGINT, wire it up.
signal.signal(signal.SIGINT, signal.SIG_DFL)

notify.init(APP_ID)
warning = notify.Notification()
warning_dss = notify.Notification()


indicator = appindicator.Indicator.new(APP_ID, ICON_DEFAULT, appindicator.IndicatorCategory.SYSTEM_SERVICES)

indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
# indicator.set_menu(build_menu(config))


## if not DSS_UP_TO_DATE:
##   do_warning()

def ver_check_loop(versions):
  global NVDSW_UP_TO_DATE
  while True:
    new_ver = check_ver(versions)
    if new_ver is not None:
      LOG.warning("new version detected: " + new_ver)
      NVDSW_UP_TO_DATE = False
      GLib.idle_add(update_sw_menu_client_item, sw_menu_client, "upgrade")
      notify_upgrade()
    else:
      NVDSW_UP_TO_DATE = True
    start_sleep_time = time.time()

#     time.sleep(settings.get()['Updates']['VERSION_CHECK_INTERVAL'])
    
    while time.time() - start_sleep_time < settings.get()['Updates']['VERSION_CHECK_INTERVAL'] or settings.get()['Updates']['VERSION_CHECK_INTERVAL'] == -1:
      time.sleep(DOUBLE_LOOP_SLEEP_INTERVAL)
#       LOG.debug('ver check loop: VERSION_CHECK_INTERVAL: ' + str(settings.get()['Updates']['VERSION_CHECK_INTERVAL']))

    LOG.debug('ver check loop: waking up')
    if ALREADY_NOTIFIED_TO_UPGRADE:
      LOG.info("upgrade notification presented. the version check loop exits now..")
      break  

def img_pull_loop():
  global img_pull_queue
  runner = DockerRunner(config)
  img_retry_queue = queue.Queue()
  while True:

#     LOG.debug('img pull loop waking up')
    while True:
      try: 
        m, yj = img_pull_queue.get(block = False)
      except:
#        LOG.debug("img pull queue empty")
        break
      j = yaml.safe_load(yj)
      img_name = j['image']
      latest_tag = j['tags'][0]
      LOG.info("img_pull_thread starting to pull " + img_name + ':' + latest_tag)
#       runner.pull_img(img_name)
      dockerpath = DOCKERFILE_DIR + '/' + j['image']
      dockerfile = 'Dockerfile' + '.' + latest_tag
      rc = runner.build_img(img_name + ':' + latest_tag, dockerpath, dockerfile)
      if rc: 
        LOG.info("img_pull_thread finished pulling " + img_name)
        GLib.idle_add(enable_pulled_menu_item, m, j)
      else:
        LOG.warning("img_pull did not succeed and will retry")
        img_retry_queue.put({m,yj})

#     LOG.debug('img pull loop sleeping for ' + str(IMG_CHECK_INTERVAL))
    time.sleep(IMG_CHECK_INTERVAL)

    # re-add the failed items, if any, into the pull queue.
    while True:
      try: 
        m, yj = img_retry_queue.get(block = False)
        img_pull_queue.put({m,yj})
      except:
        break
    
def enable_pulled_menu_item(menu_item, j):
  parent = menu_item.get_parent()
  i=0
  pos = None
  for c in parent.get_children():
    if c == menu_item:
      pos = i
      break
    i = i + 1

  if pos is None:
    LOG.error('unable to find menu item')
    return 

  parent.remove(menu_item)

  LOG.debug('inserting check menu item ' + j['name'] + ' at position ' + str(i))
  i = gtk.CheckMenuItem(label = '   ' + j['name'])
  i._container_launched = False
  i.connect('activate', do_docker, config, j)
  parent.insert(i, pos)
  i.show()
  
def check_ver(versions):  
    LOG.info('version check running')
    versions.check_pip_remote()
    if APP_ID in versions.remote:
      if semver.compare(nvdsw.__version__, versions.remote[APP_ID]) >=0:
        LOG.info("up to date: local: " + nvdsw.__version__ + ", remote: " + versions.remote[APP_ID])
        return None
      else:
        LOG.info("NOT up to date: local: " + nvdsw.__version__ + ", remote: " + versions.remote[APP_ID])
        return versions.remote[APP_ID]
    else:
      LOG.info(APP_ID + ' not in list of obsolete packages')
      return None

def load_img(img_file, width, height):
  pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(filename=img_file, width=width, height=height, preserve_aspect_ratio=True)
  return gtk.Image.new_from_pixbuf(pixbuf)


def main_with_path(script_dir):
  global SCRIPT_DIR
  SCRIPT_DIR = script_dir
  return main()

def main():
  global v
  global DSS_UP_TO_DATE
  LOG.info("in main.. script dir: " + SCRIPT_DIR)
  LOG.warn("allowing local users to access X.. this is for demos")
  # subprocess.call(["xhost", "local:"])
  subprocess.run(["xhost", "local:"], stdout=subprocess.PIPE)

  LOG.info("checking versions")
  v = VersionChecker(config, SCRIPT_DIR)
  v.check_local()

  if v.local['dss'] != "not found":
    if semver.compare(v.local['dss'],LATEST_DSS_VER) < 0:
      # likely ought to notify here with a link to the upgrade function. But, prevent nagging.
      DSS_UP_TO_DATE = False
      notify_upgrade_dss()

  try:
    os.stat(LICENSE_ACCEPTED_FILE)
    LOG.debug('license was previously accepted')
  except:
    LOG.debug('license was NOT previously accepted')
    license_str = ' '.join(LICENSE)
    comments = 'Please carefully review the terms of the End User License Agreement located in the License tab and then indicate your agreement by clicking below.\n\nTo exit, choose "I do not accept".'
    dialog = LicenseDialog(title = "Data Science Workbench", comments = comments, license_str = license_str, icon_file = ICON_DEFAULT)
    dialog.set_modal(True)
    response = dialog.run()
    if response == gtk.ResponseType.OK:
      LOG.debug("license accepted!")
      dialog.destroy()
      with open(LICENSE_ACCEPTED_FILE, 'a'):
        os.utime(LICENSE_ACCEPTED_FILE, None)

    else:
      LOG.warning("license not accepted, exiting")
      sys.exit(2)

  LOG.info("building menu: ")
  indicator.set_menu(build_menu(config, ymenus, settings))

  news_thread = threading.Thread(target=news_update_loop, args=[news_menu])

  news_thread.daemon = True
  news_thread.start()

  ver_thread = threading.Thread(target=ver_check_loop, args=[v])
  ver_thread.daemon = True
  ver_thread.start()

  if not settings.get()['Experimental']['LAUNCHER_ENABLED']:
    img_pull_thread = threading.Thread(target=img_pull_loop)
    img_pull_thread.daemon = True
    img_pull_thread.start()
  else:
    LOG.info('experimental launcher enabled; not starting the image pull thread')

  gtk.main()


if __name__ == '__main__':
  sys.exit(main())
