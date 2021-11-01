import os
import time
import ipywidgets as widgets
from IPython.display import IFrame, display, clear_output
import logging
import threading

# Get an instance of a logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

__version__ = '0.1.35.dev1'

class LoginPanel():

  def __init__(self):
    pass

  def display_gui(self):

    iframe = IFrame('https://ai.finlab.tw/api_token/', width=620, height=300)
    display(iframe)

  def wait_for_token(self):

    token = input('輸入驗證碼')
    clear_output()
    self.login(token)

  @staticmethod
  def login(token):

    # check
    if '#' not in token or token.split('#')[1] not in ['vip', 'free']:
      raise Exception('The api_token format is wrong, '
                      'please paste the api_token after re-run the process or '
                      'check api token from https://ai.finlab.tw/api_token/.')

    # set token
    role = token[token.index('#') + 1:]
    token = token[:token.index('#')]
    os.environ['finlab_id_token'] = token
    os.environ['finlab_role'] = role
    print('輸入成功!')

def login(api_token=None):

    if api_token is None:
      lp = LoginPanel()
      lp.display_gui()
      lp.wait_for_token()
    else:
      LoginPanel.login(api_token)


def get_token():
    if 'finlab_id_token' not in os.environ:
        login()

    return os.environ['finlab_id_token']


def get_role():
    if 'finlab_role' not in os.environ:
        login()

    return os.environ['finlab_role']
