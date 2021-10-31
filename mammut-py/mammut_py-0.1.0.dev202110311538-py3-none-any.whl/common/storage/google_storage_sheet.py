# coding=utf-8
from datetime import datetime
import logging

import pandas as pd
from googleapiclient.errors import HttpError
import mammut
from mammut.common.google_api import GoogleAPI
from mammut.common.storage.storage_base import SheetsStorageBase

logger = logging.getLogger()


class GoogleStorageSheet(SheetsStorageBase, GoogleAPI):
    DEFAULT_RANGE_SEPARATOR = "!"

    def __init__(self):
        SheetsStorageBase.__init__(self)

    @GoogleAPI.ensure_credentials_and_read_limits
    def get_spreadsheet_as_dataframe(
        self,
        spreadsheet_id: str,
        sheet_name,
        start_column: str,
        start_row: str,
        end_range: str,
        transpose: bool = False,
    ):
        range_name_start = (
            sheet_name
            + GoogleStorageSheet.DEFAULT_RANGE_SEPARATOR
            + start_column
            + start_row
        )
        range_data = range_name_start + ((":" + end_range) if end_range else "")
        majorDimension = "ROWS" if not transpose else "COLUMNS"

        def check_row_size(row, size):
            res = row
            if len(row) < size:
                res = row + ["" for i in range(0, size - len(row))]
            return res

        result = (
            GoogleStorageSheet.SHEETS_SERVICE.spreadsheets()
            .values()
            .get(
                spreadsheetId=spreadsheet_id,
                range=range_data,
                majorDimension=majorDimension,
            )
            .execute()
        )
        result_values = result.get("values", [])
        col_names = [h.strip() for h in result_values[0]]
        data = [check_row_size(r, len(col_names)) for r in result_values[1:]]
        data_frame = pd.DataFrame(data, columns=col_names)
        return data_frame

    @GoogleAPI.ensure_credentials_and_write_limits
    def add_rows_to_spreadsheet(
        self,
        spreadsheet_id: str,
        sheet_name: str,
        rows,
        start_row=SheetsStorageBase.DEFAULT_START_ROW,
        start_col=SheetsStorageBase.DEFAULT_START_COLUMN,
        end_range=SheetsStorageBase.DEFAULT_END_RANGE,
    ):
        range_name_start = (
            sheet_name
            + GoogleStorageSheet.DEFAULT_RANGE_SEPARATOR
            + start_col
            + start_row
        )
        body = {"values": rows}
        result = (
            GoogleStorageSheet.SHEETS_SERVICE.spreadsheets()
            .values()
            .append(
                spreadsheetId=spreadsheet_id,
                range=range_name_start,
                valueInputOption="RAW",
                body=body,
            )
            .execute()
        )
        return result.get("tableRange")

    @GoogleAPI.ensure_credentials_and_write_limits
    def append_row_to_sheet(
        self,
        spreadsheet_id: str,
        sheet_name: str,
        row,
        start_row=SheetsStorageBase.DEFAULT_START_ROW,
        start_col=SheetsStorageBase.DEFAULT_START_COLUMN,
        end_range=SheetsStorageBase.DEFAULT_END_RANGE,
    ):
        value_input_option = "RAW"
        value_range_body = {"values": [row]}

        request = (
            GoogleStorageSheet.SHEETS_SERVICE.spreadsheets()
            .values()
            .append(
                spreadsheetId=spreadsheet_id,
                range=sheet_name,
                valueInputOption=value_input_option,
                body=value_range_body,
            )
        )
        response = request.execute()
        return response

    @GoogleAPI.ensure_credentials_and_write_limits
    def create_new_sheet(self, spreadsheet_id: str, sheet_name: str):
        requests = []
        requests.append({"addSheet": {"properties": {"title": sheet_name}}})
        body = {"requests": requests}
        return (
            GoogleStorageSheet.SHEETS_SERVICE.spreadsheets()
            .batchUpdate(spreadsheetId=spreadsheet_id, body=body)
            .execute()
        )

    @GoogleAPI.ensure_credentials_and_write_limits
    def create_temporal_new_sheet(self, spreadsheet_id: str, base_sheet_title: str):
        sheet_title = (
            base_sheet_title + "-" + mammut.get_str_format_timezone_aware_datetime_now()
        )
        sheet_title = sheet_title.replace(
            mammut.TIME_SEPARATOR, mammut.TIME_ALTERNATIVE_SEPARATOR
        )
        self.create_new_sheet(spreadsheet_id, sheet_title)
        return sheet_title

    @GoogleAPI.ensure_credentials_and_read_limits
    def get_temporal_sheets_from_new_to_old(self, spreadsheet_id, base_sheet_title):
        request = GoogleStorageSheet.SHEETS_SERVICE.spreadsheets().get(
            spreadsheetId=spreadsheet_id
        )
        response = request.execute()
        result = []
        for s in response["sheets"]:
            title = s["properties"]["title"]
            if base_sheet_title in title and len(base_sheet_title) != len(title):
                time_stamp_str = title[len(base_sheet_title) + 1 :]
                time_stamp_str = time_stamp_str.replace(
                    mammut.TIME_ALTERNATIVE_SEPARATOR, mammut.TIME_SEPARATOR
                )
                time_stamp = mammut.str_parse_datetime(time_stamp_str)
                result.append((s["properties"]["sheetId"], title, time_stamp))
        result = sorted(result, key=lambda i: i[2], reverse=True)
        return result

    @GoogleAPI.ensure_credentials_and_read_limits
    def get_sheet_id(self, spreadsheet_id, identifier):
        request = GoogleStorageSheet.SHEETS_SERVICE.spreadsheets().get(
            spreadsheetId=spreadsheet_id, ranges=identifier
        )
        response = request.execute()
        result = response["sheets"][0]["properties"]["sheetId"]
        return result

    @GoogleAPI.ensure_credentials_and_write_limits
    def update_row_from_spreadsheet(
        self, spreadsheet_id, sheet_name, row, start_row, start_col
    ):
        start_index = (
            sheet_name
            + GoogleStorageSheet.DEFAULT_RANGE_SEPARATOR
            + start_col
            + start_row
        )
        value_input_option = "RAW"
        value_range_body = {"values": [row]}
        request = (
            GoogleStorageSheet.SHEETS_SERVICE.spreadsheets()
            .values()
            .update(
                spreadsheetId=spreadsheet_id,
                range=start_index,
                valueInputOption=value_input_option,
                body=value_range_body,
            )
        )
        response = request.execute()
        return response

    @GoogleAPI.ensure_credentials_and_write_limits
    def update_rows_from_spreadsheet(
        self, spreadsheet_id, sheet_name, rows, start_row, start_col
    ):
        start_index = (
            sheet_name
            + GoogleStorageSheet.DEFAULT_RANGE_SEPARATOR
            + start_col
            + start_row
        )
        value_input_option = "RAW"
        value_range_body = {"values": rows}
        request = (
            GoogleStorageSheet.SHEETS_SERVICE.spreadsheets()
            .values()
            .update(
                spreadsheetId=spreadsheet_id,
                range=start_index,
                valueInputOption=value_input_option,
                body=value_range_body,
            )
        )
        response = request.execute()
        return response

    @GoogleAPI.ensure_credentials_and_write_limits
    def delete_rows_from_spreadsheet(
        self, spreadsheet_id, sheet_name, start_index, end_index
    ):
        sheet_id = self.get_sheet_id(spreadsheet_id, sheet_name)
        batch_update_spreadsheet_request_body = {
            "requests": [
                {
                    "deleteDimension": {
                        "range": {
                            "sheetId": sheet_id,
                            "dimension": "ROWS",
                            "startIndex": start_index,  # desde sin incluir
                            "endIndex": end_index,  # hasta, incluyendolo
                        }
                    }
                }
            ]
        }
        request = GoogleStorageSheet.SHEETS_SERVICE.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id, body=batch_update_spreadsheet_request_body
        )
        response = request.execute()
        return response

    @GoogleAPI.ensure_credentials_and_write_limits
    def delete_sheet(self, spreadsheet_id, sheet_name):
        sheet_id = self.get_sheet_id(spreadsheet_id, sheet_name)
        batch_update_spreadsheet_request_body = {
            "requests": [{"deleteSheet": {"sheetId": sheet_id,}}]
        }
        request = GoogleStorageSheet.SHEETS_SERVICE.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id, body=batch_update_spreadsheet_request_body
        )
        response = request.execute()
        return response
