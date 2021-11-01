import hashlib
import json
import os
import shutil
from dataclasses import dataclass, asdict
from json.decoder import JSONDecodeError
from pathlib import Path
from typing import List, Union
from urllib.parse import urljoin

import click
import requests
from dacite import from_dict, Config

from vankrupt_workshop_client.api import (
    _env_map,
    APIEnv,
    Env,
)
from vankrupt_workshop_client.api import api_entities


@dataclass
class ChunkInOldFile:
    chunk: api_entities.Chunk
    offset_in_file: int


@dataclass
class UpdatePlan:
    items: List[Union[ChunkInOldFile, api_entities.Chunk]]


@dataclass
class InternalSequencedChunk(api_entities.SequencedChunk):
    offset: int


class ConsumerClientException(Exception):
    message: str

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


def _calculate_chunk_offsets(chunks: List[api_entities.SequencedChunk]) -> List[InternalSequencedChunk]:
    acc = 0
    res = []
    for i, ch in enumerate(chunks):
        if ch.chunk_sequence != i:
            raise ConsumerClientException(
                message=f'An error in chunk sequences found at calculate_chunk_offsets: {chunks}'
            )

        res.append(InternalSequencedChunk(offset=acc, chunk_sequence=i, chunk=ch.chunk))
        acc += ch.chunk.true_size_bytes
    return res


def _plan_update(new_file: api_entities.ModFileDownload, old_file: api_entities.ModFileDownload) -> UpdatePlan:
    new_chunks_sorted = sorted(new_file.chunks, key=lambda x: x.chunk_sequence)
    old_chunks_sorted = sorted(old_file.chunks, key=lambda x: x.chunk_sequence)

    old_file_with_offsets = _calculate_chunk_offsets(old_chunks_sorted)
    old_ids = {x.chunk.id: x for x in old_file_with_offsets}

    plan = []
    for i, chunk in enumerate(new_chunks_sorted):
        if chunk.chunk_sequence != i:
            raise ConsumerClientException(message=f'An error in chunk sequences found: {new_file}')

        # if found in an old file - use it
        if chunk.chunk.id in old_ids.keys():
            plan.append(ChunkInOldFile(
                chunk=old_ids[chunk.chunk.id].chunk,
                offset_in_file=old_ids[chunk.chunk.id].offset
            ))
        else:
            plan.append(
                chunk.chunk
            )

    return UpdatePlan(items=plan)


def _plan_download(new_file: api_entities.ModFileDownload) -> UpdatePlan:
    chunks_sorted = sorted(new_file.chunks, key=lambda x: x.chunk_sequence)
    plan = []

    for i, chunk in enumerate(chunks_sorted):
        if chunk.chunk_sequence != i:
            raise ConsumerClientException(
                message=f'An error in chunk sequences found '
                        f'at position: {i} != seq: {chunk.chunk_sequence}')
        plan.append(
            chunk.chunk
        )
    return UpdatePlan(items=plan)


