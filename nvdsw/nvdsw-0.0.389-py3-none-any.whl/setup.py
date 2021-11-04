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

import configparser
import logging
import sys
import os
import pathlib
import semver
import yaml
import shutil
import platform
import subprocess
import traceback

import uuid

from nvdsw.tools.versions import VersionChecker
from nvdsw.tools.runner import DockerRunner
from nvdsw.tools.settings_yaml import SettingsYaml
# from tools.versions import VersionChecker
# from tools.runner import DockerRunner

SCRIPT_DIR = ""
PKG_DIR = str(pathlib.Path(__file__).parent.absolute())
HOME_DIR = os.environ['HOME']

config = configparser.ConfigParser()
config.optionxform = str

lf = config.read(PKG_DIR + '/config/config.ini')
if len(lf) == 0:
  print("could not locate config file " + PKG_DIR + '/config/config.ini', file=sys.stderr)
  sys.exit(-1)

MIN_GPU_MEM = int(config['MAIN']['MIN_GPU_MEM'])
MIN_PYTHON_VER = config['MAIN']['MIN_PYTHON_VER']
if semver.compare(platform.python_version(),MIN_PYTHON_VER) < 0:
  print("You are using python " + platform.python_version() + ",but " + MIN_PYTHON_VER + " or newer is required")
  sys.exit(-1)

APP_ID = config['MAIN']['APP_ID']
APP_DIR = HOME_DIR + "/.config" + '/' + APP_ID 

try:
    os.stat(APP_DIR)
except:
    os.makedirs(APP_DIR)  

LOG_DIR = APP_DIR + '/' + config['MAIN']['LOG_DIR']
LOG_FILE = LOG_DIR + '/' + 'installer' + '.log'
LOG = logging.getLogger(APP_ID)
# LOG_FORMAT = config['MAIN']['LOG_FORMAT']
LOG_FORMAT = ('%(asctime)s - %(threadName)s - %(name)s - %(levelname)s - %(message)s')

SETUP_SUCCEEDED_FILE = APP_DIR + '/' + config['MAIN']['SETUP_SUCCEEDED_FILE']

UUID_FILE = APP_DIR + '/' + config['MAIN']['UUID_FILE']

DOCKERFILE_DIR = PKG_DIR + '/' + config['MAIN']['DOCKERFILE_DIR']

try:
    os.stat(LOG_DIR)
except:
    os.mkdir(LOG_DIR)  

# logger.setLevel(logging.DEBUG)

logging.basicConfig(filename = LOG_FILE, level=logging.DEBUG, format = LOG_FORMAT)

logFormatter = logging.Formatter(LOG_FORMAT)

# also log to stdout
consoleHandler = logging.StreamHandler(sys.stdout)
consoleHandler.setFormatter(logFormatter)
LOG.addHandler(consoleHandler)


menus_fname = PKG_DIR + "/" + config['MAIN']['MENUS_YAML']

    
try:
  ymenus = yaml.load(open(menus_fname, 'r'), Loader=yaml.SafeLoader)
except FileNotFoundError:
  LOG.error("menus file not found " + menus_fname)
  sys.exit(-1)


settings = SettingsYaml(PKG_DIR + "/" + config['MAIN']['USERSETTINGS_YAML'])
try:
  settings.load() 
except FileNotFoundError:
  LOG.error("settings file not found " + config['MAIN']['USERSETTINGS_YAML']) 
  sys.exit(-1)  

DOCKER_SOURCE_MOUNT_DIR = settings.get()['Containers']['DOCKER_SOURCE_MOUNT']
if not DOCKER_SOURCE_MOUNT_DIR.startswith('/'):
  DOCKER_SOURCE_MOUNT_DIR = os.environ['HOME'] + '/' + DOCKER_SOURCE_MOUNT_DIR
try:
  os.stat(DOCKER_SOURCE_MOUNT_DIR)
except:
  LOG.debug('creating docker source mount dir: ' + DOCKER_SOURCE_MOUNT_DIR)
  os.mkdir(DOCKER_SOURCE_MOUNT_DIR) 


