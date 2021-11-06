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



import logging
import os
import sys
import time
import traceback
from copy import copy

log = logging.getLogger('runner')


class DockerRunner:
  running_cs = {}
  containers = {}
  images = {}
  

  def __init__(self, config):
    self.inited = False
    try:
      import docker as d
      self.docker = d
      log.debug("docker found")
      self.inited = True
    except Exception:
      log.warning("unable to find docker")
      exc_type, exc_value, exc_tb = sys.exc_info()
      log.warning(traceback.format_exception(exc_type, exc_value, exc_tb))
      self.inited = False

    self.conf = config

  def initialized(self):
      return self.inited

  def run(self, ydict, attrs):
      if not self.inited:
          return False
      log.debug('run called')
      log.debug(ydict)

      try: 
        start_time = time.time()
        client = self.docker.from_env()
        # the point of using lists over dictionaries is, the same local volume may be passed through twice
        v = []
#         if ydict['volumes'] is not None:
        if attrs['volumes'] is not None:
          for va in attrs['volumes']:
            vaa = va.split(':')
            src_mnt = vaa[0]
            rest = vaa[1:]
#             if src_mnt.startswith('/'):
#               # absolute path
#               local_dir = src_mnt
#             else:
#               local_dir = os.environ['HOME'] + '/' + src_mnt 

            # this logic moved to preferences.py
            # user settings control the default directory to mount
            local_dir = src_mnt
            try:
              os.stat(local_dir)
            except:
              log.debug('creating local start dir: ' + local_dir)
              os.mkdir(local_dir) 

            v.append(local_dir + ':' + ':'.join(rest))



      # ideally, ought to check whether the docker image is already pulled.
      # we also could suppress the menu entry if the docker image is not pulled :P
      # statically, this works; but will not work when we work with dynamic containers....
        envs = ydict['environment']
        # some envs are lists so we can put weird cased vars in there
        if envs is not None and type(envs) is dict:
         for k,vv in envs.items():
          if vv is None:
            log.info("config file has no value for key " + k + " so trying env")
            v1 = os.getenv(k)
            
            if v1 is None:
              log.info("still could not get value. oh well")
            else:
              log.info("in env found value " + v1 + " for key " + k)
              envs[k] = v1

        remove_flag = False
        # this label will always be attached to the containers
        default_label = self.conf['MAIN']['DOCKER_GENERAL_LABEL']
        container_label = ydict['container_label']
        browser_port = list(attrs['ports'].keys())[0]
        labels = {}
        labels[default_label] = ''
        labels[container_label] = ''
        labels['browser_port'] = browser_port

        if self.conf['MAIN']['DOCKER_REMOVE_FLAG'] == 'True':
          remove_flag = True

        # for now, just run the latest tag
        latest_tag = ydict['tags'][0]
        name = None
        if attrs['name'] != 'auto-assigned':
          name = attrs['name']

        device_requests=[]
        gpus = []
        if attrs['gpus'] is not None:
          for gpu in attrs['gpus']:
            log.debug('gpu: ' + gpu)
            gpus.append(gpu)
#           dr = self.docker.types.DeviceRequest(count=0, device_ids = [gpu], capabilities=[['gpu']])  
          dr = self.docker.types.DeviceRequest(device_ids = gpus, capabilities=[['gpu']])
          device_requests.append(dr)
    
        if len(device_requests) > 0:
          runtime = 'nvidia'
        else:
          runtime = 'runc'

        c = client.containers.run(ydict['image'] + ':' + latest_tag,ydict['command'], detach = True, ipc_mode = 'host', remove = remove_flag, volumes = v,
#           labels = labels, entrypoint = ydict['entrypoint'], ports = ydict['ports'], environment = envs)
          labels = labels, entrypoint = ydict['entrypoint'], ports = attrs['ports'], environment = envs, name = name, runtime = runtime, device_requests = device_requests)

#        time.sleep(2)
        client.close()
        cs = c.status
        # chill until it's up and running
        while cs != 'running':
          time.sleep(0.1)
          # the attrs are cached..
          c.reload()
          cs = c.status
          log.debug("checking.. status: " + cs)
          p = c.attrs['NetworkSettings']['Ports']
          log.debug("network settings of the new container: " + str(p))
          if cs != 'running' and cs != 'created':
            log.error("failed to launch the container for some reason... status: " + cs)
            return False
          if time.time() - start_time > int(self.conf['MAIN']['DOCKER_START_TIMEOUT']):
            raise Exception("timed out waiting for container to start")
        end_time = time.time()
        cnm = c.attrs['Name'].split('/')[-1]
        log.debug("the container is up and running with name " + cnm + " and status " + cs + " in " + str(end_time-start_time) + " s")
        DockerRunner.running_cs[ydict['container_label']] = c
        return True

      except Exception:
        log.warning("unable to start container")
        exc_type, exc_value, exc_tb = sys.exc_info()
        log.warning(traceback.format_exception(exc_type, exc_value, exc_tb))  
        return False

  def stop(self, ydict):
      log.debug('stop called')
      if not self.inited:
          return False
      try: 
        c = DockerRunner.running_cs[ydict['container_label']]
#      client = self.docker.from_env()
        log.debug('attempting to stop container with status: ' + c.status)
        if c.status == 'running' or c.status == 'created':
          c.stop(timeout = int(self.conf['MAIN']['DOCKER_STOP_TIMEOUT']))
        # only try to stop containers that are not --rm already
        if self.conf['MAIN']['DOCKER_REMOVE_FLAG'] != 'True':
          c.remove()
