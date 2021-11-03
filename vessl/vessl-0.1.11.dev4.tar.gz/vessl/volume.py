import os
import tempfile
from typing import List, Optional, Tuple

from openapi_client.models import (
    ProtoVolumeMountRequest,
    ProtoVolumeMountRequests,
    ProtoVolumeMountRequestSourceArchiveFile,
    ProtoVolumeMountRequestSourceCode,
    ProtoVolumeMountRequestSourceDataset,
    ProtoVolumeMountRequestSourceDatasetVersion,
    ResponseFileMetadata,
    ResponseProjectRepository,
    VolumeFileCopyAPIPayload,
    VolumeFileCreateAPIPayload,
)
from vessl import vessl_api
from vessl.organization import _get_organization_name
from vessl.project import _get_project
from vessl.util.constant import (
    DATASET_VERSION_HASH_LATEST,
    MOUNT_PATH_EMPTY_DIR,
    MOUNT_TYPE_ARCHIVE_FILE,
    MOUNT_TYPE_CODE,
    MOUNT_TYPE_DATASET,
    MOUNT_TYPE_DATASET_VERSION,
    MOUNT_TYPE_EMPTY_DIR,
    MOUNT_TYPE_OUTPUT,
)
from vessl.util.downloader import Downloader
from vessl.util.exception import GitError, InvalidVolumeFileError, VesslApiException
from vessl.util.git import get_git_branch, get_git_diff_path, get_git_ref, get_git_repo
from vessl.util.random import random_string
from vessl.util.uploader import Uploader
from vessl.util.zipper import Zipper


def read_volume_file(volume_id: int, path: str) -> ResponseFileMetadata:
    return vessl_api.volume_file_read_api(volume_id=volume_id, path=path)


def list_volume_files(
    volume_id: int,
    need_download_url: bool = False,
    path: str = "",
    recursive: bool = False,
) -> List[ResponseFileMetadata]:
    result = vessl_api.volume_file_list_api(
        volume_id=volume_id,
        recursive=recursive,
        path=path,
        need_download_url=need_download_url,
    ).results
    return sorted(result, key=lambda x: x.path)


def create_volume_file(volume_id: int, is_dir: bool, path: str) -> ResponseFileMetadata:
    result = vessl_api.volume_file_create_api(
        volume_id=volume_id,
        volume_file_create_api_payload=VolumeFileCreateAPIPayload(
            is_dir=is_dir,
            path=path,
        ),
    )
    assert isinstance(result, ResponseFileMetadata)
    return result


def delete_volume_file(
    volume_id: int, path: str, recursive: bool = False
) -> List[ResponseFileMetadata]:
    return vessl_api.volume_file_delete_api(
        volume_id=volume_id, path=path, recursive=recursive
    ).deleted_files


def upload_volume_file(volume_id: int, path: str) -> ResponseFileMetadata:
    return vessl_api.volume_file_uploaded_api(volume_id=volume_id, path=path)


def copy_volume_file(
    source_volume_id: Optional[int],
    source_path: str,
    dest_volume_id: Optional[int],
    dest_path: str,
    recursive: bool = False,
) -> Optional[List[ResponseFileMetadata]]:
    if source_volume_id is None and dest_volume_id:
        return _copy_volume_file_local_to_remote(
            source_path,
            dest_volume_id,
            dest_path,
        )

    if dest_volume_id is None and source_volume_id:
        return _copy_volume_file_remote_to_local(
            source_volume_id,
            source_path,
            dest_path,
        )

    if source_volume_id and dest_volume_id:
        return _copy_volume_file_remote_to_remote(
            source_volume_id, source_path, dest_volume_id, dest_path, recursive
        )


