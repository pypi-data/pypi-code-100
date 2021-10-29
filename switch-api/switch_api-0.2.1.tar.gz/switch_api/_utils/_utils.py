# -------------------------------------------------------------------------
# Copyright (c) Switch Automation Pty Ltd. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
"""
A module for .....
"""
# import datetime
import re
import uuid
from collections import namedtuple
from typing import Union
import string
import secrets
import pandas
import pandera
from .._utils._constants import WORK_ORDER_STATUS, WORK_ORDER_CATEGORY, WORK_ORDER_PRIORITY

__all__ = ['generate_password', 'convert_to_sqm', 'ValidatedSetterProperty', 'ApiInputs']


# import requests
# import logging
# import sys
#
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)
# consoleHandler = logging.StreamHandler(stream=sys.stdout)
# consoleHandler.setLevel(logging.INFO)
#
# logger.addHandler(consoleHandler)
# formatter = logging.Formatter('%(asctime)s  switch_api.%(module)s.%(funcName)s  %(levelname)s: %(message)s',
#                               datefmt='%Y-%m-%dT%H:%M:%S')
# consoleHandler.setFormatter(formatter)


class ValidatedSetterProperty:
    def __init__(self, func, name=None, doc=None):
        self.func = func
        self.__name__ = name if name is not None else func.__name__
        self.__doc__ = doc if doc is not None else func.__doc__

    def __set__(self, obj, value):
        ret = self.func(obj, value)
        obj.__dict__[self.__name__] = value


def _column_name_cap(columns) -> list:
    renamed_columns = [name[0].upper() + name[1:] for name in columns.to_list()]
    return renamed_columns


def _with_func_attrs(**attrs):
    def with_attrs(f):
        for k, v in attrs.items():
            setattr(f, k, v)
        return f

    return with_attrs


def _is_valid_regex(regex):
    """Check if regex is valid.

    Parameters
    ----------
    regex : str
        A `regex` expression to be validated.

    Returns
    -------
    bool
        Valid if True, invalid if False.

    """
    try:
        re.compile(regex)
        return True
    except re.error:
        return False


ApiHeaders = namedtuple('ApiHeaders', ['default', 'integration'])

ApiInputs = namedtuple('ApiInputs',
                       ['email_address', 'user_id', 'api_project_id', 'data_feed_id', 'data_feed_file_status_id',
                        'bearer_token', 'api_base_url', 'api_projects_endpoint', 'subscription_key', 'api_headers'])

DiscoveryIntegrationInput = namedtuple(
        'DiscoveryIntegrationInput',
        ['api_project_id', 'installation_id', 'network_device_id', 'integration_device_id', 'user_id', 'batch_no'])

DataFeedFileProcessOutput = namedtuple('DataFeedFileProcessOutput',
                                       [
                                           'data_feed_id', 'data_feed_file_status_id',
                                           'client_tracking_id',
                                           'source_type', 'file_name', 'file_received',
                                           'file_process_status',
                                           'file_process_status_change', 'process_started',
                                           'process_completed',
                                           'minutes_since_received', 'minutes_since_processed',
                                           'file_size',
                                           'log_file_path', 'output', 'error'
                                       ])


def generate_password():
    """Generate a ten-character alphanumeric password with at least one lowercase character, at least one uppercase
    character, and at least three digits.
    """
    alphabet = string.ascii_letters + string.digits
    while True:
        password = ''.join(secrets.choice(alphabet) for i in range(10))
        if (any(c.islower() for c in password)
                and any(c.isupper() for c in password)
                and sum(c.isdigit() for c in password) >= 3):
            break
    return password


def convert_to_sqm(df: pandas.DataFrame, sqft_col_name: str):
    """Convert to square metres

    Convert floor area from square feet to square metres.

    Parameters
    ----------
    df : pandas.DataFrame
        The site asset register dataframe.
    sqft_col_name : str
        The name of the column containing the Floor Area values in sq. ft. to be converted.

    Returns
    -------
    df : pandas.DataFrame
        The input dataframe after converting the `sqft_col_name` column to square metres.


    """
    df[sqft_col_name] = df[sqft_col_name] * 0.09290304
    return df


