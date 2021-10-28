#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
from pg_metadata._System        import SEP
from pg_metadata.ACL            import ACL
from pg_metadata.Owner          import Owner
from pg_metadata.Comment        import Comment
from pg_metadata.TableSettings  import TableSettings
from pg_metadata.Export         import Export

class Table():
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

        self.Settings = []
        for o in (row.get("reloptions") or []):
            self.Settings.append(TableSettings(self.Schema, self.Name, o))

        self.HasOids = row.get('has_oids') or ''
        self.HasOids = self.HasOids.strip()
        assert len(self.HasOids) > 0
        self.HasOids = "OIDS=%s" % (str(self.HasOids).upper())
        self.Settings.append(TableSettings(self.Schema, self.Name, self.HasOids))

        self.Inherits = row.get('parent_table') or ''
        self.Inherits = self.Inherits.strip()

        self.Inherits = row.get("parent_table")
        if self.Inherits is not None and self.Inherits != '':
            self.Inherits = self.Inherits.strip()
        else:
            self.Inherits = None

        self.PartKey = row.get("part_key")
        if self.PartKey is not None and self.PartKey != "":
            self.PartKey = self.PartKey.strip()
        else:
            self.PartKey = None

        self.PartBorder = row.get("part_border")

        self.Path = [self.Schema, "table"]
        self.File = self.Name

        self.Owner = Owner(
            "TABLE",
            self.FullName,
            row.get("owner")
        )

        self.Comment = Comment(
            "TABLE",
            self.FullName,
            row.get("comment")
        )

        self.ACL = ACL(
            "TABLE",
            self.FullName,
            self.Owner.Owner,
            row.get("acl")
        )

        self.Columns     = []
        self.Constraints = []
        self.Indexes     = []
        self.Triggers    = []

    def __str__(self):
        return self.FullName

    def DDL_Drop(self, style=""):
        return 'DROP TABLE IF EXISTS %s;' % (self.FullName)

    def DDL_Create(self, style=""):
        r = ""
        r += "CREATE TABLE %s()" % (self.FullName)
        r += SEP

        if self.PartKey is not None:
            r += "PARTITION BY %s" % (self.PartKey)
            r += SEP

        if self.Inherits is not None:
            if self.PartBorder is not None:
                r += "PARTITION OF %s" % (self.Inherits)
                r += SEP
            else:
                r += "INHERITS ( %s )" % (self.Inherits)
                r += SEP

        if self.PartBorder is not None:
            r += self.PartBorder
            r += SEP

        r += "WITH ("
        r += SEP
        r += self.DDL_Settings(style)
        r += SEP
        r += ");"
        r += SEP

        return r

    def DDL_Settings(self, style=""):
        r = []

        for sts in sorted(self.Settings, key=lambda x: x.FullName):
            r.append(sts.DDL_Inner())

        return (",%s" % (SEP)).join(r)

    def DDL_Full(self, style=""):
        is_last_comma = len(self.Constraints) > 0

        r = ""
        r += self.DDL_Drop(style)
        r += SEP
        r += SEP

        r += "CREATE TABLE %s(" % (self.FullName)
        r += SEP

        for col in sorted(self.Columns, key=lambda x: x.OrderNum):
            r += col.QueryRaw(add_comma=is_last_comma, add_comment=True)
            r += SEP


        self.Constraints = sorted(self.Constraints, key=lambda x: x.SortKey)
        if len(self.Constraints) > 0:
            cns = [c.DDL_Inner() for c in self.Constraints]
            cns_sep = ",%s" % (SEP)
            r += cns_sep.join(cns)
            r += SEP

        r += ")"
        r += SEP

        if self.PartKey is not None:
            r += "PARTITION BY %s" % (self.PartKey)
            r += SEP

        if self.Inherits is not None:
            if self.PartBorder is not None:
                r += "PARTITION OF %s" % (self.Inherits)
                r += SEP
            else:
                r += "INHERITS ( %s )" % (self.Inherits)
                r += SEP

        if self.PartBorder is not None:
            r += self.PartBorder
            r += SEP

        r += "WITH ("
        r += SEP
        r += self.DDL_Settings(style)
        r += SEP
        r += ");"
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

        for col in self.Columns:
            cmt = col.QueryComment()
            if cmt is not None:
                r += col.QueryComment()
                r += SEP
        r += SEP

        for ind in sorted(self.Indexes, key=lambda x: x.FullName):
            r += ind.DDL_Create("%s  " % (SEP))
            r += SEP
            r += SEP

        for trg in sorted(self.Triggers, key=lambda x: x.FullName):
            r += trg.DDL_Create(style)
            r += SEP
            r += SEP

        return r.strip() + SEP

    def Export(self):
        """
            Export table for compare
        """
        name = "table_%s" % (self.FullName)

        # Sequence
        r = {
            name : Export(
                name        = name,
                type        = "table",
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
            r.update(i.Export("table"))

        return r

def QueryTable(version):
    if version in (9, 9):
        return """
            SELECT
                c.oid,
                trim(lower(n.nspname)) AS schema,
                trim(lower(c.relname)) AS name,
                trim(lower(r.rolname)) AS owner,
                trim(upper(c.relhasoids::varchar)) as has_oids,
                obj_description(c.oid) AS comment,
                case
                    when coalesce(trim(pc.relname), '') = '' then null
                    else pn.nspname || '.' || pc.relname
                end AS parent_table,
                null::varchar as part_border,
                null::varchar as part_key,
                c.relacl AS acl,
                c.reloptions
            FROM pg_class c
            JOIN pg_namespace n ON
                n.oid = c.relnamespace AND
                n.nspname !~* '^pg_temp' AND
                n.nspname !~* '^pg_toast'
            JOIN pg_roles r ON
                r.oid = c.relowner
            LEFT JOIN pg_inherits inh ON
                c.oid = inh.inhrelid
            LEFT JOIN pg_class pc ON
                pc.oid = inh.inhparent
            LEFT JOIN pg_namespace pn ON
                pn.oid = pc.relnamespace
            WHERE
                c.relkind in ('r','p') AND
                n.nspname != ALL(%s)
            ORDER BY 2,3
        """
    elif version in (10,11):
        return """
            SELECT
                c.oid,
                trim(lower(n.nspname)) AS schema,
                trim(lower(c.relname)) AS name,
                trim(lower(r.rolname)) AS owner,
                trim(upper(c.relhasoids::varchar)) as has_oids,
                obj_description(c.oid) AS comment,
                case
                    when coalesce(trim(pc.relname), '') = '' then null
                    else pn.nspname || '.' || pc.relname
                end AS parent_table,
                pg_get_expr(c.relpartbound, c.oid, true) as part_border,
                pg_get_partkeydef(c.oid) as part_key,
                c.relacl::varchar[] AS acl,
                c.reloptions
            FROM pg_class c
            JOIN pg_namespace n ON
                n.oid = c.relnamespace AND
                n.nspname !~* '^pg_temp' AND
                n.nspname !~* '^pg_toast'
            JOIN pg_roles r ON
                r.oid = c.relowner
            LEFT JOIN pg_inherits inh ON
                c.oid = inh.inhrelid
            LEFT JOIN pg_class pc ON
                pc.oid = inh.inhparent
            LEFT JOIN pg_namespace pn ON
                pn.oid = pc.relnamespace
            WHERE
                c.relkind in ('r','p') AND
                n.nspname != ALL(%s)
            ORDER BY 2,3
        """
    elif version in (12,14):
        return """
            SELECT
                c.oid,
                trim(lower(n.nspname)) AS schema,
                trim(lower(c.relname)) AS name,
                trim(lower(r.rolname)) AS owner,
                false::varchar as has_oids,
                obj_description(c.oid) AS comment,
                case
                    when coalesce(trim(pc.relname), '') = '' then null
                    else pn.nspname || '.' || pc.relname
                end AS parent_table,
                pg_get_expr(c.relpartbound, c.oid, true) as part_border,
                pg_get_partkeydef(c.oid) as part_key,
                c.relacl::varchar[] AS acl,
                c.reloptions
            FROM pg_class c
            JOIN pg_namespace n ON
                n.oid = c.relnamespace AND
                n.nspname !~* '^pg_temp' AND
                n.nspname !~* '^pg_toast'
            JOIN pg_roles r ON
                r.oid = c.relowner
            LEFT JOIN pg_inherits inh ON
                c.oid = inh.inhrelid
            LEFT JOIN pg_class pc ON
                pc.oid = inh.inhparent
            LEFT JOIN pg_namespace pn ON
                pn.oid = pc.relnamespace
            WHERE
                c.relkind in ('r','p') AND
                n.nspname != ALL(%s)
            ORDER BY 2,3
        """
