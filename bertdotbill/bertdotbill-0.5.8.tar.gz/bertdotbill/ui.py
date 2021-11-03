from bertdotbill.lessons import Lessons
from bertdotbill.logger import Logger
from bertdotbill.terminals import Terminals
from bertdotbill.config import ConfigUtil
from bertdotbill.commands import Commands
import sys

logger = Logger().init_logger(__name__)

class UI():

  def __init__(self, **kwargs):
    self.settings = kwargs['settings']
    self.config_util = ConfigUtil()
    self.args = kwargs['args']
    self.commands = Commands(self.settings, self.args)
    # Initialize Lesson Loader
    self.lessons = Lessons(
    settings=self.settings, 
    args=self.args)
    # Initialize Terminals
    self.terminals = Terminals(
    settings=self.settings, 
    args=self.args)    

  def init_terminal(self, **kwargs):
    
    webview = kwargs['webview']
    section = kwargs['section']
    set_function = kwargs['set_function']
    url = self.terminals.load(section)
    webview.windows[0].evaluate_js(
      'window.pywebview.state.%s("%s")' % (set_function, url)
    )

  def initialize(self, webview):
    if len(webview.windows) > 0:
      logger.info('Initializing UI View')

      self.init_terminal(
        webview = webview,
        section = 'rightpane',
        set_function = 'setRightPaneURL'
      )

      self.init_terminal(
        webview = webview,
        section = 'footer',
        set_function = 'setfooterURL'
      )      

      if not self.args.no_init:
        webview.windows[0].evaluate_js('window.pywebview.state.loadLesson("")')
        osCommands = self.commands.retrieve(encoded=True)
        webview.windows[0].evaluate_js('window.pywebview.state.setCommands("%s")' % osCommands)
        webview.windows[0].evaluate_js('window.pywebview.state.setpyWebViewReadyState("ready")')
        if not self.args.no_init_lesson:
          webview.windows[0].evaluate_js('window.pywebview.state.setTopics("%s")' % self.lessons.load())
    else:
      logger.info('Skipped Lesson View Initialization')