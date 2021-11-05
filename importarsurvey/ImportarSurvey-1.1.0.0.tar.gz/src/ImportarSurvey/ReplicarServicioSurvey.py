# -*- coding: utf-8 -*-

import arcpy

from datetime import datetime
from ImportarSurvey.Utiles import ToolboxLogger
from ImportarSurvey.Utiles import Configuracion
from ImportarSurvey.Utiles import ToolboxLogger
from ImportarSurvey.ArcGISPythonApiDataAccess import ArcGISPythonApiDataAccess


class ReplicarServicio : 

    def __init__(self, rutaConfiguracion):

        self.rutaConfiguracion = rutaConfiguracion
        self.config = Configuracion(rutaConfiguracion)

     
    @ToolboxLogger.log_method
    def Ejecutar(self, portal, usuario, clave, servicioFuente, numeroServiciosDestino) :
        try: 
            ToolboxLogger.info("Portal: {}".format(portal))
            ToolboxLogger.info("Servicio Origen: {}".format(servicioFuente))
            ToolboxLogger.info("Número Servicios Destino: {}".format(numeroServiciosDestino))
            ToolboxLogger.info("Usuario: {}".format(usuario))

            total_servicios = 0
            total_errores = 0

            fuente_da = ArcGISPythonApiDataAccess(portal, usuario, clave)
            fuente_da.setFeatureService(servicioFuente)
            elementoCopiar = fuente_da.searchElement(servicioFuente, 'Form')
            ##elements_to_copy = fuente_da.getElementsInFolder("Survey-FUCM30303")
            prefijoNombreServicio = self.config.getConfigKey("prefijoNombreServicios")
            for x in range(numeroServiciosDestino): 
                nombre_servicio = "{}_{}". format(prefijoNombreServicio, x)
                servicioBuscar = fuente_da.searchElement(nombre_servicio, 'Feature Service')
                if (len(servicioBuscar) == 0):
                    fuente_da.copyFeatureService(nombre_servicio)
                    ToolboxLogger.info("Servicio: {} creado.".format(nombre_servicio))
                
                elementoBuscar = fuente_da.searchElement(nombre_servicio, 'Form')
                if (len(elementoBuscar) == 0):
                    fuente_da.copyElement(elementoCopiar[0], nombre_servicio)
                    ToolboxLogger.info("Elemento: {} creado.".format(nombre_servicio))
                
                total_servicios +=1
                
                ##total_errores += errores
            
            return fuente_da, total_servicios, total_errores

        except Exception as e:
            ToolboxLogger.error("Error: {}".format(e))
        else :
            destino_da.setMode("None")
        finally :
            ToolboxLogger.info("Terminado.")
