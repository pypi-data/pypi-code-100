#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from pg_metadata._System import SEP, CheckPath

class Export():
    def __init__(self, name, type, parent, create, drop):
        """
            Class for export during compare
            @param name: Name of object in database objects dict
            @param type: Object type
            @param parent: Name of parent object
            @param create: Create script
            @param drop: Drop script
        """
        assert name is not None
        assert isinstance(name, str)
        assert len(name) > 0
        self.Name = name

        assert type is not None
        assert isinstance(type, str)
        assert len(type) > 0
        self.Type = type

        self.Parent = parent
        self.IsParent = self.Parent is None or len(str(self.Parent)) == 0

        assert create is not None
        assert isinstance(create, str)
        assert len(create) > 0
        self.Create = create

        assert drop is not None
        assert isinstance(drop, str)
        assert len(drop) > 0
        self.Drop = drop

    def WriteCreate(self, path):
        """
            Write CREATE script to file
            @param path: Path to folder
        """
        file_name = "%s_1_create.sql" % (self.Type)
        path = "/".join([path, file_name])

        with open(path, "a", encoding="utf8") as wf:
            wf.write(self.Create)
            wf.write(SEP)
            wf.write(SEP)

        print("CREATE", self.Name)

    def WriteReplace(self, path, old_drop=""):
        """
            Write REPLACE script to file
            @param path: Path to folder
        """
        if self.IsParent:
            return

        file_name = "%s_2_replace.sql" % (self.Type)
        path = "/".join([path, file_name])

        with open(path, "a", encoding="utf8") as wf:
            wf.write(old_drop)
            wf.write(SEP)
            wf.write(SEP)
            wf.write(self.Create)
            wf.write(SEP)
            wf.write(SEP)

        print("REPLACE", self.Name)

    def WriteDrop(self, path):
        """
            Write DROP script to file
            @param path: Path to folder
        """
        file_name = "%s_3_drop.sql" % (self.Type)
        path = "/".join([path, file_name])

        with open(path, "a", encoding="utf8") as wf:
            wf.write(self.Drop)
            wf.write(SEP)
            wf.write(SEP)

        print("DROP", self.Name)

    def WriteSeparateFile(self, path):
        """
            Write CREATE script as separate file
            @param path: Path to folder
        """
        if not self.IsParent:
            return

        path = "/".join([path, self.Type.lower()])
        CheckPath(path)

        file_name = self.Name.replace("%s_" % (self.Type.lower()), "")
        file_name = file_name if len(file_name) < 150 else file_name[0:150]
        file_name = "/".join([path, "%s.sql" % (file_name)])

        with open(file_name, "w", encoding="utf8") as wf:
            wf.write(self.Create)
