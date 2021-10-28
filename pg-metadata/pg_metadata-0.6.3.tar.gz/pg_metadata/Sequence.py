#!/usr/bin/python
# -*- coding: utf-8 -*-

from pg_metadata._System import SEP
from pg_metadata.ACL     import ACL
from pg_metadata.Owner   import Owner
from pg_metadata.Comment import Comment
from pg_metadata.Export  import Export

QUERY_SEQUENCE = """
    SELECT
        c.oid,
        trim(lower(n.nspname)) AS schema,
        trim(lower(c.relname)) AS name,
        trim(lower(r.rolname)) AS owner,
        trim(coalesce(obj_description(c.oid), '')) AS comment,
        c.relacl::varchar[] AS acl,
        s.increment,
        s.minimum_value,
        s.maximum_value,
        s.cycle_option = 'YES' AS is_cycle,
        1 AS start,
        1 AS cache
    FROM pg_class c
    JOIN pg_namespace n ON
        n.oid = c.relnamespace AND
        n.nspname !~* '^pg_temp' AND
        n.nspname !~* '^pg_toast' AND
        n.nspname != ALL(%s)
    JOIN pg_roles r ON
        r.oid = c.relowner
    JOIN information_schema.sequences s ON
        s.sequence_schema = n.nspname and
        s.sequence_name = c.relname
    WHERE c.relkind = 'S'
    ORDER BY 2,3
"""

class Sequence():
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

        self.Increment = row.get("increment")
        self.MinValue  = row.get("minimum_value")
        self.MaxValue  = row.get("maximum_value")
        self.IsCycle   = row.get("is_cycle")
        self.Cache     = row.get("cache")

        self.Path = [self.Schema, "sequence"]
        self.File = self.Name

        self.Owner = Owner(
            "TABLE",
            self.FullName,
            row.get("owner")
        )

        self.Comment = Comment(
            "SEQUENCE",
            self.FullName,
            row.get("comment")
        )

        self.ACL = ACL(
            "SEQUENCE",
            self.FullName,
            self.Owner.Owner,
            row.get("acl")
        )

    def __str__(self):
        return self.FullName

    def DDL_Create(self, style=""):
        r = ""
        r += "CREATE SEQUENCE %s" % (self.FullName)
        r += SEP
        r += "  INCREMENT %s" % (self.Increment)
        r += SEP
        r += "  MINVALUE %s" % (self.MinValue)
        r += SEP
        r += "  MAXVALUE %s" % (self.MaxValue)
        r += SEP
        r += "  START %s" % (1)
        r += SEP
        r += "  CACHE %s" % (self.Cache)
        r += SEP

        if self.IsCycle:
            r += "  CYCLE"

        return r.strip() + ";"

    def DDL_Drop(self, style=""):
        return 'DROP SEQUENCE IF EXISTS %s;' % (self.FullName)

    def DDL_Full(self, style=""):
        r = ""

        if style == "pgadmin3":
            r += "-- Sequence: %s" % (self.FullName)
            r += SEP
            r += SEP
            r += "-- %s" % (self.DDL_Drop(style))
            r += SEP
            r += SEP
            r += self.DDL_Create(style)
            r += SEP
            r += self.Owner.DDL_Create(style)
            r += SEP
            r += self.ACL.DDL_Create(style)
            r += SEP

            if self.Comment.IsExists:
                r += self.Comment.DDL_Create(style)
                r += SEP

        else:

            r += "-- Sequence: %s" % (self.FullName)
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
            r += self.ACL.DDL_Create(style)
            r += SEP
            r += SEP

            if self.Comment.IsExists:
                r += self.Comment.DDL_Create(style)
                r += SEP

        return r.strip() + SEP

    def Export(self):
        """
            Export sequence for compare
        """
        name = "sequence_%s" % (self.FullName)

        # Sequence
        r = {
            name : Export(
                name        = name,
                type        = "sequence",
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
