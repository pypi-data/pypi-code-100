from gql import gql, Client#, AIOHTTPTransport, RequestsHTTPTransport # This is gql version 3
from gql.transport.requests import RequestsHTTPTransport
from loguru import logger
import base64

import pandas as pd
import sys
import json
import os
import requests
import pytz
import getpass
from time import time

from .fileimport import FileImport
from .fileImportService import FileImportService
from .automation import Automation, Scheduler
from .programming import Programming

from .utils.ut_core import Defaults, Utils
from .utils.ut_meta import Meta

class TechStack(Utils, Meta):

    def __init__(self, host:str, user:str, password:str=None, usePorts=False, copyGraphQLString:bool=None,
        logLevel:str='WARNING'):
        
        logger.remove()
        logger.add(sys.stderr, format="{level:<10} {time} {message}", level=logLevel, colorize=True)

        if os.name == 'nt': 
            logger.debug('Dectected Windows, enabling pyperclip')
        else:
            logger.debug(f"Dectected platform: {os.name}")


        if password == None:
            password = getpass.getpass('Enter password: ')

        if usePorts == False:
            tokenUrl = f'https://{host}/authn/connect/token'
            dynEndpoint = f'https://{host}/dynamic-objects/graphql/'
            automationEndpoint = f'https://{host}/automation/graphql/'
            scheduleEndpoint = f'https://{host}/schedule/graphql/'
            programmingEndpoint = f'https://{host}/programming/graphql/'
            #fileImportServiceEndpoint = f'https://{host}/programming/graphql/'
        else: 
            tokenUrl = f'http://{host}:8040/connect/token'
            dynEndpoint = f'http://{host}:8050/graphql/'
            automationEndpoint = f'http://{host}:8120/graphql/'
            scheduleEndpoint = f'http://{host}:8130/graphql/'
            programmingEndpoint = f'http://{host}:8140/graphql/'
            fileImportServiceEndpoint = f'http://{host}:7200/graphql/'

        body = {
            'client_id': 'techstack-ui',
            'grant_type': 'password',
            'username': user,
            'password': password,
            'scope': 'dynamicobjectservice'
        }

        response = requests.post(tokenUrl, body)
        try:
            response =  json.loads(response.text)
            token = response['access_token']
            logger.debug(f"Got Token: {token[:10]}...")
        except:
            logger.error(response)

        header = {
            'authorization': 'Bearer ' + token
        }

        transport =  RequestsHTTPTransport(url=dynEndpoint, headers=header, verify=True)
        self.client = Client(transport=transport, fetch_schema_from_transport=True)  
        self.accessToken = token
        self.scheme = self.client.introspection

        # Defaults:
        Utils._getDefaults()
        if copyGraphQLString != None: Defaults.copyGraphQLString = copyGraphQLString
            

        # self.timeZone = defaults['timeZone']
        # self.dateTimeFormat = defaults['dateTimeFormat']

        self.FileImport = FileImport(self.client)
        try:
            self.FileImportService = FileImportService(fileImportServiceEndpoint)
        except Exception as err:
            logger.warning(f"No FileImportService available - {err}")
        self.Automation = Automation(self.accessToken, automationEndpoint)
        self.Scheduler = Scheduler(self.accessToken, scheduleEndpoint)
        self.Programming = Programming(self.accessToken, programmingEndpoint)
  
        return

    def inventories(self, filter=None, orderBy=None, asc=True) -> pd.DataFrame:
        """
        Returns a DataFrame of existing inventories.

        Parameters:
        ----------
        fields : list
            The list of fields to be queried. Optional, defaults to 'inventoryId', 
            'fieldName', 'displayName' and 'variant'.
        filter : str
            Optional, defaults to None. Use a string to add filter criteria like
            'variant eq "BASIC"'
        orderBy : str
            Select a field to sort by. Defaults to None, sorting items by changedate.
        asc : bool
            Determines the sort order of items. Defaults to True (items sorted in 
            ascending order). If set to False, a descending order is applied.

        Examples:
        >>> getInventories()
        >>> getInventories(fields=['name', 'inventoryId'], 
                filter='fieldName contains "test"', 
                orderBy='variant', asc=True)
        """

        fields = ['name', 'inventoryId', 'historyEnabled', 'hasValidityPeriods', 'isDomainUserType']
        _fields = Utils._queryFields(fields)

        resolvedFilter = ''
        if filter != None: 
            resolvedFilter = Utils._resolveFilter(filter)

        if orderBy != None:
            if asc != True:
                _orderBy = f'order: {{ {orderBy}: DESC }}'
            else:
                _orderBy = f'order: {{ {orderBy}: ASC }}'
        else: _orderBy = ''

        graphQLString= f'''query getInventories {{
        inventories 
            (first: 50 {_orderBy} {resolvedFilter})
            {{
            nodes {{
                {_fields}
                }}
            }}
        }}
        '''
        result = Utils._executeGraphQL(self, graphQLString)
        if result == None: return

        df = pd.json_normalize(result['inventories']['nodes'])
        return df

    def meta_items(self, inventory, pageSize:int=250):

        start = time()

        # unwantedColumns = ['pageInfo.hasNextPage','pageInfo.hasPreviousPage','pageInfo.startCursor', 
        # 'pageInfo.endCursor', 'edges.cursor']
        inventoryItemId = ''
        allRows = []
        cursorParam = {
                        'name': f'{inventory}_pageSize',
                        'value': {pageSize}
                    }
        count = 0

        print(f"Preparation: {round(time()-start, 2)}")
        start = time()

        while True:
            graphQLString= Meta.meta

            params = {
                'topLevelField': inventory,
                'nestingLevel': 3,
                'topLevelType': '',

                'variables': [
                    {
                        'name': f'{inventory}_pageSize',
                        'value': {pageSize}
                    }
                ]   
            }

            query = gql(graphQLString)
            result = self.client.execute(query, variable_values=params)
            print(result)
            try:
                result = self.client.execute(query, variable_values=params)
                print(result)
            except Exception as err: 
                logger.error(err)
                break

            if count == 0:
                Utils._copyGraphQLString(graphQLString)
                params['variables'].append(cursorParam)
            count += 1

            rows = result['meta']['query']['dynamicItem']['result']['grid']['rows']
            #cursor = rows[0]['values'][3]['stringValue']

            allRows += rows

            if len(rows) != pageSize: break
            
        columns = result['meta']['query']['dynamicItem']['result']['grid']['columns']

        data = []

        for row in allRows:
            _row = []
            for i in row['values']:
                for j in i.values():
                    _row.append(j)
            data.append(_row)

        cols = [column['path'] for column in columns]

        df = pd.DataFrame(data, columns=cols)

        # try:
        #     df = df.drop(unwantedColumns, axis=1)
        # except:
        #     print("Warning: deletion of paging columns failed.")
        #     return df

        print(f"Transform result to Dataframe: {round(time()-start, 2)}")
        return df

    def items(self, inventoryName:str, references=False, fields:list=None, filter:str=None, pageSize:int=500,
        orderBy=None, asc=True) -> pd.DataFrame:
        """
        Queries items of all inventory variants. Provide a list of properties you want to 
        retrieve, for referenced items or subfields use sublists. A sublist must be 
        placed right behind the node.

        Parameters:
        -----------
        inventoryName : str
            The name of the inventory.
        fields : list
            A list of all properties you want to query. Defaults to all poperties.
        pageSize : int
            The page ize of items that is used to retrieve a large number of items.
        filter : str
            Use a string to add filter criteria like
            'method eq "average" and location contains "Berlin"'.
            Defaults to None. 
        orderBy : str
            Select a field to sort by. Defaults to None.
        asc : bool
            Determines the sort order of items. Defaults to True (items sorted in 
            ascending order). If set to False, a descending order is applied.

        Example 1 (Time Series items):
        >>> getItems('MeterData', 
                ['att1', 'att2', 'att3', 'resolution', ['timeUnit', 'factor'], 'unit'], 
                filter='att2 eq "L3"')
                )

        Example 2 (default items with order):
        >>> getItems('defaultTest', ['inventoryItemId', 'changeDate', 'orderNr', 'dateTime'], 
                filter='orderNr lte 150 and orderNr gt 30', orderBy='orderNr', asc=False,
                resultAsDict=False)
        """


        # tz = globalTimeZone

        if fields != None:
            _fields = Utils._queryFields(fields, recursive=True)
        else:
            properties = Utils._properties(self, inventoryName, recursive=True)
            properties = Utils._propertyList(properties)
            
            _fields = Utils._queryFields(properties, recursive=references)

        if len(_fields) == 0:
            logger.error(f"Inventory '{inventoryName}' not found.")
            return

        resolvedFilter = ''
        if filter != None: 
            resolvedFilter = Utils._resolveFilter(filter)
        
        if orderBy != None:
            if asc != True:
                _orderBy = f'order: {{ {orderBy}: DESC }}'
            else:
                _orderBy = f'order: {{ {orderBy}: ASC }}'
        else: _orderBy = ''

        result = []
        count = 0
        lastId = ''

        while True:
            graphQLString= f''' query getItems {{
                    {inventoryName} 
                    (pageSize: {pageSize} {lastId} {resolvedFilter})
                    {{
                        edges {{
                            cursor
                            node {{
                                {_fields}
                            }}
                        }}
                    }}
                }}
                '''
            query = gql(graphQLString)

            if count == 0:
                Utils._copyGraphQLString(graphQLString)

            try:
                _result = self.client.execute(query)
            except Exception as err:
                logger.error(err)
                return
            
            if _result[inventoryName]['edges']:
                result += _result[inventoryName]['edges']
                count += 1
            try:
                cursor = _result[inventoryName]['edges'][-1]['node']['_inventoryItemId']
                lastId = f'lastId: "{cursor}"'
            except: 
                break

        df = pd.json_normalize(result)
        # Remove cursor columns and remove 'node' prefix
        try:
            del df['cursor']
        except: pass

        cols = [col.replace('node.','') for col in df.columns]
        df.columns = cols
        
        # for key, value in properties.items():
        #     if key in df.columns:
        #         if value == 'DateTime':
        #             df[key] = pd.to_datetime(df[key], format='%Y-%m-%dT%H:%M:%S').dt.tz_convert(tz)
        #         # if globalDateTimeFormat == 'dateTime': # Need to be fixed
        #         #     df[key] = df[key].dt.tz_localize(tz=None)
        # if 'changeDate' in df.columns:
        #     df['changeDate'] = pd.to_datetime(df['changeDate'], format='%Y-%m-%dT%H:%M:%S').dt.tz_convert(tz)
        #     if globalDateTimeFormat == 'dateTime':
        #         df['changeDate'] = df['changeDate'].dt.tz_localize(tz=None)

        return df

    def inventoryProperties(self, name, namesOnly=False):

        propertyFields = f'''
            name
            id
            type
            ... Scalar
            isArray
            nullable
            ... Reference
        '''

        graphQLString= f'''query Inventory {{
        inventory
            (inventoryName: "{name}")
            {{
            properties {{
                {propertyFields}
                }}
            }}
        }}
        fragment Scalar on IScalarProperty {{
            dataType
            }}
        fragment Reference on IReferenceProperty {{
            inventoryId
            inventoryName
        }}
        '''
        result = Utils._executeGraphQL(self, graphQLString)
        if result == None: return

        df = pd.json_normalize(result['inventory']['properties'])

        if namesOnly == True:
            return list(df['name'])
        else:
            return df

    def propertyList(self, name, references=True, dataTypes=False):
        """
        Gets a list of properties of an inventory and its referenced inventories.
        """

        if references != True:
            _properties = Utils._properties(self, inventoryName=name)
        else:
            _properties = Utils._properties(self, inventoryName=name, recursive=True)

        if dataTypes == False:
            properties = Utils._propertyList(_properties)
        else:
            properties = pd.Series(Utils._propertyTypes(_properties))

        return properties

    def addBasicItems(self, inventoryName:str, items:list) -> str:
        """
        Adds from a list of dicts new basic items and returns a dataframe
        of inventoryItemIds.

        Parameters:
        -----------
        inventoryFieldName : str
            The field name of the inventory.
        items : list
            A list of dictionaries for each item.

        Examples:
        ---------
        >>> items = [
                {
                'meterId': '86IEDD99',
                'dateTime': '2020-01-01T05:50:59Z'
                },
                {
                'meterId': '45IXZ52',
                'dateTime': '2020-01-07T15:41:14Z'
                }
            ]
        >>> addBasicItems('meterData', items)
        """
        items = Utils._propertiesToString(items)
        #_inventoryFieldName = utils._upperFirst(inventoryFieldName)

        graphQLString= f'''mutation addBasicItems {{
            create{inventoryName} (input: 
                {items}
            )
            {{
                errors {{
                    message
                }}
                    InventoryItems {{
                _inventoryItemId
                }}
            }}
        }} 
        '''
        result = Utils._executeGraphQL(self, graphQLString)
        if result == None: return

        key = f'create{inventoryName}'

        if result[key]['errors']:
            Utils._listGraphQlErrors(result, key)
        return result[key]['InventoryItems']

    def createInventory(self, name:str,  properties:list, variant:str=None, 
        propertyUniqueness:dict=None, historyEnabled:bool=False, 
        hasValitityPeriods:bool=False, isDomainUserType:bool=False) -> str:
        """
        Creates an inventory
        
        Parameter:
        ----------
        name : str
            Name of the new inventory (only alphanumeric characters allowed, 
            may not begin with a number)
        properties : list
            A list of dicts with the following mandatory keys: 
                name: str
                dataType: enum (STRING, BOOLEAN, DECIMAL, INT, LONG, DATE_TIME, 
                DATE_TIME_OFFSET)
            Optional keys:
                isArray: bool (Default = False)
                nullable: bool (Default = True)
                hasReference: bool (Default = False)
                inventoryId: str (mandatory if hasReference = True)
        variant : str
            The inventory variant.
        propertyUniqueness : list
            A list of properties lists that should be 
            unique in its combination. Items with the same property key can't be added.
        historyEnabled : bool
            If True, changes in properties will be recorded in item history.
        hasValidityPeriods : bool
            If true, a validity period can be added to the item.    

        Example:
        >>> propertyDefinitions = [
            {
                'name': 'meterId',
                'dataType': 'STRING',
                'isArray': False,
                'nullable': True,
            }]
        >>> createInventory('meterData', 'propertyDefinitions', 'TimeSeries') 
        """

        _properties = Utils._propertiesToString(properties)

        if variant != None:
            _variantId = Utils._getVariantId(self.variants(), variant) 
            logger.debug(f"Found variantId: {_variantId}")
            if type(_variantId) != str:
                logger.error(f"Variant name '{name} not found")
                return
        else: _variantId = ''

        if propertyUniqueness != None:
            _propertyUniqueness = 'propertyUniqueness: ' + Utils._uniquenessToString(propertyUniqueness)
            logger.debug(_propertyUniqueness)
        else: _propertyUniqueness = ''

        _history = 'true' if historyEnabled != False else 'false'
        _validityPeriods = 'true' if hasValitityPeriods != False else 'false'
        _domainUser = 'true' if isDomainUserType != False else 'false'
        

        
        graphQLString= f'''
        mutation createInventory {{
            createInventory (input: {{
                name: "{name}"        
                properties: {_properties}
                variantId: "{_variantId}"
                historyEnabled: {_history}
                hasValidityPeriods: {_validityPeriods}
                isDomainUserType: {_domainUser}
                {_propertyUniqueness}
                }})
            {{
            inventory {{
                inventoryId
            }}
            errors {{
                code
                message
                }}
            }}
        }}
        '''
        result = Utils._executeGraphQL(self, graphQLString)
        if result == None: return

        if result['createInventory']['errors']:
            Utils._listGraphQlErrors(result, 'createInventory')
            return
 
        return result['createInventory']['inventory']['inventoryId']

    def deleteInventory(self, name:str, force:bool=False) -> str:
        """ 
        Deletes an inventory with all its containg items. 
        
        Parameters:
        -----------
        inventoryFieldName : str
            The field name of the inventory.
        force : bool
            Use True to ignore confirmation.

        Example:
        ---------
        >>> deleteInventory('meterData', force=True)
        """

        inventory = self.inventories(filter=f'name eq "{name}"')
        
        if inventory.empty:
            raise Exception(f'Unknown inventory "{name}".')
        inventoryId = inventory.loc[0, 'inventoryId']
        logger.debug(f'_inventoryId: {inventoryId}')

        if force == False:
            confirm = input(f"Press 'y' to delete '{name}': ")

        graphQLString= f'''mutation deleteInventory {{
            deleteInventory (input:{{inventoryId: "{inventoryId}"}})
            {{ 
                errors {{ 
                    code
                    message
                }}
            }}
            }}
            '''

        if force == True: confirm = 'y'
        if confirm == 'y':
            result = Utils._executeGraphQL(self, graphQLString)
            if result == None: return
            if result['deleteInventory']['errors'] != 'None':
                Utils._listGraphQlErrors(result, 'deleteInventory')
            else: 
                logger.info(f"Inventory '{name}' successfully deleted.")
        else: return

    def variants(self) -> pd.DataFrame:
        """
            Returns a dataframe of available variants.
        """

        graphQLString= f'''query getVariants {{
        variants
            (first: 50)
            {{
            nodes {{
                name
                variantId
                }}
            }}
        }}
        '''
        result = Utils._executeGraphQL(self, graphQLString)
        if result == None: return

        df = pd.json_normalize(result['variants']['nodes'])
        return df

    def deleteItems(self, inventoryName:str, inventoryItemIds:list=None, filter=None, force=False):
        """
        Deletes inventory items from a list of inventoryItemIds or from a filter. 

        Parameters:
        -----------
        inventoryName : str
            The name of the inventory.
        items : list
            A list of inventoryItemIds that should be deleted.
        filter : str
            Filter criteria to select items that should be deleted
        force : bool
            Use True to ignore confirmation.

        Examples:
        ---------
        >>> deleteItems('meterData', filter='changeDate gt "2020-12-01"', force=True)
        >>> deleteItems('meterData', items=['ef73d6d5-d1d7-459a-b079-ec640cbb310e'])
        """

        if inventoryItemIds == None and filter == None:
            logger.error(f"No list of items and no filter were provided.")
        if inventoryItemIds != None and filter != None:
            logger.warning(f"List of items and filter were provided. Item list is used.")

        if filter != None:
            _result =self.items(inventoryName, ['inventoryItemId', 'inventoryId'], 
                filter=filter)
            if _result.empty:
                logger.info(f"The filter criteria '{filter}' led to no results.")
                return

            _inventoryItemIds = list(_result['_inventoryItemId'])
            
        if inventoryItemIds != None:
            _inventoryItemIds = inventoryItemIds
            #_inventoryItemIds = json.dumps(items)

        _ids = ''
        for id in _inventoryItemIds:
            _ids += f'{{_inventoryItemId: "{id}"}}\n'    
      
        logger.debug(f"GraphQL Ids: {_ids}")
            
        
        if force == False:
            confirm = input(f"Press 'y' to delete  {len(_inventoryItemIds)} items: ")

        graphQLString= f'''
            mutation deleteItems {{
                delete{inventoryName} ( input: 
                    [{_ids}]
                )
                {{
                errors {{
                    code
                    message
                    }}
                }}
            }}
            '''
        

        if force == True: confirm = 'y'
        if confirm == 'y':
            result = Utils._executeGraphQL(self, graphQLString)
            if result == None: return
        else:
            return

        if result[f'delete{inventoryName}']['errors'] != None:
            Utils._listGraphQlErrors(result, f'delete{inventoryName}')
        else:
            logger.info(f"{len(_inventoryItemIds)} items deleted.")


