import hashlib
import json
import os
import shutil
from pathlib import Path

from google.protobuf.json_format import Parse, MessageToJson

import explorer_pb2 as pb
import explorer_pb2_grpc as pb_rpc
import locapip


def server_resolved_path(path):
    joined = server_working_directory / path
    if str(server_working_directory.resolve()) not in str(joined.resolve()):
        raise Exception(f'{path}')
    return joined


def server_relative_path(path):
    joined = Path(path)
    if str(server_working_directory.resolve()) not in str(joined.resolve()):
        raise Exception(f'{path}')
    return joined.relative_to(server_working_directory)


def server_stat(request: pb.StatRequest) -> pb.StatResponse:
    path = request.path
    request.path = str(server_resolved_path(request.path))
    response = client_stat(request)
    response.path = path
    return response


def client_stat(request: pb.StatRequest) -> pb.StatResponse:
    path = Path(str(request.path))
    response = pb.StatResponse(path=request.path)
    if path.exists():
        os_stat = os.stat(path)
        response.exists = True
        response.size = os_stat.st_size
        response.is_dir = path.is_dir()
        response.is_file = path.is_file()

        if path.is_file() and request.enable_sha1:
            file_hash = hashlib.sha1()
            file_hash.update(path.read_bytes())
            response.sha1 = file_hash.hexdigest()

        response.modified_timestamp = int(os_stat.st_mtime)
        if hasattr(os_stat, "st_birthtime"):
            response.created_timestamp = int(os_stat.st_birthtime)
        else:
            response.created_timestamp = int(os_stat.st_ctime)
    return response


def server_makedir(request: pb.Makedir) -> pb.Makedir:
    path = request.path
    request.path = str(server_resolved_path(request.path))
    response = client_makedir(request)
    response.path = path
    return response


def client_makedir(request: pb.Makedir) -> pb.Makedir:
    path = Path(str(request.path))
    if path.exists():
        if path.is_dir():
            request.conflict = False
            return request
        elif request.override:
            os.remove(path)
            os.makedirs(path)
            request.conflict = True
            return request
        else:
            request.conflict = True
            return request
    else:
        os.makedirs(path)
        request.conflict = False
        return request


def server_init_unmatched_file(request: pb.MatchFile) -> pb.MatchFile:
    request.path = str(server_resolved_path(request.path))
    response = client_init_unmatched_file(request)
    response.path = str(server_relative_path(response.path))
    return response


def client_init_unmatched_file(request: pb.MatchFile) -> pb.MatchFile:
    path = Path(request.path)
    if path.exists():
        if path.is_file():
            file_hash = hashlib.sha1()
            file_hash.update(path.read_bytes())
            sha1 = file_hash.hexdigest()
            if sha1 == request.sha1:
                request.matched = True
            else:
                os.remove(path)
                path.touch()
            return request
        else:
            shutil.rmtree(path)
            path.touch()
            return request
    else:
        path.touch()
        return request


class Service(pb_rpc.ExplorerServicer):
    async def stat(self, request: pb.StatRequest, context):
        return server_stat(request)

    async def listdir(self, request: pb.StatRequest, context):
        path = server_resolved_path(request.path)
        for name in os.listdir(path):
            request_ = pb.StatRequest(path=str(path / name), enable_sha1=request.enable_sha1)
            yield server_stat(request_)

    async def remove(self, request: pb.Remove, context):
        path = server_resolved_path(request.path)
        if not path.exists():
            request.not_found = True
        else:
            if path.is_dir():
                shutil.rmtree(path)
            if path.is_file():
                os.remove(path)
        return request

    async def rename(self, request: pb.Rename, context):
        path = server_resolved_path(request.path)
        new_path = server_resolved_path(request.new_path)
        if not path.exists():
            request.not_found = True
        else:
            path.rename(new_path)
        return request

    async def makedir(self, request: pb.Makedir, context):
        return server_makedir(request)

    async def upload_init(self, request_iterator, context):
        async for request in request_iterator:
            if request.WhichOneof('type') == 'copy_dir':
                makedir = server_makedir(pb.Makedir(path=request.copy_dir.server_path, override=True))
                yield request
            elif request.WhichOneof('type') == 'copy_file':
                match_file = server_init_unmatched_file(pb.MatchFile(path=request.copy_file.server_path))
                request.copy_file.matched = match_file.matched
                yield request

    async def upload_file(self, request_iterator, context):
        async for request in request_iterator:
            save_path = server_resolved_path(request.info.server_path)
            save_path.touch()
            with save_path.open("r+b") as io:
                io.seek(request.info.offset)
                io.write(request.content)
            yield request.info

    async def download_init(self, request, context):
        server_parent = Path(request.server_path)
        client_parent = Path(request.client_path) / server_parent.name
        server_parent = server_resolved_path(server_parent)

        copy_dirs = []
        copy_files = []

        if server_parent.is_dir():
            copy_dir = pb.CopyDir(client_path=request.client_path, server_path=request.server_path)
            copy_dirs.append(copy_dir)
            for parent, dir_names, file_names in os.walk(server_parent):
                for name in dir_names:
                    server_path = Path(parent) / name
                    client_path = client_parent / server_path.relative_to(server_parent)
                    copy_dir = pb.CopyDir(client_path=str(client_path),
                                          server_path=str(server_relative_path(server_path)))
                    copy_dirs.append(copy_dir)
                for name in file_names:
                    server_path = Path(parent) / name
                    client_path = client_parent / server_path.relative_to(server_parent)
                    copy_file = pb.CopyFile(client_path=str(client_path),
                                            server_path=str(server_relative_path(server_path)))
                    copy_files.append(copy_file)
        elif server_parent.is_file():
            copy_file = pb.CopyFile(client_path=request.client_path, server_path=request.server_path)
            copy_files.append(copy_file)

        for copy_dir in copy_dirs:
            yield pb.CopyInit(copy_dir=copy_dir)

        for copy_file in copy_files:
            path = server_resolved_path(copy_file.server_path)
            file_hash = hashlib.sha1()
            file_hash.update(path.read_bytes())
            sha1 = file_hash.hexdigest()
            copy_file.sha1 = sha1
            copy_file.size = os.stat(path).st_size
            yield pb.CopyInit(copy_file=copy_file)

    async def download_file(self, request_iterator, context):
        async for request in request_iterator:
            with server_resolved_path(request.server_path).open("r+b") as io:
                offset = io.tell()
                content = io.read(chunk_size)
                while len(content) > 0:
                    info = pb.CopyChunkInfo(client_path=request.client_path,
                                            server_path=request.server_path,
                                            offset=offset, size=len(content))
                    yield pb.CopyChunk(info=info, content=content)
                    offset = io.tell()
                    content = io.read(chunk_size)


