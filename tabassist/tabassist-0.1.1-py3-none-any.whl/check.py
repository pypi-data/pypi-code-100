# coding: utf-8
"""Check styleguide for workbook elements."""
import click
import re
from inspect import getmembers, isfunction
from tableaudocumentapi import Field

from tabassist.error import Error


class CheckField():
    """Checks for datasource's field in workbook."""

    def __init__(self, field: Field) -> None:
        """Initilize class for given Field object from tableaudocumentapi package."""
        self._field = field
        self.field_name = self._set_field_name()

    def _set_field_name(self):
        if self._field.caption is not None:
            return self._field.caption
        else:
            field_name = self._field.name
            return field_name.replace('[', '').replace(']', '')

    def _is_parameter(self):
        """Return True if field is a parameter."""
        if 'parameter' in self._field.id.lower():
            return True
        else:
            return False

    def run(self):
        """Start checks for current field."""
        if self._field.name != '[:Measure Names]':
            for cls_method_name, cls_method in getmembers(CheckField, isfunction):
                if cls_method_name.startswith('check_'):
                    yield cls_method(self)

    def check_field_in_lowercase(self):
        """Check if field name not in lowercase."""
        for letter in self.field_name:
            if letter.isupper():
                return Error('T100',
                             'field not in lowercase',
                             self.field_name)

    def check_trailing_witespace(self):
        """Check if field name contains trailing whitespace."""
        if self.field_name[0] == ' ' or self.field_name[-1] == ' ':
            return Error('T101',
                         'field has trailing whitespace',
                         self.field_name)

    def check_non_allowed_symbol(self):
        """Check if field name has non allowed symbols."""
        if bool(re.search(r'[^a-zA-Z0-9_\s%]', self.field_name)):
            return Error('T102',
                         'field has non allowed symbol(s)',
                         self.field_name)

    def check_non_unique_name(self):
        """Check if field name wasn't renamed after duplicating."""
        if '(copy)' in self.field_name:
            return Error('T103',
                         'field has \'(copy)\' as a part of name',
                         self.field_name)

    def _comment_exist(self):
        if self._field.calculation and \
           self._field.caption:
            lines = self._field.calculation.split('\n')
            for line in lines:
                if line[:2] == '//':
                    return True
            return False

    def check_comment_exist(self):
        """Check if inline comment exist in field formula (calculation)."""
        if self._comment_exist() is False and \
           self._is_parameter() is False:
            return Error('T104',
                         'field doesn’t have comment',
                         self.field_name)

    def check_comment_position(self):
        """Check if inline comment starts from first line."""
        if self._comment_exist() and \
           self._field.calculation:
            if self._field.calculation[:2] != '//':
                return Error('T105',
                             'field has inline comment '
                             'which doesn’t start from first line',
                             self.field_name)

    def check_unused_by_worksheet(self):
        """Check if field is unused by any worksheet."""
        if len(self._field.worksheets) == 0 and \
           self._is_parameter() is False:
            return Error('T106',
                         'field doesn’t used by any worksheet',
                         self.field_name)
