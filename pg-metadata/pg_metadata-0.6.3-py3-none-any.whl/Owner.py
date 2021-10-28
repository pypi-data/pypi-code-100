#!/usr/bin/python
# -*- coding: utf-8 -*-

from pg_metadata._System import SEP, STYLE_PGADMIN3
from pg_metadata.Export  import Export
class Owner():
    def __init__(self, instance_type, instance_name, owner_name):
        self.Type = instance_type or ""
        self.Type = self.Type.strip().upper()
        assert len(self.Type) > 0

        self.Instance = instance_name or ""
        self.Instance = self.Instance.strip()
        assert len(self.Instance) > 0

        self.Owner = owner_name or ""
        self.Owner = self.Owner.strip()
        assert len(self.Owner) > 0

    def __str__(self):
        return "%s -> %s -> %s" % (self.Type, self.Instance, self.Owner)

    def DDL_Create(self, style=""):
        r = ""
        if style == STYLE_PGADMIN3:
            r += "ALTER %s %s" % (self.Type, self.Instance)
            r += SEP
            r += "  OWNER TO %s;" % (self.Owner)
        else:
            r += "ALTER %s %s OWNER TO %s;" % (self.Type, self.Instance, self.Owner)
        return r

    def Export(self):
        type = "owner_%s" % (self.Type.lower())
        name = "owner_%s" % (self.Instance)
        prnt = "%s_%s" % (self.Type.lower(), self.Instance)
        return {
            name : Export(
                name        = name,
                type        = type,
                parent      = prnt,
                create      = self.DDL_Create(),
                drop        = "/* DROP OWNER */"
            )
        }
