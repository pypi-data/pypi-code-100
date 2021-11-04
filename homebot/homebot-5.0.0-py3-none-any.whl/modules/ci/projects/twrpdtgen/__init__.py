"""twrpdtgen CI project."""

from datetime import date
from git import Repo
from git.exc import GitCommandError
from github import Github, GithubException
from twrpdtgen.utils.logging import LOGE
from homebot.core.config import get_config
from homebot.core.error_handler import format_exception
from homebot.modules.ci.parser import CIParser
from pathlib import Path
import requests
from telegram import Update
from telegram.ext import CallbackContext
from tempfile import TemporaryDirectory
from twrpdtgen.devicetree import DeviceTree
from twrpdtgen.utils.deviceinfo import PARTITIONS

BUILD_DESCRIPTION = ["ro.build.description"] + [f"ro.{partition}.build.description" for partition in PARTITIONS]

class Project:
	name = "twrpdtgen"

	def __init__(self, update: Update, context: CallbackContext, args: list[str]):
		"""Init twrpdtgen project class."""
		self.update = update
		self.context = context
		self.args = args
		parser = CIParser(prog="/ci twrpdtgen")
		parser.set_output(self.update.message.reply_text)
		parser.add_argument('url', help='URL of the image')
		self.parsed_args = parser.parse_args(args)

	def build(self):
		status_message = self.update.message.reply_text("Downloading file...")

		# Download file
		tempdir = TemporaryDirectory()
		path = Path(tempdir.name)
		url = self.parsed_args.url
		file = path / "recovery.img"
		open(file, 'wb').write(requests.get(url, allow_redirects=True).content)

		# Generate device tree
		status_message.edit_text("Generating device tree...")
		try:
			devicetree = DeviceTree(file)
			devicetree_folder = devicetree.dump_to_folder(path / "working", git=True)
		except Exception as e:
			status_message.edit_text("Device tree generation failed\n"
									f"Error: {e}")
			return

		today = date.today()
		build_description = devicetree.deviceinfo.get_prop(BUILD_DESCRIPTION, raise_exception=False)
		if build_description is not None:
			branch = build_description.replace(" ", "-")
		else:
			status_message.edit_text("Failed to get build description prop, using date as a branch")
			branch = f"{today.year}-{today.month}-{today.day}"

		# Upload to GitHub
		status_message.edit_text("Pushing to GitHub...")
		gh_username = get_config("ci.github_username")
		gh_token = get_config("ci.github_token")
		gh_org_name = get_config("ci.twrpdtgen.github_org")
		repo_name = f"android_device_{devicetree.deviceinfo.manufacturer}_{devicetree.deviceinfo.codename}"
		git_repo_url = f"https://{gh_username}:{gh_token}@github.com/{gh_org_name}/{repo_name}"

		# Get organization
		try:
			gh = Github(gh_token)
			gh_org = gh.get_organization(gh_org_name)
		except GithubException as error:
			status_message.edit_text(f"Failed to get organization\n"
									 f"Error: {error}")
			return

		# Create repo if needed
		status_message.edit_text("Creating repo if needed...")
		try:
			devicetree_repo = gh_org.create_repo(name=repo_name, private=False, auto_init=False)
		except GithubException as error:
			if error.status != 422:
				status_message.edit_text("Repo creation failed\n"
										 f"Error: {error.status} {error}")
				return
			devicetree_repo = gh_org.get_repo(name=repo_name)

		status_message.edit_text("Pushing...")
		try:
			Repo(devicetree_folder).git.push(git_repo_url, f"HEAD:refs/heads/{branch}")
			devicetree_repo.edit(default_branch=branch)
		except GitCommandError as e:
			status_message.edit_text("Error: Push to remote failed!")
			LOGE("Push to GitHub failed:\n"
			     f"{format_exception(e)}")
			return

		status_message.edit_text("Done")

		channel_id = get_config("ci.twrpdtgen.channel_id")
		self.context.bot.send_message(channel_id,
									  "TWRP device tree generated\n"
									  f"Codename: {devicetree.deviceinfo.codename}\n"
									  f"Manufacturer: {devicetree.deviceinfo.manufacturer}\n"
									  f"Build description: {build_description}\n"
									  f"Device tree: {devicetree_repo.html_url}/tree/{branch}",
									  disable_web_page_preview=True)
