"""Remote upload utils library."""

from ftplib import FTP, error_perm
from homebot.core.config import get_config
from homebot.core.logging import LOGI, LOGW
import os.path
import paramiko
from pathlib import Path
import shutil

class UploaderBase:
	def __init__(self, profile):
		"""Initialize the uploader variables."""
		self.destination_path_base = Path(get_config(f"libupload.{profile}.base_dir"))
		self.host = get_config(f"libupload.{profile}.host")
		self.port = get_config(f"libupload.{profile}.port")
		self.server = self.host if self.port is None else f"{self.host}:{self.port}"
		self.username = get_config(f"libupload.{profile}.username")
		self.password = get_config(f"libupload.{profile}.password")

	def upload(self, file: Path, destination: Path):
		"""Upload an artifact using settings from config.env."""
		if not file.is_file():
			raise FileNotFoundError("File doesn't exists")

		if self.destination_path_base is None:
			destination_path = destination
		else:
			destination_path = self.destination_path_base / destination

		LOGI(f"Started uploading of {file.name}")

		self._upload(file, destination_path)

		LOGI(f"Finished uploading of {file.name}")
		return True

	def _upload(self, file: Path, destination_path: Path):
		raise NotImplementedError("Trying to upload with UploaderBase")

class UploaderLocalcopy(UploaderBase):
	def _upload(self, file: Path, destination_path: Path):
		os.makedirs(destination_path, exist_ok=True)
		shutil.copy(file, destination_path)

class UploaderFTP(UploaderBase):
	def _upload(self, file: Path, destination_path: Path):
		ftp = FTP(self.server)
		ftp.login(self.username, self.password)
		self.chdir(ftp, destination_path)
		with open(file, 'rb') as f:
			ftp.storbinary('STOR %s' % file.name, f)
			f.close()
		ftp.close()

	def chdir(self, ftp: FTP, remote_directory: Path):
		if remote_directory == '/':
			ftp.cwd('/')
			return
		if remote_directory == '':
			return
		try:
			ftp.cwd(str(remote_directory))
		except error_perm:
			dirname, basename = os.path.split(str(remote_directory).rstrip('/'))
			self.chdir(ftp, dirname)
			ftp.mkd(basename)
			ftp.cwd(basename)
			return True

class UploaderSFTP(UploaderBase):
	def _upload(self, file: Path, destination_path: Path):
		transport = paramiko.Transport(self.server)
		transport.connect(username=self.username, password=self.password)
		sftp = paramiko.SFTPClient.from_transport(transport)
		self.chdir(sftp, destination_path)
		sftp.put(file, file.name)
		sftp.close()
		transport.close()

	def chdir(self, sftp: paramiko.SFTPClient, remote_directory: Path):
		if remote_directory == '/':
			sftp.chdir('/')
			return
		if remote_directory == '':
			return
		try:
			sftp.chdir(str(remote_directory))
		except IOError:
			dirname, basename = os.path.split(str(remote_directory).rstrip('/'))
			self.chdir(sftp, dirname)
			sftp.mkdir(basename)
			sftp.chdir(basename)
			return True

METHODS: dict[str, UploaderBase] = {
	"localcopy": UploaderLocalcopy,
	"ftp": UploaderFTP,
	"sftp": UploaderSFTP,
}

profiles = get_config("libupload", {}).keys()
uploaders: dict[str, UploaderBase] = {
	profile: METHODS.get(get_config(f"libupload.{profile}.method"), UploaderBase)(profile)
	for profile in profiles
}

def Uploader(profile: str = "default", fallback_to_default: bool = False) -> UploaderBase:
	if fallback_to_default:
		if not profile in uploaders:
			profile = "default"

	if not profile in uploaders:
		raise AssertionError(f"Profile {profile} not found")

	return uploaders[profile]
