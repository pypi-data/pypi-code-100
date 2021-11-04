from datetime import datetime
from pathlib import Path
from homebot import bot_path
from homebot.core.config import get_config
from homebot.core.error_handler import format_exception
from homebot.core.logging import LOGE
from homebot.lib.libupload import Uploader
from homebot.modules.ci.artifacts import STATUS_ERROR, STATUS_SUCCESS, STATUS_UPLOADING, Artifacts
from homebot.modules.ci.parser import CIParser
from homebot.modules.ci.projects.aosp.post import PostManager, chat_id
from homebot.modules.ci.projects.aosp.returncode import ERROR_CODES, NEEDS_LOGS_UPLOAD, SUCCESS
import re
import subprocess
from telegram.ext import CallbackContext
from telegram.update import Update

ADDITIONAL_ARTIFACTS = [
	"boot.img",
	"vendor_boot.img",
	"dtbo.img",
	"recovery.img",
]

class AOSPProject:
	"""
	This class represent an AOSP project.
	"""
	# This value will also be used for folder name
	name: str
	# Version of the project
	version: str
	# Android version to display on Telegram post
	android_version: str
	# Name of the parent folder used when uploading
	category: str
	# These next 2 values are needed for lunch (e.g. "lineage"_whyred-"userdebug")
	lunch_prefix: str
	lunch_suffix: str
	# Target to build (e.g. to build a ROM's OTA package, use "bacon" or "otapackage", for a recovery project, use "recoveryimage")
	build_target: str
	# Filename of the zip. You can also use wildcards if the name isn't fixed
	zip_name: str
	# Regex to extract date from zip name, empty string to just use full name minus ".zip"
	date_regex: str

	def __init__(self, update: Update, context: CallbackContext, args: list[str]):
		"""Initialize AOSP project class."""
		self.update = update
		self.context = context
		self.args = args
		parser = CIParser(prog="/ci")
		parser.set_output(self.update.message.reply_text)
		parser.add_argument('device', help='device codename')
		parser.add_argument('-ic', '--installclean', help='make installclean before building', action='store_true')
		parser.add_argument('-c', '--clean', help='make clean before building', action='store_true')
		parser.add_argument('--release', help='upload build to release profile', action='store_true')
		parser.set_defaults(clean=False, installclean=False, release=False)
		self.parsed_args = parser.parse_args(args)

	def build(self):
		project_dir = Path(f"{get_config('ci.main_dir', '')}/{self.name}-{self.version}")
		device_out_dir: Path = project_dir / "out" / "target" / "product" / self.parsed_args.device

		artifacts = Artifacts(device_out_dir, [self.zip_name] + ADDITIONAL_ARTIFACTS)
		post_manager = PostManager(self, self.parsed_args.device, artifacts)

		if self.parsed_args.clean is True:
			clean_type = "clean"
		elif self.parsed_args.installclean is True:
			clean_type = "installclean"
		else:
			clean_type = "none"

		post_manager.update("Building")

		command = [bot_path / "modules" / "ci" / "projects" / "aosp" / "tools" / "building.sh",
		           "--sources", project_dir,
		           "--lunch_prefix", self.lunch_prefix,
		           "--lunch_suffix", self.lunch_suffix,
		           "--build_target", self.build_target,
		           "--clean", clean_type,
		           "--device", self.parsed_args.device]

		last_edit = datetime.now()
		process = subprocess.Popen(command, encoding="UTF-8",
		                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		while True:
			output = process.stdout.readline()
			if output == '' and process.poll() is not None:
				break
			if not output:
				continue

			now = datetime.now()
			if (now - last_edit).seconds < 150:
				continue

			result = re.search(r"\[ +([0-9]+% [0-9]+/[0-9]+)\]", output.strip())
			if result is None:
				continue
			result_split = str(result.group(1)).split()
			if len(result_split) != 2:
				continue

			percentage, targets = re.split(" +", result.group(1))
			post_manager.update(f"Building: {percentage} ({targets})")

			last_edit = now

		returncode = process.poll()

		# Process return code
		build_result = ERROR_CODES.get(returncode, "Build failed: Unknown error")

		post_manager.update(build_result)

		needs_logs_upload = NEEDS_LOGS_UPLOAD.get(returncode, False)
		if needs_logs_upload != False:
			log_file = open(project_dir / needs_logs_upload, "rb")
			self.context.bot.send_document(chat_id, log_file)
			log_file.close()

		if returncode != SUCCESS or get_config("ci.upload_artifacts", False) is not True:
			return

		# Upload artifacts
		if self.parsed_args.release:
			uploader_profile = "release"
		else:
			uploader_profile = "ci"

		try:
			uploader = Uploader(uploader_profile)
		except Exception as e:
			post_manager.update(f"{build_result}\n"
			                    f"Upload failed: {type(e)}: {e}")
			return

		artifacts.update()

		zip_filename = list(device_out_dir.glob(self.zip_name))
		if not zip_filename:
			return

		zip_filename = zip_filename[0].name
		date_match = re.search(self.date_regex, zip_filename)
		if date_match and self.date_regex != "":
			folder_name = date_match.group(1)
		else:
			folder_name = zip_filename.removesuffix(".zip")

		post_manager.update()
		upload_path = Path() / self.parsed_args.device / folder_name
		for artifact in artifacts.keys():
			artifacts[artifact] = STATUS_UPLOADING
			post_manager.update()

			try:
				uploader.upload(artifact, upload_path)
			except Exception as e:
				artifacts[artifact] = STATUS_ERROR
				LOGE(f"Error while uploading artifact {artifact.name}:\n"
			         f"{format_exception(e)}")
			else:
				artifacts[artifact] = STATUS_SUCCESS

			post_manager.update()
