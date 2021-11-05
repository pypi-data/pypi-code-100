import arcpy
import codecs
import arcgis

from arcgis.gis import GIS
from arcgis import features
from arcgis import geometry
from arcgis.features import _version
from datetime import datetime

from ImportarSurvey.DataAccess import DataAccess
from ImportarSurvey.Utiles import ToolboxLogger

DEFAULT_FILTER_STRING = "1=1"

class ArcGISWFMApiDataAccess(DataAccess) :
    def __init__(self, pathConnectionFile = None) :
        DataAccess.__init__(self)

        if pathConnectionFile == None :
            self.__conn =  arcpy.wmx.Connect()
        else :
            self.__conn =  arcpy.wmx.Connect(pathConnectionFile)

    def _getJobsByUser(self, userName):
        jobsUser = self.__conn.queryJobs("JOB_ID,JOB_NAME,ASSIGNED_TO,JOB_TYPE_ID,ASSIGNED_TYPE,STATUS,STAGE, START_DATE, DUE_DATE, STARTED_DATE, END_DATE, PERC_COMPLETE","JTX_JOBS","ID,Job Name,Assigned To, Job Type, Assigned Type, Status, Stage, Start Date, Due Date, Started Date, End Date, Perc Complete ", "ASSIGNED_TO = '" + userName + "'", "JOB_NAME")
        return jobsUser
	
    def _getAssignmentsUser(self, userName):
        assignmentsUser = self.__conn.queryJobs("JOB_ID,ID_SOLICITUD, ID_TRAMITE, TIPO_TRAMITE","WMX_EC_GESTIONEDICION","ID_Job,ID_Solicitud,ID_Tramite,Tipo_Tramite", "EDITOR_ASIGNADO = '" + userName + "'", "JOB_ID")
        return assignmentsUser

    def _getRequestById(self, requestID):
        
        requestData = self.__conn.queryJobs("JOB_ID,ID_SOLICITUD, ID_TRAMITE, TIPO_TRAMITE, CEDULA_CATASTRAL, VERSION","WMX_EC_GESTIONEDICION","ID_Job,ID_Solicitud,ID_Tramite,Tipo_Tramite,Cedula_Catastral,Version", "ID_Solicitud = '" + requestID + "'", "JOB_ID")
        return requestData  

    def __find_table(self, table_name) : 
        if self.__feature_service == None:
            raise Exception("Capa o tabla '{}' no disponible.".format(table_name))
        elif self.__feature_service.layers == None:
            raise Exception("Capa o tabla '{}' no disponible.".format(table_name))

        table = [x for x in self.__feature_service.layers if x.properties["name"].lower() == table_name.lower()]

        if len(table) == 0 :
            table = [x for x in self.__feature_service.tables if x.properties["name"].lower() == table_name.lower()]

        if len(table) == 0:
            return None

        return table[0]

    def getTable(self, table_name) :
        return self.__find_table(table_name)

    def _search_da(self, table, fields, filter = None, return_geometry = True) :
        features = []

        ToolboxLogger.debug("nombre : {}".format(table.properties.name))
        ToolboxLogger.debug("filtro : {}".format(filter))
        ToolboxLogger.debug("campos : {}".format(fields))

        if filter != "" :

            if filter == None  :
                filter = DEFAULT_FILTER_STRING

            if isinstance(fields, list) :
                outFields = str.join(",", fields)
            else :
                outFields = fields

            if self.__version != None :
                gdb_version = self.__version.properties.versionName
                query = table.query(where= filter, outFields = outFields, return_geometry = return_geometry, gdb_version = gdb_version)
            else :
                query = table.query(where = filter, outFields = outFields, return_geometry = return_geometry)

            features = []
            for feature in query.features :
                f = feature.attributes
                if feature.geometry:
                    f["geometry"] = feature.geometry
                features.append(f)

        ToolboxLogger.debug("len(query)) : {}".format(len(features)))
        return features

    def _getFeature(self, record) :
        record_copy = record.copy()
        if "geometry" in record_copy:
            geo = record_copy["geometry"]
            del record_copy["geometry"]

            return features.Feature(attributes=record_copy, geometry=geometry.Geometry(geo))
        else :
            return features.Feature(attributes=record_copy)

        itemProject = self.__gis.content.get(projectID)
        project = arcgis.apps.workforce.Project(itemProject)
        return project