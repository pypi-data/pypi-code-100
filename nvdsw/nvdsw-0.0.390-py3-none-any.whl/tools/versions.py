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

import sys,os
import logging
import subprocess
import traceback
import shutil
import json
import time
from nvdsw.tools.hardware import HWStats
from nvdsw.tools.runner import DockerRunner


log = logging.getLogger('versions')



class VersionChecker:
  PIP_VER_CHECK_CMD = "pip3 list -o --format json"
  PIP_NVDSW_UPGRADE_CMD = "pip3 install -U nvdsw"
  
  def __init__(self, config, sc_dir):
    self.conf = config 
    self.local = {}
    self.remote = {}
    self.script_dir = sc_dir
    log.debug("in version checker.. passed script_dir is " + sc_dir)

  def check_local(self):
    self.check_driver_local()
    self.check_docker_local()
    self.check_nvdocker_local()
    self.check_cuda_local()
      
    self.check_ngc_cli_local()
    self.check_kaggle_cli_local()
    self.check_aws_cli_local()

    self.check_dss_local()
    self.check_jupyter_repo2docker_local()

  def check_driver_local(self):
    hwstats = HWStats(self.conf)
    self.local['driver'] = hwstats.get_driver_version()

  def check_cuda_local(self):
    CUDA_VER_JSON = self.conf['MAIN']['CUDA_VER_JSON']
    CUDA_VER_FILE = self.conf['MAIN']['CUDA_VER_FILE']

    try:
      with open(CUDA_VER_JSON) as f:
        data = json.load(f)
        self.local['cuda'] = data['cuda']['version']
        return
    except:
      log.warning(CUDA_VER_JSON  + " not found or could not be parsed") 
      self.local['cuda'] = "not found"

    try:
      with open(CUDA_VER_FILE) as f:
        s = f.readline()
        self.local['cuda'] = s.split()[2]
    except:
      log.warning(CUDA_VER_FILE  + " not found") 
      self.local['cuda'] = "not found"

  def check_ngc_cli_local(self):
    self.local['ngc'] = "not found"
    try:
      if self.script_dir is not None:
        self.local['ngc'] = subprocess.run([self.script_dir + "/ngc", "--version"], stdout=subprocess.PIPE).stdout.split()[-1].decode('utf-8')
      else:
        self.local['ngc'] = subprocess.run([os.environ['HOME'] + "/.local/bin/ngc", "--version"], stdout=subprocess.PIPE).stdout.split()[-1].decode('utf-8')
    except:
      log.warning("error locating NGC cli")
      exc_type, exc_value, exc_tb = sys.exc_info()
      log.warning(traceback.format_exception(exc_type, exc_value, exc_tb))
#      log.warning(sys.exc_info())

  def check_docker_local(self):
    runner = DockerRunner(self.conf)
    self.local['docker'] = runner.get_docker_ver()

  def check_aws_cli_local(self):
    runner = DockerRunner(self.conf)
    self.local['aws'] = runner.get_aws_cli_ver()

  def check_kaggle_cli_local(self):
    self.local['kaggle'] = "not found"
    try:
#      self.local['kaggle'] = subprocess.run([os.environ['HOME'] + "/.local/bin/kaggle", "--version"], stdout=subprocess.PIPE).stdout.split()[-1].decode('utf-8').split(',')[0]
      self.local['kaggle'] = subprocess.run(["/bin/sh", "-c", "pip3 show kaggle |grep Version"], stdout=subprocess.PIPE).stdout.decode('utf-8').rstrip().split(':')[1].strip()
    except:
      log.warning("error locating kaggle cli")
      exc_type, exc_value, exc_tb = sys.exc_info()
      log.warning(traceback.format_exception(exc_type, exc_value, exc_tb))
