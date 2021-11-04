__version__ = "0.1.1"
__author__ = 'Modelbit'

class __Modelbit:
  _API_URL = 'http://web:3000/api/jupyter/'
  _state = {}
    
  def __init__(self):
    import threading
    self._state = self._state
    self._check_token_thread = threading.Thread(target=self._check_token_polling)

  def _is_authenticated(self):
    return 'user_email' in self._state

  def _get_json(self, path):
    import urllib.request, json
    try:
      with urllib.request.urlopen(f'{self._API_URL}{path}') as url:
          return json.loads(url.read().decode())
    except BaseException as err:
      return {"error": f'Unable to reach Modelbit. ({err})'}
    
  def _print_mk(self, str):
    from IPython.display import display, Markdown
    display(Markdown(str))

  def _login(self):
    if self._is_authenticated():
      connectedTag = '<span style="color:green; font-weight: bold;">connected</span>'
      self._print_mk(f'You\'re {connectedTag} to Modelbit as {self._state["user_email"]}.')
      return

    if 'uuid' not in self._state:
      data = self._get_json('get_token')
      self._state['uuid'] = data['uuid']
      self._state['jwt'] = data['jwt']

    displayUrl = 'modelbit.com/t/' + self._state["uuid"]
    linkUrl = f'http://localhost:3000/t/{self._state["uuid"]}'
    aTag = f'<a style="text-decoration:none;" href="{linkUrl}" target="_blank">{displayUrl}</a>'
    helpTag = '<a style="text-decoration:none;" href="/" target="_blank">Learn more.</a>'
    self._print_mk('**Connect to Modelbit**<br/>' +
      f'Open {aTag} to authenticate this kernel, then re-run this cell. {helpTag}')
    if not self._check_token_thread.is_alive():
      self._check_token_thread.start()

  def _check_token(self):
    data = self._get_json(f'check_token?token={self._state["jwt"]}')
    if 'user_email' in data:
      self._state['user_email'] = data['user_email']

  def _check_token_polling(self):
    from time import sleep
    error_count = 0
    while not self._is_authenticated():
      try:
        self._check_token()
      except:
        error_count += 1
      sleep(3)

  def _call_api_or_print_error(self, path):
    data = self._get_json(path)
    if 'error' in data and data['error'] == 'jwt expired':
      if 'uuid' in self._state: del self._state['uuid']
      if 'user_email' in self._state: del self._state['user_email']
      data['error'] = 'Your modelbit session has expired. Re-run `mb = modelbit.login()` to re-authenticate.'

    if 'error' in data:
      self._print_mk(f'**Error:** {data["error"]}')
      return False
    return data

  # API Methods ---------------------------------------------

  def datasets(self):
    import timeago, datetime
    data = self._call_api_or_print_error(f'datasets/list?token={self._state["jwt"]}')
    if not data: return
        
    formatStr = "| Name | Last Modified |\n" + \
      "|:-|-:|\n"
    for d in data['datasets']:
      timeVal = timeago.format(datetime.datetime.fromtimestamp(d["modifiedAtMs"]/1000), datetime.datetime.now())
      formatStr += f'| <pre>{ d["name"] }</pre> | { timeVal } |\n'
    self._print_mk(formatStr)

  def dataset_open(self, ds_name):
    from urllib.parse import quote_plus
    data = self._call_api_or_print_error(f'datasets/get?token={self._state["jwt"]}&dsName={quote_plus(ds_name)}')
    if not data: return

    rows = data["rows"]
    r = 0
    while r < len(rows):
      yield rows[r]
      r += 1

def login():
  _modelbit = __Modelbit()
  _modelbit._login()
  return _modelbit

