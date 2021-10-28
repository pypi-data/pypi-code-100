
"""
Presubmission script to export max scene files.

To write your own presubmission script, use this as a jumping off point and
consult the Conductor Max reference documentation.
https://docs.conductortech.com/reference/max/#pre-submission-script
"""
 
import os
from pymxs import runtime as rt
 
 
def main(dialog, *args):
    """
    Export assets needed for a max render.

    Return an object containing the list of generated assets.

    args

    """
    fn = os.path.splitext(args[0])[0]

    max_scene = export_max_scene(dialog, fn)
 
    amendments = {
        "upload_paths": [max_scene]
    }
    return amendments


def export_max_scene(dialog, max_scene_prefix):
 
    camera_name = dialog.main_tab.section(
        "GeneralSection").camera_component.combobox.currentText()
    print("Set the current view to look through camera: {}", format(
        camera_name))

    rt.viewport.setCamera(rt.getNodeByName(camera_name))

    print("Ensure directory is available for max scene file")
    _ensure_directory_for(max_scene_prefix)

    print("Closing render setup window if open...")
    if rt.renderSceneDialog.isOpen():
        rt.renderSceneDialog.close()
 

    print("Exporting max scene file")
    
    result = rt.saveMaxFile(
        max_scene_prefix,
        clearNeedSaveFlag=False, 
        useNewFile=False)
    
    max_scene = "{}.max".format(max_scene_prefix)
    if os.path.exists(max_scene):
        print("Scene was exported successfully")
    else:
        raise ValueError(
            "Max scene save failed.")

    print("Completed max scene export..")

    return max_scene

 

def _ensure_directory_for(path):
    """Ensure that the parent directory of `path` exists"""
    dirname = os.path.dirname(path)
    if not os.path.isdir(dirname):
        os.makedirs(dirname)
