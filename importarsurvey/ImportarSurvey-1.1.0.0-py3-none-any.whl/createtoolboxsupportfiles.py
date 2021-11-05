import arcpy
import os

PYT_PATH = "esri\\toolboxes\\ImportarSurvey_AMCO.pyt"

folder_path = os.path.dirname(os.path.realpath(__file__))
pyt_path = os.path.join(folder_path, PYT_PATH)

arcpy.gp.createtoolboxsupportfiles(pyt_path)