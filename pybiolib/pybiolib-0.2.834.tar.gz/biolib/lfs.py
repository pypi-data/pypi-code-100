import io
import multiprocessing
import os
import zipfile as zf
from itertools import repeat

import requests

from biolib.app import BioLibApp
from biolib.biolib_api_client.biolib_account_api import BiolibAccountApi
from biolib.biolib_api_client.biolib_large_file_system_api import BiolibLargeFileSystemApi
from biolib.biolib_api_client import BiolibApiClient
from biolib.biolib_api_client.lfs_types import LfsUploadPartMetadata
from biolib.biolib_logging import logger
from biolib.biolib_errors import BioLibError
from biolib.typing_utils import List, Tuple, Iterator


def upload_chunk(input_tuple) -> Tuple[LfsUploadPartMetadata, int]:
    chunk_tuple, lfs_version = input_tuple
    part_number, chunk = chunk_tuple
    upload_url_response = BiolibLargeFileSystemApi.get_upload_url(
        resource_version_uuid=lfs_version['uuid'],
        part_number=part_number,
    )
    presigned_upload_url = upload_url_response['presigned_upload_url']
    max_upload_retries = 5

    for retry_count in range(max_upload_retries):
        try:
            logger.info(f'Uploading part {part_number}...')
            response = requests.put(data=chunk, url=presigned_upload_url)

        except BrokenPipeError as error:
            if retry_count == max_upload_retries - 1:
                raise BioLibError(f"Max retries hit, when uploading part {part_number}. Exiting...") from error
            else:
                logger.warning(f"Encountered error when uploading part {part_number}. Retrying...")
                continue

        except Exception as error:
            logger.debug(str(error))
            raise BioLibError(f'Failed to reach out to S3 at url: {presigned_upload_url}') from error

        if not response.ok:
            raise BioLibError(response.content)

        break  # Break if no exception thrown and response is OK

    return LfsUploadPartMetadata(PartNumber=part_number, ETag=response.headers['ETag']), len(chunk)


def get_lfs_info_from_uri(lfs_uri):
    lfs_uri_parts = lfs_uri.split('/')
    lfs_uri_parts = [uri_part for uri_part in lfs_uri_parts if '@' not in uri_part]  # Remove hostname
    team_account_handle = lfs_uri_parts[0]
    lfs_name = lfs_uri_parts[1]
    account = BiolibAccountApi.fetch_by_handle(team_account_handle)
    return account, lfs_name


def get_files_size_and_of_dir(dir_path):
    data_size = 0
    file_list = []
    for path, _, files in os.walk(dir_path):
        for file in files:
            file_path = os.path.join(path, file)
            if os.path.islink(file_path):
                continue  # skip symlinks
            file_list.append(file_path)
            data_size += os.path.getsize(file_path)
    return file_list, data_size


def get_iterable_zip_stream(files, chunk_size: int) -> Iterator[bytes]:
    class ChunkedIOBuffer(io.RawIOBase):
        def __init__(self, chunk_size: int):
            super().__init__()
            self.chunk_size = chunk_size
            self.tmp_data = bytearray()

        def get_buffer_size(self):
            return len(self.tmp_data)

        def read_chunk(self):
            chunk = bytes(self.tmp_data[:self.chunk_size])
            self.tmp_data = self.tmp_data[self.chunk_size:]
            return chunk

        def write(self, data):
            data_length = len(data)
            self.tmp_data += data
            return data_length

    # create chunked buffer to hold data temporarily
    io_buffer = ChunkedIOBuffer(chunk_size)

    # create zip writer that will write to the io buffer
    zip_writer = zf.ZipFile(io_buffer, mode='w')  # type: ignore

    for file_path in files:
        # generate zip info and prepare zip pointer for writing
        z_info = zf.ZipInfo.from_file(file_path)
        zip_pointer = zip_writer.open(z_info, mode='w')

        # read file chunk by chunk
        with open(file_path, 'br') as file_pointer:
            while True:
                chunk = file_pointer.read(chunk_size)
                if len(chunk) == 0:
                    break
                # write the chunk to the zip
                zip_pointer.write(chunk)
                # if writing the chunk caused us to go over chunk_size, flush it
                if io_buffer.get_buffer_size() > chunk_size:
                    yield io_buffer.read_chunk()
        zip_pointer.close()

    # flush any remaining data in the stream (e.g. zip file meta data)
    zip_writer.close()
    while True:
        chunk = io_buffer.read_chunk()
        if len(chunk) == 0:
            break
        yield chunk


def create_large_file_system(lfs_uri: str):
    BiolibApiClient.assert_is_signed_in(authenticated_action_description='create a Large File System')
    lfs_account, lfs_name = get_lfs_info_from_uri(lfs_uri)
    lfs_resource = BiolibLargeFileSystemApi.create(account_uuid=lfs_account['public_id'], name=lfs_name)
    logger.info(f"Successfully created new Large File System '{lfs_resource['uri']}'")


def push_large_file_system(lfs_uri: str, input_dir: str) -> None:
    BiolibApiClient.assert_is_signed_in(authenticated_action_description='push data to a Large File System')

    if not os.path.isdir(input_dir):
        raise BioLibError(f'Could not find folder at {input_dir}')

    lfs_resource = BioLibApp(lfs_uri)

    files_to_zip, data_size = get_files_size_and_of_dir(input_dir)
    data_size_in_mb = round(data_size / 10 ** 6)
    print(f'Zipping {len(files_to_zip)} files, in total ~{data_size_in_mb}mb of data')

    lfs_resource_version = BiolibLargeFileSystemApi.create_version(resource_uuid=lfs_resource.uuid)
    bytes_written = 0
    parts: List[LfsUploadPartMetadata] = []
    process_pool = multiprocessing.Pool(
        # use 8 cores, unless less is available
        processes=min(8, multiprocessing.cpu_count() - 1),
        maxtasksperchild=10,
    )

    chunk_iterator = enumerate(get_iterable_zip_stream(files=files_to_zip, chunk_size=50_000_000), 1)  # 50 MB
    full_iterator = zip(chunk_iterator, repeat(lfs_resource_version))

    for part_metadata, chunk_length in process_pool.imap(upload_chunk, full_iterator):
        parts.append(part_metadata)

        # calculate approximate progress
        # note: it's approximate because data_size doesn't include the size of zip metadata
        bytes_written += chunk_length
        approx_progress_percent = min(bytes_written / (data_size + 1) * 100, 100)
        print(f'Wrote {chunk_length} bytes, the approximate progress is {round(approx_progress_percent, 2)}%')

    BiolibLargeFileSystemApi.complete_upload(lfs_resource_version['uuid'], parts, size_bytes=data_size)
    logger.info(f"Successfully pushed a new LFS version '{lfs_resource_version['uri']}'")
