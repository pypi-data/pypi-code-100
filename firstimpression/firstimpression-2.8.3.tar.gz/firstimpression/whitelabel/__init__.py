import threading
from typing import Any, Optional

import firebase_admin
import google.cloud.firestore_v1.client as client
from firebase_admin import firestore
from firstimpression.api.request import give_error_message, request_json
from firstimpression.scala import ScalaPlayer

scala = ScalaPlayer('WHITELABEL')

svars = scala.variables

CREDENTIALS_URL = 'https://dev.fi-api.io/credentials/firebase'
HEADERS_FI_API = {
    'Authorization': 'Token {}'.format(scala.fi_api_key)
}

class Firebase:

    def __init__(self) -> None:
        self.project_id = svars['Player.firebase_project_id']
        self.credentials = self.__get_credentials()

        self.callback_done = threading.Event()

        firebase_admin.initialize_app(self.credentials)

        self.db: client.Client  = firestore.client()

        self.on_snapshot = self.__get_on_snapshot()


    def __get_on_snapshot(self):

        def on_snapshot(doc: Any, changes: Any, read_time: Any) -> None:
            for change in changes:
                if change.type.name == 'ADDED':
                    trigger = change.document.to_dict()
                    if trigger['active'] == True:
                        change_triggers(trigger['triggername'])
                    else:
                        change_triggers(None)
                elif change.type.name == 'REMOVED':
                    self.callback_done.set()
                elif change.type.name == 'MODIFIED':
                    trigger = change.document.to_dict()
                    if trigger['active'] == True:
                        change_triggers(trigger['trigger_name'])
                    else:
                        change_triggers(None)

        return on_snapshot


    def __get_credentials(self):

        if self.project_id is None:
            scala.error('The project ID is not set for this player', True)

        params = {
            'project_id': self.project_id
        }

        response_json, is_error = request_json(CREDENTIALS_URL, HEADERS_FI_API, params, False)

        if is_error:
            message = give_error_message(response_json)
            if response_json['type'] == 'ERROR':
                scala.error(message)
            elif response_json['type'] == 'WARN':
                scala.warn(message)

            raise SystemExit

        response_json: Any

        return response_json[0]

    def get_query(self):
        return self.db.collection('triggers').where('player', '==', scala.uuid)


def change_triggers(playlist: Optional[str]):
    for key in svars:
        if 'Channel' in key:
            svars[key] = False


    if playlist is not None:
        svars['Channel.{}'.format(playlist)] = True
