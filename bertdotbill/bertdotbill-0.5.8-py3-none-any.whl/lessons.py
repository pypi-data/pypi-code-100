import base64
from bertdotbill.defaults import default_terminal_address
from bertdotbill.logger import Logger
from bertdotbill.config import ConfigUtil
import json
import sys

logger = Logger().init_logger(__name__)

class Lessons():

  def __init__(self, **kwargs):
    self.settings = kwargs['settings']
    self.args = kwargs['args']
    self.config_util = ConfigUtil()

  def initialize(self, webview):
    if len(webview.windows) > 0:
      logger.info('Initializing Lesson View')
      default_console_address = self.config_util.get(
        self.settings,'terminals.default.address', default_terminal_address
      )
      terminals = self.settings.get('terminals', {})
      if terminals:
        terminal_address = terminals.get(
          'footer',{}).get('address', default_console_address)
      else:
        terminal_address = default_console_address
      webview.windows[0].evaluate_js('window.pywebview.state.setiFrameURL("%s")' % terminal_address)
      if not self.args.no_init:
        webview.windows[0].evaluate_js('window.pywebview.state.loadLesson("")')
        if not self.args.no_init_lesson:
          webview.windows[0].evaluate_js('window.pywebview.state.setTopics("%s")' % self.load())
    else:
      logger.info('Skipped Lesson View Initialization')

  def load(self):

    logger.info('Loading available topics')
    topics = self.settings.get('topics', {})
    available_lesson_count = 0

    if isinstance(topics, list):
      topics_string = str(json.dumps(topics))
      logger.debug('Topic List: %s' % topics_string)
      topics_bytes = topics_string.encode("ascii")
      encoded_lessons_list = base64.b64encode(topics_bytes)
      encoded_lessons = encoded_lessons_list.decode("utf-8")
      return encoded_lessons
    else:
      logger.warning("Improperly structured 'topics' config block, seek --help")
    logger.info('Successfully loaded available lessons')