#!/usr/bin/python
# -*- coding: utf-8 -*-

from pg_metadata._System import SEP
from pg_metadata.ACL     import ACL
from pg_metadata.Owner   import Owner
from pg_metadata.Comment import Comment
from pg_metadata.Export  import Export

QUERY_FOREIGN_SERVER = """
    select
        s.oid,
        s.srvname as server_name,
        w.fdwname as fdw_name,
        o.rolname as owner_name,
        s.srvoptions as options,
        s.srvacl::varchar[] AS acl,
        obj_description(s.oid) AS comment
    from pg_foreign_server s
    join pg_roles o on
        o.oid = s.srvowner
    join pg_foreign_data_wrapper w on
        w.oid = s.srvfdw
"""

class ForeignServer():
    def __init__(self, row={}):
        assert row is not None
        assert isinstance(row, dict)
        assert len(row.keys()) > 0

        self.Schema = "_foreign"

        self.Name = row.get('server_name')
        assert self.Name is not None
        self.Name = self.Name.strip().lower()
        assert len(self.Name) > 0

        self.FDW = row.get('fdw_name')
        assert self.FDW is not None
        self.FDW = self.FDW.strip().lower()
        assert len(self.FDW) > 0

        self.Options = row.get("options")

        self.Path = [self.Schema, "server"]
        self.File = self.Name

        self.Owner = Owner(
            "SERVER",
            self.Name,
            row.get("owner_name")
        )

        self.Comment = Comment(
            "SERVER",
            self.Name,
            row.get("comment")
        )

        self.ACL = ACL(
            "FOREIGN SERVER",
            self.Name,
            self.Owner.Owner,
            row.get("acl")
        )

    def __str__(self):
        return self.Name

    def DDL_Drop(self, style=""):
        return 'DROP SERVER IF EXISTS %s;' % (self.Name)

    def DDL_Full(self, style=""):
        r = ""
        r += "-- Server: %s" % (self.Name)
        r += SEP
        r += SEP
        r += "-- %s" % (self.DDL_Drop(style))
        r += SEP
        r += SEP
        r += "CREATE SERVER %s" % (self.Name)
        r += SEP
        r += "FOREIGN DATA WRAPPER %s" % (self.FDW)
        r += SEP
        r += "OPTIONS("
        r += SEP
        r += self.DDL_Options(style)
        r += SEP
        r += ");"
        r += SEP
        r += SEP
        r += self.Owner.DDL_Create(style)
        r += SEP
        r += self.ACL.DDL_Create(style)
        r += SEP

        if self.Comment.IsExists:
            r += self.Comment.DDL_Create(style)
            r += SEP

        return r.strip() + SEP

    def DDL_Options(self, style=""):
        result = []

        for o in sorted(self.Options):
            o = o.split("=")
            if len(o) != 2:
                continue
            result.append("    %s = '%s'" % (o[0], o[1]))

        separator = ",%s" % (SEP)
        return separator.join(result)

    def Export(self):
        """
            Export foreign server for compare
        """
        name = "foreign_server_%s" % (self.Name)

        # Sequence
        r = {
            name : Export(
                name        = name,
                type        = "foreign_server",
                parent      = None,
                create      = self.DDL_Full(),
                drop        = self.DDL_Drop()
            )
        }

        # Grants
        r.update(self.ACL.Export())

        # Owner
        r.update(self.Owner.Export())

        # Comment
        r.update(self.Comment.Export())

        return r
