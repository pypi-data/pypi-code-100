#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import shutil
from multiprocessing import Pool
from pg_metadata.Database import Database

class Grabber():
    def __init__(self, connect, target_path, exclude_schemas=[], style=""):
        assert connect is not None
        assert isinstance(connect, dict)
        assert len(connect.keys()) > 0

        assert target_path is not None
        assert isinstance(target_path, str)
        assert len(target_path) > 0

        self.Style          = style
        self.TargetPath     = target_path
        self.ExcludeSchemas = exclude_schemas or []
        self.Database       = Database(connect, self.ExcludeSchemas)

    def CreatePath(self, path=[]):
        full_path = self.TargetPath
        for p in path:
            full_path = '/'.join([full_path, p])
            if not os.path.exists(full_path):
                os.mkdir(full_path)
        return full_path

    def GetPath(self, file_path, file_name):
        path = self.TargetPath
        for p in file_path:
            path = "/".join([path, p])
            if not os.path.exists(path):
                os.mkdir(path)
        file_name += '.sql'
        file_name = '/'.join([path, file_name])
        return file_name

    def WriteNamespace(self, namespace):
        file_name = self.GetPath(namespace.Path, namespace.File)
        with open(file_name, 'w', encoding='utf-8') as wf:
            wf.write(namespace.DDL_Full(self.Style))

    def WriteTable(self, table):
        file_name = self.GetPath(table.Path, table.File)
        with open(file_name, 'w', encoding='utf-8') as wf:
            wf.write(table.DDL_Full(self.Style))

    def WriteFunction(self, function):
        file_name = self.GetPath(function.Path, function.File)
        with open(file_name, 'w', encoding='utf-8') as wf:
            wf.write(function.DDL_Full(self.Style))

    def WriteView(self, view):
        file_name = self.GetPath(view.Path, view.File)
        with open(file_name, 'w', encoding='utf-8') as wf:
            wf.write(view.DDL_Full(self.Style))

    def WriteSequence(self, sequence):
        file_name = self.GetPath(sequence.Path, sequence.File)
        with open(file_name, 'w', encoding='utf-8') as wf:
            wf.write(sequence.DDL_Full(self.Style))

    def WriteForeignServer(self, server):
        file_name = self.GetPath(server.Path, server.File)
        with open(file_name, 'w', encoding='utf-8') as wf:
            wf.write(server.DDL_Full(self.Style))

    def WriteForeignTable(self, table):
        file_name = self.GetPath(table.Path, table.File)
        with open(file_name, 'w', encoding='utf-8') as wf:
            wf.write(table.DDL_Full(self.Style))

    def CreateFolders(self):
        if os.path.exists(self.TargetPath):
            shutil.rmtree(self.TargetPath)
        os.mkdir(self.TargetPath)

        for k,tbl in self.Database.Tables.items():
            self.CreatePath(tbl.Path)

        for k,fnc in self.Database.Functions.items():
            self.CreatePath(fnc.Path)

        for k,seq in self.Database.Sequences.items():
            self.CreatePath(seq.Path)

        for k,vw in self.Database.Views.items():
            self.CreatePath(vw.Path)

        for k,fs in self.Database.ForeignServers.items():
            self.CreatePath(fs.Path)

        for k,ft in self.Database.ForeignTables.items():
            self.CreatePath(ft.Path)

    def Grab(self):
        self.Database.Parse()
        self.CreateFolders()

        pool = Pool(processes=8)
        pool.map(self.WriteNamespace,       [v for k,v in self.Database.Namespaces.items()])
        pool.map(self.WriteTable,           [v for k,v in self.Database.Tables.items()])
        pool.map(self.WriteFunction,        [v for k,v in self.Database.Functions.items()])
        pool.map(self.WriteView,            [v for k,v in self.Database.Views.items()])
        pool.map(self.WriteSequence,        [v for k,v in self.Database.Sequences.items()])
        pool.map(self.WriteForeignServer,   [v for k,v in self.Database.ForeignServers.items()])
        pool.map(self.WriteForeignTable,    [v for k,v in self.Database.ForeignTables.items()])
