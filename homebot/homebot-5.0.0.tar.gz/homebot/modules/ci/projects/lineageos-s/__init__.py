"""LineageOS S CI project."""

from homebot.modules.ci.projects.aosp.project import AOSPProject

class Project(AOSPProject):
	name = "LineageOS"
	version = "19.0"
	android_version = "12"
	category = "ROMs"
	lunch_prefix = "lineage"
	lunch_suffix = "userdebug"
	build_target = "bacon"
	zip_name = "lineage-*.zip"
	date_regex = "lineage-[0-9.]+-(.+?)-.*.zip"
