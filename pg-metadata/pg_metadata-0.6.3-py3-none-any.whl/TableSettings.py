#!/usr/bin/python
# -*- coding: utf-8 -*-

class TableSettings():
    def __init__(self, schema_name, table_name, setting):
        self.Schema = schema_name or ''
        self.Schema = self.Schema.strip().lower()
        assert len(self.Schema) > 0

        self.Table = table_name or ''
        self.Table = self.Table.strip().lower()
        assert len(self.Table) > 0

        self.FullTable = '%s.%s' % (self.Schema, self.Table)

        setting = setting or ''
        setting = setting.strip().lower()
        assert len(setting) > 0
        assert setting.find('=') >= 0

        self.Field = setting.split('=')[0].strip().upper()
        self.Value = setting.split('=')[1].strip().upper()

        self.FullName = '%s.%s' % (self.FullTable, self.Field)

    def __str__(self):
        return "%s=%s" % (self.Field, self.Value)

    def DDL_Inner(self, style=""):
        return "  %s=%s" % (self.Field, self.Value)

    def DDL_Drop(self, style=""):
        return """ALTER TABLE %s RESET (%s);""" % (
            self.FullTable, self.Field)

    def DDL_Create(self, style=""):
        return """ALTER TABLE %s SET (%s = %s);""" % (
            self.FullTable, self.Field, self.Value)
