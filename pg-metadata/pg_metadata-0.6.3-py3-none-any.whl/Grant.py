#!/usr/bin/python
# -*- coding: utf-8 -*-

from pg_metadata._System import SEP
from pg_metadata.Export  import Export

class Grant():
    def __init__(self, instance_type, instance_name, owner_name, is_grant, permissions, role_name):
        self.Type = instance_type or ""
        self.Type = self.Type.strip().upper()
        assert len(self.Type) > 0

        self.Instance = instance_name or ""
        self.Instance = self.Instance.strip()
        assert len(self.Instance) > 0

        assert is_grant is not None
        assert isinstance(is_grant, bool)
        self.Status = "GRANT" if is_grant else "REVOKE"
        self.StatusDrop = "GRANT" if not is_grant else "REVOKE"

        self.Prep = "TO" if is_grant else "FROM"
        self.PrepDrop = "TO" if not is_grant else "FROM"

        assert permissions is not None
        assert isinstance(permissions, list)
        assert len(permissions) > 0
        self.Permissions = ", ".join(sorted(permissions))

        self.Owner = owner_name or ""
        self.Owner = self.Owner.strip()
        assert len(self.Owner) > 0

        self.Role = role_name or ""
        self.Role = self.Role.strip()
        assert len(self.Role) > 0

    def __str__(self):
        return "%s -> %s -> %s" % (self.Type, self.Instance, self.Role)

    def DDL_Create(self, style=""):
        r = ""
        r += "%s %s ON %s %s %s %s;" % (
            self.Status, self.Permissions, self.Type,
            self.Instance, self.Prep, self.Role
        )
        return r

    def DDL_Drop(self, style=""):
        r = ""
        r += "%s %s ON %s %s %s %s;" % (
            self.StatusDrop, self.Permissions, self.Type,
            self.Instance, self.PrepDrop, self.Role
        )
        return r

    def Export(self):
        type = "grant_%s" % (self.Type.lower())
        name = "%s_%s_%s" % (type, self.Instance, self.Role)
        prnt = "%s_%s" % (self.Type.lower(), self.Instance)
        return {
            name : Export(
                name        = name,
                type        = type,
                parent      = prnt,
                create      = self.DDL_Create(),
                drop        = self.DDL_Drop()
            )
        }