#      client.close()
        DockerRunner.running_cs.pop(ydict['container_label'])
        return True
      except Exception:
        log.warning("unable to get stop container")
        exc_type, exc_value, exc_tb = sys.exc_info()
        log.warning(traceback.format_exception(exc_type, exc_value, exc_tb)) 
        return False 

  def stop_all(self):
      log.debug('stop_all called')
      try:
       for k,v in DockerRunner.running_cs.items():
         log.debug('attempting to stop container with status: ' + v.status)
         if v.status == 'running' or v.status == 'created':
           v.stop(timeout = int(self.conf['MAIN']['DOCKER_STOP_TIMEOUT']))
         v.remove()
       log.debug('stop_all done')
       return True
      except Exception:
        log.warning("unable to stop all")
        exc_type, exc_value, exc_tb = sys.exc_info()
        log.warning(traceback.format_exception(exc_type, exc_value, exc_tb)) 
        return False

  def get_aws_cli_ver(self):
      ver = "not found"
      if not self.inited:
          return ver
      try:
        client = self.docker.from_env()
        ver = client.containers.run(self.conf['MAIN']['AWS_DOCKER_IMAGE'], '--version', remove = True).decode('utf-8').split()[0].split('/')[1]
        client.close()
      except Exception:
        log.warning("unable to get aws cli version")
        exc_type, exc_value, exc_tb = sys.exc_info()
        log.warning(traceback.format_exception(exc_type, exc_value, exc_tb))
      return ver
      
  def update_aws_cli(self):
    if not self.inited:
      return
    try: 
      client = self.docker.from_env()
      client.images.pull(self.conf['MAIN']['AWS_DOCKER_IMAGE'])
      client.close()
      return True
    except Exception:
      log.warning("unable to update aws cli")
      exc_type, exc_value, exc_tb = sys.exc_info()
      log.warning(traceback.format_exception(exc_type, exc_value, exc_tb)) 
      return False 

  def get_docker_ver(self):
      ver = "not found"
      if not self.inited:
          return ver
      try:
        client = self.docker.from_env()
        ver = client.version()['Version']
        client.close()
      except Exception:
        log.warning("unable to connect to docker")
        exc_type, exc_value, exc_tb = sys.exc_info()
        log.warning(traceback.format_exception(exc_type, exc_value, exc_tb))  

      return ver

  def remove_container_if_exists(self, cont_name):
    log.debug('checking if container ' + cont_name + ' exists')
    if not self.inited:
      return False

    try:
      client = self.docker.from_env()
      c = client.containers.get(cont_name)
      log.debug("container present, stopping / removing..")
      c.stop()
      c.remove()
      log.debug("container removed")
      client.close()
    except self.docker.errors.NotFound:
      log.debug("container " + cont_name + " is not found")  
      client.close()
    except Exception:
      log.warning("unable to connect to docker")
      exc_type, exc_value, exc_tb = sys.exc_info()
      log.warning(traceback.format_exception(exc_type, exc_value, exc_tb))
      client.close()

  def remove_container_by_label(self, label):
    log.debug('trying to remove any container with label ' + label)
    if not self.inited:
      return False

    try:
      client = self.docker.from_env()
      cs = client.containers.list()
      for c in cs:
        if label in c.labels:
          log.debug("container " + c.name + " present, stopping / removing..")
    #      c.stop()
          c.remove(force = True)
          log.debug("container " + c.name + " removed")
      client.close()
    except Exception:
      log.warning("unable to connect to docker")
      exc_type, exc_value, exc_tb = sys.exc_info()
      log.warning(traceback.format_exception(exc_type, exc_value, exc_tb))
      client.close()      

  def image_exists_locally(self, img_name):
    log.debug('checking if image ' + img_name + ' exists locally')
    if not self.inited:
      return False

    try:
      client = self.docker.from_env()
      i = client.images.get(img_name)
      log.debug("the image is present locally")
      client.close()
      return True
    except self.docker.errors.ImageNotFound:
      log.info("image " + img_name + " is not present locally")  
      client.close()
      return False
    except Exception:
      log.warning("unable to connect to docker")
      exc_type, exc_value, exc_tb = sys.exc_info()
      log.warning(traceback.format_exception(exc_type, exc_value, exc_tb))
      client.close()
      return False


  def pull_img(self, img_name):
    if not self.inited:
      return False
    try:
      client = self.docker.from_env()
      log.debug("pulling image " + img_name)
      i = client.images.pull(img_name)
      log.debug("pulled image " + img_name)
      client.close()
      return True
    except self.docker.errors.ImageNotFound:
      log.info("image " + img_name + " is not found")  
      client.close()
      return False
    except Exception:
      log.warning("unable to connect to docker")
      exc_type, exc_value, exc_tb = sys.exc_info()
      log.warning(traceback.format_exception(exc_type, exc_value, exc_tb))
      client.close()
      return False    


  def build_img(self, img_name, docker_path, dockerfile):
    if not self.inited:
      return False
    try:
      client = self.docker.from_env()
      log.debug("building image " + img_name)
      client.images.build(tag = img_name, path = docker_path, dockerfile = dockerfile)
      log.debug("built image " + img_name)
      client.close()
      return True
    except Exception:
      log.warning("unable to connect to docker")
      exc_type, exc_value, exc_tb = sys.exc_info()
      log.warning(traceback.format_exception(exc_type, exc_value, exc_tb))
      client.close()
      return False 

