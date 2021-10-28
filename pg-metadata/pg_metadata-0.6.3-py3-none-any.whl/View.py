#!/usr/bin/python
# -*- coding: utf-8 -*-

from pg_metadata._System import SEP
from pg_metadata.ACL     import ACL
from pg_metadata.Owner   import Owner
from pg_metadata.Comment import Comment
from pg_metadata.Export  import Export

QUERY_VIEW = """
    SELECT
        c.oid,
        trim(lower(n.nspname)) AS schema,
        trim(lower(c.relname)) AS name,
        trim(lower(r.rolname)) AS owner_name,
        trim(coalesce(obj_description(c.oid), '')) AS comment,
        pg_get_viewdef(c.oid, true) as definition,
        c.relacl::varchar[] AS acl,
        c.relkind = 'm' as is_materialized
    FROM pg_class c
    JOIN pg_namespace n ON
        n.oid = c.relnamespace AND
        n.nspname !~* '^pg_temp' AND
        n.nspname !~* '^pg_toast' AND
        n.nspname != ALL(%s)
    JOIN pg_roles r ON
        r.oid = c.relowner
    WHERE c.relkind in ('v','m')
    ORDER BY 2,3
"""

class View():
    def __init__(self, row={}):
        assert row is not None
        assert isinstance(row, dict)
        assert len(row.keys()) > 0

        self.Oid = row.get('oid')
        assert self.Oid is not None and self.Oid > 0

        self.Schema = row.get('schema') or ''
        self.Schema = self.Schema.strip()
        assert len(self.Schema) > 0

        self.Name = row.get('name') or ''
        self.Name = self.Name.strip()
        assert len(self.Name) > 0

        self.FullName = "%s.%s" % (self.Schema, self.Name)

        self.Definition = row.get('definition') or ''
        self.Definition = self.Definition.strip()
        assert len(self.Definition) > 0

        self.IsMaterialized = row.get("is_materialized")

        self.Path = [self.Schema, "view"]
        self.File = self.Name

        self.Owner = Owner(
            "TABLE",
            self.FullName,
            row.get("owner_name")
        )

        self.Comment = Comment(
            "MATERIALIZED VIEW" if self.IsMaterialized else "VIEW",
            self.FullName,
            row.get("comment")
        )

        self.ACL = ACL(
            "TABLE",
            self.FullName,
            self.Owner.Owner,
            row.get("acl")
        )

        self.Indexes = []

    def __str__(self):
        return self.FullName

    def DDL_Create(self, style=""):
        r = ""

        if self.IsMaterialized:
            r += "CREATE MATERIALIZED VIEW %s AS" % (self.FullName)
        else:
            r += "CREATE OR REPLACE VIEW %s AS" % (self.FullName)
        r += SEP
        r += self.Definition

        return r

    def DDL_Drop(self, style=""):
        if self.IsMaterialized:
            return 'DROP MATRIALIZED VIEW IF EXISTS %s;' % (self.FullName)
        else:
            return 'DROP VIEW IF EXISTS %s;' % (self.FullName)

    def DDL_Full(self, style=""):
        r = ''
        r += self.DDL_Drop(style)
        r += SEP
        r += SEP
        r += self.DDL_Create(style)
        r += SEP
        r += SEP
        r += self.Owner.DDL_Create(style)
        r += SEP
        r += self.ACL.DDL_Create(style)
        r += SEP
        r += SEP

        if self.Comment.IsExists:
            r += self.Comment.DDL_Create(style)
            r += SEP
            r += SEP

        for ind in sorted(self.Indexes, key=lambda x: x.FullName):
            r += ind.DDL_Create("%s  " % (SEP))
            r += SEP
            r += SEP

        return r.strip() + SEP

    def Export(self):
        """
            Export view for compare
        """
        name = "view_%s" % (self.FullName)

        # Sequence
        r = {
            name : Export(
                name        = name,
                type        = "view",
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

        for i in self.Indexes:
            r.update(i.Export("view"))

        return r
