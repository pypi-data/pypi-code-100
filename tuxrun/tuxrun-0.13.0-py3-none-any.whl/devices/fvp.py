# -*- coding: utf-8 -*-
# vim: set ts=4
#
# Copyright 2021-present Linaro Limited
#
# SPDX-License-Identifier: MIT

from typing import List

from tuxrun.devices import Device
from tuxrun.exceptions import InvalidArgument
import tuxrun.templates as templates


class FVPDevice(Device):
    prompts: List[str] = []
    support_tests = False

    def validate(
        self,
        mcp_fw,
        mcp_romfw,
        rootfs,
        scp_fw,
        scp_romfw,
        parameters,
        tests,
        uefi,
        **kwargs,
    ):
        invalid_args = ["--" + k.replace("_", "-") for k in kwargs if kwargs[k]]
        if len(invalid_args) > 0:
            raise InvalidArgument(
                f"Invalid option(s) for fvp devices: {', '.join(invalid_args)}"
            )

        mandatory = ["mcp_fw", "mcp_romfw", "rootfs", "scp_fw", "scp_romfw", "uefi"]
        args = locals()
        missing_args = ["--" + k for k in mandatory if not args[k]]
        if len(missing_args) > 0:
            raise InvalidArgument(
                f"Missing option(s) for fvp devices: {', '.join(missing_args)}"
            )

    def definition(self, **kwargs):
        # Options that can *not* be updated
        kwargs["prompts"] = self.prompts
        kwargs["support_tests"] = self.support_tests

        # render the template
        return templates.jobs.get_template("fvp.yaml.jinja2").render(**kwargs)

    def device_dict(self, context):
        return templates.devices.get_template("fvp.yaml.jinja2").render(**context)


class FVPMorelloAndroid(FVPDevice):
    name = "fvp-morello-android"

    prompts = ["console:/ "]
    support_tests = True

    def validate(self, tests, parameters, **kwargs):
        super().validate(tests=tests, parameters=parameters, **kwargs)
        userdata_required = [
            t in tests for t in ["binder", "bionic", "compartment", "logd"]
        ]
        if any(userdata_required) and not parameters.get("USERDATA"):
            raise InvalidArgument(
                "--parameters USERDATA=http://... is "
                "mantadory for fvp-morello-android test"
            )
        if "lldb" in tests and not parameters.get("LLDB_URL"):
            raise InvalidArgument(
                "--parameters LLDB_URL=http://... is "
                "mantadory for fvp-morello-android lldb test"
            )
        if "lldb" in tests and not parameters.get("TC_URL"):
            raise InvalidArgument(
                "--parameters TC_URL=http://... is "
                "mantadory for fvp-morello-android lldb test"
            )


class FVPMorelloBusybox(FVPDevice):
    name = "fvp-morello-busybox"

    prompts = ["/ # "]
    support_tests = False


class FVPMorelloOE(FVPDevice):
    name = "fvp-morello-oe"

    prompts = ["root@morello-fvp:~# "]
    support_tests = True