def _copy_volume_file_local_to_remote(
    source_path: str, dest_volume_id: int, dest_path: str
) -> List[ResponseFileMetadata]:
    """Copy local to remote

    Behavior works like linux cp command
    - `source_path` is file
      - `dest_path` is not a directory: copy as file with new name
      - `dest_path` is directory: copy file into directory with original name
    - `source_path` is directory
      - `dest_path` is file: error
      - `dest_path` does not exist: create `dest_path` and copy contents of `source_path`
      - `dest_path` exists: copy `source_path` as subdirectory of `dest_path`
    """

    output = "Successfully uploaded {} out of {} file(s)."
    source_path = source_path.rstrip("/")

    try:
        dest_file = read_volume_file(dest_volume_id, dest_path)
    except VesslApiException:
        dest_file = None

    if not os.path.isdir(source_path):
        if dest_file and (dest_file.is_dir or dest_path.endswith("/")):
            dest_path = os.path.join(dest_path, os.path.basename(source_path))

        uploaded_file = Uploader.upload(source_path, dest_volume_id, dest_path)

        print(output.format(1, 1))
        return [uploaded_file]

    if dest_file and not dest_file.is_dir:
        raise InvalidVolumeFileError(
            f"Destination path is not a directory: {dest_path}."
        )

    if dest_file and dest_file.is_dir:
        dest_path = os.path.join(dest_path, os.path.basename(source_path))

    paths = Uploader.get_paths_in_dir(source_path)
    uploaded_files = Uploader.bulk_upload(source_path, paths, dest_volume_id, dest_path)

    print(output.format(len(uploaded_files), len(paths)))
    return uploaded_files


def _copy_volume_file_remote_to_local(
    source_volume_id: int,
    source_path: str,
    dest_path: str,
) -> None:
    """Copy remote to local

    Behavior works like linux cp command
    - `source_path` is file
      - `dest_path` is not a directory: copy as file with new name
      - `dest_path` is directory: copy file into directory with original name
    - `source_path` is directory
      - `dest_path` is file: error
      - `dest_path` does not exist: create `dest_path` and copy contents of `source_path`
      - `dest_path` exists: copy `source_path` as subdirectory of `dest_path`
    """

    output = "Successfully downloaded {} out of {} file(s)."
    source_file = read_volume_file(source_volume_id, source_path)

    if not source_file.is_dir:
        if os.path.isdir(dest_path):
            dest_path = os.path.join(dest_path, os.path.basename(source_file.path))

        Downloader.download(dest_path, source_file)

        print(output.format(1, 1))
        return

    files = list_volume_files(
        volume_id=source_volume_id,
        need_download_url=True,
        path=source_path,
        recursive=True,
    )

    if os.path.isfile(dest_path):
        raise InvalidVolumeFileError(
            f"Destination path is not a directory: {dest_path}."
        )

    prefix = source_path.rstrip("/")
    if os.path.isdir(dest_path):
        prefix = os.path.dirname(prefix)

    if prefix:
        prefix += "/"
        for file in files:
            file.path = file.path.replace(prefix, "", 1)  # Remove prefix
            file.path = os.path.normpath(file.path)

    downloaded_files = Downloader.bulk_download(dest_path, files)
    print(output.format(len(downloaded_files), len([x for x in files if not x.is_dir])))


def _copy_volume_file_remote_to_remote(
    source_volume_id: int,
    source_path: str,
    dest_volume_id: int,
    dest_path: str,
    recursive: bool,
) -> None:
    if source_volume_id != dest_volume_id:
        raise InvalidVolumeFileError("Files can only be copied within the same volume.")

    files = vessl_api.volume_file_copy_api(
        volume_id=source_volume_id,
        volume_file_copy_api_payload=VolumeFileCopyAPIPayload(
            dest_path=dest_path,
            recursive=recursive,
            source_dataset_version="latest",
            source_path=source_path,
        ),
    ).copied_files

    print(f"Successfully downloaded {len(files)} out of {len(files)} file(s).")