#      log.warning(sys.exc_info())      

  def check_nvdocker_local(self):
    self.local['nvdocker'] = 'not found'
    try:
      self.local['nvdocker'] = subprocess.run(["/bin/sh", "-c", "apt list --installed nvidia-docker2"], stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.split()[2].decode('utf-8')
    except:
      log.warning("error locating nvdocker")
      exc_type, exc_value, exc_tb = sys.exc_info()
      log.warning(traceback.format_exception(exc_type, exc_value, exc_tb))
#      log.warning(sys.exc_info()) 

  def check_dss_local(self):
    self.local['dss'] = "not found"
    try:
      out = subprocess.run(["/bin/sh", "-c", "grep '^STACK_VERSION=' " + os.environ['HOME'] + "/data-science-stack/data-science-stack"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
      self.local['dss'] = out.stdout.decode('utf-8').rstrip().split('=')[1]
    except:
      log.warning("error locating data science stack")
      log.error(out.stderr)
      exc_type, exc_value, exc_tb = sys.exc_info()
      log.warning(traceback.format_exception(exc_type, exc_value, exc_tb))
#      log.warning(sys.exc_info())   


  def check_jupyter_repo2docker_local(self):
    self.local['jr2d'] = "not found"
    try:
      self.local['jr2d'] = subprocess.run(["/bin/sh", "-c", "pip3 show jupyter-repo2docker |grep Version"], stdout=subprocess.PIPE).stdout.decode('utf-8').rstrip().split(':')[1].strip()
    except:
      log.warning("error locating data science stack")
      exc_type, exc_value, exc_tb = sys.exc_info()
      log.warning(traceback.format_exception(exc_type, exc_value, exc_tb))
#      log.warning(sys.exc_info()) 

  def check_pip_remote(self):
    out = None
    try:
      out = subprocess.run(["/bin/sh", "-c", "pip3 list -o --format json --retries 1"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)    
    except:
      log.error("error pulling latest pip information")
      log.error(out.stderr)
#      log.error(sys.exc_info())
      exc_type, exc_value, exc_tb = sys.exc_info()
      log.error(traceback.format_exception(exc_type, exc_value, exc_tb))
      log.error("done trying to pull latest pip information") 

    if out.stdout is not None:
      self.parse_pip_output(out.stdout)

  def parse_pip_output(self, out):
    try:
      for j in json.loads(out):
        if j['name'] == 'nvdsw':
          self.remote['nvdsw'] = j['latest_version']
          self.local['nvdsw'] = j['version']

        if j['name'] == 'kaggle':
          self.remote['kaggle'] = j['latest_version']
          self.local['kaggle'] = j['version']  

        if j['name'] == 'jupyter-repo2docker':
          self.remote['jupyter-repo2docker'] = j['latest_version']
          self.local['jupyter-repo2docker'] = j['version']   
      
    except:
      log.error("error parsing pip json")
      log.error("out: " + out)
      exc_type, exc_value, exc_tb = sys.exc_info()
      log.error(traceback.format_exception(exc_type, exc_value, exc_tb))
#      log.error(sys.exc_info())

#   def check_remote(self):
#     self.check_driver_remote()
#     self.check_docker_remote()
#     self.check_nvdocker_remote()
#     self.check_cuda_remote()
      
#    self.check_ngc_cli_remote()
#     self.check_kaggle_cli_remote()
#     self.check_aws_cli_remote()

#     self.check_dss_remote()
#     self.check_jupyter_repo2docker_remote()

  def install_update_jupyter_repo2docker(self):
    log.debug("repo2docker install_update starting")
    out = subprocess.run(["/bin/sh", "-c", "pip3 install -U jupyter-repo2docker"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if out.returncode == 0:
      log.info("jupyter repo2docker updated")
    else:
      log.warning("unable to upgrade jupyter repo2docker:")
      log.warning(out.stdout)
      log.warning(out.stderr)

  def install_update_kaggle(self):
    log.debug("kaggle install_update starting")
    out = subprocess.run(["/bin/sh", "-c", "pip3 install -U kaggle"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if out.returncode == 0:
      log.info("kaggle updated")
    else:
      log.warning("unable to upgrade kaggle:")
      log.warning(out.stdout)
      log.warning(out.stderr)    
    log.debug("kaggle install_update done")

  def install_update_aws(self):
    log.debug("aws install_update starting")
    runner = DockerRunner(self.conf)
    runner.update_aws_cli()
    log.debug("aws install_update done")
    return True

  def install_update_ngc(self):
    log.debug("ngc install_update starting")
    log.debug(self.conf['MAIN']['NGC_CLI_URL'])
    cmd = "curl -o /tmp/ngccli_cat_linux.zip " +  self.conf['MAIN']['NGC_CLI_URL'] + " && unzip -o -d /tmp /tmp/ngccli_cat_linux.zip && chmod u+x /tmp/ngc && rm /tmp/ngccli_cat_linux.zip"
    out = subprocess.run(["/bin/sh", "-c", cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if out.returncode == 0:
#      os.rename('/tmp/ngc', os.environ['HOME'] + "/.local/bin/ngc") 
      if self.script_dir is not None:
        shutil.copy('/tmp/ngc', self.script_dir + "/ngc") 
      else:
        shutil.copy('/tmp/ngc', os.environ['HOME'] + "/.local/bin/ngc") 
      log.info("ngc updated")
      log.debug(out.stdout)
      log.debug(out.stderr)
    else:
      log.warning("unable to update ngc:")
      log.warning(out.stdout)
      log.warning(out.stderr)
      return False
    log.debug("ngc install_update done")
    return True

#  def install_update_dss(self):
#    log.debug("ngc install_update starting")
#    # this needs to be shell because it needs to be interactive..
#    cmd = ["/usr/bin/gnome-terminal","--working-directory="+os.environ['HOME']+"/.local/bin", "--", "bash",  "-c", "./iudss.sh;bash"]
#    subprocess.call(cmd)
#    out = subprocess.run(["/bin/bash", "-c", os.environ['HOME'] + "/.local/bin/iudss.sh"], capture_output=True)

  def update_nvdsw(self):
    log.debug("nvdsw update starting")
    out = subprocess.run(["/bin/sh", "-c", "pip3 install -U nvdsw" ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if out.returncode == 0:
      log.info("nvdsw updated")
      log.debug(out.stdout.decode('utf-8'))
      log.debug(out.stderr.decode('utf-8'))
    else:
      log.warning("unable to upgrade nvdsw:")
      log.warning(out.stdout.decode('utf-8'))
      log.warning(out.stderr.decode('utf-8'))    
    log.debug("nvdsw update done")  

    return out.stdout.decode('utf-8'), out.stderr.decode('utf-8'), out.returncode

  def get_nvdswd_start_cmd(self):
    if self.script_dir is not None:
      return self.script_dir + "/nvdswd"
    else:
      return os.environ['HOME'] + "/.local/bin/nvdswd"

  def launch_nvdsw(self):
    log.debug("nvdsw launch starting")
    # subprocess.Popen
    if self.script_dir is not None:
      proc = subprocess.Popen(self.script_dir + "/nvdsw", shell = True)
    else:
      proc = subprocess.Popen(os.environ['HOME'] + "/.local/bin/nvdsw", shell = True)
    log.debug("nvdsw launch sleeping 5")
    time.sleep(5)
    log.debug("nvdsw launch polling")
    rc = proc.poll()
    # None is good

    log.debug("nvdsw launch returning")

    return rc    