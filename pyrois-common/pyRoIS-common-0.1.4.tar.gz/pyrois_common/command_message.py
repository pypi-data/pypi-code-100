# command_message.py
#
# Copyright 2019 Ryota Higashi

from typing import List




class MD_Identifier:  # [ISO19115]
    def __init__(self, authority: str, code: str):
        self.authority = authority  # https://www.wmo.int/schemas/wmdr/1.0RC8/documentation/schemadoc/schemas/referenceSystem_xsd/elements/authority.html
        self.code = code            # https://www.wmo.int/schemas/wmdr/1.0RC4/documentation/schemadoc/schemas/identification_xsd/elements/MD_DataIdentification.html

class RoIS_Identifier(MD_Identifier):
    def __init__(self, codebook_reference: str, version: str):
        self.codebook_reference = codebook_reference
        self.version = version



class Parameter:
    def __init__(self, name: str, data_type_ref: RoIS_Identifier, value: any):
        self.name = name                    # use="required"
        self.data_type_ref = data_type_ref  # minOccurs="1" maxOccurs="1"
        self.value = value                  # minOccurs="1" maxOccurs="1"

class ResultList:
    def __init__(self, parameters: List[Parameter]):
        self.parameters = parameters

class ArgumentList:
    def __init__(self, parameters: List[Parameter]):
        self.parameters = parameters       # minOccurs="1" maxOccurs="unbounded"

class ParameterList:
    def __init__(self, parameters: List[Parameter]):
        self.parameters = parameters

class Command_Result_Message:
    def __init__(self, command_id: str, condition: str, results: ResultList):
        self.command_id = command_id
        self.condition = condition      # QueryExpression[iso19143] = filterCondition(xml)
        self.results = results

class Query_Message:
    def __init__(self, query_type: str, condition: str, results: ResultList):
        self.query_type = query_type
        self.condition = condition
        self.results = results

class Event_Message:
    def __init__(self, event_id: str, event_type: str, subscribe_id: str, expire: str): #expire: "YYYY-MM-DDTHH:MM:SS"
        self.event_id = event_id
        self.event_type = event_type
        self.subscribe_id = subscribe_id
        self.expire = expire        

class Event_Detail_Message:
    def __init__(self, event_id: str, condition: str, results: ResultList):
        self.event_id = event_id
        self.condition = condition
        self.results = results

class Error_Message:
    def __init__(self, error_id: str, error_type: str, subscribe_id: str, expire: str):
        self.error_id = error_id
        self.error_type = error_type
        self.subscribe_id = subscribe_id
        self.expire = expire

class Error_Detail_Message:
    def __init__(self, error_id: str, condition: str, results: ResultList):
        self.error_id = error_id
        self.condition = condition
        self.results = results

###

class CommandBase:
    def __init__(self, delay_time: int):        # delay_time: int
        self.delay_time = delay_time            # use="optional"

class CommandUnitSequence:
    def __init__(self, l: List[CommandBase]): 
        self.command_unit_list = l              # minOccurs="1" maxOccurs="unbounded"

class CommandMessage(CommandBase):
    def __init__(self, component_ref: RoIS_Identifier, command_type: str, command_id: str, arguments: ArgumentList):
        self.component_ref = component_ref      # minOccurs="1" maxOccurs="1"
        self.command_type = command_type        # use="required"
        self.command_id = command_id            # use="required"
        self.arguments = arguments              # minOccurs="0" maxOccurs="1"
    
class Branch:
    def __init__(self, command_list: List[CommandMessage]):
        self.command_list = command_list        # maxOccurs=”unbounded”

class ConcurrentCommands(CommandBase):
    def __init__(self, branch_list: List[Branch]):
        self.branch_list = branch_list