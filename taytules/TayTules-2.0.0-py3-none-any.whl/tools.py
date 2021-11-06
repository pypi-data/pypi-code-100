import subprocess
import time
import os

def install(*packages):
  for i in range(len(packages)):
    package = packages[i]
    try:
      print('Checking for package...')
      exec('import '+package)
    except:
      print('Package not found\nStarting install...')
      try: os.system('pip install '+package)
      except Exception as err: print(str(err)+'\nCould not install package')
    else:
       print(package + ' was already installed')

def clear(secs=0):
  time.sleep(secs)
  os.system('cls')

def check_install(package):
  try: os.system('import '+package)
  except: return False
  else: return True