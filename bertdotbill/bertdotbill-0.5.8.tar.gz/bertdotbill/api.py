import base64
import os
import markdown
from bertdotbill.extensions import NewTabExtension
from jinja2 import Template
from bertdotbill.commands import Commands
from bertdotbill.logger import Logger
from bertdotbill.config import ConfigUtil
from bertdotwebadapter import WebAdapter

logger = Logger().init_logger(__name__)

class API:

  def __init__(self, webview, args, settings, **kwargs):
    self.settings = settings
    self.args = args
    self.webview = webview
    self.commands = Commands(settings, self.args)
    self.webadapter = WebAdapter(fail_on_errors=True, verify_tls=self.args.verify_tls)
    self.config_util = ConfigUtil()
    self.global_username = os.environ.get('GLOBAL_USERNAME') or self.args.username or self.config_util.get(self.settings,'auth.global.username')
    self.global_password = os.environ.get('GLOBAL_PASSWORD') or self.args.password or self.config_util.get(self.settings,'auth.global.password')
    
  def log(self, level, message):
    if level == 'error':
      logger.error(message)
    elif level == 'debug':
      logger.debug(message)
    else:
      logger.info(message)

  def fullscreen(self):
    self.webview.windows[0].toggle_fullscreen()

  def launch_command(self, command_key, args=None):
    self.commands.launch(command_key, args)

  # TODO: Move all lessons-related functions
  # to the lessons package file
  def encode_lesson(self, rendered_lesson):
      rendered_lesson_bytes = rendered_lesson.encode("ascii")
      encoded_lesson = base64.b64encode(rendered_lesson_bytes)      
      return encoded_lesson.decode("utf-8")

  def render_lesson(self, git_url, lesson_content, norender_markdown=False):

    initial_data = {
    'environment': os.environ
    }
    lesson_content = str(lesson_content)
    lesson_content = lesson_content.strip()
    lesson_template = Template(lesson_content)
    try:
      rendered_lesson = lesson_template.render(
        session=initial_data
      )
    except Exception as e:
      err = str(e)
      logger.error('I had trouble rendering the lesson at %s, error was %s' % (git_url, err))
      rendered_lesson = ('''
        <div class="lesson-error-container">
          <div class="lesson-error-text">
          Error in rendering lesson at %s:<br /> %s
          </div>
        </div>
        ''' % (git_url, err)
      )
      return rendered_lesson
    if norender_markdown:
      return rendered_lesson
    else:
      rendered_lesson = markdown.markdown(rendered_lesson, 
        extensions=[NewTabExtension(), 
        'markdown.extensions.admonition',
        'markdown.extensions.attr_list', 
        'markdown.extensions.codehilite',
        'markdown.extensions.toc']
        )
      return rendered_lesson

  # TODO: git_url should be renamed to lesson_url
  def load_lesson(self, git_url, no_ui=False, norender_markdown=False):
    git_url = os.environ.get('GIT_URL') or git_url
    res_ok = False
    # TODO: Employ per-lesson credentials
    if not no_ui and len(self.webview.windows) > 0:
      try:
        res = self.webadapter.get(git_url, 
          username=self.global_username,
          password=self.global_password,        
          cache_path='.')
        res_ok = True
      except Exception as e:
        err = str(e)
        logger.error('I had trouble retrieving the lesson at %s, error was %s' % (git_url, err))
        html_err_message = '''
          <div class="lesson-error-container">
            <div class="lesson-error-text">
            I had trouble retrieving the lesson at %s<br />
            Error was: %s<br />
            </div>
          </div>
        ''' % (git_url, err)
        encoded_lesson = self.encode_lesson(html_err_message)
      if res_ok:
        lesson_content = res
        logger.info('Attempting to render and encode lesson at %s' % git_url)
        rendered_lesson = self.render_lesson(git_url, lesson_content, norender_markdown=norender_markdown)
        logger.debug(rendered_lesson)
        try:
          encoded_lesson = self.encode_lesson(rendered_lesson)
        except Exception as e:
          err = str(e)
          logger.error('I had trouble encoding the lesson at %s' % git_url, err)
          html_err_message = '''
            <div class="lesson-error-container">
              <div class="lesson-error-text">
              I had trouble encoding the lesson at %s<br />
              Error was: %s
              </div>
            </div>
          ''' % (git_url, err)
          encoded_lesson = self.encode_lesson(html_err_message)
      try:
        # Load the lesson content
        self.webview.windows[0].evaluate_js('window.pywebview.state.loadLesson("%s")' % encoded_lesson)
        # Add click events to all elements with class 'clickable-code'
        self.webview.windows[0].evaluate_js('window.pywebview.state.addClickEvents()')
        # Auto-generate the table of contents via tocbot
        self.webview.windows[0].evaluate_js('window.pywebview.state.initTOCbot()')
      except Exception as e:
        self.webview.windows[0].evaluate_js('alert("Encountered an error: %s")' % e) 
    elif no_ui:
      res = self.webadapter.get(git_url, 
        username=self.global_username,
        password=self.global_password,        
        cache_path='.')
      lesson_content = str(res)
      rendered_lesson = self.render_lesson(lesson_content, norender_markdown=norender_markdown)
      print(rendered_lesson)

  def save_content(self, content):
    filename = self.webview.windows[0].create_file_dialog(self.webview.SAVE_DIALOG)
    if not filename:
        return

    with open(filename, 'w') as f:
        f.write(content)

  def ls(self):
    return os.listdir('.')