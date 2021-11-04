"""LineageOS R CI project."""

from homebot.modules.ci.projects.aosp.project import AOSPProject

class Project(AOSPProject):
	name = "LineageOS"
	version = "18.1"
	android_version = "11"
	category = "ROMs"
	lunch_prefix = "lineage"
	lunch_suffix = "userdebug"
	build_target = "bacon"
	zip_name = "lineage-*.zip"
	date_regex = "lineage-[0-9.]+-(.+?)-.*.zip"
