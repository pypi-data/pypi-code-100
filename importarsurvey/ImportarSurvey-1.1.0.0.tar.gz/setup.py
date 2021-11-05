import os 
from setuptools import setup 
 
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()    
 
setup(name='ImportarSurvey', 
        version='1.1.0.0',
        author='Esri Colombia',
        author_email='mtorres@esri.co',
        license='MIT',
        long_description=long_description,
        long_description_content_type="text/markdown",
        url='https://dev.azure.com/esrico-con-uaecd-ladm/ImportarEncuestaActualizacionCatastral',
        description=('ArcGIS Pro Toolbox para la Precarga e Inyeccion de Encuestas de Actualización Catastral'),
        python_requires= '>=3.7',
        classifiers=[
            'Programming Language :: Python :: 3.7',
            'License :: OSI Approved :: MIT License',
            'Operating System :: Microsoft :: Windows :: Windows 10',
        ],
        packages=['ImportarSurvey'], 
        package_data={'ImportarSurvey':['esri/toolboxes/*',  
                    'esri/arcpy/*', 'esri/help/gp/*',  
                    'esri/help/gp/toolboxes/*', 'esri/help/gp/messages/*'] 
                    }, 
      )