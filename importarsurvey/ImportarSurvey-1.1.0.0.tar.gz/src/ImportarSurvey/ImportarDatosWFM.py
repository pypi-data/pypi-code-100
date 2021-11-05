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

class Importar:
    def __init__(self, datosFuenteWFM, destino_da, claseDestino=''):
        self.estadisticas = Estadisticas()
        self.datosFuenteWFM = datosFuenteWFM
        self.destino_da = destino_da
        ##self.claseFuentePrincipal = clasePrincipal
        self.claseDestinoPrincipal=claseDestino
        
    def _getMainTable(self):
        return self.claseFuentePrincipal

    def _nombreTabla(self, nombreLargoTabla):
        ruta, nombre = path.split(nombreLargoTabla)
        ruta = ruta

        return nombre

    def _actualizarEstadistica(self, nombreTabla, tipo):
        self.estadisticas.actualizarEstadistica(nombreTabla, tipo)

    def _cumpleCondicion(self, condicion, registro):
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
    def _obtener_valores_mapeados(self, campos, registro_origen) :
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
    
    @ToolboxLogger.log_method
    def _add_mapped_da(self, table, campos_busqueda, campos, registro_origen, valores_pk, usar_geometria=False):
        try:
            attributes = {}
            attributesRemove=[]
            if isinstance(campos_busqueda, list) and isinstance(valores_pk, list):
                for campo_busqueda in campos_busqueda:
                    index = campos_busqueda.index(campo_busqueda)
                    attributes[campo_busqueda] = valores_pk[index]
            else:
                attributes[campos_busqueda] = valores_pk

            if campos:
                for campo in campos:

                    if "valor_predeterminado" in campo:
                        valor=campo["valor_predeterminado"]

                    if "origen" in campo :
                        if campo["origen"] != "ND":
                            valor = registro_origen[campo["origen"]]
                            if valor == None and "valor_predeterminado" in campo:
                                valor = campo["valor_predeterminado"]    
                        elif "destino" in campo:
                            if campo["origen"] == "ND" and campo["destino"].upper()=="PARENTGLOBALID":
                                valor = self.parentGlobalId
                            else :
                                valor = campo["valor_predeterminado"]    
                    elif "valor" in campo :
                        valor = campo["valor"]
                    else :
                        valor = None

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
                            attributes[campo["destino"]]=None
                            attributesRemove.append(campo["destino"])

                        ToolboxLogger.debug(
                            "---->ins - {} = {}".format(campo["destino"], valor)
                        )
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
            if resultado:
                self._actualizarEstadistica(table.properties.name, "C")

            return resultado
        except Exception as e:

            self._actualizarEstadistica(table.properties.name, "E")
            ToolboxLogger.debug("ERROR: ---->{}".format(e))

        return None

    @ToolboxLogger.log_method
    def _update_mapped_da(self, table, campos_busqueda, campos, registro_origen, valores_pk, usar_geometria=False):
        ToolboxLogger.debug("---->campos_busqueda: {}".format(campos_busqueda))
        ToolboxLogger.debug("---->valores_pk: {}".format(valores_pk))
        attributesRemove=[]
        try:
            where = DataAccess.getWhereClause(campos_busqueda, valores_pk)

            query = self.destino_da.query(table, ["*"], where, return_geometry=usar_geometria)
            count = len(query) if query != None else 0
            
            if(count > 0) :
                for feature in query:
                    attributes = {}
                    if "geometry" in feature and "geometry" in registro_origen:  
                        if feature["geometry"] != registro_origen["geometry"] :
                            attributes["geometry"] = registro_origen["geometry"]
                    
                    if campos:
                        for campo in campos:
                            if "origen" in campo :
                                if campo["origen"] != "ND":
                                    valor = registro_origen[campo["origen"]]
                                    if valor == None and "valor_predeterminado" in campo:
                                        valor = campo["valor_predeterminado"]    
                                elif "destino" in campo:
                                    if campo["origen"] == "ND" and campo["destino"].upper()=="PARENTGLOBALID":
                                        valor = self.parentGlobalId
                                    else :
                                        valor = campo["valor_predeterminado"]    
                            elif "valor" in campo :
                                valor = campo["valor"]
                            else :
                                valor = None

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
                                    attributes[campo["destino"]]=None
                                    attributesRemove.append(campo["destino"])
                                ToolboxLogger.debug("---->upd - {} = {}".format(campo["destino"], valor))

                        if len(attributes) > 0 :
                            attributes[table.properties.objectIdField] = feature[table.properties.objectIdField]
                            attributes[table.properties.globalIdField] = feature[table.properties.globalIdField]
                            
                            resultado = self.destino_da.update(table, attributes)
                            if resultado:
                                self._actualizarEstadistica(table.properties.name, "U")

                            return resultado
                            
                    self._actualizarEstadistica(table.properties.name, "NU")
                    return attributes

        except Exception as e:
            # self._actualizarEstadistica(table.properties.name, "E")
            ToolboxLogger.debug("ERROR: ---->{}".format(e))

        return None 

    @ToolboxLogger.log_method
    def actualizar_mapeado(self, nombre_tabla, campo_busqueda, campos, registro_origen, valor_relacion, tipo_operacion, usar_geometria = False):
        
        if nombre_tabla == "[main_feature]":
            tabla = self.destino_da.getTable(self.claseDestinoPrincipal)
        else:
            tabla = self.destino_da.getTable(nombre_tabla)

        r = None
        if tipo_operacion == "C":
            r = self._add_mapped_da(
                tabla, campo_busqueda, campos, registro_origen, valor_relacion, usar_geometria
            )
        elif tipo_operacion == "U":
            r = self._update_mapped_da(
                tabla, campo_busqueda, campos, registro_origen, valor_relacion, usar_geometria
            )
        elif tipo_operacion == "CU":
            r = self._update_mapped_da(
                tabla, campo_busqueda, campos, registro_origen, valor_relacion, usar_geometria
            )
            if r == None:
                r = self._add_mapped_da(
                    tabla, campo_busqueda, campos, registro_origen, valor_relacion, usar_geometria
                )
        return r

    @ToolboxLogger.log_method
    def _actualizarRelacionesOrigen(self, relacion_origen,
                                    registro_origen,
                                    valor_pk_origen,
                                    valor_pk_destino_padre):
        #ToolboxLogger.debug("relacion_origen: {}".format(relacion_origen))
        #ToolboxLogger.debug("registro_origen: {}".format(registro_origen))
        #ToolboxLogger.debug("valor_pk_origen: {}".format(valor_pk_origen))
        #ToolboxLogger.debug("valor_pk_destino_padre: {}".format(valor_pk_destino_padre))

        tbl_origen_hija = relacion_origen["origenHija"]
        tbl_destino = relacion_origen["destinoHija"]
        campos_destino = relacion_origen["campos"]
        tipoOperacion = relacion_origen["tipoOperacion"]
        llaveRelacionOrigen = relacion_origen["llaveRelacionOrigen"]
        llaveRelacionDestino = relacion_origen["llaveRelacionDestino"]
        llaveForaneaPadre = relacion_origen["llaveForaneaOrigen"]
        esllaveForaneaOrigenGuid = relacion_origen["esllaveForaneaOrigenGuid"]
        llavePrimariaDestino = relacion_origen["llavePrimariaDestino"]
        llavePrimariaOrigen = relacion_origen["llavePrimariaOrigen"]
        cardinalidad = relacion_origen["detalleRelacion"]["cardinalidad"]
        condicion = relacion_origen["condicion"] if "condicion" in relacion_origen else None
        idRelacion = relacion_origen["idRelacion"] if "idRelacion" in relacion_origen else None
        filtro = relacion_origen["filtroDestino"] if "filtroDestino" in relacion_origen else None
        filtroOrigen = relacion_origen["filtroOrigen"] if "filtroOrigen" in relacion_origen else None
        usarGeometria = relacion_origen["usarGeometria"] if "usarGeometria" in relacion_origen else False

        if tbl_destino == "[main_feature]":
            tbl_destino = self.claseDestinoPrincipal

        ToolboxLogger.debug("Origen: {}".format(tbl_origen_hija))
        ToolboxLogger.debug("Destino: {}".format(tbl_destino))
        if filtroOrigen:
            ToolboxLogger.debug("Filtro Origen: {}".format(filtroOrigen))
        if filtro:
            ToolboxLogger.debug("Filtro Destino: {}".format(filtro))


        self._actualizarEstadistica(tbl_destino, "")
        ##Esto es necesario para el proceso inverso de Marcelo.  En este sentido del precargue no se requiere
        ##self.destino_da.describeRelation(tbl_destino, idRelacion)

        if esllaveForaneaOrigenGuid:
            valor_pk_origen = "{}".format(valor_pk_origen)

        operador=None
        if filtroOrigen:
            if "operador" in filtroOrigen:
                operador = [None, filtroOrigen["operador"]]
            llave = [llaveForaneaPadre, filtroOrigen["campo"]]
            valor = [valor_pk_origen, filtroOrigen["valor"]]
        else:
            if llaveForaneaPadre!= "ND":
                llave = llaveForaneaPadre
                valor = valor_pk_origen
            else:
                llave=llaveRelacionOrigen
                valor=registro_origen[relacion_origen["campoBusquedaOrigen"]]

        where = DataAccess.getWhereClause(llave, valor, operador)

        registros_origen_hija = self.fuente_da.query(
            tbl_origen_hija, ["*"], where)

        for registro_origen_hija in registros_origen_hija:

            #ToolboxLogger.debug("registro_origen_hija: {}".format(registro_origen_hija))
            ##Procesamiento registros dependientes
            if not self._cumpleCondicion(condicion, registro_origen_hija):
                ToolboxLogger.debug("No cumple condición")
                return

            if cardinalidad == "M-M":
                ToolboxLogger.debug("'Relación M-M'")
                relationshipClass = relacion_origen["detalleRelacion"]["relationshipClass"]
                llaveForaneaPadre = relacion_origen["detalleRelacion"]["llaveForaneaPadre"]
                llaveForaneaHija = relacion_origen["detalleRelacion"]["llaveForaneaHija"]

                if "tipoOperacion" in relacion_origen["detalleRelacion"]:
                    tipoOperacionRelacion = relacion_origen["detalleRelacion"]["tipoOperacion"]
                else:
                    tipoOperacionRelacion = tipoOperacion

                if filtro:
                    llave_relacion = [llaveRelacionDestino, filtro["campo"]]
                    valor_relacion = [
                        registro_origen_hija[llaveRelacionOrigen], filtro["valor"]]
                else:
                    llave_relacion = llaveRelacionDestino
                    valor_relacion = registro_origen_hija[llaveRelacionOrigen]

                ToolboxLogger.debug("Tabla Principal")
                ##Cuando la relacion es M-M y se inserta un registro en una de las tablas de rompimiento se hace necesario
                ##obtener el GlobalId del registro insertado para poderlo insertar en las tablas de rompimiento.
                ##Por eso se recibe el resultado de la operacion de edición o inserción para usarlo posteriormente como 
                ##llave en el filtro que va a permitir el registro en la tabla de rompimiento
                resultadoOperacion= self.actualizar_mapeado(
                                    tbl_destino,
                                    llave_relacion,
                                    campos_destino,
                                    registro_origen_hija,
                                    valor_relacion,
                                    tipoOperacion, 
                                    usarGeometria
                )
                
                if valor_relacion == None and resultadoOperacion!= None:
                    valor_relacion = resultadoOperacion["globalId"] if "globalId" in resultadoOperacion else None

                where = DataAccess.getWhereClause(
                    llave_relacion, valor_relacion)

                registros_destino = self.destino_da.query(
                    tbl_destino, [llaveRelacionDestino,
                                  llavePrimariaDestino], where
                )

                if len(registros_destino) if registros_destino != None else 0 == 1:
                    valor_pk_destino_hija = registros_destino[0][llavePrimariaDestino]
                    ToolboxLogger.debug(
                        "valor_pk_destino_padre: {}".format(
                            valor_pk_destino_padre)
                    )
                    ToolboxLogger.debug(
                        "valor_pk_destino_hija: {}".format(
                            valor_pk_destino_hija)
                    )
                    tbl_relacion = relationshipClass
                    ToolboxLogger.debug("Tabla Relación")
                    self.actualizar_mapeado(
                        tbl_relacion,
                        [llaveForaneaPadre, llaveForaneaHija],
                        None,
                        None,
                        [valor_pk_destino_padre, valor_pk_destino_hija],
                        tipoOperacionRelacion
                    )
                elif len(registros_destino) if registros_destino != None else 0 > 1:
                    ToolboxLogger.debug(
                        "Error de Integridad Referencial: {}".format(
                            tbl_destino)
                    )
            elif cardinalidad == "1-M":
                ToolboxLogger.debug("'Relación 1-M'")

                llaveForaneaHija = relacion_origen["detalleRelacion"]["llaveForaneaHija"]

                
                ToolboxLogger.debug("valor_pk_destino_padre: {}".format(valor_pk_destino_padre))
                ToolboxLogger.debug("llaveForaneaHija: {}".format(llaveForaneaHija))
                ToolboxLogger.debug("Tabla Principal")

                if filtro:
                    llave_relacion = [llaveForaneaHija, filtro["campo"]]
                    valor_relacion = [valor_pk_destino_padre, filtro["valor"]]
                else:
                    if "campoLlaveRegOrigen" in relacion_origen["detalleRelacion"]:
                        self.parentGlobalId=valor_pk_destino_padre
                        valor_relacion = registro_origen_hija[relacion_origen["detalleRelacion"]["campoLlaveRegOrigen"]]
                    else:
                        valor_relacion = valor_pk_destino_padre
                        
                    
                    llave_relacion = llaveForaneaHija

                self.actualizar_mapeado(
                    tbl_destino,
                    llave_relacion,
                    campos_destino,
                    registro_origen_hija,
                    valor_relacion,
                    tipoOperacion,
                    usarGeometria
                )

            # Procesamiento Recursivo
            relacionesOrigenHija = relacion_origen["relacionesOrigen"] if "relacionesOrigen" in relacion_origen else [
            ]
            if relacionesOrigenHija:
                ToolboxLogger.debug("Procesar Relaciones Origen")

                valor_pk_origen_hija = registro_origen_hija[llavePrimariaOrigen]

                ToolboxLogger.debug("llave_relacion: {}".format(llave_relacion))
                ToolboxLogger.debug("valor_relacion: {}".format(valor_relacion))

                if isinstance(llave_relacion, str) and llave_relacion.upper()=='PARENTGLOBALID':
                    self.parentGlobalId=valor_relacion

                where = DataAccess.getWhereClause(
                    llave_relacion, valor_relacion)

                registros_destino = self.destino_da.query(
                    tbl_destino, [llaveRelacionDestino,
                                  llavePrimariaDestino], where
                )
                if(len(registros_destino) > 0):
                    valor_pk_destino = registros_destino[0][llavePrimariaDestino]

                    ToolboxLogger.debug(
                        "valor_pk_destino: {}".format(valor_pk_destino))
                    ToolboxLogger.debug("****Procesamiento Recursivo****")

                    for relacion in relacionesOrigenHija:
                        self._actualizarRelacionesOrigen(
                            relacion, registro_origen_hija, valor_pk_origen_hija, valor_pk_destino)

    @ToolboxLogger.log_method
    def _actualizarRelacionDestino(self, relacion_destino, registro_origen, valor_pk_destino):

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

        self._actualizarEstadistica(tbl_destino, "")

        ToolboxLogger.debug("Destino: {}".format(tbl_destino))
        ##Esto es necesario para el proceso inverso de Marcelo.  En este sentido del precargue no se requiere
        ##self.destino_da.describeRelation(tbl_destino, idRelacion)   
        if not self._cumpleCondicion(condicion, registro_origen):
            ToolboxLogger.debug("No cumple condición")
            return

        self.actualizar_mapeado(
            tbl_destino,
            llaveForaneaDestino,
            campos,
            registro_origen,
            valor_pk_destino,
            tipoOperacion,
            usarGeometria
        )

        # Para obtener el valor de la llave Primaria Destino
        where = DataAccess.getWhereClause(
            llaveForaneaDestino, valor_pk_destino
        )
        registros_destino = self.destino_da.query(
            tbl_destino, llavePrimariaDestino, where
        )

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
                    self._actualizarRelacionesOrigen(
                        relacion, registro_origen, valor_pk_origen, valor_pk_destino)

        elif len(registros_destino) > 1:
            ToolboxLogger.debug(
                "Error de Integridad Refencial: {}".format(tbl_destino)
            )

    @ToolboxLogger.log_method
    def actualizarRelacionesOrigen(self, mapeo, registro_origen, valor_pk_origen, valor_pk_destino_padre):
        relacionesOrigen = mapeo["relacionesOrigen"]

        for relacion in relacionesOrigen:
            self._actualizarRelacionesOrigen(
                relacion, registro_origen, valor_pk_origen, valor_pk_destino_padre)

    @ToolboxLogger.log_method
    def actualizarRelacionesDestino(self, mapeo, registro_origen, valor_pk_destino):
        relaciones_destino = mapeo["relacionesDestino"]

        for relacion_destino in relaciones_destino:
            self._actualizarRelacionDestino(
                relacion_destino, registro_origen, valor_pk_destino)

    @ToolboxLogger.log_method
    def actualizarRegistroOrigen(self, tabla, llave, registro) :
        pass

    @ToolboxLogger.log_method
    def actualizarMapeo(self, mapeo, camposFiltro = None, valoresFiltro = None):
        self.timer = TimeUtil()

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
        pattern = "{:<45} {:>3} creados {:>3} actualizados {:>3} no actualizados {:>3} errores {:>3} total"
        ancho = len(pattern) + 29

        if origen == "[main_feature]":
            origen = self._getMainTable()
        if destino == "[main_feature]":
            destino = self.claseDestinoPrincipal

        ToolboxLogger.info("origen: {}".format(origen))
        ToolboxLogger.info("destino: {}".format(destino))
        ToolboxLogger.debug("llaveRelacionOrigen: {}".format(llaveRelacionOrigen))

        campos_origen = []
        campos_origen.append(llaveRelacionOrigen)

        for campo in campos:
            campos_origen.append(campo["origen"])

        tbl_origen = origen
        tbl_destino = destino

        filtroOrigen = mapeo["filtroOrigen"] if "filtroOrigen" in mapeo else None
        ql = QueryList()

        if camposFiltro != None and valoresFiltro != None : 
            ql.addQuery(QueryItem(camposFiltro, valoresFiltro))

        if filtroOrigen :
            ql.addQuery(QueryItem(filtroOrigen["campo"], filtroOrigen["valor"]))

        where = ql.getWhereClause()
        ToolboxLogger.info("where: {}".format(where))
        datos_origen = self.fuente_da.query(tbl_origen, ["*"], where)

        if len(datos_origen) > 0:
            for registro_origen in datos_origen:
                ToolboxLogger.debug("-".ljust(ancho, "-"))      
                ToolboxLogger.debug("{}: {}={}".format(tbl_origen, llavePrimariaOrigen, registro_origen[llavePrimariaOrigen]))

                self.estadisticas.agregarEstadistica()

                valor_relacion_origen = registro_origen[llaveRelacionOrigen]
                ToolboxLogger.debug(
                    "valor_relacion_origen: {}".format(valor_relacion_origen)
                )

                self.actualizar_mapeado(
                    tbl_destino,
                    llaveRelacionDestino,
                    campos,
                    registro_origen,
                    valor_relacion_origen,
                    tipoOperacion,
                    usarGeometria
                )

                # Para obtener el valor de la llave Primaria Destino
                where = DataAccess.getWhereClause(
                    llaveRelacionDestino, valor_relacion_origen
                )
                registros_destino = self.destino_da.query(
                    tbl_destino, [llaveRelacionDestino,
                                  llavePrimariaDestino], where
                )
                if len(registros_destino) if registros_destino != None else 0 == 1:
                    valor_pk_destino = registros_destino[0][llavePrimariaDestino]
                    if llaveEsGuid:
                        valor_pk_destino = "{}".format(valor_pk_destino)

                    #Actualizar Relaciones Destino
                    ToolboxLogger.debug("Procesando Relaciones Destino")
                    ToolboxLogger.debug(
                        "valor_pk_destino: {}".format(valor_pk_destino)
                    )
                    self.actualizarRelacionesDestino(
                        mapeo, registro_origen, valor_pk_destino
                    )

                    # Actualizar Relaciones Origen
                    ToolboxLogger.debug("Procesando Relaciones Origen")
                    valor_pk_origen = registro_origen[llavePrimariaOrigen]
                    ToolboxLogger.debug(
                        "valor_pk_origen: {}".format(valor_pk_origen)
                    )

                    self.actualizarRelacionesOrigen(
                        mapeo, registro_origen, valor_pk_origen, valor_pk_destino
                    )

                elif len(registros_destino) > 1:
                    ToolboxLogger.debug(
                        "Error de Integridad Refencial: {}".format(destino)
                    )

                self.actualizarRegistroOrigen(tbl_origen, llavePrimariaOrigen, registro_origen)

        ToolboxLogger.info("")

        ToolboxLogger.info("-".ljust(ancho, "-"))
        cuenta_total = 0
        errores = 0

        for tabla in self.estadisticas.tablasEstadisticas:
            ToolboxLogger.info(pattern.format(tabla,
                self.estadisticas.obtenerTotalEstadisticasTabla(tabla, "C"),
                self.estadisticas.obtenerTotalEstadisticasTabla(tabla, "U"),
                self.estadisticas.obtenerTotalEstadisticasTabla(tabla, "NU"),
                self.estadisticas.obtenerTotalEstadisticasTabla(tabla, "E"),
                self.estadisticas.obtenerTotalEstadisticasTabla(tabla, "T")))

        cuenta_total = self.estadisticas.obtenerTotalEstadisticas("T")
        errores = self.estadisticas.obtenerTotalEstadisticas("E")

        ToolboxLogger.info("-".ljust(ancho, "-"))
        ToolboxLogger.info(self.timer.stopTimer("Tiempo Total: "))
        
        ToolboxLogger.info("Total Creados        : {}".format(self.estadisticas.obtenerTotalEstadisticas("C")))
        ToolboxLogger.info("Total Actualizados   : {}".format(self.estadisticas.obtenerTotalEstadisticas("U")))
        ToolboxLogger.info("Total No Actualizados: {}".format(self.estadisticas.obtenerTotalEstadisticas("NU")))
        ToolboxLogger.info("Total Errores        : {}".format(errores))
        ToolboxLogger.info("Total Registros      : {}".format(cuenta_total))
        ToolboxLogger.info("Total Tablas         : {}".format(len(self.estadisticas.tablasEstadisticas)))
        ToolboxLogger.info("Total Encuestas      : {}".format(len(self.estadisticas.estadisticas)))

        if cuenta_total > 0:
            ToolboxLogger.info("Tiempo por registro  : {}".format(self.timer.timeSpan / cuenta_total))
        else :
            ToolboxLogger.info("Tiempo por registro  : {}".format(0))

        ToolboxLogger.info("-".ljust(ancho, "-"))

        return  len(datos_origen), cuenta_total, errores

