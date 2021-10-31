import os
import re
from azure.storage.blob import BlobServiceClient,  __version__
from dummit.secrets import AzureSecretsManager, SecretsSingleton

class Location:
    """parent for all locations, some will be same for all input types like ExactLocation 
    and some will need different featuers based on the location like VersionedByDateLocalFileLocation"""
    def __init__(self,location_string):
        self.location_string = location_string # here some resource identifier will end
        self._mapped = False # use for non Exact locations
    def __str__(self):
        return self.location_string
    def getLocationString(self):
        return self.location_string
    def parseAsAzureLocation(self):
        """
        sample for what I try to parse: 
            prod_blob_connection_key@playgroundblob01/dummit/demos/products_file.dev.csv
        """
        regexp = "(.+)@([^/]+)/([^/]+)/(.+)"
        m = re.search(regexp,self.getLocationString())
        return {
            "keyvault_secret_name" : m.group(1),
            "storage_account" : m.group(2),
            "storage_container" : m.group(3),
            "storage_blob" : m.group(4)
        }
    
    def parseAsSharepointLocation(self):
        raise NotImplementedError("code is not there :(")

    def mappedWell():
        return self._mapped

class ExactLocation(Location):
    """ Nothing extra here vs the base Location"""
    def mappedWell():
        return True #it is always mapped well :)

class VersionedByDateLocalFileLocation(Location):
    """ And here a 'chicken and egg' situation occurs. 
    Making 'PresenceTest' for those Locations a bit of a nonsense / repetition
    I will need to check for the file and update the location_string on the fly 
    or set it to some false value that will fail the 'PresenceTest'

    WARNING: 
        If there are is more than a single file matching the regexp, 
        it will actually not map to anything!
    """
    def __init__(self,params,location_string):
        super().__init__(location_string)
        if "yyyymmdd" in location_string:
            regexp = "(.+)/(.+)"
            m = re.search(regexp,location_string)
            path = m.group(1).replace("yyyymmdd",params["run_date"])
            file_regex = m.group(2).replace("yyyymmdd",params["run_date"])
            matches = []
            try:
                for file in os.listdir(path):
                    if re.search(file_regex,file):
                        matches.append(file)
                if len(matches)==1:
                    self.location_string = path + "/" + file  
                    self._mapped = True
                else:
                    self._mapped = False
            except: # any issues while trying to find it ... it is marked as not mapped 
                self._mapped = False
        else:
            raise NotImplementedError("only yyyymmdd timestamp is implemented as of now")

class VersionedByDateAzureBlobLocation(Location):
    def __init__(self,params,location_string):
        super().__init__(location_string)
        if "yyyymmdd" in location_string:
            self.location_string = location_string.replace("yyyymmdd",params["run_date"])
            connection_details = self.parseAsAzureLocation()
            conn_string = SecretsSingleton().getSecretValueByName(connection_details["keyvault_secret_name"])
            blob_service_client = BlobServiceClient.from_connection_string(conn_string)
            container_client = blob_service_client.get_container_client(connection_details["storage_container"])
            mask = self.getNameStartsWith()
            blobs_matching_location = list(container_client.list_blobs(mask))
            if len(blobs_matching_location)==1:
                # ugly way to get this location rewriten with the right values for the BlobInput to work
                exact_location = str(blobs_matching_location[0].name)
                connection_details = self.parseAsAzureLocation()
                self.location_string = self.location_string.replace(connection_details["storage_blob"], exact_location)            
                self._mapped = True
            else:
                self._mapped = False # no file at all or more than one file, thats not what we want
        else:
            raise NotImplementedError("only yyyymmdd timestamp is implemented as of now")
        self._mapped = False

    def getNameStartsWith(self):
        # as azure blob api allows to use "startsWith" blob filtering this is a dirty way to get
        # from a regexp that uses .* to a "startsWith" string, 
        full_blob_path = self.parseAsAzureLocation()["storage_blob"]
        position = full_blob_path.find('.*')
        result = full_blob_path[:position-1]
        return result
