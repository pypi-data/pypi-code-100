import openpyxl
import yaml

def create(args):

  # creating yaml structure
  vlocity_yaml = {}
  vlocity_yaml['projectPath'] = args['outputfolder']
  vlocity_yaml['queries'] = []

  wb = openpyxl.load_workbook(args['xlsx'])
  sheet = wb[args['excelsheet']]

  componentTypeList = []
  componentNameList = []
  index = 0

  for cell in sheet['A']:
      if cell.value and sheet['B'][index].value and cell.value != 'ComponentType':
          if 'raptor' in cell.value.lower():
              vlocity_yaml['queries'].append({'VlocityDataPackType': 'DataRaptor', 'query': 'Select Id from %vlocity_namespace%__DRBundle__c where Name = \'' +
                sheet['B'][index].value + '\' LIMIT 1'})
          if 'flex' in cell.value.lower():
              vlocity_yaml['queries'].append({'VlocityDataPackType': 'VlocityCard', 'query': 'Select id, Owner.name,Name,CreatedDate From vlocity_cmt__VlocityCard__c where Name = \'' +
                sheet['B'][index].value + '\' and id = \'' + sheet['C'][index].value + '\' LIMIT 1'})
          if 'integration' in cell.value.lower():
              vlocity_yaml['queries'].append({'VlocityDataPackType': 'IntegrationProcedure', 'query': 'Select Id, %vlocity_namespace%__Type__c, %vlocity_namespace%__SubType__c, %vlocity_namespace%__Version__c from %vlocity_namespace%__OmniScript__c where Name = \'' +
                sheet['B'][index].value + '\' and Id = \'' + sheet['C'][index].value + '\' LIMIT 1'})
          if 'omniscript' in cell.value.lower():
              vlocity_yaml['queries'].append({'VlocityDataPackType': 'OmniScript', 'query': 'Select Id, %vlocity_namespace%__Type__c,  %vlocity_namespace%__SubType__c, %vlocity_namespace%__Language__c from %vlocity_namespace%__OmniScript__c where Name = \'' +
                sheet['B'][index].value + '\' and Id = \'' + sheet['C'][index].value + '\' LIMIT 1'})
      index += 1
  print("yaml creation")
  with open(args['yaml'], 'w') as outfile:
      yaml.dump(vlocity_yaml, outfile, default_flow_style=False)