# def convert_to_pascal_case(text: str):
#     text = re.sub(r"^[\-_:\.\s]", '', str(text))
#     text = str.upper(text[0]) + text[1:]
#     if not text:
#         return text
#     text = re.sub(r"[\-_:\.\s]([a-z])", lambda matched: str.upper(matched.group(1)), text)
#     return re.sub(r"[\-_:\.\s]", '', text)
#
#     # return lowercase(text[0]) + re.sub(r"[\-_\.\s]([a-z])", lambda matched: uppercase(matched.group(1)), text[1:])
#     # str(text).upper()
#     #
#     # text = re.sub(r"^[\-_\.]", '', str(lowercase(text)))
#     # if not text:
#     #     return text
#     # return lowercase(text[0]) + re.sub(r"[\-_\.\s]([a-z])", lambda matched: uppercase(matched.group(1)), text[1:])


def convert_to_pascal_case(text: Union[str,list]):
    if type(text) == str:
        text = re.sub(r"^[\-_:\.\s]", '', str(text))
        text = str.upper(text[0]) + text[1:]
        if not text:
            return text
        text = re.sub(r"[\-_:\.\s]([a-z])", lambda matched: str.upper(matched.group(1)), text)
        return re.sub(r"[\-_:\.\s]", '', text)
    elif type(text) == list:
        for i in range(len(text)):
            text_item = text[i]

            text_item = re.sub(r"^[\-_:\.\s]", '', str(text_item))
            text_item = str.upper(text_item[0]) + text_item[1:]
            if not text_item:
                text[i] = text_item
            text_item = re.sub(r"[\-_:\.\s]([a-z])", lambda matched: str.upper(matched.group(1)), text_item)

            text[i] = re.sub(r"[\-_:\.\s]", '', text_item)
        return text


_site_schema = pandera.DataFrameSchema(
    {
        'InstallationName': pandera.Column(pandera.String, checks=pandera.Check.str_length(1, 255)),
        'InstallationCode': pandera.Column(pandera.STRING, coerce=True, checks=pandera.Check.str_length(1, 100)),
        'Address': pandera.Column(pandera.String, checks=[pandera.Check.str_length(1, 250)]),
        'Country': pandera.Column(pandera.String, checks=[pandera.Check.str_length(1, 50)]),
        'Suburb': pandera.Column(pandera.String, checks=[pandera.Check.str_length(1, 50)]),
        'State': pandera.Column(pandera.String, checks=[pandera.Check.str_length(1, 100)], required=False),
        'StateName': pandera.Column(pandera.String, checks=[pandera.Check.str_length(1, 50, n_failure_cases=None)]),
        'FloorAreaM2': pandera.Column(pandera.Float, checks=[pandera.Check.greater_than_or_equal_to(0)]),
        'ZipPostCode': pandera.Column(pandera.STRING, checks=[pandera.Check.str_length(1, 20)]),
        'Latitude': pandera.Column(pandera.Float, required=False),
        'Longitude': pandera.Column(pandera.Float, required=False),
        'Timezone': pandera.Column(pandera.String, required=False),
        'InstallationId': pandera.Column(pandera.String, required=False),
    }
)

