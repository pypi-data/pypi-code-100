import sys
from tkinter import Tk
from tkinter import filedialog as fd
import logging
import os
import trimesh

import numpy as np

from src.PYSimultanRadiation.shading_analysis import ShadingAnalysis, create_shading_template, ProjectLoader
from src.PYSimultanRadiation.geometry.utils import angle

create_shading_template()

if __name__ == '__main__':

    Tk().withdraw()
    project_filename = fd.askopenfilename(title='Select a SIMULTAN Project...',
                                          filetypes=[("SIMULTAN", ".simultan")]
                                          )
    if project_filename in [None, '']:
        logging.error('No SIMULTAN Project selected')
        sys.exit()
    print(f'selected {project_filename}')

    project_loader = ProjectLoader(project_filename=project_filename,
                                   user_name='admin',
                                   password='admin')

    project_loader.load_project()

    shading_analysis = ShadingAnalysis(project_filename=project_loader.project_filename,
                                       user_name=project_loader.user_name,
                                       password=project_loader.password,
                                       template_parser=project_loader.template_parser,
                                       data_model=project_loader.data_model,
                                       typed_data=project_loader.typed_data,
                                       setup_component=project_loader.setup_components[0])

    face_normals = np.array([x.normal for x in shading_analysis.geo_model.faces])
    irradiation_vectors = shading_analysis.location.generate_irradiation_vector(shading_analysis.dti)

    aois = irradiation_vectors.apply(calc_aoi, axis=1, result_type='expand')



    print('done')
