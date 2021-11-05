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

class ImportarDatos:

    def __init__(self, 
        fuente_da, 
        destino_da, 
        claseFuentePrincipal = '', 
        claseDestinoPrincipal = '', 
        usuarioCampo = '') :

        self.fuente_da = fuente_da
        self.destino_da = destino_da
        self.claseFuentePrincipal = claseFuentePrincipal
        self.claseDestinoPrincipal = claseDestinoPrincipal
        self.usuarioCampo = usuarioCampo

        self.estadisticas = Estadisticas()
        self.parentGlobalId = ''

    def obtenerTablaPrincipal(self):
        return self.claseFuentePrincipal

    def nombreTabla(self, nombreLargoTabla):
        ruta, nombre = path.split(nombreLargoTabla)
        ruta = ruta

        return nombre

    def actualizarEstadistica(self, nombreTabla, tipo = "", guid = '{}'):
        self.estadisticas.actualizarEstadistica(nombreTabla, tipo, guid)

    def cumpleCondicion(self, condicion, registro):
        if condicion != None:
            condicion_campo = condicion["campo"] if "campo" in condicion else None
            condicion_valor = condicion["valor"] if "valor" in condicion else None

            if condicion_campo and condicion_valor:

                if isinstance(condicion_valor, list):
                    ToolboxLogger.debug("{} in {} <=> {} = {}".format(
                        condicion_campo, condicion_valor, condicion_campo, registro[condicion_campo]))
                    valor = [x for x in condicion_valor if x ==
                             registro[condicion_campo]]
                    if valor:
                        return True
                else:
                    ToolboxLogger.debug("Condicion -> {} = {} <=> {} = {}".format(
                        condicion_campo, condicion_valor, condicion_campo, registro[condicion_campo]))
                    return registro[condicion_campo] == condicion_valor
            return False
        else:
            return True

    @ToolboxLogger.log_method
    def obtenerValoresMapeados(self, campos, registro_origen) :
        geometria = registro_origen["geometry"] if "geometry" in registro_origen else None
        atributos = registro_origen["attributes"] if "attributes" in registro_origen else None

        registro = {}
        if campos:
            for campo in campos:
                if "origen" in campo :
                    valor = atributos[campo["origen"]]
                elif "valor" in campo :
                    valor = campo["valor"]
                else :
                    valor = None

                if "esGuid" in campo and valor != None:
                    valor = "{}".format(valor)
                
                if valor != None :
                    registro[campo["destino"]] = valor
                    ToolboxLogger.debug(
                        "---->mapeo - {} = {}".format(campo["destino"], valor)
                    )
        return registro, geometria
    
    def _obtenerCamposMapeo(self, mapeo, llaves) :
        campos = []

        def agregar(item) :
            if not item in campos and item != "ND":
                campos.append(item)

        if "relacion" in llaves and llaves["relacion"] in mapeo:
            agregar(mapeo[llaves["relacion"]])
        if "primaria" in llaves and llaves["primaria"] in mapeo :
            agregar(mapeo[llaves["primaria"]])
        if "foranea" in llaves and llaves["foranea"]  in mapeo :
            agregar(mapeo[llaves["foranea"]])
        if "hija" in llaves and "detallesRelacion" in mapeo and llaves["hija"] in mapeo["detallesRelacion"] :
            agregar(mapeo["detallesRelacion"][llaves["hija"]])
        if "padre" in llaves and "detallesRelacion" in mapeo and llaves["padre"] in mapeo["detallesRelacion"] :
            agregar(mapeo["detallesRelacion"][llaves["padre"]])
        if "campos" in mapeo :
            for campo_mapeo in mapeo["campos"] :
                if llaves["tipo"] in campo_mapeo :
                    agregar(campo_mapeo[llaves["tipo"]])
        return campos

    def _obtenerCamposOrigen(self, mapeo) :
        llaves = {"tipo": "origen", 
                  "relacion" : "llaveRelacionOrigen", 
                  "primaria" : "llavePrimariaOrigen",
                  "foranea" : "llaveForaneaOrigen"}
        return self._obtenerCamposMapeo(mapeo, llaves)

    def _obtenerCamposDestino(self, mapeo) :
        llaves = {"tipo": "destino", 
                  "relacion" : "llaveRelacionDestino", 
                  "primaria" : "llavePrimariaDestino",
                  "foranea" : "llaveForaneaDestino", 
                  "hija" : "llaveForaneaHija", 
                  "padre" : "llaveForaneaPadre"}
        return self._obtenerCamposMapeo(mapeo, llaves)
   
    @ToolboxLogger.log_method
    def crearRegistro(self, table, campos_busqueda, campos, registro_origen, valores_pk, usar_geometria=False):
        ToolboxLogger.debug("---->campos_busqueda: {}".format(campos_busqueda))
        ToolboxLogger.debug("---->valores_pk: {}".format(valores_pk))
        try:
            attributes = {}
            if isinstance(campos_busqueda, list) and isinstance(valores_pk, list):
                enum_campos = DataAccess.enumElements(campos_busqueda)
                enum_valores = DataAccess.enumElements(valores_pk)
                for enum_campo in enum_campos:
                    index = enum_campos.index(enum_campo)
                    attributes[enum_campo] = enum_valores[index]
                ToolboxLogger.debug("---->campos_busqueda: {}".format(enum_campos))
                ToolboxLogger.debug("---->valores_pk: {}".format(enum_valores))
            else:
                attributes[campos_busqueda] = valores_pk
            ToolboxLogger.debug("---->attributes: {}".format(attributes))

            if registro_origen and "geometry" in registro_origen:  
                attributes["geometry"] = registro_origen["geometry"]

            if campos:
                for campo in campos:
                    if "origen" in campo and campo["origen"] in registro_origen :
                        if campo["origen"] != "ND":
                            valor = registro_origen[campo["origen"]]
                        elif "destino" in campo:
                            if campo["origen"] == "ND" and campo["destino"].upper()=="PARENTGLOBALID":
                                valor = self.parentGlobalId
                    elif "valor" in campo :
                        valor = campo["valor"]
                    else :
                        valor = None

                    if valor == None and "valor_predeterminado" in campo:
                        valor = campo["valor_predeterminado"]    

                    if "esGuid" in campo and valor != None:
                        valor = "{}".format(valor)
                    
                    if valor != None :
                        if str(valor).strip() != '':
                            fieldToFill = [x for x in table.properties.fields if x.name.upper() == campo["destino"].upper()]
                            if len(fieldToFill)  > 0 :
                                if fieldToFill[0].type == 'esriFieldTypeDate' :
                                    attributes[campo["destino"]] = int(valor)  
                                else:
                                    attributes[campo["destino"]] = str(valor).strip()
                        else :
                            attributes[campo["destino"]] = None

                        ToolboxLogger.debug("---->ins - {} = {}".format(campo["destino"], valor))
                    else :
                        if table :
                            fields = [x for x in table.properties.fields if x.name.upper() == campo["destino"].upper()]
                            if len(fields)  > 0 :
                                field = fields[0]
                                if field.nullable == False and field.defaultValue != None :
                                    attributes[campo["destino"]] = field.defaultValue 
                                    ToolboxLogger.debug("---->ins - {} = {}".format(campo["destino"], field.defaultValue))  
                                else:
                                    attributes[campo["destino"]] = None
                                    ToolboxLogger.debug("---->ins - {} = {}".format(campo["destino"], 'null'))  


            resultado = self.destino_da.add(table, attributes)
            ToolboxLogger.debug("resultado = {}".format(resultado))  
            if resultado:
                guid = resultado["globalId"] if "globalId" in resultado else '{}'
                self.actualizarEstadistica(table.properties.name, "C", guid)

            return resultado
        except Exception as e:
            self.actualizarEstadistica(table.properties.name, "E")
            ToolboxLogger.info("Tabla: {}, ERROR: ---->{}".format(table.properties.name, e))

        return None

    @ToolboxLogger.log_method
    def actualizarRegistro(self, table, campos_busqueda, campos, registro_origen, valores_pk, operadores_pk = None, conectores_pk = None, usar_geometria = False):
        ToolboxLogger.debug("---->campos_busqueda: {}".format(campos_busqueda))
        ToolboxLogger.debug("---->valores_pk: {}".format(valores_pk))
        attributesRemove=[]
        where = DataAccess.getWhereClause(campos_busqueda, valores_pk, operadores_pk, conectores_pk)
        query = self.destino_da.query(table, ["*"], where, return_geometry = usar_geometria)
        count = len(query) if query != None else 0
        try:
            if(count > 0) :
                for feature in query:
                    attributes = {}
                    if "geometry" in feature and "geometry" in registro_origen:
                        # ToolboxLogger.debug("feature['geometry'] = {}".format(feature["geometry"]))
                        # ToolboxLogger.debug("registro_origen['geometry'] = {}".format(registro_origen["geometry"]))
                        if feature["geometry"] != registro_origen["geometry"] :
                            attributes["geometry"] = registro_origen["geometry"]
                    
                    if campos:
                        for campo in campos:
                            if "origen" in campo and campo["origen"] in registro_origen:
                                if campo["origen"] != "ND":
                                    valor = registro_origen[campo["origen"]]
                                elif "destino" in campo:
                                    if campo["origen"] == "ND" and campo["destino"].upper()=="PARENTGLOBALID":
                                        valor = self.parentGlobalId
                                    elif "valor_predeterminado" in campo :
                                        valor = campo["valor_predeterminado"]  
                            elif "valor" in campo :
                                valor = campo["valor"]
                            else :
                                valor = None

                            if valor == None and "valor_predeterminado" in campo:
                                valor = campo["valor_predeterminado"]    

                            if "esGuid" in campo and valor != None:
                                valor = "{}".format(valor)
                                
                            key  = [x for x in feature if x.lower() == campo["destino"].lower()]
                            valor_destino = feature[key[0]] if key != [] else None
                            
                            if valor != None and valor != valor_destino :
                                if str(valor).strip() != '':
                                    fieldToFill = [x for x in table.properties.fields if x.name.upper() == campo["destino"].upper()]
                                    if len(fieldToFill)  > 0 :
                                        if fieldToFill[0].type == 'esriFieldTypeDate' :
                                            attributes[campo["destino"]] = int(valor)  
                                        else:
                                            attributes[campo["destino"]] = str(valor).strip()
                                else :
                                    attributes[campo["destino"]] = None
                                    attributesRemove.append(campo["destino"])
                                ToolboxLogger.debug("---->upd - {} = {}".format(campo["destino"], valor))

                        if len(attributes) > 0 :
                            attributes[table.properties.objectIdField] = feature[table.properties.objectIdField]
                            attributes[table.properties.globalIdField] = feature[table.properties.globalIdField]
                            
                            resultado = self.destino_da.update(table, attributes)
                            ToolboxLogger.debug("resultado = {}".format(resultado))
                            if resultado:
                                guid = resultado["globalId"] if "globalId" in resultado else '{}'
                                self.actualizarEstadistica(table.properties.name, "U", guid)

                            return resultado
                            
                    self.actualizarEstadistica(table.properties.name, "NU", feature[table.properties.globalIdField])
                    return attributes

        except Exception as e:
            if feature:
                self.actualizarEstadistica(table.properties.name, "E", feature[table.properties.globalIdField])
            else :
                self.actualizarEstadistica(table.properties.name, "E", {})

            ToolboxLogger.info("Tabla: {}, ERROR: ---->{}".format(table.properties.name, e))
        return None 

    @ToolboxLogger.log_method
    def actualizarMapeado(self, nombre_tabla, campo_busqueda, campos, registro_origen, valor_relacion, operadores = None, conectores = None, tipo_operacion = "U", usar_geometria = False):
        
        if nombre_tabla == "[main_feature]":
            tabla = self.destino_da.getTable(self.claseDestinoPrincipal)
        else:
            tabla = self.destino_da.getTable(nombre_tabla)

        r = None
        if tipo_operacion == "C":
            r = self.crearRegistro(
                tabla, campo_busqueda, campos, registro_origen, valor_relacion, usar_geometria
            )
        elif tipo_operacion == "U":
            r = self.actualizarRegistro(
                tabla, campo_busqueda, campos, registro_origen, valor_relacion, operadores, conectores, usar_geometria
            )
        elif tipo_operacion == "CU":
            r = self.actualizarRegistro(
                tabla, campo_busqueda, campos, registro_origen, valor_relacion, operadores, conectores, usar_geometria
            )
            if r == None:
                r = self.crearRegistro(
                    tabla, campo_busqueda, campos, registro_origen, valor_relacion, usar_geometria
                )
        return r

    @ToolboxLogger.log_method
    def actualizarRelacionesOrigen(self, relacion_origen,
                                    registro_origen,
                                    valor_pk_origen,
                                    valor_pk_destino_padre):
        #ToolboxLogger.debug("relacion_origen: {}".format(relacion_origen))
        #ToolboxLogger.debug("registro_origen: {}".format(registro_origen))
        ToolboxLogger.debug("valor_pk_origen: {}".format(valor_pk_origen))
        ToolboxLogger.debug("valor_pk_destino_padre: {}".format(valor_pk_destino_padre))

        tbl_origen_hija = relacion_origen["origenHija"]
        tbl_destino = relacion_origen["destinoHija"]
        campos_destino = relacion_origen["campos"]
        tipoOperacion = relacion_origen["tipoOperacion"]
        llaveRelacionOrigen = relacion_origen["llaveRelacionOrigen"]
        llaveRelacionDestino = relacion_origen["llaveRelacionDestino"]
        llaveForaneaOrigen = relacion_origen["llaveForaneaOrigen"]
        esllaveForaneaOrigenGuid = relacion_origen["esllaveForaneaOrigenGuid"]
        llavePrimariaDestino = relacion_origen["llavePrimariaDestino"]
        llavePrimariaOrigen = relacion_origen["llavePrimariaOrigen"]
        detalleRelacion = relacion_origen["detalleRelacion"] if "detalleRelacion" in relacion_origen else None
        if detalleRelacion :
            cardinalidad = detalleRelacion["cardinalidad"] 
            llaveForaneaHija = detalleRelacion["llaveForaneaHija"]
            relationshipClass = detalleRelacion["relationshipClass"] if "relationshipClass" in detalleRelacion else None
            llaveForaneaPadre = detalleRelacion["llaveForaneaPadre"] if "llaveForaneaPadre" in detalleRelacion else None

        condicion = relacion_origen["condicion"] if "condicion" in relacion_origen else None
        idRelacion = relacion_origen["idRelacion"] if "idRelacion" in relacion_origen else None
        filtro = relacion_origen["filtroDestino"] if "filtroDestino" in relacion_origen else None
        filtroOrigen = relacion_origen["filtroOrigen"] if "filtroOrigen" in relacion_origen else None
        conectorFiltroDestino = relacion_origen["conectorFiltroDestino"] if "conectorFiltroDestino" in relacion_origen else None
        conectorFiltroOrigen = relacion_origen["conectorFiltroOrigen"] if "conectorFiltroOrigen" in relacion_origen else None
        usarGeometria = relacion_origen["usarGeometria"] if "usarGeometria" in relacion_origen else False

        if tbl_destino == "[main_feature]":
            tbl_destino = self.claseDestinoPrincipal

        ToolboxLogger.debug("Origen: {}".format(tbl_origen_hija))
        ToolboxLogger.debug("Destino: {}".format(tbl_destino))
        ToolboxLogger.debug("Relación '{}'".format(cardinalidad))
        ToolboxLogger.debug("llaveForaneaHija: {}".format(llaveForaneaHija))
        
        if filtroOrigen:
            ToolboxLogger.debug("Filtro Origen: {}".format(filtroOrigen))
        if filtro:
            ToolboxLogger.debug("Filtro Destino: {}".format(filtro))

        self.actualizarEstadistica(tbl_destino)

        if esllaveForaneaOrigenGuid:
            valor_pk_origen = "{}".format(valor_pk_origen)

        # Esta consulta se hace para obtener los registros de la tabla origen hija relacionados
        # con la tabla origen padre. En condiciones normales responden a la consulta con la claúsula
        # where [llaveForaneaOrigen] = valor_pk_origen más los filtros aplicados a los campos 
        # de la tabla origen hija 

        operador = None
        if llaveForaneaOrigen != "ND":
            llave_Relacion = [llaveForaneaOrigen]
            valor_Relacion = [registro_origen[relacion_origen["campoBusquedaOrigen"]] if "campoBusquedaOrigen" in relacion_origen else valor_pk_origen]
        else:
            llave_Relacion = [llaveRelacionOrigen]
            valor_Relacion = [registro_origen[relacion_origen["campoBusquedaOrigen"]]]

        if filtroOrigen:
            if "operador" in filtroOrigen:
                operador = [None, filtroOrigen["operador"]]
            llave = llave_Relacion + [filtroOrigen["campo"]]
            valor = valor_Relacion + [filtroOrigen["valor"]]
        else:
            llave = llave_Relacion
            valor = valor_Relacion

        where = DataAccess.getWhereClause(llave, valor, operador)
        registros_origen_hija = self.fuente_da.query(tbl_origen_hija, ["*"], where, return_geometry= usarGeometria)

        origen_hija_i = 0
        origen_hija_n = len(registros_origen_hija)

        for registro_origen_hija in registros_origen_hija:

            origen_hija_i += 1
            ToolboxLogger.debug("registro_origen_hija: '{}' {} de {}".format(tbl_origen_hija, origen_hija_i, origen_hija_n))

            ##Procesamiento registros dependientes
            if not self.cumpleCondicion(condicion, registro_origen_hija):
                ToolboxLogger.debug("No cumple condición")
                return

            valor_rk_origen_hija = registro_origen_hija[llaveRelacionOrigen] if llaveRelacionOrigen in registro_origen_hija else ""
            ToolboxLogger.debug("valor_rk_origen_hija: '{}' = {}".format(llaveRelacionOrigen, valor_rk_origen_hija))

            if filtro:
                if not "valor" in filtro and "campo" in filtro:
                    if isinstance(filtro["campo"], str) :
                        campos_filtro = []
                        campos_filtro.append(filtro["campo"])
                    else :
                        campos_filtro = filtro["campo"]
                    valores_filtro = []

                    for campo in campos_filtro :
                        campo_mapeo = [x for x in campos_destino if x["destino"].lower() == campo.lower()]
                        valor_destino = registro_origen_hija[campo_mapeo[0]["origen"]] if campo_mapeo else None
                        if valor_destino:
                            valores_filtro.append(valor_destino)

                    ToolboxLogger.debug("filtro: {}".format(filtro))
                else :
                    valores_filtro = filtro["valor"]

            if cardinalidad == "M-M":
                if "tipoOperacion" in relacion_origen["detalleRelacion"]:
                    tipoOperacionRelacion = relacion_origen["detalleRelacion"]["tipoOperacion"]
                else:
                    tipoOperacionRelacion = tipoOperacion

                llave_relacion = [llaveRelacionDestino]
                valor_relacion = [registro_origen_hija[llaveRelacionOrigen]]

                if filtro:
                    llave_relacion = llave_relacion + [filtro["campo"]]
                    valor_relacion = valor_relacion + [valores_filtro]
                
                conector_relacion = [conectorFiltroDestino] if conectorFiltroDestino else None

                ToolboxLogger.debug("Tabla Principal")
                ##Cuando la relacion es M-M y se inserta un registro en una de las tablas de rompimiento se hace necesario
                ##obtener el GlobalId del registro insertado para poderlo insertar en las tablas de rompimiento.
                ##Por eso se recibe el resultado de la operacion de edición o inserción para usarlo posteriormente como 
                ##llave en el filtro que va a permitir el registro en la tabla de rompimiento
                resultadoOperacion = self.actualizarMapeado(
                                    tbl_destino,
                                    llave_relacion,
                                    campos_destino,
                                    registro_origen_hija,
                                    valor_relacion,
                                    conectores= conector_relacion,
                                    tipo_operacion = tipoOperacion, 
                                    usar_geometria = usarGeometria
                )
                if resultadoOperacion != {}:
                    guid = self.verificarRegistroOrigen(
                        tbl_origen_hija, 
                        llaveRelacionOrigen, 
                        registro_origen_hija, 
                        resultadoOperacion)
                    valor_pk_destino_hija = guid
                    valor_relacion[0] = guid
                else :
                    valor_pk_destino_hija = registro_origen_hija[llaveRelacionOrigen]

                llave_relacion_mm = [llaveForaneaPadre, llaveForaneaHija]
                valor_relacion_mm = [valor_pk_destino_padre, valor_pk_destino_hija]
                where = DataAccess.getWhereClause(llave_relacion_mm, valor_relacion_mm)
                registros_relacion = self.destino_da.query(relationshipClass, [llaveForaneaPadre, llaveForaneaHija], where)

                if tipoOperacionRelacion == "U" and len(registros_relacion) < 1:
                    valor_relacion_mm = [valor_pk_destino_padre, "NULL"]
                    operadores_relacion = [None, "IS"]
                    where = DataAccess.getWhereClause(llave_relacion_mm, valor_relacion_mm, operadores_relacion)
                    registros_relacion = self.destino_da.query(relationshipClass, [llavePrimariaDestino, llaveForaneaPadre, llaveForaneaHija], where)
                    llave_relacion_mm = llavePrimariaDestino
                    campos_relacion_mm = [{"origen": "ND", 
                                           "destino" : llaveForaneaHija, 
                                           "valor_predeterminado" :  valor_pk_destino_hija}]

                    relacion_i = 0
                    relacion_n = len(registros_relacion)
                    for registro_relacion in registros_relacion :
                        valor_relacion_mm = registro_relacion[llavePrimariaDestino]

                        relacion_i += 1
                        ToolboxLogger.debug("Relación: {} de {}".format(relacion_i, relacion_n))

                        ToolboxLogger.debug(
                            "valor_relacion_mm: {} = '{}'".format(
                                llave_relacion_mm,
                                valor_relacion_mm)
                        )
                        ToolboxLogger.debug("Tabla Relación")
                        resultadoOperacion = self.actualizarMapeado(
                            relationshipClass,
                            llave_relacion_mm,
                            campos_relacion_mm,
                            registro_relacion,
                            valor_relacion_mm, 
                            tipo_operacion = tipoOperacionRelacion, 
                            usar_geometria = usarGeometria
                        )
                else :
                    campos_relacion_mm = None
                    relacion_i = 0
                    relacion_n = len(registros_relacion)

                    if relacion_n > 0:
                        for registro_relacion in registros_relacion :
                            relacion_i += 1
                            ToolboxLogger.debug("Relación: {} de {}".format(relacion_i, relacion_n))

                            ToolboxLogger.debug(
                                "valor_pk_destino_padre: {}".format(
                                    valor_pk_destino_padre)
                            )
                            ToolboxLogger.debug(
                                "valor_pk_destino_hija: {}".format(
                                    valor_pk_destino_hija)
                            )
                            ToolboxLogger.debug("Tabla Relación")
                            resultadoOperacion = self.actualizarMapeado(
                                relationshipClass,
                                llave_relacion_mm,
                                campos_relacion_mm,
                                registro_relacion,
                                valor_relacion_mm, 
                                tipo_operacion = tipoOperacionRelacion, 
                                usar_geometria = usarGeometria
                            )
                    else :
                        ToolboxLogger.debug(
                            "valor_pk_destino_padre: {}".format(
                                valor_pk_destino_padre)
                        )
                        ToolboxLogger.debug(
                            "valor_pk_destino_hija: {}".format(
                                valor_pk_destino_hija)
                        )
                        ToolboxLogger.debug("Tabla Relación")
                        resultadoOperacion = self.actualizarMapeado(
                            relationshipClass,
                            llave_relacion_mm,
                            campos_relacion_mm,
                            None,
                            valor_relacion_mm, 
                            tipo_operacion = tipoOperacionRelacion, 
                            usar_geometria = usarGeometria
                        )

            elif cardinalidad == "1-M":

                # Para cada registro de la tabla origen hija se efectúa actualizarMapeado, que actualiza
                # los registros de la tabla destino hija en caso de que existan o los crea en caso de que no
                # existan. Internamente la operación hace una consulta en la tabla destino hija para determinar
                # si el registro existe y en principio la consulta obtiene el registro de la tabla destino hija
                # que esté relacionado con el registro de correspondiente de la tabla destino padre mediante
                # la llaveForaneaHija que debe ser igual a la llaveForaneaDestino si existe, pero como esta consulta
                # puede arrojar varios registros y la operacion actualizarMapeo actua sobre un solo registro se debe 
                # agregar otra llave para hacer el resultado unico, esto se logra relacionando adicionamente el registro
                # actual de la tabla origen hija con la tabla destino hija mediante el par de llaves llaveRelacionOrigen
                # y llaveRelacionDestino. En condicones normales esta consulta debería tener una claúsula where del tipo
                # "llaveRelacionDestino = valor_rk_origen_hija AND llaveForaneHija = valor_pk_destino_padre" más 
                # los filtros que se agreguen a los campos de la tabla destino hija.

                if valor_rk_origen_hija != '' :
                    llave_relacion = [llaveRelacionDestino, llaveForaneaHija]
                    llaveAlternaOrigen = detalleRelacion["campoLlaveRegOrigen"] if "campoLlaveRegOrigen" in detalleRelacion else None
                    if llaveAlternaOrigen :
                        # self.parentGlobalId = valor_pk_destino_padre
                        valor_relacion = [registro_origen_hija[llaveAlternaOrigen], self.parentGlobalId]
                    else:
                        valor_relacion = [valor_rk_origen_hija, valor_pk_destino_padre]
                else :
                    llave_relacion = [llaveForaneaHija]
                    valor_relacion = [valor_pk_destino_padre]

                if filtro:
                    if isinstance(filtro, list) :
                        llave = llave_relacion + filtro["campo"]
                        valor = valor_relacion + filtro["valor"]
                    else :
                        llave = llave_relacion + [filtro["campo"]]
                        valor = valor_relacion + [filtro["valor"]]
                else :
                    llave = llave_relacion
                    valor = valor_relacion
                        
                ToolboxLogger.debug("Tabla Principal")
                resultadoOperacion = self.actualizarMapeado(
                    tbl_destino,
                    llave,
                    campos_destino,
                    registro_origen_hija,
                    valor,
                    tipo_operacion = tipoOperacion, 
                    usar_geometria = usarGeometria
                )
                if resultadoOperacion != {}:
                    guid = self.verificarRegistroOrigen(
                        tbl_origen_hija, 
                        llaveRelacionOrigen, 
                        registro_origen_hija, 
                        resultadoOperacion)
                    valor_relacion[0] = guid if llave_relacion[0] == llavePrimariaDestino else valor_relacion[0]

            where = DataAccess.getWhereClause(llave_relacion, valor_relacion)
            registros_resultado = self.destino_da.query(tbl_destino, [llaveRelacionDestino, llavePrimariaDestino], where)
            ToolboxLogger.debug("registros_resultado--> {}".format(registros_resultado))

            # Procesamiento Recursivo
            relacionesOrigenHija = relacion_origen["relacionesOrigen"] if "relacionesOrigen" in relacion_origen else []
            if relacionesOrigenHija:
                ToolboxLogger.debug("Procesar Relaciones Origen")
                ToolboxLogger.debug("llave_relacion: '{}'".format(llave_relacion))
                ToolboxLogger.debug("valor_relacion: '{}'".format(valor_relacion))

                if isinstance(llave_relacion, str) and llave_relacion.lower() == 'parentglobalid':
                    self.parentGlobalId = valor_relacion

                where = DataAccess.getWhereClause(llave_relacion, valor_relacion)
                registros_destino_hija = self.destino_da.query(tbl_destino, [llaveRelacionDestino, llavePrimariaDestino], where)

                valor_pk_origen_padre = registro_origen[llavePrimariaOrigen] if llavePrimariaOrigen in registro_origen else ""
                ToolboxLogger.debug("valor_pk_origen_padre: '{}' = '{}'".format(llavePrimariaOrigen, valor_pk_origen_padre))

                valor_fk_origen_hija = registro_origen_hija[llaveForaneaOrigen] if llaveForaneaOrigen in registro_origen_hija else ""
                ToolboxLogger.debug("valor_fk_origen_hija : '{}' = '{}'".format(llaveForaneaOrigen, valor_fk_origen_hija))

                valor_pk_origen_hija = registro_origen_hija[llavePrimariaOrigen] if llavePrimariaOrigen in registro_origen_hija else ""
                ToolboxLogger.debug("valor_pk_origen_hija : '{}' = '{}'".format(llavePrimariaOrigen, valor_pk_origen_hija))

                destino_hija_i = 0
                destino_hija_n = len(registros_destino_hija)

                for registro_destino_hija in registros_destino_hija :
                    destino_hija_i += 1
                    ToolboxLogger.debug("Registro Origen Hija: '{}' {} de {}".format(tbl_destino, destino_hija_i, destino_hija_n))

                    valor_pk_destino = registro_destino_hija[llavePrimariaDestino]

                    ToolboxLogger.debug(
                        "valor_pk_destino: '{}' = '{}'".format(llavePrimariaDestino, valor_pk_destino))
                    ToolboxLogger.debug("****Procesamiento Recursivo****")

                    relacion_origen_i = 0
                    relacion_origen_n = len(relacionesOrigenHija)

                    for relacion in relacionesOrigenHija:
                        relacion_origen_i += 1
                        ToolboxLogger.debug("Relacion Origen '{}' {} de {}".format(tbl_destino, relacion_origen_i, relacion_origen_n))

                        self.actualizarRelacionesOrigen(
                            relacion, registro_origen_hija, valor_pk_origen_hija, valor_pk_destino)

    @ToolboxLogger.log_method
    def actualizarRelacionesDestino(self, relacion_destino, registro_origen, valor_pk_destino):

        tbl_destino = relacion_destino["destino"]
        llaveForaneaDestino = relacion_destino["llaveForaneaDestino"]
        llavePrimariaDestino = relacion_destino["llavePrimariaDestino"]
        llavePrimariaOrigen = relacion_destino["llavePrimariaOrigen"]
        llaveEsGuid = relacion_destino["llaveEsGuid"]

        campos = relacion_destino["campos"]
        tipoOperacion = relacion_destino["tipoOperacion"]
        condicion = relacion_destino["condicion"] if "condicion" in relacion_destino else None
        idRelacion = relacion_destino["idRelacion"] if "idRelacion" in relacion_destino else None
        usarGeometria = relacion_destino["usarGeometria"] if "usarGeometria" in relacion_destino else False

        if tbl_destino == "[main_feature]":
            tbl_destino = self.claseDestinoPrincipal
        self.actualizarEstadistica(tbl_destino)

        ToolboxLogger.debug("Destino: {}".format(tbl_destino))

        if not self.cumpleCondicion(condicion, registro_origen):
            ToolboxLogger.debug("No cumple condición")
            return

        resultadoOperacion = self.actualizarMapeado(
            tbl_destino,
            llaveForaneaDestino,
            campos,
            registro_origen,
            valor_pk_destino,
            tipo_operacion = tipoOperacion, 
            usar_geometria = usarGeometria
        )

        # Para obtener el valor de la llave Primaria Destino
        where = DataAccess.getWhereClause(
            llaveForaneaDestino, valor_pk_destino
        )
        registros_destino = self.destino_da.query(tbl_destino, llavePrimariaDestino, where)

        if len(registros_destino) if registros_destino != None else 0 == 1:
            valor_pk_destino = registros_destino[0][llavePrimariaDestino]
            if llaveEsGuid:
                valor_pk_destino = "{}".format(valor_pk_destino)

            # Actualizar Relaciones Origen
            valor_pk_origen = registro_origen[llavePrimariaOrigen]

            relacionesOrigenHija = relacion_destino["relacionesOrigen"] if "relacionesOrigen" in relacion_destino else [
            ]
            if relacionesOrigenHija:
                ToolboxLogger.debug("Procesar Relaciones Origen")

                ToolboxLogger.debug("****Procesamiento Recursivo****")
                for relacion in relacionesOrigenHija:
                    self.actualizarRelacionesOrigen(
                        relacion, registro_origen, valor_pk_origen, valor_pk_destino)

        elif len(registros_destino) > 1:
            ToolboxLogger.debug(
                "Error de Integridad Refencial: {}".format(tbl_destino)
            )

    @ToolboxLogger.log_method
    def procesarRelacionesOrigen(self, mapeo, registro_origen, valor_pk_origen, valor_pk_destino_padre):
        relacionesOrigen = mapeo["relacionesOrigen"]

        for relacion in relacionesOrigen:
            self.actualizarRelacionesOrigen(
                relacion, registro_origen, valor_pk_origen, valor_pk_destino_padre)

    @ToolboxLogger.log_method
    def procesarRelacionesDestino(self, mapeo, registro_origen, valor_pk_destino):
        relaciones_destino = mapeo["relacionesDestino"]

        for relacion_destino in relaciones_destino:
            self.actualizarRelacionesDestino(
                relacion_destino, registro_origen, valor_pk_destino)

    @ToolboxLogger.log_method
    def actualizarRegistroOrigen(self, tabla, registro, llave, valor = None) :
        pass

    @ToolboxLogger.log_method
    def actualizarRegistroDestino(self, tabla, registro, llave, valor = None) :
        pass
    
    def agregarInforme(self) :
        pass

    @ToolboxLogger.log_method
    def verificarRegistroOrigen(self, tabla, llave, registro, resultadoOperacion) :
        if resultadoOperacion :
            valor_relacion = resultadoOperacion["globalId"] if "globalId" in resultadoOperacion else None
            if valor_relacion :
                    self.actualizarRegistroOrigen(tabla, registro, llave, valor_relacion)
        else :
            valor_relacion = None
                    
        return valor_relacion

    @ToolboxLogger.log_method
    def procesarMapeo(self, mapeo, queryList):
        self.timer = TimeUtil()

        try :
            # Actualizar tabla principal
            origen = mapeo["origen"]
            destino = mapeo["destino"]
            llaveRelacionOrigen = mapeo["llaveRelacionOrigen"]
            llaveRelacionDestino = mapeo["llaveRelacionDestino"]
            llavePrimariaDestino = mapeo["llavePrimariaDestino"]
            llavePrimariaOrigen = mapeo["llavePrimariaOrigen"]
            llaveEsGuid = mapeo["llaveEsGuid"]
            campos = mapeo["campos"]
            tipoOperacion = mapeo["tipoOperacion"]
            usarGeometria = mapeo["usarGeometria"] if "usarGeometria" in mapeo else False
            pattern = "{:<45} {:>3} creados {:>3} actualizados {:>3} no actualizados {:>3} errores {:>3} registros {:>3} operaciones"
            ancho = len(pattern) + 29

            if origen == "[main_feature]":
                origen = self.obtenerTablaPrincipal()
            if destino == "[main_feature]":
                destino = self.claseDestinoPrincipal

            ToolboxLogger.info("origen: '{}'".format(origen))
            ToolboxLogger.info("destino: '{}'".format(destino))
            ToolboxLogger.debug("llaveRelacionOrigen: '{}'".format(llaveRelacionOrigen))

            campos_origen = []
            campos_origen.append(llaveRelacionOrigen)

            for campo in campos:
                campos_origen.append(campo["origen"])

            tbl_origen = origen
            tbl_destino = destino

            filtroOrigen = mapeo["filtroOrigen"] if "filtroOrigen" in mapeo else None
            if filtroOrigen :
                queryList.addQuery(QueryItem(filtroOrigen["campo"], filtroOrigen["valor"]))

            where = queryList.getWhereClause()
            datos_origen = self.fuente_da.query(tbl_origen, ["*"], where, return_geometry = usarGeometria)
            ToolboxLogger.info("Origen: {}, {} registros encontrados".format(tbl_origen, len(datos_origen)))
            ToolboxLogger.info("filtro: {}".format(where))

            procesados = 0
            if len(datos_origen) > 0:
                for registro_origen in datos_origen:
                    ToolboxLogger.info("-".ljust(ancho, "-"))

                    procesados += 1
                    ToolboxLogger.info("'{}': Registro {}".format(tbl_origen, procesados)) 

                    self.estadisticas.agregarEstadistica()
                    self.estadisticas.agregarEncuesta(registro_origen[llavePrimariaOrigen])

                    valor_primaria_origen = registro_origen[llavePrimariaOrigen]
                    valor_relacion_origen = registro_origen[llaveRelacionOrigen]
                    ToolboxLogger.info("valor_primaria_origen: '{}' = '{}'".format(llavePrimariaOrigen, valor_primaria_origen))
                    ToolboxLogger.info("valor_relacion_origen: '{}' = '{}'".format(llaveRelacionOrigen, valor_relacion_origen))

                    resultadoOperacion = self.actualizarMapeado(
                        tbl_destino,
                        llaveRelacionDestino,
                        campos,
                        registro_origen,
                        valor_relacion_origen,
                        tipo_operacion = tipoOperacion, 
                        usar_geometria = usarGeometria
                    )
                    if resultadoOperacion != {}:
                        guid = self.verificarRegistroOrigen(
                            tbl_origen, 
                            llaveRelacionOrigen, 
                            registro_origen, 
                            resultadoOperacion)
                        valor_relacion_origen = guid if llaveRelacionDestino == llavePrimariaDestino else valor_relacion_origen


                    # Para obtener el valor de la llave Primaria Destino
                    where = DataAccess.getWhereClause(llaveRelacionDestino, valor_relacion_origen)
                    registros_destino = self.destino_da.query(tbl_destino, ["*"], where)

                    # Las llaves RelacionOrigen y RelacionDestino deberían ser del tipo GUID y deberían ser únicas
                    # por lo tanto si la consulta trae más de un registro se presenta un error de integridad referencial
                    # entre el origen y el destino es una relación 0..1

                    if len(registros_destino) if registros_destino != None else 0 == 1:
                        valor_pk_destino = registros_destino[0][llavePrimariaDestino]
                        if llaveEsGuid:
                            valor_pk_destino = "{}".format(valor_pk_destino)

                        #Actualizar Relaciones Destino
                        ToolboxLogger.debug("Procesando Relaciones Destino")
                        ToolboxLogger.debug("valor_pk_destino: {}".format(valor_pk_destino))
                        self.procesarRelacionesDestino(mapeo, registro_origen, valor_pk_destino)

                        # Actualizar Relaciones Origen
                        ToolboxLogger.debug("Procesando Relaciones Origen")
                        valor_pk_origen = registro_origen[llavePrimariaOrigen]
                        ToolboxLogger.debug("valor_pk_origen: {}".format(valor_pk_origen))
                        self.parentGlobalId = valor_pk_destino
                        self.procesarRelacionesOrigen(mapeo, registro_origen, valor_pk_origen, valor_pk_destino)

                    elif len(registros_destino) > 1:
                        ToolboxLogger.info("Error de Integridad Refencial: {}".format(destino))
                        self.actualizarEstadistica(tbl_destino, "E")
                    
                    self.actualizarRegistroOrigen(tbl_origen, registro_origen, llavePrimariaOrigen)
                    self.actualizarRegistroDestino(tbl_destino, registros_destino[0], llavePrimariaDestino)
            ToolboxLogger.info("")
        except Exception as e:
            ToolboxLogger.info("!".ljust(ancho, "*"))
            ToolboxLogger.info("Error: {}".format(e))
            ToolboxLogger.info("!".ljust(ancho, "*"))
        finally :
            ToolboxLogger.info("-".ljust(ancho, "-"))
            cuenta_total = 0
            errores = 0
            for tabla in self.estadisticas.tablasEstadisticas:
                ToolboxLogger.info(pattern.format(tabla,
                    self.estadisticas.obtenerTotalEstadisticasTabla(tabla, "C"),
                    self.estadisticas.obtenerTotalEstadisticasTabla(tabla, "U"),
                    self.estadisticas.obtenerTotalEstadisticasTabla(tabla, "NU"),
                    self.estadisticas.obtenerTotalEstadisticasTabla(tabla, "E"),
                    self.estadisticas.obtenerTotalRegistrosTabla(tabla),
                    self.estadisticas.obtenerTotalOperacionesTabla(tabla)))

            cuenta_total = self.estadisticas.obtenerTotalRegistros()
            errores = self.estadisticas.obtenerTotalEstadisticas("E")

            ToolboxLogger.info("-".ljust(ancho, "-"))
            ToolboxLogger.info(self.timer.stopTimer("Tiempo Total: "))
            
            ToolboxLogger.info("Total Creados        : {}".format(self.estadisticas.obtenerTotalEstadisticas("C")))
            ToolboxLogger.info("Total Actualizados   : {}".format(self.estadisticas.obtenerTotalEstadisticas("U")))
            ToolboxLogger.info("Total No Actualizados: {}".format(self.estadisticas.obtenerTotalEstadisticas("NU")))
            ToolboxLogger.info("Total Errores        : {}".format(errores))
            ToolboxLogger.info("Total Registros      : {}".format(cuenta_total))
            ToolboxLogger.info("Total Operaciones    : {}".format(self.estadisticas.obtenerTotalOperaciones()))
            ToolboxLogger.info("Total Tablas         : {}".format(self.estadisticas.obtenerTotalTablas()))
            ToolboxLogger.info("Total Encuestas      : {}".format(self.estadisticas.obtenerNumeroEstadisticas()))
            
            self.agregarInforme()

            if cuenta_total > 0:
                ToolboxLogger.info("Tiempo por registro  : {}".format(self.timer.timeSpan / cuenta_total))
            else :
                ToolboxLogger.info("Tiempo por registro  : {}".format(0))
            ToolboxLogger.info("-".ljust(ancho, "-"))

            return  len(datos_origen), cuenta_total, errores