_work_order_schema = pandera.DataFrameSchema(
    columns={
        'WorkOrderId': pandera.Column(pandera.String, required=True),
        'InstallationId': pandera.Column(pandera.String, checks=[
            pandera.Check(lambda x: uuid.UUID(x).__class__ == uuid.UUID, element_wise=True)], required=True),
        'WorkOrderSiteIdentifier': pandera.Column(pandera.STRING, coerce=True, required=True),
        'WorkOrderCategory': pandera.Column(pandera.String, checks=[
            pandera.Check.isin(list(WORK_ORDER_CATEGORY.__args__), ignore_na=False)], required=True),
        'Type': pandera.Column(pandera.String, required=True),
        'Description': pandera.Column(pandera.String, required=True),
        'Priority': pandera.Column(pandera.String, checks=[
            pandera.Check.isin(list(WORK_ORDER_PRIORITY.__args__), ignore_na=False)], required=True),
        'Status': pandera.Column(pandera.String, checks=[
            pandera.Check.isin(list(WORK_ORDER_STATUS.__args__), ignore_na=False)], required=True),
        'CreatedDate': pandera.Column(pandera.DateTime, required=True, nullable=False),
        'LastModifiedDate': pandera.Column(pandera.DateTime, required=True, nullable=True),
        'WorkStartedDate': pandera.Column(pandera.DateTime, required=True, nullable=True),
        'WorkCompletedDate': pandera.Column(pandera.DateTime, required=True, nullable=True),
        'ClosedDate': pandera.Column(pandera.DateTime, required=True, nullable=True),
        'RawPriority': pandera.Column(pandera.String, required=True, nullable=False),
        'RawWorkOrderCategory': pandera.Column(pandera.String, required=True, nullable=False),
        'SubType': pandera.Column(pandera.String, required=False, nullable=True),
        'Vendor': pandera.Column(pandera.String, required=False, nullable=True),
        'VendorId': pandera.Column(pandera.String, required=False, nullable=True),
        'EquipmentClass': pandera.Column(pandera.String, required=False, nullable=True),
        'RawEquipmentClass': pandera.Column(pandera.String, required=False, nullable=True),
        'EquipmentLabel': pandera.Column(pandera.String, required=False, nullable=True),
        'RawEquipmentId': pandera.Column(pandera.String, required=False, nullable=True),
        'TenantId': pandera.Column(pandera.String, required=False, nullable=True),
        'TenantName': pandera.Column(pandera.String, required=False, nullable=True),
        'NotToExceedCost': pandera.Column(pandera.Float, required=False, nullable=True),
        'TotalCost': pandera.Column(pandera.Float, required=False, nullable=True),
        'BillableCost': pandera.Column(pandera.Float, required=False, nullable=True),
        'NonBillableCost': pandera.Column(pandera.Float, required=False, nullable=True),
        'Location': pandera.Column(pandera.String, required=False, nullable=True),
        'RawLocation': pandera.Column(pandera.String, required=False, nullable=True),
        'ScheduledStartDate': pandera.Column(pandera.DateTime, required=False, nullable=True),
        'ScheduledCompletionDate': pandera.Column(pandera.DateTime, required=False, nullable=True),
    },
    coerce=True,
    strict=False,
    name=None
)

# def adx_support(api_inputs: ApiInputs, build_sites=False, build_sensors=False):
#     adx_support_prefix = ''
#     if api_inputs.datacentre == 'AU':
#         adx_support_prefix = 'australiaeast'
#     elif api_inputs.datacentre == 'EA':
#         adx_support_prefix = 'australiaeast'
#     elif api_inputs.datacentre == 'US':
#         adx_support_prefix = 'centralus'
#
#     if adx_support_prefix == '':
#         logger.error('Invalid Data Centre: ' + api_inputs.datacentre)
#         return
#
#     if build_sites:
#         adx_support_url = 'https://adxsupport-' + adx_support_prefix + \
#                           '-prod.azurewebsites.net/api/sites?apiProjectId=' + api_inputs.api_project_id
#         requests.get(adx_support_url)
#
#     if build_sensors:
#         adx_support_url = 'https://adxsupport-' + adx_support_prefix + \
#                           '-prod.azurewebsites.net/api/sensors?apiProjectId=' + api_inputs.api_project_id
#         requests.get(adx_support_url)