# Some stand alone functions
def setGlobalDefault(default:str, value:object, verbose:bool=False) -> None:
    """
    Sets a default value for a specific option.
    Available defaults:
    timeZone : str
        A time zone provided in IANA or isoformat (e.g. 'Europe/Berlin' or 'CET')
    dateTimeFormat: str
        Use 'dateTimeOffSet' or 'dateTime'

    Parameters:
    -----------
    default : str
        Choose a default, e.g. 'timeZone'.
    value : object
        Choose a value to be set as default.
    verbose : bool
        If True, config file information will be shown.
    """
    #global globalTimeZone, globalDateTimeFormat

    ## Check for valid defaults:
    defaults = ['timeZone', 'dateTimeFormat', 'copyGraphQLString']
    if default not in defaults:
        raise ValueError(f"Unknown default '{default}'.")

    ## Check config file and create if not existing:
    path = os.path.abspath(__file__)
    path = path.replace('core.py', 'config.json')
    if verbose: print(f"Path to config file: '{path}'")

    try:
        with open(path, 'r') as configFile:
            content = json.load(configFile)
    except:
        print('I excepted')
        with open(path, 'w') as configFile:
            content = {
                'timeZone': 'local',
                'dateTimeFormat': 'dateTimeOffset',
                'copyGraphQLString': False
                }
            json.dump(content, configFile, indent=4)
    
    ## Check for valid values:
    if default == 'timeZone':
        pytz.timezone(value)
        globalTimeZone = value
    if default == 'dateTimeFormat':
        if value not in ['dateTimeOffset', 'dateTime']:
            raise ValueError(f"'{value}' is no valid DateTime format. Use 'dateTimeOffset' or 'dateTime'")
        globalDateTimeFormat = value
    if default == 'copyGraphQLString':
        if value not in [True, False]:
            raise TypeError(f"'{value}' is not valid. Use True or False.")
    # if default == 'saveAccessToken':
    #     if value not in [True, False]:
    #         raise TypeError(f"'{value}' is not valid. Use True or False.")
    # if default == 'tokenValidityHours':
    #     if type(value) != int:
    #         raise TypeError(f"'{value}' is not valid. Use an integer number.")

    ## New content
    content[default] = value
    print(content)

    ## Write to config file:
    with open(path, 'w') as configFile:
        #content = json.load(configFile)
        if verbose: print(f"Current settings of config file: \n {content}")
        json.dump(content, configFile, indent=4)
    if verbose: print(f"{default} set to {value}.")
    return



def encodeBase64(file:str):
    with open(file) as file:
        content = file.read()
        content = base64.b64encode(content.encode('ascii'))
        return content.decode('UTF8')
        
def decodeBase43(content:str):
    return base64.b64decode(content)