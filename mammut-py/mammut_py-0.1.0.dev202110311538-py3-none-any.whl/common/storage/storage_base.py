# coding=utf-8


class SheetsStorageBase(object):
    DEFAULT_START_COLUMN = "A"
    DEFAULT_START_ROW = "1"
    DEFAULT_END_RANGE = "Z"

    def __init__(self, storage_path=""):
        self.storage_path = storage_path

    def get_spreadsheet_as_dataframe(
        self,
        spreadsheet_id: str,
        sheet_name,
        start_column: str,
        start_row: str,
        end_range: str,
        transpose: bool = False,
    ):
        pass

    def add_rows_to_spreadsheet(
        self,
        spreadsheet_id: str,
        sheet_name: str,
        rows,
        start_row=DEFAULT_START_ROW,
        start_col=DEFAULT_START_COLUMN,
        end_range=DEFAULT_END_RANGE,
    ):
        pass

    def append_row_to_sheet(
        self,
        spreadsheet_id: str,
        sheet_name: str,
        row,
        start_row=DEFAULT_START_ROW,
        start_col=DEFAULT_START_COLUMN,
        end_range=DEFAULT_END_RANGE,
    ):
        pass

    def create_new_sheet(self, spreadsheet_id: str, sheet_name: str):
        pass

    def create_temporal_new_sheet(self, spreadsheet_id: str, base_sheet_title: str):
        pass

    def get_temporal_sheets_from_new_to_old(self, spreadsheet_id, base_sheet_title):
        pass

    def get_sheet_id(self, spreadsheet_id, identifier):
        pass

    def update_row_from_spreadsheet(
        self, spreadsheet_id, sheet_name, row, start_row, start_col
    ):
        pass

    def update_rows_from_spreadsheet(
        self, spreadsheet_id, sheet_name, rows, start_row, start_col
    ):
        pass

    def delete_rows_from_spreadsheet(
        self, spreadsheet_id, sheet_name, start_index, end_index
    ):
        pass

    def delete_sheet(self, spreadsheet_id, sheet_name):
        pass


class SlidesStorageBase(object):
    slides_metadata_re_string = "(sheet-id|Sheet-id|SHEET-ID)[ ]*->[ ]*([a-zA-Z0-9-_]+)"

    def __init__(self, storage_path=""):
        self.storage_path = storage_path

    def get_slide_elements(self, presentation_id):
        pass

    def get_slides_metadata_re_string(self):
        return self.slides_metadata_re_string
