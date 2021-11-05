# -*- coding: utf-8 -*-

import arcpy

from datetime import datetime
from ImportarSurvey.Utiles import ToolboxLogger
from ImportarSurvey.Utiles import Configuracion
from ImportarSurvey.Utiles import ToolboxLogger
from ImportarSurvey.ArcGISPythonApiDataAccess import ArcGISPythonApiDataAccess
from ImportarSurvey.ImportarDatosInyeccion import ImportarDatosInyeccion
from ImportarSurvey.ProcesarEncuestas import ProcesarEncuestas

class InyectarEncuestas(ProcesarEncuestas) : 

    def __init__ (self, 
        rutaConfiguracion, 
        portal, 
        usuario, 
        clave, 
        servicioFuente, 
        servicioDestino, 
        versionFuente = '', 
        versionDestino = '', 
        usuarioCampo = ''):
        super().__init__(
            rutaConfiguracion, 
            portal, 
            usuario, 
            clave, 
            servicioFuente,  
            servicioDestino, 
            versionFuente = versionFuente,
            versionDestino = versionDestino, 
            usuarioCampo = usuarioCampo)

    @ToolboxLogger.log_method
    def calcularConsultaInicial(self) :
        campos =  ["estadoenc", "estado_sincronizacion"]
        valores = ["cerrada", "sin_sincronizar"]

        tabla = self.fuente_da.getTable(self.servicioFuente)
        f = [x for x in tabla.properties.fields if x.name.lower() == "usuario_portal"]
        if f:
            campos.append("usuario_portal")
            valores.append(self.usuario_campo)

        self.obtenerConsultaInicial(campos, valores)
        
        return

    @ToolboxLogger.log_method
    def limpiarProceso(self):
        if self.destino_da:
            ToolboxLogger.info("stopEditing: '{}'".format(self.destino_da.stopEditing(True)))
            ToolboxLogger.info("stopReading: '{}'".format(self.destino_da.stopReading()))
            self.destino_da.setMode(None)
            ToolboxLogger.info("purgeVersion: '{}'".format(self.destino_da.purgeVersion(self.versionDestino)))
        
        return

    @ToolboxLogger.log_method
    def inicializarProceso(self) :
        try :
            ToolboxLogger.info("Portal: '{}'".format(self.portal))
            ToolboxLogger.info("Servicio Origen: '{}'".format(self.servicioFuente))
            ToolboxLogger.info("Servicio Destino: '{}'".format(self.servicioDestino))
            ToolboxLogger.info("Usuario: '{}'".format(self.usuario))
            ToolboxLogger.info("Usuario Campo: '{}'".format(self.usuario_campo))
            ToolboxLogger.info("Versión Destino: '{}'".format(self.versionDestino))

            self.destino_da = ArcGISPythonApiDataAccess(self.portal, self.usuario, self.clave)
            self.destino_da.setFeatureService(self.servicioDestino)
            self.destino_da.setVersionManager()

            if not self.versionDestino:
                self.versionDestino = self.crearVersion(self.destino_da, self.servicioFuente)
                ToolboxLogger.info("Se creó la version: '{}'".format(self.versionDestino))
            else :
                ToolboxLogger.info("Versión Destino: '{}'".format(self.versionDestino))

            if self.destino_da.setVersion(self.versionDestino) :
                bloqueado, purgado = self.destino_da.isVersionLocked(self.versionDestino)
                bloqueado = False
                if not bloqueado:
                    self.destino_da.setMode("edit")
                    ToolboxLogger.info("startReading: '{}'".format(self.destino_da.startReading()))
                    ToolboxLogger.info("startEditing: '{}'".format(self.destino_da.startEditing()))

                    self.fuente_da = ArcGISPythonApiDataAccess(self.portal, self.usuario, self.clave)
                    self.fuente_da.setFeatureService(self.servicioFuente)
                    self.fuente_da.outSpatialReference = self.destino_da.getSpatialReference()
                    self.fuente_da.returnZ = self.destino_da.hasZ
                    
                    ToolboxLogger.debug("Referencia Espacial Destino : '{}'".format(self.fuente_da.outSpatialReference))
                    ToolboxLogger.debug("Tiene Z Destino : '{}'".format( self.fuente_da.returnZ))

                    self.importarDatos = ImportarDatosInyeccion(
                        self.fuente_da, 
                        self.destino_da, 
                        self.servicioFuente, 
                        self.servicioDestino, 
                        self.usuario_campo)
                else :
                    ToolboxLogger.info("Error: Versión Destino está en Uso!")
                    if purgado:
                        ToolboxLogger.info("La versión en uso se purgó. Intente de nuevo.")
            else :
                ToolboxLogger.info("Error: Versión Destino no encontrada!")

        except Exception as e:
            ToolboxLogger.info("Error: {}".format(e))
        
        return
            

