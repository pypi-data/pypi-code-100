# -*- coding: utf-8 -*-

import arcpy

from datetime import datetime
from ImportarSurvey.Utiles import ToolboxLogger
from ImportarSurvey.Utiles import Configuracion
from ImportarSurvey.Utiles import ToolboxLogger
from ImportarSurvey.DataAccess import DataAccess
from ImportarSurvey.DataAccess import QueryItem
from ImportarSurvey.DataAccess import QueryList
from ImportarSurvey.ArcGISPythonApiDataAccess import ArcGISPythonApiDataAccess
from ImportarSurvey.ImportarDatos import ImportarDatos

class ProcesarEncuestas : 

    def __init__ (self, 
        rutaConfiguracion, 
        portal, 
        usuario, 
        clave, 
        servicioFuente, 
        servicioDestino, 
        versionFuente = '', 
        versionDestino = '', 
        usuarioCampo = '') :
       
        self.rutaConfiguracion = rutaConfiguracion
        self.config = Configuracion(rutaConfiguracion)

        self.portal = portal
        self.usuario = usuario
        self.usuario_campo = usuarioCampo if usuarioCampo != '' else usuario
        self.clave = clave
        self.servicioFuente = servicioFuente
        self.versionDestino = versionDestino
        self.servicioDestino = servicioDestino
        self.versionDestino = versionDestino
        self.versionFuente = versionFuente

        self.destino_da = None
        self.fuente_da = None
        self.importarDatos = None

    @ToolboxLogger.log_method
    def inicializarProceso(self) :
        return

    @ToolboxLogger.log_method
    def limpiarProceso(self):
        return

    @ToolboxLogger.log_method
    def calcularConsultaInicial(self) :
        return 

    @ToolboxLogger.log_method
    def crearVersion(self, da, nombre_formulario) :
        fecha_hora = datetime.now()
        nombre_version = "{}_{}".format(nombre_formulario, fecha_hora.strftime("%Y%m%d%H%M%S"))
        descripcion = "Carga Formulario Survey {}, {}".format(nombre_formulario, fecha_hora.strftime("%Y-%m-%d %H:%M"))
        
        return da.createVersion(nombre_version, "Protected", descripcion)

    @ToolboxLogger.log_method
    def obtenerConsultaInicial(self, campos, valores) :
        ToolboxLogger.debug("campos : '{}'".format(campos))
        ToolboxLogger.debug("valores: '{}'".format(valores))

        self.consultaInicial = QueryList()
        self.consultaInicial.addQuery(QueryItem(campos, valores))

    @ToolboxLogger.log_method
    def Ejecutar(self) :
        total_encuestas = 0
        total_registros = 0
        total_errores = 0
        patron_fecha_hora = "%Y-%m-%d %H:%M:%S"
        try: 
            ToolboxLogger.info("Iniciado: {}".format(datetime.now().strftime(patron_fecha_hora)))
            self.inicializarProceso()
            if self.importarDatos :
                mapeos = self.config.getConfigKey("mapeos")
                for mapeo in mapeos :
                    self.calcularConsultaInicial()
                    encuestas, registros, errores = self.importarDatos.procesarMapeo(mapeo, self.consultaInicial)
                    total_encuestas += encuestas
                    total_registros += registros
                    total_errores += errores 
            self.limpiarProceso()
        except Exception as e:
            ToolboxLogger.info("Error: {}".format(e))
        finally :
            ToolboxLogger.info("Terminado: {}".format(datetime.now().strftime(patron_fecha_hora)))
            
        return total_encuestas, total_registros, total_errores