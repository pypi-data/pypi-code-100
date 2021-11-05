# -*- coding: utf-8 -*-

import arcpy

from ImportarSurvey.Utiles import ToolboxLogger
from ImportarSurvey.Utiles import Configuracion
from ImportarSurvey.Utiles import ToolboxLogger
from ImportarSurvey.DataAccess import DataAccess
from ImportarSurvey.DataAccess import QueryItem
from ImportarSurvey.DataAccess import QueryList
from ImportarSurvey.ArcGISPythonApiDataAccess import ArcGISPythonApiDataAccess
from ImportarSurvey.ImportarDatosPrecarga import ImportarDatosPrecarga
from ImportarSurvey.ProcesarEncuestas import ProcesarEncuestas

class PrecargarEncuestas(ProcesarEncuestas):
    
    def __init__(self, 
        rutaConfiguracion, 
        portal, 
        usuario, 
        clave, 
        servicioFuente, 
        servicioDestino, 
        versionFuente = '', 
        versionDestino = '', 
        usuarioCampo = '', 
        idsPrecarga = ''):

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
        self.idsPrecarga = idsPrecarga

    @ToolboxLogger.log_method
    def calcularConsultaInicial(self) :
        campos = ["NUMERO_PREDIAL"]
        valores = []
        valores.append(self.idsPrecarga.split(';'))

        self.obtenerConsultaInicial(campos, valores)

        return

    @ToolboxLogger.log_method
    def inicializarProceso(self) :
        try :
            ToolboxLogger.info("Portal: {}".format(self.portal))
            ToolboxLogger.info("Servicio Origen: {}".format(self.servicioFuente))
            ToolboxLogger.info("Servicio Destino: {}".format(self.servicioDestino))
            ToolboxLogger.info("Usuario: {}".format(self.usuario))
            ToolboxLogger.info("Usuario Campo: {}".format(self.usuario_campo))
            ToolboxLogger.info("Versión Fuente: {}".format(self.versionFuente))
            
            self.fuente_da = ArcGISPythonApiDataAccess(self.portal, self.usuario, self.clave)
            self.fuente_da.setFeatureService(self.servicioFuente)
            self.fuente_da.setVersionManager()

            if not self.versionFuente:
                self.versionFuente = self.crearVersion(self.fuente_da, self.servicioFuente)
                ToolboxLogger.info("Se creó la version: {}".format(self.versionFuente))
            else :
                ToolboxLogger.info("Versión Fuente: {}".format(self.versionFuente))

            if self.fuente_da.setVersion(self.versionFuente):
                self.destino_da = ArcGISPythonApiDataAccess(self.portal, self.usuario, self.clave)
                self.destino_da.setFeatureService(self.servicioDestino)
                self.fuente_da.outSpatialReference = self.destino_da.getSpatialReference()
                self.fuente_da.returnZ = self.destino_da.hasZ
                
                ToolboxLogger.debug("Referencia Espacial Destino : '{}'".format(self.fuente_da.outSpatialReference))
                ToolboxLogger.debug("Tiene Z Destino : '{}'".format( self.fuente_da.returnZ))

                self.importarDatos = ImportarDatosPrecarga(
                    self.fuente_da, 
                    self.destino_da, 
                    self.servicioFuente, 
                    self.servicioDestino, 
                    self.usuario_campo)
            else:
                ToolboxLogger.info("Error: Versión Fuente No encontrada!")
        except Exception as e:
            ToolboxLogger.info("Error: {}".format(e))

        return


                