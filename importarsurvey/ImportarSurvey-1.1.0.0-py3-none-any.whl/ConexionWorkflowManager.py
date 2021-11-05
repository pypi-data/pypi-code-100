# -*- coding: utf-8 -*-

import arcpy

from ImportarSurvey.Utiles import ToolboxLogger
from ImportarSurvey.Utiles import Configuracion
from ArcGISWFMApiDataAccess import ArcGISWFMApiDataAccess

class ConexionWorkflowManager():

    def __init__(self, rutaConfiguracion, pathConnectionFile):

        self.rutaConfiguracion = rutaConfiguracion
        self.config = Configuracion(rutaConfiguracion)

        self.rutaArchivoConexion = pathConnectionFile
       

    @ToolboxLogger.log_method
    def Ejecutar(self, usuario) :
        try: 
            ToolboxLogger.info("Ruta Archivo Conexion: {}".format(self.rutaArchivoConexion))

            total_encuestas = 0
            total_registros = 0
            total_errores = 0

            WFM = ArcGISWFMApiDataAccess(self.rutaArchivoConexion)
            # jobs = WFM._getJobsByUser(usuario)
            # for row in jobs.rows:
	        #     print(row[0])

            assignments = WFM._getAssignmentsUser(usuario)
            for row in assignments.rows:
	            print(row[0])           
            # workforceProject = workForce_da.openWorkforceProject(self.workforceProjectID)

            # destino_da = ArcGISPythonApiDataAccess(self.portal, self.usuario, self.clave)
            # destino_da.setFeatureService(self.servicioDestino)          
            

            return total_encuestas, total_registros, total_errores, 

        except Exception as e:
            ToolboxLogger.error("Error: {}".format(e))
        finally :
            ToolboxLogger.info("Terminado.")
            
        return total_encuestas, total_registros, total_errores

    
    @ToolboxLogger.log_method
    def GetRequestByID(self, requestID) :
        requestData=None
        try: 
            ToolboxLogger.info("Ruta Archivo Conexion: {}".format(self.rutaArchivoConexion))
            ToolboxLogger.info("ID Radicación: {}".format(requestID))
            WFM = ArcGISWFMApiDataAccess(self.rutaArchivoConexion)
            requestData = WFM._getRequestById(requestID)
            # for row in assignments.rows:
	        #     print(row[0])           
           
        except Exception as e:
            ToolboxLogger.error("Error: {}".format(e))
        finally :
            ToolboxLogger.info("Terminado.")
            
        return requestData
            