def _configure_volume_mount_requests(
    dataset_mounts: Optional[List[str]],
    git_ref_mounts: Optional[List[str]],
    git_diff_mount: Optional[str],
    archive_file_mount: Optional[str],
    root_volume_size: Optional[str],
    working_dir: Optional[str],
    output_dir: Optional[str],
    **kwargs,
) -> ProtoVolumeMountRequests:
    requests = [
        _configure_volume_mount_request_empty_dir(),
        _configure_volume_mount_request_output(output_dir),
    ]

    if git_ref_mounts is None and git_diff_mount is None and archive_file_mount is None:
        # No information for code mount is given - user is creating new experiment from CLI.
        # Generate VolumeMountRequest from projectRepository and local working directory
        requests.extend(_configure_volume_mount_request_local(**kwargs))
    else:
        # Explicit information for code mount is given - user is reproducing experiment from CLI.
        if git_ref_mounts is not None:
            requests.extend(
                _configure_volume_mount_request_codes(
                    git_ref_mounts, git_diff_mount, **kwargs
                )
            )
        if archive_file_mount is not None:
            requests.append(
                _configure_volume_mount_request_archive_file(
                    archive_file_mount, **kwargs
                )
            )

    if dataset_mounts is not None:
        requests += [
            _configure_volume_mount_request_dataset(dataset_mount, **kwargs)
            for dataset_mount in dataset_mounts
        ]

    return ProtoVolumeMountRequests(
        root_volume_size=root_volume_size,
        working_dir=working_dir,
        requests=requests,
    )


def _configure_volume_mount_request_dataset(
    dataset_mount: str, **kwargs
) -> ProtoVolumeMountRequest:
    from vessl.dataset import read_dataset, read_dataset_version

    mount_path, dataset_path = dataset_mount.split(":", 1)
    mount_path = os.path.join(mount_path, "")  # Ensure path ends in /

    organization_name = _get_organization_name(**kwargs)
    dataset_name = dataset_path
    dataset_version_hash = DATASET_VERSION_HASH_LATEST

    if "@" in dataset_path:
        # Example: mnist@3d1e0f91c
        dataset_name, dataset_version_hash = dataset_path.rsplit("@", 1)

    if "/" in dataset_name:
        # Example: org1/mnist@3d1e0f91c
        organization_name, dataset_name = dataset_name.split("/", 1)

    dataset = read_dataset(dataset_name, organization_name=organization_name)

    if not dataset.is_version_enabled:
        return ProtoVolumeMountRequest(
            mount_type=MOUNT_TYPE_DATASET,
            mount_path=mount_path,
            dataset=ProtoVolumeMountRequestSourceDataset(
                dataset_id=dataset.id,
                dataset_name=dataset_name,
            ),
        )

    if dataset_version_hash != DATASET_VERSION_HASH_LATEST:
        dataset_version_hash = read_dataset_version(
            dataset.id, dataset_version_hash
        ).version_hash  # Get full version hash from truncated one given by input

    return ProtoVolumeMountRequest(
        mount_type=MOUNT_TYPE_DATASET_VERSION,
        mount_path=mount_path,
        dataset_version=ProtoVolumeMountRequestSourceDatasetVersion(
            dataset_id=dataset.id,
            dataset_name=dataset_name,
            dataset_version_hash=dataset_version_hash,
        ),
    )


