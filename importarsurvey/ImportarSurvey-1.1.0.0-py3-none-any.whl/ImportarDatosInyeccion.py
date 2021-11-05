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

class ImportarDatosInyeccion(ImportarDatos) :

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

    def agregarInforme(self) :
        ToolboxLogger.info("Total Aceptadas      : {}".format(self.estadisticas.totalEstadoEncuesta("estado_aceptacion", "aceptada")))
        ToolboxLogger.info("Total No Aceptadas   : {}".format(self.estadisticas.totalEstadoEncuesta("estado_aceptacion", "no_aceptada")))
        ToolboxLogger.info("Total Sincronizadas  : {}".format(self.estadisticas.totalEstadoEncuesta("estado_sincronizacion", "sincronizada")))

    @ToolboxLogger.log_method
    def actualizarRegistroOrigen(self, nombre_tabla, registro, llave, valor = None) :
        try :
            if nombre_tabla == self.claseFuentePrincipal and not valor :
                registro["estado_sincronizacion"] = "sincronizada"
                registro["estadoenc"] = None

                if self.estadisticas.obtenerEstadisticasActual("E") < 1 :
                    registro["estado_aceptacion"] = "aceptada"
                else :
                    registro["estado_aceptacion"] = "no_aceptada"

                resultado = self.fuente_da.update(nombre_tabla, registro)
                self.estadisticas.actualizarEncuesta(registro[llave], 
                    {"estado_sincronizacion": registro["estado_sincronizacion"],
                     "estado_aceptacion": registro["estado_aceptacion"],
                     "estadoenc": registro["estadoenc"]})
                ToolboxLogger.debug("Resultado Cambio de Estado: {}".format(resultado))
            else :
                if valor and llave in registro and valor != registro[llave]:
                    valor_anterior = registro[llave]
                    tabla = self.fuente_da.getTable(nombre_tabla)

                    registro_a_actualizar = {}
                    registro_a_actualizar[tabla.properties.globalIdField] = registro[tabla.properties.globalIdField]
                    registro_a_actualizar[tabla.properties.objectIdField] = registro[tabla.properties.objectIdField]
                    registro_a_actualizar[llave] = valor

                    resultado = self.fuente_da.update(tabla, registro_a_actualizar)
                    if resultado != {} :
                        guid = resultado["globalId"] if "globalId" in resultado else '{}'
                        ToolboxLogger.debug("Cambio de llave en '{}' para 'globalId' = '{}'':".format(nombre_tabla, guid))
                        ToolboxLogger.debug("'{}' de '{}' a '{}'".format(llave, valor_anterior, valor))
                    else :
                        ToolboxLogger.debug("No cambio de llave en '{}':".format(tabla))
                        ToolboxLogger.debug("Para '{}' = '{}'".format(llave, valor))
        except Exception as ex:
            ToolboxLogger.info("Error: {}".format(ex))



