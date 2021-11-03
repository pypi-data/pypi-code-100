# Set App Name
app_name = "Bert's Interactive Lesson Loader (BILL)"
gui_dirname = 'bill.gui'
default_terminal_address = 'ws://127.0.0.1:5000/'
terminal_check_timeout = 5
allowed_command_patterns =[
  'docker.run.*berttejeda.ansible:latest start-bash-websocket.py',
  'control..name.Microsoft.CredentialManager'
]
webengine_choices = [
  'gtk',
  'qt',
  'edgechromium',
  'edgehtml',
  'mshtml',
  'cef'
]
settings = {
  "terminals": {
    "default": {
      "address": "ws://127.0.0.1:5000/ws"
    },
    "footer": {
      "address": "ws://127.0.0.1:5000/ws"
    },
    "rightpane": {
      "address": "ws://127.0.0.1:5000/ws"
    }
  },
  "external_configs": [
    {
      "name": "bertdotlessons",
      "uri": "https://raw.githubusercontent.com/berttejeda/bert.lessons/main/bill.config.yaml"
    }
  ]
}