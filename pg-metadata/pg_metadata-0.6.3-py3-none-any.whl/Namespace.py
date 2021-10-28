#!/usr/bin/python
# -*- coding: utf-8 -*-

from pg_metadata._System import SEP, STYLE_PGADMIN3
from pg_metadata.ACL     import ACL
from pg_metadata.Owner   import Owner
from pg_metadata.Comment import Comment
from pg_metadata.Export  import Export

QUERY_NAMESPACE = """
    SELECT
        n.oid,
        trim(lower(n.nspname)) AS name,
        trim(lower(r.rolname)) AS owner,
        trim(coalesce(obj_description(n.oid), '')) AS comment,
        n.nspacl::varchar[] as acl
    FROM pg_namespace n
    JOIN pg_roles r ON
        r.oid = n.nspowner
    WHERE
        n.nspname != ALL(%s) AND
        n.nspname !~* '^pg_temp' AND
        n.nspname !~* '^pg_toast'
    ORDER BY 2,3
"""

class Namespace():
    def __init__(self, row={}):
        assert row is not None
        assert isinstance(row, dict)
        assert len(row.keys()) > 0

        self.Oid = row.get("oid")
        assert self.Oid is not None and self.Oid > 0

        self.Name = row.get("name") or ""
        self.Name = self.Name.strip()
        assert len(self.Name) > 0

        self.Path = [self.Name]
        self.File = self.Name

        self.Owner = Owner(
            "SCHEMA",
            self.Name,
            row.get("owner")
        )

        self.Comment = Comment(
            "SCHEMA",
            self.Name,
            row.get("comment")
        )

        self.ACL = ACL(
            "SCHEMA",
            self.Name,
            self.Owner.Owner,
            row.get("acl")
        )

    def __str__(self):
        return self.Name

    def DDL_Header(self, style=""):
        return "Schema: %s" % (self.Name)

    def DDL_Create(self, style=""):
        r = ""
        r += "CREATE SCHEMA %s;" % (self.Name)
        return r

    def DDL_Drop(self, style=""):
        if style == STYLE_PGADMIN3:
            return "-- DROP SCHEMA %s" % (self.Name)
        else:
            return "DROP SCHEMA IF EXISTS %s;" % (self.Name)

    def DDL_Full(self, style=""):
        r = ""

        if style == "pgadmin3":
            r += "-- %s" % (self.DDL_Header(style))
            r += SEP
            r += SEP
            r += "-- %s" % (self.DDL_Drop(style))
            r += SEP
            r += SEP
            r += self.DDL_Create(style)
            r += SEP
            r += SEP
            r += self.Owner.DDL_Create()
            r += SEP
            r += self.ACL.DDL_Create()
            r += SEP

            if self.Comment.IsExists:
                r += self.Comment.DDL_Create()
                r += SEP

        else:
            r += "-- %s" % (self.DDL_Header(style))
            r += SEP
            r += SEP
            r += "-- %s" % (self.DDL_Drop(style))
            r += SEP
            r += SEP
            r += self.DDL_Create(style)
            r += SEP
            r += SEP
            r += self.Owner.DDL_Create(style)
            r += SEP
            r += SEP
            r += self.ACL.DDL_Create()
            r += SEP
            r += SEP

            if self.Comment.IsExists:
                r += self.Comment.DDL_Create()
                r += SEP

        return r.strip() + SEP

    def Export(self):
        """
            Export namespace for compare
        """
        name = "namespace_%s" % (self.Name)

        # Sequence
        r = {
            name : Export(
                name        = name,
                type        = "namespace",
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
