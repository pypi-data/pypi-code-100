#!/usr/bin/env python

import sys
import logging
import argparse
from regipy.registry import NKRecord, RegistryHive
from regipy import convert_wintime

g_logger = logging.getLogger("amcache2")


class InventoryApplicationFileEntry:
    def __init__(self, entry: NKRecord):
        self.__timestamp = convert_wintime(entry.header.last_modified, as_json=False)

        for value in entry.iter_values():
            if value.name.lower() == 'lowercaselongpath':
                self.__lower_case_long_path = value.value
            elif value.name.lower() == 'originalfilename':
                self.__original_filename = value.value
            elif value.name.lower() == 'name':
                self.__name = value.value
            elif value.name.lower() == 'size':
                self.__size = value.value

        if self.__name.lower() == str(self.__original_filename).lower():
            self.__displayname = self.__lower_case_long_path
        else:
            self.__displayname = "%s (%s) "% (self.__lower_case_long_path, self.__original_filename)

    def __str__(self):
        return "{MD5}|{name}|{inode}|{mode_as_string}|{UID}|{GID}|{size}|{atime}|{mtime}|{ctime}|{crtime}".format(
            MD5 = "0",
            name = self.__displayname,
            inode = "0",
            mode_as_string = "0",
            UID = "0",
            GID = "0",
            size = self.__size,
            atime = "-1",
            mtime = self.__timestamp.strftime('%s'),
            ctime = "-1",
            crtime = "-1"
        )


class InventoryApplicationFileList:
    def __init__(self, hive):
        self.__files = list()
        root_key = hive.get_key("Root")
        iaf_key = root_key.get_subkey("InventoryApplicationFile")
        self.__parse_iaf(iaf_key)

    def __parse_iaf(self, iaf):
        for file_key in iaf.iter_subkeys():
            self.__files.append(InventoryApplicationFileEntry(file_key))

    def __iter__(self):
        return self.__files.__iter__()


def main(argv=None):
    if argv is None:
        argv = sys.argv

    parser = argparse.ArgumentParser(
        description="Parse program execution entries from the Amcache.hve Registry hive")
    parser.add_argument("registry_hive", type=str,
                        help="Path to the Amcache.hve hive to process")
    args = parser.parse_args(argv[1:])

    hive = RegistryHive(args.registry_hive)
    for f in InventoryApplicationFileList(hive):
        print(str(f))


if __name__ == "__main__":
    main(argv=sys.argv)