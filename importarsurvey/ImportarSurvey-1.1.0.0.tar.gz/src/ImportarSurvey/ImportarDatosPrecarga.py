# -*- coding: utf-8 -*-

import arcpy
import uuid

from os import path
from arcpy import da
from ImportarSurvey.Utiles import ToolboxLogger
from ImportarSurvey.Utiles import Configuracion
from ImportarSurvey.Utiles import TimeUtil
from ImportarSurvey.DataAccess import DataAccess
from ImportarSurvey.DataAccess import QueryItem
from ImportarSurvey.DataAccess import QueryList
from ImportarSurvey.Estadisticas import Estadisticas
from ImportarSurvey.ImportarDatos import ImportarDatos

class ImportarDatosPrecarga(ImportarDatos) :

    def __init__(self, 
        fuente_da, 
        destino_da, 
        claseFuentePrincipal = '', 
        claseDestinoPrincipal = '', 
        usuarioCampo = '') :

        super().__init__(
            fuente_da,
            destino_da,
            claseFuentePrincipal = claseFuentePrincipal,
            claseDestinoPrincipal = claseDestinoPrincipal,
            usuarioCampo = usuarioCampo)

    @ToolboxLogger.log_method
    def actualizarRegistroDestino(self, tabla, registro, llave, valor = None) :
        try :
            if tabla == self.claseDestinoPrincipal and self.usuarioCampo != '' :
                llave = "usuario_portal" 
                valor = self.usuarioCampo

                if valor and llave in registro :
                    registro[llave] = valor
                    resultado = self.destino_da.update(tabla, registro)
                    ToolboxLogger.debug("Se actualizó el usuario de la encuesta : '{}'".format(valor))
                else :
                    ToolboxLogger.debug("No se actualizó.")

        except Exception as e:
            ToolboxLogger.info("Error: {}".format(e))