# def invalidDateTime(df: pandas.DataFrame, col_fmt: DATETIME_COL_FMT, datetime_col: Optional[List[str]],
#                     date_col: Optional[List[str]], time_col: Optional[List[str]], dt_fmt: Optional[str]):
#     """Check for datetime errors.
#
#     Parameters
#     ----------
#     df : pandas.DataFrame
#         The dataframe that contains the columns to be validated.
#     col_fmt: DATETIME_COL_FMT
#         The format of the columns: one of - DateTime, Date, Time
#     datetime_col: List[str]
#         List of column names
#     dt_fmt: Optional[str]
#         The expected format of the datetime columns to be coerced.
#
#     Returns
#     -------
#     df : pandas.DataFrame
#         The original dataframe input after dropping any rows with datetime errors
#     df_invalid_datetime: pandas.DataFrame
#         Dataframe containing the rows of the input df that contained invalid datetime values.
#
#     """
#     if col_fmt == 'DateTime':
#         val_dt_cols = []
#         for i in datetime_col:
#             val_dt_cols.append(i + '_dt')
#         lst = [None] * len(datetime_col)
#         for i in range(len(datetime_col)):
#             df[val_dt_cols[i]] = pandas.to_datetime((df[datetime_col[i]]), errors='coerce', format=dt_fmt)
#             lst[i] = df[df[val_dt_cols[i]].isnull()]
#             df = df[df[val_dt_cols[i]].notnull()]
#             lst[i] = lst[i].drop(val_dt_cols[i], axis=1)
#             df = df.drop(val_dt_cols[i], axis=1)
#         df_invalid_datetime = pandas.concat(lst, axis=0)
#         df[datetime_col] = df[datetime_col].apply(lambda x: pandas.to_datetime(x, format=dt_fmt))
#         return df_invalid_datetime, df
#     elif col_fmt == 'Date':
#         date_col
#         pass
#     elif col_fmt == 'Time':
#         time_col
#         dt_fmt
#         pass
#     return 'Error: col_fmt not valid'


# def invalid_datetime(df: pandas.DataFrame, col_fmt: DATETIME_COL_FMT, datetime_col: Optional[List[str]],
#                      date_col: Optional[List[str]] = None, time_col: Optional[List[str]] = None,
#                      dt_fmt: Optional[str] = None):
#     """Check for datetime errors.
#
#     Parameters
#     ----------
#     df : pandas.DataFrame
#         The dataframe that contains the columns to be validated.
#     col_fmt: DATETIME_COL_FMT
#         The format of the columns: one of - DateTime, Date, Time
#     datetime_col: List[str]
#         List of column names
#     dt_fmt: Optional[str]
#         The expected format of the datetime columns to be coerced. The strftime to parse time, eg "%d/%m/%Y", note
#         that "%f" will parse all the way up to nanoseconds. See strftime documentation for more information on
#         choices: https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior
#
#     Returns
#     -------
#     df : pandas.DataFrame
#         The original dataframe input after dropping any rows with datetime errors
#     df_invalid_datetime: pandas.DataFrame
#         Dataframe containing the rows of the input df that contained invalid datetime values.
#
#     """
#
#     if type(datetime_col) == str:
#         datetime_col = [datetime_col]
#     elif type(datetime_col) == list:
#         datetime_col
#     else:
#         return 'datetime_col: Invalid format. datetime_col must be a string or list of strings.'
#
#     if col_fmt == 'DateTime':
#         val_dt_cols = []
#         for i in datetime_col:
#             val_dt_cols.append(i + '_dt')
#         lst = [None] * len(datetime_col)
#
#         if dt_fmt is None:
#             for i in range(len(datetime_col)):
#                 df[val_dt_cols[i]] = pandas.to_datetime((df[datetime_col[i]]), errors='coerce')
#                 lst[i] = df[df[val_dt_cols[i]].isnull()]
#                 df = df[df[val_dt_cols[i]].notnull()]
#                 lst[i] = lst[i].drop(val_dt_cols[i], axis=1)
#                 df = df.drop(val_dt_cols[i], axis=1)
#             df_invalid_datetime = pandas.concat(lst, axis=0)
#             df[datetime_col] = df[datetime_col].apply(lambda x: pandas.to_datetime(x))
#             return df_invalid_datetime, df
#         else:
#             for i in range(len(datetime_col)):
#                 df[val_dt_cols[i]] = pandas.to_datetime((df[datetime_col[i]]), errors='coerce', format=dt_fmt)
#                 lst[i] = df[df[val_dt_cols[i]].isnull()]
#                 df = df[df[val_dt_cols[i]].notnull()]
#                 lst[i] = lst[i].drop(val_dt_cols[i], axis=1)
#                 df = df.drop(val_dt_cols[i], axis=1)
#             df_invalid_datetime = pandas.concat(lst, axis=0)
#             df[datetime_col] = df[datetime_col].apply(lambda x: pandas.to_datetime(x, format=dt_fmt))
#             return df_invalid_datetime, df
#     elif col_fmt == 'Date':
#         date_col
#         pass
#     elif col_fmt == 'Time':
#         time_col
#         dt_fmt
#         pass
#     return 'Error: col_fmt not valid'
