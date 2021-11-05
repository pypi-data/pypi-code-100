import pandas as pd
import requests
import json

""" 
Read google sheet as dataframe
Usage example: read_gsheet("https://sheet.google.com/45qwd3533")
"""

def read_gsheet(url, credentials=None, sheet=None):

    import gspread

    if credentials != True:

        gc = gspread.service_account(credentials)

    if sheet != None:

        wks = gc.open_by_url(url).worksheet(sheet)

    else:

        wks = gc.open_by_url(url).get_worksheet(0)

    data = wks.get_values(value_render_option='UNFORMATTED_VALUE', date_time_render_option="FORMATTED_STRING")

    headers = data.pop(0)

    df = pd.DataFrame(data, columns=headers)

    # else:

    # df = ##chiamata API

    return df

""" 
Read hubspot contacts as dataframe
Usage example: read_hubspot_contacts(api_key)
"""
def read_hubspot_contacts(api_key, offset=100):
    
    from askdata.integrations import hubspot

    return hubspot.get_contacts(api_key, offset)