#!/usr/bin/python
# -*- coding: utf-8 -*-

from pg_metadata._System import SEP
from pg_metadata.Grant   import Grant

class ACL():
    def __init__(self, instance_type, instance_name, owner_name, acl):
        self.InstanceType = instance_type or ""
        self.InstanceType = self.InstanceType.strip().upper()
        assert len(self.InstanceType) > 0

        self.InstanceName = instance_name or ""
        self.InstanceName = self.InstanceName.strip()
        assert len(self.InstanceName) > 0

        self.Owner = owner_name or ""
        self.Owner = self.Owner.strip()
        assert len(self.Owner) > 0

        self.Grants = {}
        self.Parse(acl)

    def __str__(self):
        return "%s -> %s -> %s" % (self.InstanceType, self.InstanceName, self.Grants.keys())

    def DDL_Create(self, style=""):
        r = ""
        for grant in sorted([g.DDL_Create(style) for g in self.Grants.values()]):
            r += grant
            r += SEP
        return r.strip()

    def DDL_Drop(self, style=""):
        r = ""
        for grant in sorted([g.DDL_Drop(style) for g in self.Grants.values()]):
            r += grant
            r += SEP
        return r.strip()

    def Parse(self, acl_value):
        acl_value = acl_value or []

        for acl in acl_value:
            spl = acl.split("=")
            if len(spl) != 2:
                continue

            role_name = spl[0].strip()
            if role_name == "":
                role_name = "public"

            permissions = []

            grants = spl[1].replace("/%s" % (self.Owner), "").strip()
            if grants.strip() == "":
                permissions.append("ALL")
            elif grants == "U":
                permissions.append("USAGE")
            elif grants == "UC":
                permissions.append("ALL")
            elif grants == "arwdDxt":
                permissions.append("ALL")
            elif grants == "rwU":
                permissions.append("ALL")
            elif grants == "X":
                permissions.append("EXECUTE")
            else:
                if grants.find("r") >= 0:
                    permissions.append("SELECT")
                if grants.find("a") >= 0:
                    permissions.append("INSERT")
                if grants.find("w") >= 0:
                    permissions.append("UPDATE")
                if grants.find("d") >= 0:
                    permissions.append("DELETE")
                if grants.find("D") >= 0:
                    permissions.append("TRUNCATE")
                if grants.find("x") >= 0:
                    permissions.append("REFERENCES")
                if grants.find("t") >= 0:
                    permissions.append("TRIGGER")

            self.Grants[role_name] = Grant(
                self.InstanceType,
                self.InstanceName,
                self.Owner,
                True,
                permissions,
                role_name
            )

        if "public" not in self.Grants.keys():
            self.Grants["public"] = Grant(
                self.InstanceType,
                self.InstanceName,
                self.Owner,
                False,
                ["ALL"],
                "public"
            )

        if self.Owner not in self.Grants.keys():
            self.Grants[self.Owner] = Grant(
                self.InstanceType,
                self.InstanceName,
                self.Owner,
                True,
                ["ALL"],
                self.Owner
            )

    def Export(self):
        r = {}
        for g in self.Grants.values():
            r.update(g.Export())
        return r
