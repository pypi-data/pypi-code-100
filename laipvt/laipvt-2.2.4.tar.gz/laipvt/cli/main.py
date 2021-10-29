#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from laipvt.sysutil.args import Args

def main():
    args = Args().parse_args()
    func = args.which
    if func == "delete":
        from laipvt.cli.delete import delete_main
        delete_main(args)
    else:
        from laipvt.cli.deploy import deploy_main
        deploy_main(args)

