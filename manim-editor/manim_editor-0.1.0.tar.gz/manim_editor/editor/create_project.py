"""Create Manim Editor project."""
import os
import json
from typing import Any, Dict, Tuple, List

from .manim_loader import get_scenes


def create_project_dir(project_name: str) -> Tuple[bool, str]:
    """Ensure existence of project dir.
    Return True if success and message for the user."""
    print(f"Creating project '{project_name}'.")
    # TODO: valid dir name check for Windows
    if project_name == "":
        return False, "The project name can't be empty."
    if os.path.exists(project_name):
        # empty dirs are ok
        if len(os.listdir(project_name)) == 0:
            return True, f"The project directory '{project_name}' has already been created. It will be used."
        return False, f"The project name '{project_name}' points to a filled directory. If this is a project, you can open it instead."
    try:
        os.mkdir(project_name)
    except FileNotFoundError:
        return False, f"Creation of project directory '{project_name}' failed."
    return True, f"Created new project directory '{project_name}'."


class SectionId:
    def __init__(self, scene_id: int, section_id: int):
        self.scene_id = scene_id
        self.section_id = section_id


def populate_project(project_name: str, section_ids: List[SectionId]) -> bool:
    """Create project JSON file, copy selected section video files and create thumbnails.
    Return False at failure."""
    print(f"Populating project '{project_name}'.")
    # TODO: could theoretically be cached
    scenes = get_scenes()
    # select sections according to ids set by frontend
    sections = [scenes[section.scene_id].sections[section.section_id] for section in section_ids]

    project: List[Dict[str, Any]] = []

    # prepare section
    for id, section in enumerate(sections):
        if not section.set_project(project_name, id):
            return False
        project.append(section.get_dict())

    # write project file
    with open(os.path.join(project_name, "project.json"), "w") as file:
        json.dump(project, file, indent=4)
    return True
