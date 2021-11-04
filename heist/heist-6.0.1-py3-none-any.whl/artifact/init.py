import hashlib
import os
import pathlib
import shutil
import tarfile
import tempfile
import zipfile

import aiohttp


def __init__(hub):
    hub.artifact.ACCT = ["artifact"]


def extract(hub, tmpdir, binary):
    """
    extract the binary into the temporary directory
    """
    # create tmp dir and unzip/untar the artifact
    if tarfile.is_tarfile(binary):
        salt_tar = tarfile.open(binary)
        salt_tar.extractall(tmpdir)
        salt_tar.close()
        return True
    elif zipfile.is_zipfile(binary):
        salt_zip = zipfile.ZipFile(binary)
        salt_zip.extractall(tmpdir)
        salt_zip.close()
        return True
    hub.log.error("Binary is not a zip file or tar file. Will not extract")
    return False


def verify(hub, location, hash_value, hash_type="sha256"):
    with open(location, "rb") as fp:
        file_hash = getattr(hashlib, hash_type)(fp.read()).hexdigest()
        if not file_hash == hash_value:
            return False
    return True


async def fetch(hub, session, url, download=False, location=False):
    """
    Fetch a url and return json. If downloading artifact
    return the download location.
    """
    async with session.get(url) as resp:
        if resp.status == 200:
            if download:
                with open(location, "wb") as fn_:
                    fn_.write(await resp.read())
                return location
            return await resp.json()
        hub.log.critical(f"Cannot query url {url}. Returncode {resp.status} returned")
        return False


async def get(
    hub,
    artifact_name: str,
    target_os: str,
    version: str = None,
    repo_data=None,
):
    """
    Fetch a url return the download location.
    """
    async with aiohttp.ClientSession() as session:
        with tempfile.TemporaryDirectory() as tmpdirname:
            # Download and verify the designated Heist manager artifact
            tmp_artifact_location = await hub.artifact[artifact_name].get(
                target_os=target_os,
                version=version,
                repo_data=repo_data,
                session=session,
                tmpdirname=pathlib.Path(tmpdirname),
            )
            if not tmp_artifact_location:
                return False

            artifacts_dir = pathlib.Path(hub.OPT.heist.artifacts_dir)
            artifact_location = artifacts_dir / tmp_artifact_location.name
            if not hub.tool.path.clean_path(artifacts_dir, tmp_artifact_location.name):
                hub.log.error(
                    f"The tmp artifact {tmp_artifact_location.name} is not in the correct directory"
                )
                return False

            # artifact is already downloaded we do not need to copy/check
            if tmp_artifact_location == artifact_location:
                return True

            hub.log.info(
                f"Copying the artifact {artifact_location.name} to {str(artifacts_dir)}"
            )
            shutil.move(tmp_artifact_location, artifact_location)

    # ensure artifact was downloaded
    if not any(str(version) in x for x in os.listdir(str(artifacts_dir))):
        hub.log.critical(
            f"Did not find the {version} artifact in {str(artifacts_dir)}."
            f" Untarring the artifact failed or did not include version"
        )
        return False
    return artifact_location


def version(hub):
    # TODO Determine which artifact to use, find the right plugin, and find out the target's version of the artifact
    ...


def deploy(hub):
    # TODO Determine which artifact to use, find the right plugin, and execute it's deploy function
    ...


async def clean(hub, target_name, tunnel_plugin):
    """
    Clean up the deployed artifact and files
    """
    # remove run directory
    run_dir = hub.heist.CONS[target_name]["run_dir"]
    ret = await hub.tunnel[tunnel_plugin].cmd(target_name, f"[ -d {run_dir} ]")
    if ret.returncode == 0:
        await hub.tunnel[tunnel_plugin].cmd(target_name, f"rm -rf {run_dir}")

    # remove parent directory if its empty
    # If its not empty, there might be another running instance of heist that
    # was previously deployed
    await hub.tunnel[tunnel_plugin].cmd(
        target_name, f"rmdir {hub.heist.CONS[target_name]['run_dir'].parent}"
    )
