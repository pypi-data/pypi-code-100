from __future__ import print_function
from datetime import date, timezone, datetime, timedelta
from tzlocal import get_localzone_name
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from .db import getPath, Data, Database
from .setting import *
from rich import print
from .setting import *


SCOPES = ['https://www.googleapis.com/auth/calendar']

CNAME = getConfig('calendar', 'NAME')
CID = getConfig('calendar', 'ID')

database = Database()


class Service():
    '''
    Service class is helper class to connect to Google Calendar API

    ...
    
    Atributes
    ---------
    `SCOPES` : list
        Google calendar API permision scopes 
    `calendar` : dict
        Contain calendar ID, calendar name is a dictionary key to access
    `service`
        Google calendar API connection

    Methods
    --------
    `login()`
        Get permistion to your google account and save your token
    `logout()`
        Remove permistion token
    `list_events()`

     '''
    
    ##############################################################################
    #                           Private method
    ##############################################################################
    def __init__(self, scopes=SCOPES):
        Service.SCOPES = scopes
        Service.token_file = getPath('token.json')
        Service.credentials_file = getPath('credentials.json')
        self.login()

    def _calendar_list(self):
        '''List all calendar in Google calendar then keep it on calendar atribute
        
        retuen
        -------
        dict:
            Calendar name is a key to calendar ID
        '''
        page_token = None
        self.calendar = {}
        while True:
            item = self.service.calendarList().list(pageToken=page_token).execute()

            for calendar_list_entry in item['items']:
                self.calendar[calendar_list_entry['summary']
                              ] = calendar_list_entry['id']

            page_token = item.get('nextPageToken')

            if not page_token:
                break
        return self.calendar

    def _newCalendar(self, CNAME:str):
        ''' Create calendar to Google calendar if not already

        Parameter
        ----------
        `CNAME`:str
            Name of calendar to create
        '''
        clist = self._calendar_list()
        if(CNAME not in clist):
            id =self.service.calendars().insert(body={
                'summary': CNAME
            }).execute()
            setConfig('calendar','ID',id['id'])
        else:setConfig('calendar','ID',clist[CNAME])
        global CID
        CID = getConfig('calendar','ID')
        

    def __isotime(time: datetime):
        '''Add timezone to datetime then return datetime in ISO format

        Patameter
        -----------
        `time` : datetime
            Time that you want to format it to ISO format
        
        Return
        --------
        `str`
            Time in ISO format or return `None` if not available
        '''
        if time:
            return time.replace(tzinfo=timezone.utc).isoformat()
        return None

    def __toDataclass(event):
        '''Convert Google event JSON to Dataclass `Data`

        Paramiter
        ----------
        `event`
            Google event object

        Return
        ---------
        `Data`
            Data class to keep event
        '''
        tmp = Data(event['summary'], event['id'])
        if 'location' in event:
            tmp.location = event['location']
        if 'description' in event:
            tmp.detail = event['description']
        if 'htmlLink' in event:
            tmp.htmllink = event['htmlLink']

        if 'dateTime' in event['start']:
            date = event['start']['dateTime']
            date = tuple([int(x) for x in date[:10].split('-')] +
                            [int(x) for x in date[11:-1].split(':')])
            tmp.start = datetime(*date)

            date = event['end']['dateTime']
            date = tuple([int(x) for x in date[:10].split('-')] +
                            [int(x) for x in date[11:-1].split(':')])
            tmp.end = datetime(*date)
        else:
            date = event['start']['date']
            tmp.start = datetime(*[int(x) for x in date.split('-')])
            date = event['end']['date']
            tmp.end = datetime(*[int(x) for x in date.split('-')])

        return tmp


    ##############################################################################
    #                          Public method 
    ##############################################################################

    def login(self):
        """ Get permistion to your google account and save your token"""
        creds = None
        if os.path.exists(Service.token_file):
            creds = Credentials.from_authorized_user_file( Service.token_file, Service.SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    Service.credentials_file, Service.SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(Service.token_file, 'w') as token:
                token.write(creds.to_json())

        self.service = build('calendar', 'v3', credentials=creds)
        self._newCalendar(CNAME)

    def logout(self):
        '''Remove token'''
        if os.path.exists(Service.token_file):
            os.remove(Service.token_file)

        else:
            print("You are not loged in.")

    def list_events(self, dateMin: datetime = None, dateMax: datetime = None, RETURN=False,callback=None):
        dateMin = Service.__isotime(dateMin)
        dateMax = Service.__isotime(dateMax)
        if(RETURN):
            data = []
        page_token = None
        while True:
            events = self.service.events().list(
                calendarId=CID,
                timeMin=dateMin,
                timeMax=dateMax,
                pageToken=page_token,
            ).execute()
            for event in events['items']:
                tmp = Service.__toDataclass(event)
                if callback:
                    callback()
                    # database.add(tmp).execute()
                if(RETURN):
                    data.append(tmp)
            page_token = events.get('nextPageToken')
            if not page_token:
                break
        if(RETURN):
            return data

    def add_event(self, data: Data, RETURN=False):
        '''Add event to Google calendar.
        Parameter
        ------------
        `data`:Data
            Event to add to Google calendar
        '''
        tz = get_localzone_name()
        event = {
            'summary': data.name,
            'start': {
                'dateTime': data.start.replace(tzinfo=timezone.utc).astimezone().isoformat(),
                'timeZone': tz
            },
            'end':{
                'dateTime': data.end.replace(tzinfo=timezone.utc).astimezone().isoformat(),
                'timeZone': tz
            }
        }
        if data.location :
            event['location'] = data.location
        if data.detail:
            event['description'] = data.detail
        event = self.service.events().insert(calendarId=CID, body=event).execute()
        if RETURN:return Service.__toDataclass(event)

    def update_event(self,id:str,confirm,RETURN=False):
        '''Update event in Google Calendar
        Parameters
        ---------
        `id` :str
            event ID
        `confirm`:function
            funtion callback mannual change value of event
        `RETURN`:bool
            Option to return event
            
        Return
        ---------
        `Data`
            If option RETURN is True will return the new Event that have updated
        '''
        data = self.service.events().get(calendarId=CID, eventId=id ).execute()
        data = confirm(data)
        if data:
            updated_event = self.service.events().update(calendarId=CID, eventId=data['id'], body=data).execute()
            if RETURN: return Service.__toDataclass(updated_event)

    def delete_event(self,id:str,confirm=True):
        if not (confirm  is True or confirm is False):
            confirm = confirm(self.service.events().get(calendarId=CID, eventId=id ).execute())
        if confirm:
            try:self.service.events().delete(calendarId=CID, eventId=id).execute()
            except:pass





if __name__ == '__main__':
    print("google service")
    service = Service()

    a = Data('tme')
    a.start = datetime(2021,10,29)
    a.location = 'Home'
    service.add_event(a)
    # print(service.list_events(RETURN=False))
    # service.delete_event('3i02l4l32ngd24n2f4d4ls0chs')
    # def b(data):
    #     # print(data)
    #     data['summary'] = 'anirut'
    #     return data
    # print(service.update_event('63vkqhoq1n5p7rtcijei9p84jj',b,True))
