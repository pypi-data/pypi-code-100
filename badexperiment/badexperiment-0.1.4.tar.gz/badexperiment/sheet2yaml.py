import os
import pandas as pd

# pip install --upgrade google-api-python-client
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# sudo pip install google-auth-oauthlib
from google_auth_oauthlib.flow import InstalledAppFlow

# AttributeError: module 'pyparsing' has no attribute 'downcaseTokens'
# ERROR: httplib2 0.20.1 has requirement pyparsing<3,>=2.4.2, but you'll have pyparsing 3.0.3 which is incompatible.
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

# The ID and range of a sample spreadsheet.
IOT_SPREADSHEET_ID = "1lj4OuEE4IYwy2v7RzcG79lHjNdFwmDETMDTDaRAWojY"
IOT_RANGE_NAME = "Glossary of terms!A1:Z"

CV_RANGE_NAME = "Controlled Terms!A1:Z"

# reusing google_api_credentials.json from https://github.com/cancerDHC/sheet2linkml
client_secret_flie = "../google_api_credentials.json"


def get_creds():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(client_secret_flie, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds


def get_sheet_service(creds):
    service = build("sheets", "v4", credentials=creds)
    # Call the Sheets API
    sheet_service = service.spreadsheets()
    return sheet_service


def get_gsheet_tab(sheet_service, sheet_id, range_name):
    result = (
        sheet_service.values().get(spreadsheetId=IOT_SPREADSHEET_ID, range=IOT_RANGE_NAME).execute()
    )
    return result


# # any benefit to doing this without pandas?
# #  lighter weight?
# #  harder to program?

def get_iot_glassary_frame():
    creds = get_creds()
    sheet_service = get_sheet_service(creds)
    iot_glossary_tab = get_gsheet_tab(sheet_service, IOT_SPREADSHEET_ID, IOT_RANGE_NAME)
    iot_glossary_frame = pd.DataFrame(iot_glossary_tab["values"], columns=iot_glossary_tab["values"][0]).drop(0)
    return iot_glossary_frame


def get_iot_controlled_terms_frame():
    creds = get_creds()
    sheet_service = get_sheet_service(creds)
    controlled_terms_tab = get_gsheet_tab(sheet_service, IOT_SPREADSHEET_ID, CV_RANGE_NAME)
    controlled_terms_frame = pd.DataFrame(controlled_terms_tab["values"],
                                          columns=controlled_terms_tab["values"][0]).drop(0)
    return controlled_terms_frame

def get_ct_dol(controlled_terms_frame):
    ct_dol = {k: [i for i in v if i] for (k, v) in controlled_terms_frame.items()}

def get_ct_keys(get_ct_dol):
    ct_keys = list(ct_dol.keys())
    ct_keys.sort()
    return ct_keys