def _configure_volume_mount_request_local(**kwargs) -> List[ProtoVolumeMountRequest]:
    project = _get_project(**kwargs)

    local_git_owner, local_git_repo = None, None
    local_repo_is_project_repository = False
    try:
        local_git_owner, local_git_repo = get_git_repo()
    except GitError:
        pass

    volume_mount_requests: List[ProtoVolumeMountRequest] = []
    used_mount_pathes = set()
    for repo in project.project_repositories:
        mount_path = f"/home/vessl/{repo.git_repo}"
        if mount_path in used_mount_pathes:
            mount_path = f"/home/vessl/{repo.git_repo}-{repo.git_owner}"

        git_mount_info = f"github/{repo.git_owner}/{repo.git_repo}/latest"
        git_diff_path = None
        if repo.git_owner == local_git_owner and repo.git_repo == local_git_repo:
            # Current working directory is one of the project repository.
            # Mount VolumeSourceCode with potential uncommitted changes
            local_repo_is_project_repository = True
            git_diff_path = get_git_diff_path(project)
            git_mount_info = git_mount_info.replace("latest", get_git_ref())
        volume_mount_requests.append(
            _configure_volume_mount_request_code(
                git_ref_mount=f"{mount_path}:{git_mount_info}",
                git_diff_mount=None
                if git_diff_path is None
                else f"{mount_path}:{git_diff_path}",
            )
        )

    if not local_repo_is_project_repository:
        # Current working directory is not a known git directory.
        # Mount whole directory as a VolumeSourceArchivedFile
        cwd = os.path.abspath(os.getcwd())
        zip_path = os.path.abspath(
            os.path.join(tempfile.gettempdir(), f"{project.name}_{random_string()}.zip")
        )
        zipper = Zipper(zip_path, "w")
        zipper.zipdir(cwd, zipper)
        zipper.close()

        uploaded = Uploader.upload(
            local_path=zipper.filename,
            volume_id=project.volume_id,
            remote_path=os.path.basename(zipper.filename),
        )
        os.remove(zipper.filename)
        volume_mount_requests.append(
            _configure_volume_mount_request_archive_file(
                archive_file_mount=f"/home/vessl/local:{uploaded.path}"
            )
        )

    return volume_mount_requests


def _configure_volume_mount_request_codes(
    git_ref_mounts: List[str], git_diff_mount: str, **kwargs
) -> List[ProtoVolumeMountRequest]:
    return [
        _configure_volume_mount_request_code(git_ref_mount, git_diff_mount, **kwargs)
        for git_ref_mount in git_ref_mounts
    ]


def _configure_volume_mount_request_code(
    git_ref_mount: str, git_diff_mount: str, **kwargs
) -> ProtoVolumeMountRequest:
    # Generate ProtoVolumeMountRequestSourceCode from git_ref_mount
    # ref_mount_info = <provider>/<owner>/<repo>/<commit>
    ref_mount_path, ref_mount_info = git_ref_mount.split(":", 1)
    code_info = ref_mount_info.split("/", 3)

    vmr_source_code = ProtoVolumeMountRequestSourceCode(
        git_provider=code_info[0],
        git_owner=code_info[1],
        git_repo=code_info[2],
        git_ref=code_info[3],
    )

    # Add optional git_diff parameter if git_diff_mount has same mount path
    if git_diff_mount is not None:
        diff_mount_path, diff_mount_file = git_diff_mount.split(":", 1)
        if ref_mount_path == diff_mount_path:
            vmr_source_code.git_diff_file = diff_mount_file

    return ProtoVolumeMountRequest(
        mount_type=MOUNT_TYPE_CODE,
        mount_path=ref_mount_path,
        code=vmr_source_code,
    )


def _configure_volume_mount_request_archive_file(
    archive_file_mount: str,
) -> ProtoVolumeMountRequest:
    mount_path, archive_file_path = archive_file_mount.split(":", 1)

    return ProtoVolumeMountRequest(
        mount_type=MOUNT_TYPE_ARCHIVE_FILE,
        mount_path=mount_path,
        archive_file=ProtoVolumeMountRequestSourceArchiveFile(
            archive_file=archive_file_path,
        ),
    )


def _configure_volume_mount_request_empty_dir() -> ProtoVolumeMountRequest:
    return ProtoVolumeMountRequest(
        mount_type=MOUNT_TYPE_EMPTY_DIR,
        mount_path=MOUNT_PATH_EMPTY_DIR,
    )


def _configure_volume_mount_request_output(output_dir: str) -> ProtoVolumeMountRequest:
    return ProtoVolumeMountRequest(
        mount_type=MOUNT_TYPE_OUTPUT,
        mount_path=output_dir,
    )
