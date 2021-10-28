#!/usr/bin/python
# -*- coding: utf-8 -*-

from pg_metadata._System import SEP

QUERY_TABLE_CONSTRAINT = """
    select
        c.oid as oid,
        trim(lower(n.nspname)) as schema,
        trim(lower(t.relname)) as table,
        trim(lower(c.conname)) as name,
        trim(lower(c.contype)) as type,
        case trim(lower(c.contype))
            when 'p' then 1
            when 'u' then 2
            when 'c' then 3
            when 'f' then 4
            else          5
        end::integer as order_num,
        pg_get_constraintdef(c.oid) as definition,
        case trim(lower(c.confupdtype))
            when 'a' then 'ON UPDATE NO ACTION'
            when 'r' then 'ON UPDATE RESTRICT'
            when 'c' then 'ON UPDATE CASCADE'
            when 'n' then 'ON UPDATE SET NULL'
            when 'd' then 'ON UPDATE SET DEFAULT'
        end as update_action,
        case trim(lower(c.confdeltype))
            when 'a' then 'ON DELETE NO ACTION'
            when 'r' then 'ON DELETE RESTRICT'
            when 'c' then 'ON DELETE CASCADE'
            when 'n' then 'ON DELETE SET NULL'
            when 'd' then 'ON DELETE SET DEFAULT'
        end as delete_action,
        case trim(lower(c.confmatchtype))
            when 'f' then 'MATCH FULL'
            when 'p' then 'MATCH PARTIAL'
            when 'u' then 'MATCH SIMPLE'
            when 's' then 'MATCH SIMPLE'
        end as match_action,
        case
            when trim(lower(c.contype)) != 'f' then ''
            when c.condeferrable and c.condeferred then
                'DEFERRABLE INITIALLY DEFERRED'
            when c.condeferrable and not c.condeferred then
                'DEFERRABLE INITIALLY IMMEDIATE'
            else
                'NOT DEFERRABLE'
        end as deferrable_type
    from pg_constraint c
    join pg_namespace n on
        n.oid = c.connamespace AND
        n.nspname !~* '^pg_temp' AND
        n.nspname !~* '^pg_toast' AND
        n.nspname != ALL(%s)
    join pg_class t on
        t.oid = c.conrelid
    where c.conislocal
    order by 1,2,3
"""

class TableConstraint():
    def __init__(self, row={}):
        assert row is not None
        assert isinstance(row, dict)
        assert len(row.keys()) > 0

        self.Oid = row.get('oid')
        assert self.Oid is not None and self.Oid > 0

        self.Schema = row.get('schema') or ''
        self.Schema = self.Schema.strip().lower()
        assert len(self.Schema) > 0

        self.Table = row.get('table') or ''
        self.Table = self.Table.strip().lower()
        assert len(self.Table) > 0

        self.FullTable = '%s.%s' % (self.Schema, self.Table)

        self.Name = row.get('name') or ''
        self.Name = self.Name.strip().lower()
        assert len(self.Name) > 0

        self.FullName = '%s.%s.%s' % (self.Schema, self.Table, self.Name)

        self.Type = row.get('type') or ''
        self.Type = self.Type.strip().lower()
        assert len(self.Type) > 0

        self.IsForeignKey = (self.Type == 'f')

        self.OrderNum = row.get("order_num") or 6

        self.SortKey = "%s_%s" % (self.OrderNum, self.FullName)

        self.Definition = row.get('definition') or ''
        assert len(self.Definition) > 0

        self.UpdateAction = row.get('update_action') or ''
        self.UpdateAction = self.UpdateAction.strip().upper()

        self.DeleteAction = row.get('delete_action') or ''
        self.DeleteAction = self.DeleteAction.strip().upper()

        self.MatchAction = row.get('match_action') or ''
        self.MatchAction = self.MatchAction.strip().upper()

        self.DeferrableType = row.get('deferrable_type') or ''
        self.DeferrableType = self.DeferrableType.strip().upper()

    def __str__(self):
        return self.FullName

    def GetDefinition(self, separator=" "):
        if not self.IsForeignKey:
            return "CONSTRAINT %s %s" % (self.Name, self.Definition)

        definition = self.Definition
        if definition.find(' ON') > -1:
            definition = definition[0:definition.find(') ON') + 1]

        #definition = definition.replace("REFERENCES", separator+"REFERENCES")

        return separator.join([
            "CONSTRAINT %s" % (self.Name),
            definition,
            self.MatchAction,
            self.UpdateAction,
            self.DeleteAction,
            self.DeferrableType
        ])

    def DDL_Inner(self):
        separator = "%s    " % (SEP)
        return "  " + self.GetDefinition(separator)

    def DDL_Create(self):
        return "ALTER TABLE %s ADD %s;" % (self.FullTable, self.GetDefinition(" "))

    def DDL_Drop(self):
        return 'ALTER TABLE %ss DROP CONSTRAINT %s;' % (self.FullTable, self.Name)
