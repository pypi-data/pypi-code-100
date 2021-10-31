# coding=utf-8
from collections import defaultdict
import configparser
import os
from pkg_resources import resource_string
import re
from typing import Dict

from mammut.common.storage.storage_base import SheetsStorageBase, SlidesStorageBase
from mammut.common.storage.embedded_storage_excel import EmbeddedStorageExcel
from mammut.common.storage.emdedded_storage_powerpoint import EmbeddedStoragePowerPoint
from mammut.common.storage.google_storage_sheet import GoogleStorageSheet
from mammut.common.storage.google_storage_slide import GoogleStorageSlide


class StorageManager:
    __STORAGE_INFERRED__: Dict[str, bool] = defaultdict(lambda: False)
    __USE_LOCAL_STORAGE__: Dict[str, bool] = defaultdict(lambda: False)

    current_sheets_implementation: SheetsStorageBase = None
    current_slides_implementation: SlidesStorageBase = None

    def __init__(self, storage_path=""):
        self.configurations = configparser.ConfigParser()
        self.configurations.read_string(
            resource_string("mammut.resources", "features.ini").decode("utf-8")
        )
        self.configurations.read(["data/features.ini", "features.ini"])

        if storage_path == "":
            if not os.getenv("LOCAL_STORAGE_BASE_FOLDER") is None:
                self.local_storage_path = os.getenv("LOCAL_STORAGE_BASE_FOLDER")
            else:
                self.local_storage_path = self.configurations["STORAGE"][
                    "local_storage_base_folder"
                ]
        else:
            self.local_storage_path = storage_path

        self.local_storage_regex = self.configurations["STORAGE"]["local_storage_regex"]
        self.google_storage_regex = self.configurations["STORAGE"][
            "google_storage_regex"
        ]

    # Infer which is the right storage for that running notebook.
    def infer_spreadsheet_storage(self, documentId: str):
        if not StorageManager.__STORAGE_INFERRED__[documentId]:
            if re.match(self.local_storage_regex, documentId) is not None:
                self.current_sheets_implementation = EmbeddedStorageExcel(
                    self.local_storage_path
                )
                StorageManager.__STORAGE_INFERRED__[documentId] = True
                StorageManager.__USE_LOCAL_STORAGE__[documentId] = True
                return self.current_sheets_implementation
            elif re.match(self.google_storage_regex, documentId) is not None:
                self.current_sheets_implementation = GoogleStorageSheet()
                StorageManager.__STORAGE_INFERRED__[documentId] = True
                StorageManager.__USE_LOCAL_STORAGE__[documentId] = False
                return self.current_sheets_implementation
            else:
                raise Exception("Unknown package spreadsheets data storage")
        else:
            if StorageManager.__USE_LOCAL_STORAGE__[documentId]:
                if self.current_sheets_implementation is None:
                    self.current_sheets_implementation = EmbeddedStorageExcel(
                        self.local_storage_path
                    )
                return self.current_sheets_implementation
            else:
                if self.current_sheets_implementation is None:
                    self.current_sheets_implementation = GoogleStorageSheet()
                return self.current_sheets_implementation

    def infer_slides_storage(self, documentId: str):
        if not StorageManager.__STORAGE_INFERRED__[documentId]:
            if re.match(self.local_storage_regex, documentId) is not None:
                self.current_slides_implementation = EmbeddedStoragePowerPoint(
                    self.local_storage_path
                )
                StorageManager.__STORAGE_INFERRED__[documentId] = True
                StorageManager.__USE_LOCAL_STORAGE__[documentId] = True
                return self.current_slides_implementation
            elif re.match(self.google_storage_regex, documentId) is not None:
                self.current_slides_implementation = GoogleStorageSlide()
                StorageManager.__STORAGE_INFERRED__[documentId] = True
                StorageManager.__USE_LOCAL_STORAGE__[documentId] = False
                return self.current_slides_implementation
            else:
                raise Exception("Unknown package slides data storage")
        else:
            if StorageManager.__USE_LOCAL_STORAGE__[documentId]:
                if self.current_slides_implementation is None:
                    self.current_slides_implementation = EmbeddedStoragePowerPoint(
                        self.local_storage_path
                    )
                return self.current_slides_implementation
            else:
                if self.current_slides_implementation is None:
                    self.current_slides_implementation = GoogleStorageSlide()
                return self.current_slides_implementation

    @staticmethod
    def __add_local_storage_sheet_file_extension(documentId: str):
        if StorageManager.__USE_LOCAL_STORAGE__[documentId]:
            if documentId.endswith(".xlsx"):
                return documentId
            else:
                return documentId + ".xlsx"
        else:
            return documentId

    @staticmethod
    def __add_local_storage_presentation_file_extension(documentId: str):
        if StorageManager.__USE_LOCAL_STORAGE__[documentId]:
            if documentId.endswith(".pptx"):
                return documentId
            else:
                return documentId + ".pptx"
        else:
            return documentId

    def get_spreadsheet_as_dataframe(
        self,
        spreadsheet_id: str,
        sheet_name,
        start_column: str,
        start_row: str,
        end_range: str,
        transpose: bool = False,
    ):
        local_spreadsheet_id = self.__add_local_storage_sheet_file_extension(
            spreadsheet_id
        )
        return self.infer_spreadsheet_storage(
            local_spreadsheet_id
        ).get_spreadsheet_as_dataframe(
            local_spreadsheet_id,
            sheet_name,
            start_column,
            start_row,
            end_range,
            transpose,
        )

    def add_rows_to_spreadsheet(
        self,
        spreadsheet_id: str,
        sheet_name: str,
        rows,
        start_row=SheetsStorageBase.DEFAULT_START_ROW,
        start_col=SheetsStorageBase.DEFAULT_START_COLUMN,
        end_range=SheetsStorageBase.DEFAULT_END_RANGE,
    ):
        local_spreadsheet_id = self.__add_local_storage_sheet_file_extension(
            spreadsheet_id
        )
        return self.infer_spreadsheet_storage(
            local_spreadsheet_id
        ).add_rows_to_spreadsheet(
            local_spreadsheet_id, sheet_name, rows, start_row, start_col, end_range
        )

    def append_row_to_sheet(
        self,
        spreadsheet_id: str,
        sheet_name: str,
        row,
        start_row=SheetsStorageBase.DEFAULT_START_ROW,
        start_col=SheetsStorageBase.DEFAULT_START_COLUMN,
        end_range=SheetsStorageBase.DEFAULT_END_RANGE,
    ):
        local_spreadsheet_id = self.__add_local_storage_sheet_file_extension(
            spreadsheet_id
        )
        return self.infer_spreadsheet_storage(local_spreadsheet_id).append_row_to_sheet(
            local_spreadsheet_id, sheet_name, row, start_row, start_col, end_range
        )

    def create_new_sheet(self, spreadsheet_id: str, sheet_name: str):
        local_spreadsheet_id = self.__add_local_storage_sheet_file_extension(
            spreadsheet_id
        )
        return self.infer_spreadsheet_storage(local_spreadsheet_id).create_new_sheet(
            local_spreadsheet_id, sheet_name
        )

    def create_temporal_new_sheet(self, spreadsheet_id: str, base_sheet_title: str):
        local_spreadsheet_id = self.__add_local_storage_sheet_file_extension(
            spreadsheet_id
        )
        return self.infer_spreadsheet_storage(
            local_spreadsheet_id
        ).create_temporal_new_sheet(local_spreadsheet_id, base_sheet_title)

    def get_temporal_sheets_from_new_to_old(self, spreadsheet_id, base_sheet_title):
        local_spreadsheet_id = self.__add_local_storage_sheet_file_extension(
            spreadsheet_id
        )
        return self.infer_spreadsheet_storage(
            local_spreadsheet_id
        ).get_temporal_sheets_from_new_to_old(local_spreadsheet_id, base_sheet_title)

    def get_sheet_id(self, spreadsheet_id, identifier):
        local_spreadsheet_id = self.__add_local_storage_sheet_file_extension(
            spreadsheet_id
        )
        return self.infer_spreadsheet_storage(local_spreadsheet_id).get_sheet_id(
            local_spreadsheet_id, identifier
        )

    def update_row_from_spreadsheet(
        self, spreadsheet_id, sheet_name, row, start_row, start_col
    ):
        local_spreadsheet_id = self.__add_local_storage_sheet_file_extension(
            spreadsheet_id
        )
        return self.infer_spreadsheet_storage(
            local_spreadsheet_id
        ).update_row_from_spreadsheet(
            local_spreadsheet_id, sheet_name, row, start_row, start_col
        )

    def update_rows_from_spreadsheet(
        self, spreadsheet_id, sheet_name, rows, start_row, start_col
    ):
        local_spreadsheet_id = self.__add_local_storage_sheet_file_extension(
            spreadsheet_id
        )
        return self.infer_spreadsheet_storage(
            local_spreadsheet_id
        ).update_rows_from_spreadsheet(
            local_spreadsheet_id, sheet_name, rows, start_row, start_col
        )

    def delete_rows_from_spreadsheet(
        self, spreadsheet_id, sheet_name, start_index, end_index
    ):
        local_spreadsheet_id = self.__add_local_storage_sheet_file_extension(
            spreadsheet_id
        )
        return self.infer_spreadsheet_storage(
            local_spreadsheet_id
        ).delete_rows_from_spreadsheet(
            local_spreadsheet_id, sheet_name, start_index, end_index
        )

    def delete_sheet(self, spreadsheet_id, sheet_name):
        local_spreadsheet_id = self.__add_local_storage_sheet_file_extension(
            spreadsheet_id
        )
        return self.infer_spreadsheet_storage(local_spreadsheet_id).delete_sheet(
            local_spreadsheet_id, sheet_name
        )

    def get_slide_elements(self, presentation_id):
        local_presentation_id = self.__add_local_storage_presentation_file_extension(
            presentation_id
        )
        return self.infer_slides_storage(local_presentation_id).get_slide_elements(
            local_presentation_id
        )

    def get_slides_metadata_re_string(self, presentation_id):
        local_spreadsheet_id = self.__add_local_storage_sheet_file_extension(
            presentation_id
        )
        return self.infer_slides_storage(
            local_spreadsheet_id
        ).get_slides_metadata_re_string()
