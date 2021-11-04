from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseDownload,MediaFileUpload
from googleapiclient.discovery import build
import pprint
import io


SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = '/content/velvety-ray-315205-4e6f5ea04518.json'

def get_book(file_id='1O1zr77rg41u91srsM-OL0mOHCoadrUVW', file_name='minei_triod.csv'):
    service = mount_on_drive()
    request = service.files().get_media(fileId=file_id)
    filename = '/content/sample_data/' + file_name
    fh = io.FileIO(filename, 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print ("Download %d%%." % int(status.progress() * 100))

def mount_on_drive():
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return build('drive', 'v3', credentials=credentials)