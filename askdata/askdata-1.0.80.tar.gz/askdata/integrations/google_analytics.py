import os
import sys
import json
import datetime
import requests
import pandas as pd
import numpy as np
import argparse
import logging
import logging.config

from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

# Logging
logger = logging.getLogger(__name__)

# Constants
SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
KEY_FILE_LOCATION = './credentials/ga-api-key.json'
VIEW_ID = 'ga:157729614'

# Functions
def initialize_analyticsreporting():
    '''Initializes an Analytics Reporting API V4 service object.

    Returns:
      An authorized Analytics Reporting API V4 service object.
    '''
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        KEY_FILE_LOCATION, SCOPES)

    # Build the service object.
    analytics = build('analyticsreporting', 'v4', credentials=credentials)

    return analytics

def get_report(analytics, start_date, end_date):
    '''Queries the Analytics Reporting API V4.

    Args:
      analytics: An authorized Analytics Reporting API V4 service object.
    Returns:
      The Analytics Reporting API V4 response.
    '''
    return analytics.reports().batchGet(
        body={
            'reportRequests': [
                {
                    'viewId': VIEW_ID,
                    'dateRanges': [{'startDate': start_date, 'endDate': end_date}],
                    'metrics': [{'expression': 'ga:sessions'},
                                {'expression': 'ga:users'},
                                {'expression': 'ga:avgSessionDuration'},
                                {'expression': 'ga:percentNewSessions'},
                                {'expression': 'ga:pageviews'},
                                {'expression': 'ga:uniquePageviews'},
                                {'expression': 'ga:avgTimeOnPage'},
                                {'expression': 'ga:bounceRate'},
                                {'expression': 'ga:exitRate'},
                                {'expression': 'ga:pageValue'},
                                {'expression': 'ga:transactions'},
                                {'expression': 'ga:transactionRevenue'},
                                {'expression': 'ga:transactionsPerSession'},
                                {'expression': 'ga:transactionsPerUser'},
                                {'expression': 'ga:goal1Completions'},
                                {'expression': 'ga:goal2Completions'},
                                {'expression': 'ga:goal3Completions'},
                                {'expression': 'ga:goal4Completions'},
                                {'expression': 'ga:goal5Completions'},
                                {'expression': 'ga:goal6Completions'},
                                {'expression': 'ga:goal7Completions'},
                                {'expression': 'ga:goal8Completions'},
                                {'expression': 'ga:goal9Completions'}],
                    'dimensions': [{'name': 'ga:date'},
                                   {'name': 'ga:sourceMedium'},
                                   {'name': 'ga:campaign'},
                                   {'name': 'ga:adContent'},
                                   {'name': 'ga:keyword'},
                                   {'name': 'ga:adGroup'},
                                   {'name': 'ga:deviceCategory'},
                                   {'name': 'ga:landingPagePath'},
                                   {'name': 'ga:exitPagePath'},
                                   {'name': 'ga:date'}]
                }]
        }
    ).execute()

''' Transform the response in a dataframe '''
def response_to_dataframe(response):
    ''' Parses and prints the Analytics Reporting API V4 response.

    Args:
      response: An Analytics Reporting API V4 response.
    '''
    list = []
    for report in response.get('reports', []):
        columnHeader = report.get('columnHeader', {})
        dimensionHeaders = columnHeader.get('dimensions', [])
        metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])

        for row in report.get('data', {}).get('rows', []):
            dict = {}
            dimensions = row.get('dimensions', [])
            dateRangeValues = row.get('metrics', [])

            for header, dimension in zip(dimensionHeaders, dimensions):
                dict[header] = dimension

            for i, values in enumerate(dateRangeValues):
                for metric, value in zip(metricHeaders, values.get('values')):
                    if ',' in value or ',' in value:
                        dict[metric.get('name')] = float(value)
                    else:
                        dict[metric.get('name')] = int(value)

            list.append(dict)

    df = pd.DataFrame(list)
    return df
