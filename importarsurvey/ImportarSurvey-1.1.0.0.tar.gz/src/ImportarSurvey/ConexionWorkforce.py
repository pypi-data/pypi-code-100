# -*- coding: utf-8 -*-

import arcpy

from arcgis.apps import workforce
from ImportarSurvey.Utiles import ToolboxLogger
from ImportarSurvey.Utiles import Configuracion
from ImportarSurvey.Utiles import ToolboxLogger
from ImportarSurvey.ArcGISPythonApiDataAccess import ArcGISPythonApiDataAccess
from ImportarSurvey.ImportarDatos import Importar

class ConexionWorkforce():

    def __init__(self, rutaConfiguracion, portal, usuario, clave, workforceProjectID):

        self.rutaConfiguracion = rutaConfiguracion
        self.config = Configuracion(rutaConfiguracion)

        self.portal = portal
        self.usuario = usuario
        self.clave = clave
        self.workforceProjectID = workforceProjectID

    @ToolboxLogger.log_method
    def openWorkforceProject(self, projectID):
        itemProject = self.__gis.content.get(projectID)
        project = workforce.Project(itemProject)
        return project
        
    @ToolboxLogger.log_method
    def Ejecutar(self, servicioDestino) :
        try: 
            ToolboxLogger.info("Portal: {}".format(self.portal))
            ToolboxLogger.info("ID Proyecto Workforce: {}".format(self.workforceProjectID))
            ToolboxLogger.info("Servicio Destino: {}".format(servicioDestino))
            ToolboxLogger.info("Usuario: {}".format(self.usuario))
            ToolboxLogger.info("Clave: {}".format(self.clave))
            
            total_encuestas = 0
            total_registros = 0
            total_errores = 0

            workForce_da = ArcGISPythonApiDataAccess(self.portal, self.usuario, self.clave)
            workforceProject = workForce_da.openWorkforceProject(self.workforceProjectID)

            destino_da = ArcGISPythonApiDataAccess(self.portal, self.usuario, self.clave)
            destino_da.setFeatureService(self.servicioDestino)          
            

            return total_encuestas, total_registros, total_errores, 

        except Exception as e:
            ToolboxLogger.error("Error: {}".format(e))
        finally :
            ToolboxLogger.info("Terminado.")
            
        return total_encuestas, total_registros, total_errores
    
    
    @ToolboxLogger.log_method
    def CrearAsignacionWF(self, dataWFM) :
        assignmentsAdded = None
        try: 
            ToolboxLogger.info("Portal: {}".format(self.portal))
            ToolboxLogger.info("Usuario: {}".format(self.usuario))
            ToolboxLogger.info("Clave: {}".format(self.clave))
            ToolboxLogger.info("ID Proyecto Workforce: {}".format(self.workforceProjectID))

            total_encuestas = 0
            total_registros = 0
            total_errores = 0

            workForce_da = ArcGISPythonApiDataAccess(self.portal, self.usuario, self.clave)
            workforceProject = workForce_da.openWorkforceProject(self.workforceProjectID)
            assignments = []
            assignments.append(
                workforce.Assignment(
                    workforceProject,
                    version="tales",
                    assignment_type="Actualización",
                    work_order_id = dataWFM.rows[0]['id_solicitud'],
                    status="unassigned",
                    location="Terreno: " + dataWFM.rows[0]['cedula_catastral']
                )
            )
            assignmentsAdded = workforceProject.assignments.batch_add(assignments)

        except Exception as e:
            ToolboxLogger.error("Error: {}".format(e))
        finally :
            ToolboxLogger.info("Terminado.")
            
        return assignmentsAdded
                    