class ConsumerClient:
    env: APIEnv
    env_vars: Env

    def __init__(self, env: APIEnv = APIEnv.release):
        self.env = env
        self.env_vars = _env_map[env]

    def _get_chunk_download_url(self, mod_id: int, chunk: api_entities.Chunk):
        url = self.env_vars.chunk_url_template.substitute(mod_id=mod_id, hash=chunk.custom_hash)
        return url

    def _download_and_verify_chunk(self, url: str, chunk: api_entities.Chunk) -> bytes:
        blob = requests.get(url).content
        assert len(blob) == chunk.storage_used_bytes
        raw = self.env_vars.decompress_func(blob)
        assert len(raw) == chunk.true_size_bytes
        assert self.env_vars.hash_func(raw).hexdigest() == chunk.custom_hash
        return raw

    def _cut_and_verify_chunk(self, file: str, chunk: ChunkInOldFile) -> bytes:
        with open(file, 'rb') as f:
            f.seek(chunk.offset_in_file, os.SEEK_SET)
            raw = f.read(chunk.chunk.true_size_bytes)
        assert self.env_vars.hash_func(raw).hexdigest() == chunk.chunk.custom_hash
        return raw

    def _execute_plan(
            self,
            plan: UpdatePlan,
            mods_home_dir: str,
            mod_id: int,
            platform: api_entities.GamingPlatform,
            file_to_save: api_entities.ModFileDownload,
    ):
        root = Path.joinpath(Path(mods_home_dir), str(mod_id), platform.value)
        downloaded = reused = 0

        # save new file to .../bin2
        with open(Path.joinpath(root, 'bin2'), 'wb') as write_to:
            with click.progressbar(plan.items) as plan_items:
                for item in plan_items:
                    if isinstance(item, api_entities.Chunk):
                        url = self._get_chunk_download_url(mod_id=mod_id, chunk=item)
                        try:
                            raw = self._download_and_verify_chunk(url, chunk=item)
                            downloaded += 1
                        except AssertionError as e:
                            raise ConsumerClientException(message=f'Chunk assertion fail: {e}')
                    elif isinstance(item, ChunkInOldFile):
                        try:
                            old_file_path = Path.joinpath(root, 'bin')
                            raw = self._cut_and_verify_chunk(file=old_file_path, chunk=item)
                            reused += 1
                        except AssertionError as e:
                            raise ConsumerClientException(
                                message=f'Assertion fail when reusing chunk, most probably, save file is corrupted: {e}'
                            )
                    write_to.write(raw)
        print(f"reused: {reused}, downloaded: {downloaded}")

        # confirm resulting file's md5 hash just in case
        with open(Path.joinpath(root, 'bin2'), 'rb') as a_file:
            content = a_file.read()
            md5_hash = hashlib.md5()
            md5_hash.update(content)
            digest = md5_hash.hexdigest()
            if not digest == file_to_save.file_md5_hash:
                raise ConsumerClientException(
                    message=f'Resulting file hash mismatch. Got: {digest}, expected: {file_to_save.file_md5_hash}'
                )

        # delete .../bin file
        Path.joinpath(root, 'bin').unlink(missing_ok=True)
        # rename .../bin2 to .../bin
        Path.rename(
            Path.joinpath(root, 'bin2'),
            Path.joinpath(root, 'bin'),
        )
        # save new metadata
        with open(Path.joinpath(root, 'meta.txt'), 'w') as metadata_dump:
            w_dict = asdict(file_to_save)
            w_str = json.dumps(w_dict)
            metadata_dump.write(w_str)

    def filter_mods(
            self,
            platform: api_entities.GamingPlatform,
            page: int,
            size: int,
    ) -> api_entities.Page[api_entities.ModBase]:
        """
        Get mods for a platform.

        :param platform: the platform to filter mods for
        :param page:
        :param size:
        :return:
        """
        resp = requests.get(
            url=urljoin(
                base=self.env_vars.api_url,
                url=f'mods/platform/{platform}/?page={page}&size={size}'
            )
        )
        resp.raise_for_status()
        resp_json = resp.json()
        mods = from_dict(data_class=api_entities.Page, data=resp_json, config=Config(check_types=False))
        return mods

    def inspect_mod(
            self,
            mod_id: int,
    ) -> api_entities.ModInspect:
        """
        Inspect a mod, without all the download metadata.

        :param mod_id:
        :return:
        """
        resp = requests.get(
            url=urljoin(
                base=self.env_vars.api_url,
                url=f'mods/{mod_id}/with_files/'
            )
        )
        resp.raise_for_status()
        resp_json = resp.json()
        for f in resp_json['files']:
            f['platform'] = api_entities.GamingPlatform[f['platform']]
        mod = from_dict(data_class=api_entities.ModInspect, data=resp_json)
        return mod

    def get_mod_download_metadata(
            self,
            platform: api_entities.GamingPlatform,
            mod_id: int,
    ) -> api_entities.ModDownload:
        """
        Get all the metadata needed to download the mod.

        :param platform:
        :param mod_id:
        :return:
        """
        resp = requests.get(
            url=urljoin(
                base=self.env_vars.api_url,
                url=f'mods/{mod_id}/{platform.value}/download/'
            )
        )
        resp.raise_for_status()
        resp_json = resp.json()
        for f in resp_json['files']:
            f['platform'] = api_entities.GamingPlatform[f['platform']]
        mod = from_dict(data_class=api_entities.ModDownload, data=resp_json)
        return mod

    def save_mod(
            self,
            mods_home_dir: str,
            platform: api_entities.GamingPlatform,
            mod_id: int,
    ):
        """
        Download, extract, install and verify the installation of the mod.

        :param mods_home_dir:
        :param platform:
        :param mod_id:
        :return:
        """
        root = Path.joinpath(Path(mods_home_dir), str(mod_id), platform.value)

        if root.is_dir():
            raise IsADirectoryError("File directory not empty, either delete or choose update.")
        else:
            root.mkdir(parents=True)

        mod = self.get_mod_download_metadata(mod_id=mod_id, platform=platform)
        file = mod.files[0]
        plan = _plan_download(new_file=file)
        self._execute_plan(
            plan=plan,
            mods_home_dir=mods_home_dir,
            mod_id=mod_id,
            platform=platform,
            file_to_save=file
        )

    def update_mod(
            self,
            mods_home_dir: str,
            platform: api_entities.GamingPlatform,
            mod_id: int,
    ):
        """
        Download, extract, install and verify the installation of the mod.

        :param mods_home_dir:
        :param platform:
        :param mod_id:
        :return:
        """
        root = Path.joinpath(Path(mods_home_dir), str(mod_id), platform.value)

        if not root.is_dir():
            raise NotADirectoryError("File directory empty, download the mod first.")
        mod = self.get_mod_download_metadata(mod_id=mod_id, platform=platform)
        new_file = mod.files[0]
        with open(Path.joinpath(root, 'meta.txt'), 'r') as metadata:
            old_s = metadata.read()
            try:
                old_d = json.loads(old_s)
            except JSONDecodeError:
                raise ConsumerClientException(message='Corrupt metadata, reinstall the mod')
            old_d['platform'] = api_entities.GamingPlatform[old_d['platform']]

            old_file = from_dict(data_class=api_entities.ModFileDownload, data=old_d)
        plan = _plan_update(new_file=new_file, old_file=old_file)
        self._execute_plan(
            plan=plan,
            mods_home_dir=mods_home_dir,
            mod_id=mod_id,
            platform=platform,
            file_to_save=new_file
        )

    @staticmethod
    def delete_mod(
            mods_home_dir: str,
            platform: api_entities.GamingPlatform,
            mod_id: int,
    ):
        path = Path.joinpath(Path(mods_home_dir), str(mod_id), platform.value)
        shutil.rmtree(path)