def os_ok():
  d = {}
  with open("/etc/os-release") as f:
    for line in f:
      k,v = line.rstrip().split("=")
      d[k] = v.strip('"') 

  LOG.debug("detected OSNAME: " + d['NAME'] + " ver: " + d['VERSION_ID'])
  if d['NAME'] != 'Ubuntu':
    LOG.debug("unsupported OSNAME: " + d['NAME'])
    return False

  if d['VERSION_ID'] == '20.04' or d['VERSION_ID'] == '18.04':
    return True

  LOG.debug("unsupported OS ver: " + d['VERSION_ID'])
  return False

def i_am_headless():
  if '[installed' in subprocess.run(["/bin/sh", "-c", "apt list --installed ubuntu-desktop"], stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.decode('utf-8'):
    # expecting something like 'Listing...\nubuntu-desktop/focal-updates,now 1.450.2 amd64 [installed]\n'
    return False
  else:
    return True

def gpu_present():
  # EC2 g4dn.xlarge, Ubuntu 20.04, Tesla T4: 3D controller: NVIDIA Corporation TU104GL [Tesla T4] (rev a1)
  if subprocess.run(["/bin/sh", "-c", "lspci | grep -e 'VGA compatible controller: NVIDIA Corporation' -e '3D controller: NVIDIA Corporation'"], stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.decode('utf-8') == '':
    return False
  else:
    return True

def gpu_ok(min_gpu_mem):
  from pynvml import nvmlDeviceGetHandleByIndex, nvmlDeviceGetMemoryInfo, nvmlDeviceGetCount, nvmlInit
  nvmlInit()
  deviceCount = nvmlDeviceGetCount()
  if deviceCount < 1:
    LOG.error("GPU not found")
    return False

  LOG.debug("detected " + str(deviceCount) + " GPUs")

  for i in range(deviceCount):
    handle = nvmlDeviceGetHandleByIndex(i)
    mem = nvmlDeviceGetMemoryInfo(handle)
    LOG.debug("detected GPU with gpu mem: " + str(mem.total))
    if mem.total >= min_gpu_mem:
      return True

  return False

def image_exists_locally(img_name):
  LOG.debug('checking if image ' + img_name + ' exists locally')

  try:
    import docker
    client = docker.from_env()
    i = client.images.get(img_name)
    LOG.debug("the image is present locally")
    client.close()
    return True
  except docker.errors.ImageNotFound:
    LOG.info("image " + img_name + " is not present locally")  
    client.close()
    return False
  except Exception:
    LOG.warning("unable to connect to docker")
    exc_type, exc_value, exc_tb = sys.exc_info()
    LOG.warning(traceback.format_exception(exc_type, exc_value, exc_tb))
    client.close()
    return False

# def pull_containers():
def build_containers():
#   LOG.debug("pull containers starting")
  LOG.debug("build containers starting")
  LOG.debug("DOCKEFILE_DIR: " + DOCKERFILE_DIR)
  try:
    import docker
    client = docker.from_env()
  except:
#     LOG.warning("unable to import docker and therefore unable to pull containers")
    LOG.warning("unable to import docker and therefore unable to build containers")
    return False
  for i in ymenus['jupyter'] + ymenus['demos']:
#     if i['pull_on_setup'] == 'y':
    if i['build_on_setup'] == 'y':  
      for ver in i['versions']:
#        LOG.debug("processing ver: " + ver)
        if not image_exists_locally(i['image'] + ':' + ver):
#         LOG.info("pulling container: " + i['image'])
          LOG.info("building container: " + i['image'] + ':' + ver)
#         client.images.pull(i['image'])

#        sdf = os.listdir(DOCKERFILE_DIR  + '/' + i['image'])[0]
          LOG.debug("building: " + DOCKERFILE_DIR + '/' + i['image'] + ':' + ver)
          client.images.build(tag = i['image'] + ':' + ver, path = DOCKERFILE_DIR + '/' + i['image'], dockerfile = 'Dockerfile' + '.' + ver)
        else:
          LOG.info("image "+ i['image'] + ':' + ver + " already exists locally, not building")
  client.close()
#   LOG.debug("pull containers done")
  LOG.debug("pull containers done")
  return True

def build_dss_container_if_needed():
  LOG.debug("checking for the dss container")
  os.system(SCRIPT_DIR + '/bdssc.sh')
  if os.WEXITSTATUS != 0:
    LOG.error("build dss container failed")
    return False
  LOG.debug("dss container done")
  return True

def install_code():
  LOG.debug("install_code starting")
  CODE_EXEC = "/snap/bin/code"

  try:
    os.stat(CODE_EXEC)
  except:
    os.system("snap install code --classic")
    # it will return not 0 for whatever reason
    if os.WEXITSTATUS != 0:
      LOG.warning("code install rc:" + str(os.WEXITSTATUS))
      return True

  LOG.debug("install code done")
  return True

def install_autostart():
  LOG.debug("install_autostart starting")
  # need to copy nvdsw.desktop to ~/.config/autostart
  # and add this line: Exec=/home/dima/.config/nvdss/nvdss.py
  astart_dir = os.environ['HOME'] + "/.config/autostart"
  try:
    os.stat(astart_dir)
  except:
    os.mkdir(astart_dir)

  src_file = SCRIPT_DIR + '/nvdsw.desktop'
  tgt_file = astart_dir + '/nvdsw.desktop'
 
  try:
    shutil.copy(src_file, tgt_file) 
    LOG.info("installed autostart entry to " + astart_dir + '/nvdsw.desktop')
  except:
    LOG.error("could not copy " + src_file + " to " + tgt_file)
    return False
 
  with open(tgt_file, 'a') as f:  
    print("Exec=" + SCRIPT_DIR + '/nvdsw', file = f)
  LOG.debug("install_autostart done")  
  return True

def slz(ver_str):

  nl = []
  l = ver_str.split('.')
  for str in l:
    while str.startswith('0') and len(str) > 1:
      str = str[1:]
    nl.append(str)
  return '.'.join(nl)

def sverc(a,b):
  # if a version has fewer than three parts, assume the last one is 0
  if len(a.split('.')) < 3:
    a = a + '.0' 
  if len(b.split('.')) < 3:
    b = b + '.0'

  a = slz(a)
  b = slz(b)

  return semver.compare(a,b)

def install_ubuntu_pkgs(pkg_list):
  for pkg in pkg_list:
    LOG.info("attempting to install: " + pkg)
    str = 'dpkg -s ' + pkg + '>/dev/null 2>&1 ;if [ $? -ne 0 ];then sudo apt install -y ' + pkg + ';else echo ' + pkg + ' already installed;fi'
    #print(str)
    os.system(str)
  #  if os.WEXITSTATUS != 0:
  #    LOG.error("install ubuntu packages failed")
  #    return False
  LOG.info("installation complete: " + pkg)
  return True

def main_with_path(script_dir):
  global SCRIPT_DIR
  SCRIPT_DIR = script_dir
  return main()

def main():
  LOG.info("in main.. script dir: " + SCRIPT_DIR)
  try:
    os.stat(UUID_FILE)
    LOG.info("the uuid file was previously generated. Not going to overwrite it")
  except:
    LOG.debug("Generating UUID file")
    with open(UUID_FILE, "w") as uuidf:
      uuidf.write(str(uuid.uuid4()) + '\n')

#  try:
#    os.stat(SETUP_SUCCEEDED_FILE)
#    LOG.info("the setup was successfully completed previously, exiting")
#    print("the setup was already successfully run. Exiting")
#    sys.exit(0)
#  except:
#    LOG.debug("No previous successful setup run detected, proceeding")

  if not os_ok():
    LOG.error("OS not supported, unable to proceed")
    sys.exit(-1)

  if i_am_headless():
    LOG.error("unable to proceed on headless")
    sys.exit(-1)

  if not gpu_present():
    LOG.error("unable to proceed: GPU is not detected")
    sys.exit(-1)

  # this is a Ubuntu-specific hack, unfortunatately.. 
  # install_ubuntu_pkg(['gir1.2-appindicator3-0.1', 'code', 'curl', 'unzip'])
  # we need git so we can install the data science stack. the rest we don't care until after the dss is installed.
  pkgs = config['setup']['PACKAGES']
  if not install_ubuntu_pkgs(pkgs.split(' ')):
    LOG.error("unable to proceed")
    sys.exit(-1)

#  os.system('sudo apt install -y gir1.2-appindicator3-0.1')
  v = VersionChecker(config, SCRIPT_DIR)
  # 1. get all the versions of everything 
  v.check_local()
#  print(v.local)
#  v.check_remote()

  # need to watch out for the -y flag

  # we don't _need_ to install the data science stack if:
  # the driver is reasonably new and 
  # nvdocker is installed.
  # or, the dss is already the latest version
  
  # for now, let's just require DSS.
  # if v.local['driver'] != 'not found' and sverc(v.local['driver'], config['MAIN']['MIN_DRIVER_VERSION']) >=0 and \
  #     v.local['nvdocker'] != 'not found' or \
  if v.local['dss'] != 'not found' and sverc(v.local['dss'], config['MAIN']['LATEST_DSS_VERSION']) == 0:
    LOG.info("no need to install / update dss because driver is: " + v.local['driver'] + ", nvdocker is: " + v.local['nvdocker'] + ", dss is: " + v.local['dss'])
  else:
    LOG.info("need to install / update dss because driver is: " + v.local['driver'] + ", nvdocker is: " + v.local['nvdocker'] + ", dss is: " + v.local['dss']) 
#    os.system(os.environ['HOME']+"/.local/bin/iudss.sh")
    rc = os.system(SCRIPT_DIR + '/iudss.sh')
    if os.WEXITSTATUS(rc) == 0:
      LOG.info("The Data Science Stack installed successfully. Please reboot and re-run the installer.")
    else:
      LOG.warning("The Data Science Stack failed to install. Please inspect the logs and try again.")

    sys.exit(-1)
    # v.install_update_dss()
 
  # if we made it thus far, we can now use pynvml to query GPU[s]
  if not gpu_ok(MIN_GPU_MEM):
    LOG.error("unable to proceed: insufficient GPU capabilities")
    sys.exit(-1)


  if not install_code():
    LOG.error("unable to proceed")
    sys.exit(-1)


  LOG.info("installing autostart shortcut")
  if not install_autostart():
    LOG.error("unable to proceed")
    sys.exit(-1)
  
  # always install / update ngc cli
  LOG.info("installing / updating ngc cli")
  if not v.install_update_ngc():
    LOG.error("unable to proceed")
    sys.exit(-1)    
  LOG.info("ngc cli installed")


# these are now pre-reqs
#  LOG.info("installing / updating kaggle cli")
#  v.install_update_kaggle()

#  LOG.info("installing / updating repo2docker")
#  v.install_update_jupyter_repo2docker()


  
  if v.local['nvdocker'] != 'not found':
    LOG.info("installing / updating the aws cli")
    # commented out until we pip install
    # v.install_update_aws()
    DockerRunner(config).update_aws_cli()
    LOG.info("installing / updating docker containers")
#    pull_containers()
    if not settings.get()['Experimental']['LAUNCHER_ENABLED']:
      build_containers()
    else:
      LOG.info("new launcher enabled. Not pre-building containers.")

  # we are now pulling the dss container also
  #  build_dss_container_if_needed()
  else:
    LOG.info("installer cannot proceed until nvdocker is operational.")
    LOG.info("if you just installed the data science stack, please reboot and re-run the installer")
    sys.exit(-1)

  LOG.info("all done!")
  with open(SETUP_SUCCEEDED_FILE, 'a'):
        os.utime(SETUP_SUCCEEDED_FILE, None) 
# ------------------
  # 3. optionally, install desktop shortcuts
  # 4. optinally, install the background




if __name__ == '__main__':
  sys.exit(main())
