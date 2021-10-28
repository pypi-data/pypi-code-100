#!/usr/bin/python
# -*- coding: utf-8 -*-

from pg_metadata._System import SEP
from pg_metadata.ACL     import ACL
from pg_metadata.Owner   import Owner
from pg_metadata.Comment import Comment
from pg_metadata.Export  import Export

class Function():
    def __init__(self, row={}):
        assert row is not None
        assert isinstance(row, dict)
        assert len(row.keys()) > 0

        self.Oid = row.get('oid')
        assert self.Oid is not None and self.Oid > 0

        self.Schema = row.get('schema') or ''
        self.Schema = self.Schema.strip()
        assert len(self.Schema) > 0

        self.Name = row.get('proc') or ''
        self.Name = self.Name.strip()
        assert len(self.Name) > 0

        self.ArgsInTypes = row.get('args_in_types') or ''
        self.ArgsInTypes = self.ArgsInTypes.strip()

        self.FullName = "%s.%s" % (self.Schema, self.Name)

        self.NameWithParams = "%s.%s(%s)" % (self.Schema, self.Name, self.ArgsInTypes)

        self.ArgsIn = row.get('args_in') or ''
        self.ArgsIn = self.ArgsIn.strip()

        self.ArgsOut = row.get('args_out') or ''
        self.ArgsOut = self.ArgsOut.strip()

        self.Cost = row.get('cost') or 0
        self.Cost = self.Cost

        self.Rows = row.get('rows') or 0
        self.Rows = self.Rows

        self.Language = row.get('lang') or ''
        self.Language = self.Language.strip()
        assert len(self.Language) > 0

        self.Volatility = row.get('volatility') or ''
        self.Volatility = self.Volatility.strip()
        assert len(self.Volatility) > 0

        self.HasDuplicate = row.get('has_duplicate') or False
        self.IsTrigger = row.get('is_trigger') or False
        self.IsRecord = row.get('is_record') or False

        self.Code = row.get('code') or ''
        self.Code = self.Code.strip()
        assert len(self.Code) > 0

        self.Folder = 'triggers' if self.IsTrigger else 'functions'
        self.Path = [self.Schema, self.Folder]
        self.File = self.Name

        self.Owner = Owner(
            "FUNCTION",
            self.NameWithParams,
            row.get("owner")
        )

        self.Comment = Comment(
            "FUNCTION",
            self.NameWithParams,
            row.get("comment")
        )

        self.ACL = ACL(
            "FUNCTION",
            self.NameWithParams,
            self.Owner.Owner,
            row.get("acl")
        )

    def __str__(self):
        return self.FullName

    def DDL_Create(self, style=""):
        r = ''
        r += 'CREATE OR REPLACE FUNCTION %s.%s' % (self.Schema, self.Name)
        r += self.DDL_ArgsIn(style)
        r += 'RETURNS %s AS' % (self.DDL_ArgsOut(style))
        r += SEP
        r += '$BODY$'
        r += SEP
        r += self.Code
        r += SEP
        r += '$BODY$'
        r += SEP
        r += '  LANGUAGE %s %s' % (self.Language, self.Volatility)

        if self.Cost > 0:
            r += SEP
            r += '  COST %s' % (int(self.Cost))

        if self.Rows > 0:
            r += SEP
            r += '  ROWS %s' % (int(self.Rows))

        r += ';'

        return r

    def DDL_Drop(self, style=""):
        return 'DROP FUNCTION %s(%s);' % (self.FullName, self.ArgsInTypes)

    def DDL_ArgsIn(self, style=""):
        if len(self.ArgsIn or '') == 0:
            return "()" + SEP
        else:
            r = ""
            r += "("
            r += SEP
            r += "    %s" % (self.ArgsIn.replace(',', ',%s   ' % (SEP)))
            r += SEP
            r += ")"
            r += SEP
            return r

    def DDL_ArgsOut(self, style=""):
        if self.IsRecord:
            return self.ArgsOut.replace(',', ',\n   ').replace('TABLE(', 'TABLE(\n    ').replace(')', '\n)')
        else:
            return self.ArgsOut

    def DDL_Full(self, style=""):
        r = ''
        r += "-- Function: %s(%s)" % (self.FullName, self.ArgsInTypes)
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
            Export functions for compare
        """
        name = "function_%s" % (self.NameWithParams)

        # Sequence
        r = {
            name : Export(
                name        = name,
                type        = "function",
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

QUERY_FUNCTION = """
    select
        p.oid,
        trim(lower(n.nspname)) as schema,
        trim(lower(p.proname)) as proc,
        oidvectortypes(proargtypes) as args_in_types,
        pg_get_function_arguments(p.oid) as args_in,
        pg_get_function_result(p.oid) as args_out,
        coalesce(p.procost, 0) as cost,
        coalesce(p.prorows, 0) as rows,
        trim(lower(o.rolname)) as owner,
        trim(lower(l.lanname)) as lang,
        obj_description(p.oid) as comment,
        case
            when p.provolatile = 'i' then 'IMMUTABLE'
            when p.provolatile = 's' then 'STABLE'
            when p.provolatile = 'v' then 'VOLATILE'
        end || case
            when p.proisstrict then ' STRICT'
            else ''
        end || case
            when not p.prosecdef then ''
            else ' SECURITY DEFINER'
        end as volatility,
        count(*) over (partition by n.oid, p.oid) > 1 as has_duplicate,
        coalesce(trim(lower(t.typname)), '') = 'trigger' as is_trigger,
        coalesce(trim(lower(t.typname)), '') = 'record' as is_record,
        replace(p.prosrc, E'\r', '') as code,
        p.proacl::varchar[] as acl
    from pg_proc p
    join pg_namespace n on
        n.oid = p.pronamespace and
        n.nspname !~* '^pg_temp' AND
        n.nspname !~* '^pg_toast' AND
        n.nspname != ALL(%s)
    join pg_language l on
        l.oid = p.prolang and
        l.lanname in ('sql','plpgsql','plpythonu','plpython3u','plproxy')
    join pg_roles o on
        o.oid = p.proowner
    join pg_type t on
        t.oid = p.prorettype
    order by 1
"""