async def upload_init_request(cpp_request):
    request_dict = json.loads(cpp_request(str()))
    client_parent = Path(request_dict['client_path'])
    server_parent = Path(request_dict['server_path']) / client_parent.name

    copy_dirs = []
    copy_files = []

    if client_parent.is_dir():
        copy_dir = pb.CopyDir(client_path=str(client_parent), server_path=str(server_parent))
        copy_dirs.append(copy_dir)
        for parent, dir_names, file_names in os.walk(client_parent):
            for name in dir_names:
                client_path = Path(parent) / name
                server_path = server_parent / client_path.relative_to(client_parent)
                copy_dir = pb.CopyDir(client_path=str(client_path), server_path=str(server_path))
                copy_dirs.append(copy_dir)
            for name in file_names:
                client_path = Path(parent) / name
                server_path = server_parent / client_path.relative_to(client_parent)
                copy_file = pb.CopyFile(client_path=str(client_path), server_path=str(server_path))
                copy_files.append(copy_file)
    elif client_parent.is_file():
        copy_file = pb.CopyFile(client_path=str(client_parent), server_path=str(server_parent))
        copy_files.append(copy_file)

    for copy_dir in copy_dirs:
        yield pb.CopyInit(copy_dir=copy_dir)

    for copy_file in copy_files:
        path = Path(copy_file.client_path)
        file_hash = hashlib.sha1()
        file_hash.update(path.read_bytes())
        sha1 = file_hash.hexdigest()
        copy_file.sha1 = sha1
        copy_file.size = os.stat(path).st_size
        yield pb.CopyInit(copy_file=copy_file)


async def upload_init_response(response_message_iterator: pb.CopyInit, cpp_response):
    async for response_message in response_message_iterator:
        if response_message.WhichOneof('type') == 'copy_file':
            cpp_response(MessageToJson(response_message.copy_file, True, True))


async def upload_file_request(cpp_request):
    while True:
        request_json = cpp_request(str())
        if len(request_json) == 0:
            break
        request_message = Parse(request_json, pb.CopyFile())
        if not request_message.matched:
            with Path(request_message.client_path).open("r+b") as io:
                offset = io.tell()
                content = io.read(chunk_size)
                while len(content) > 0:
                    info = pb.CopyChunkInfo(client_path=request_message.client_path,
                                            server_path=request_message.server_path,
                                            offset=offset, size=len(content))
                    yield pb.CopyChunk(info=info, content=content)
                    offset = io.tell()
                    content = io.read(chunk_size)


async def upload_file_response(response_iterator, cpp_response):
    async for response_message in response_iterator:
        response_json = MessageToJson(response_message, True, True)
        cpp_response(response_json)


async def download_init_response(response_message_iterator, cpp_response):
    async for response_message in response_message_iterator:
        if response_message.WhichOneof('type') == 'copy_dir':
            makedir = client_makedir(pb.Makedir(path=response_message.copy_dir.client_path, override=True))
        elif response_message.WhichOneof('type') == 'copy_file':
            match_file = client_init_unmatched_file(pb.MatchFile(path=response_message.copy_file.client_path))
            response_message.copy_file.matched = match_file.matched
            cpp_response(MessageToJson(response_message.copy_file, True, True))


async def download_file_request(cpp_request):
    while True:
        request_json = cpp_request(str())
        if len(request_json) == 0:
            break
        request_message = Parse(request_json, pb.CopyFile())
        if not request_message.matched:
            yield request_message


async def download_file_response(response_iterator, cpp_response):
    async for response_message in response_iterator:
        save_path = Path(response_message.info.client_path)
        save_path.touch()
        with save_path.open("r+b") as io:
            io.seek(response_message.info.offset)
            io.write(response_message.content)
        cpp_response(MessageToJson(response_message.info, True, True))


chunk_size = 1 * 1024 * 1024  # 1Mib

if locapip.server is not None:
    pb_rpc.add_ExplorerServicer_to_server(Service(), locapip.server)
    server_working_directory: Path = Path(locapip.config[__name__]['working_directory']).resolve()
else:
    locapip.pb[__name__] = pb
    locapip.stub[__name__] = pb_rpc.ExplorerStub

    locapip.py_request[__name__] = {
        'stat': pb.StatRequest,
        'listdir': pb.StatRequest,
        'makedir': pb.Makedir,
        'remove': pb.Remove,
        'rename': pb.Rename,
        'upload_init': upload_init_request,
        'upload_file': upload_file_request,
        'download_init': pb.CopyDir,
        'download_file': download_file_request,
    }

    locapip.py_response[__name__] = {
        'upload_init': upload_init_response,
        'upload_file': upload_file_response,
        'download_init': download_init_response,
        'download_file': download_file_response,
    }
