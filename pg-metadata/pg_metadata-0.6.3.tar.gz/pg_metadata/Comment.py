#!/usr/bin/python
# -*- coding: utf-8 -*-

from pg_metadata._System import SEP, STYLE_PGADMIN3
from pg_metadata.Export  import Export

class Comment():
    def __init__(self, instance_type, instance_name, comment):
        self.Type = instance_type or ""
        self.Type = self.Type.strip().upper()
        assert len(self.Type) > 0

        self.Instance = instance_name or ""
        self.Instance = self.Instance.strip()
        assert len(self.Instance) > 0

        self.Comment = comment or ""
        self.Comment = self.Comment.strip()

        self.IsExists = len(self.Comment) > 0

    def __str__(self):
        return "%s -> %s -> %s" % (self.Type, self.Instance, self.Comment)

    def DDL_Create(self, style=""):
        r = ""
        if len(self.Comment) > 0:
            if style == STYLE_PGADMIN3:
                r += "COMMENT ON %s %s" % (self.Type, self.Instance)
                r += SEP
                r += "  IS '%s';" % (self.Comment)
            else:
                r += "COMMENT ON %s %s IS '%s';" % (self.Type, self.Instance, self.Comment)
        return r

    def DDL_Drop(self, style=""):
        r = ""
        if style == STYLE_PGADMIN3:
            r += "COMMENT ON %s '%s'" % (self.Type, self.Instance)
            r += SEP
            r += "  IS '';"
        else:
            r += "COMMENT ON %s %s IS '';" % (self.Type, self.Instance)
        return r

    def Export(self):
        type = "comment_%s" % (self.Type.lower())
        name = "comment_%s" % (self.Instance)
        prnt = "%s_%s" % (self.Type.lower(), self.Instance)
        return {
            name : Export(
                name        = name,
                type        = type,
                parent      = prnt,
                create      = self.DDL_Create() or self.DDL_Drop(),
                drop        = self.DDL_Drop()
            )
        }
