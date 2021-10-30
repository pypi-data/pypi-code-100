import time
import requests
import subprocess
import os
import hashlib
import platform
import json
import tempfile
import apt

BUFFER_SIZE = 65536
PROGRESS_BAR_WIDTH = 70

ARCHITECTURE_CONVERSION = {"armv7l": "ARMv7", "x86_64": "Intel/AMD 64-bit"}

def update():
    python_architecture = platform.machine()

    if python_architecture in ARCHITECTURE_CONVERSION:
        architecture = ARCHITECTURE_CONVERSION[python_architecture]
    else:
        exit(f"Error: Script does not support architecture: {python_architecture}")

    print("Finding latest Plex version...")

    resp = requests.get('https://plex.tv/api/downloads/5.json', params={'_': int(time.time() * 1000)})

    try:
        data = resp.json()['computer']['Linux']
        version = data['version']
        releases = data['releases']
    except (json.decoder.JSONDecodeError, KeyError):
        exit("Error: Unable to parse Plex versions")

    print("Checking if lastest version installed...")

    apt_cache = apt.Cache()
    if 'plexmediaserver' in apt_cache:
        installed_versions = apt_cache['plexmediaserver'].versions
        for v in installed_versions:
            if v.version == version:
                exit("Latest version already installed")

    print("Downloading Plex...")

    url = None

    try:
        for release in releases:
            if architecture in release['label']:
                url = release['url']
                download_checksum = release['checksum']
                break
    except KeyError:
        exit("Error: Unable to parse Plex architectures")

    if url:
        filename = url.split('/')[-1]

        with tempfile.TemporaryDirectory() as tmpdirname:
            try:
                filepath = download_file(url, tmpdirname, download_checksum)
            except ValueError as e:
                exit("Error with download. Reason: {e}")

            print("Installing Plex...")

            subprocess.run(['sudo', 'apt', 'install', filepath])
    else:
        exit(f"Error: No plex version found for architecture: {python_architecture}")

def download_file(url, directory, sha1_compare):

    sha1 = hashlib.sha1()

    resp = requests.get(url, stream = True)

    filename = resp.headers['Content-Disposition'] if 'Content-Disposition' in resp.headers else url.split('/')[-1]
    filesize = int(resp.headers['Content-Length']) if 'Content-Length' in resp.headers else -1
    filepath = os.path.join(directory, filename)

    bytes_downloaded = 0

    with open(filepath, 'wb') as file:
        for data in resp.iter_content(BUFFER_SIZE):
            file.write(data)
            sha1.update(data)

            bytes_downloaded += len(data)

            if filesize > 0:
                progress = int(bytes_downloaded / filesize * PROGRESS_BAR_WIDTH)
                print("[{}{}]".format("=" * progress, " " * (PROGRESS_BAR_WIDTH - progress)), end='\r')
            else:
                print("{} bytes downloaded".format(bytes_downloaded), end='\r')

        print()

    if sha1.hexdigest() != sha1_compare:
        raise ValueError("Hashes do not match")

    return filepath
