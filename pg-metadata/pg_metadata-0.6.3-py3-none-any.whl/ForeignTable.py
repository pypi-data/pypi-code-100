#!/usr/bin/python
# -*- coding: utf-8 -*-

from pg_metadata._System import SEP, STYLE_PGADMIN3
from pg_metadata.ACL     import ACL
from pg_metadata.Owner   import Owner
from pg_metadata.Comment import Comment
from pg_metadata.Export  import Export

QUERY_FOREIGN_TABLE = """
    select
        c.oid,
        n.nspname as schema_name,
        c.relname as table_name,
        o.rolname as owner_name,
        s.srvname as server_name,
        t.ftoptions as options,
        obj_description(c.oid) AS comment,
        c.relacl::varchar[] AS acl,
        (
            select array_agg(concat_ws(' ',
                a.attname,
                trim(lower(format_type(a.atttypid, a.atttypmod))),
                case when a.attnotnull then 'NOT NULL' end
            ))
            from pg_attribute a
            where
                a.attrelid = c.oid and
                a.attnum > 0
        ) as columns_list
    from pg_foreign_table t
    join pg_foreign_server s on
        s.oid = t.ftserver
    join pg_class c on
        c.oid = t.ftrelid
    join pg_roles o on
        o.oid = c.relowner
    join pg_namespace n on
        n.oid = c.relnamespace AND
        n.nspname !~* '^pg_temp' AND
        n.nspname !~* '^pg_toast' AND
        n.nspname != ALL(%s)
"""

class ForeignTable():
    def __init__(self, row={}):
        assert row is not None
        assert isinstance(row, dict)
        assert len(row.keys()) > 0

        self.Schema = row.get("schema_name")
        assert self.Schema is not None
        self.Schema = self.Schema.strip().lower()
        assert len(self.Schema) > 0

        self.Name = row.get('table_name')
        assert self.Name is not None
        self.Name = self.Name.strip().lower()
        assert len(self.Name) > 0

        self.FullName = "%s.%s" % (self.Schema, self.Name)

        self.Server = row.get('server_name')
        assert self.Server is not None
        self.Server = self.Server.strip()
        assert len(self.Server) > 0

        self.Options = row.get("options")

        self.Path = [self.Schema, "foreign_table"]
        self.File = self.Name

        self.Owner = Owner(
            "FOREIGN TABLE",
            self.FullName,
            row.get("owner_name")
        )

        self.Comment = Comment(
            "FOREIGN TABLE",
            self.FullName,
            row.get("comment")
        )

        self.ACL = ACL(
            "TABLE",
            self.FullName,
            self.Owner.Owner,
            row.get("acl")
        )

        self.Columns = row.get("columns_list")

    def __str__(self):
        return self.Name

    def DDL_Drop(self, style=""):
        return 'DROP FOREIGN TABLE IF EXISTS %s;' % (self.FullName)

    def DDL_Full(self, style=""):
        r = ""
        r += "-- Foreign Table: %s" % (self.FullName)
        r += SEP
        r += SEP
        r += "-- %s" % (self.DDL_Drop(style))
        r += SEP
        r += SEP
        r += "CREATE FOREIGN TABLE %s(" % (self.FullName)
        r += SEP
        r += self.DDL_Columns(style)
        r += SEP
        r += ")"
        r += SEP
        r += "SERVER %s" % (self.Server)
        r += SEP
        r += "OPTIONS("
        r += SEP
        r += self.DDL_Options(style)
        r += SEP
        r += ");"
        r += SEP
        r += SEP

        if self.Owner.Owner is not None:
            r += self.Owner.DDL_Create(style)
            r += SEP

        if len(self.ACL.Grants.keys()) > 0:
            r += self.ACL.DDL_Create(style)
            r += SEP

        if self.Comment.IsExists:
            r += SEP
            r += self.Comment.DDL_Create(style)
            r += SEP

        return r.strip() + SEP

    def DDL_Options(self, style=""):
        result = []

        for o in sorted(self.Options):
            o = o.split("=")
            if len(o) != 2:
                continue
            result.append("    %s '%s'" % (o[0], o[1]))

        separator = ",%s" % (SEP)
        return separator.join(result)

    def DDL_Columns(self, style=""):
        result = []
        for col in self.Columns:
            result.append("    %s" % (col))
        separator = ",%s" % (SEP)
        return separator.join(result)

    def Export(self):
        """
            Export foreign table for compare
        """
        name = "foreign_table_%s" % (self.FullName)

        # Sequence
        r = {
            name : Export(
                name        = name,
                type        = "foreign_table",
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
