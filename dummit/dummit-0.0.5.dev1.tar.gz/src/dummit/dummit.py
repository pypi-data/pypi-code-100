import os
import yaml
import time
import uuid

from dummit.secrets import SecretsSingleton

from . import factories as df
from . import tests as dt

class ConfigUninteligibleException(Exception):
    pass

class TextLogger():
    """ Simple logging helper. 
    To be expanded with HTML one or one that stores results in DB, central log service ...
       ... or some ReportPortal whatever"""
    def logTest(self,test,message):
        print (self.timestamp(),str(test),str(message))
    def logMessage(self,message):
        print (self.timestamp(),message)
    def timestamp(self):
        return time.strftime("%d/%m/%Y %H:%M:%S %Z", time.localtime())

class TestLibrary():
    def __init__(self,yaml_string:str,params_dict: dict, logger:TextLogger):
        # Set the logger so I can start logging
        self.logger = logger
        self.logger.logMessage(f"Logger Started")
        
        # Load the yaml config
        config = yaml.load(yaml_string,Loader=yaml.SafeLoader)
        self.logger.logMessage("Config Loaded") 

        # Load the secrets data (provider and location for it), initiate the SecretsSingleton
        secrets = config.get("secrets",None)
        if secrets:
            provider = secrets.get("secrets_provider","")
            params = secrets.get("secrets_params_string","")
            if provider=="" or params =="":
                raise ConfigUninteligibleException("secrets not defined well")
            self.secretsManager = SecretsSingleton()
            self.secretsManager.configure(provider,params)
            self.logger.logMessage("Secrets processed")
        else:
            self.secretsManager = None
            self.logger.logMessage("Secrets not there in config file. That is fine. Just letting you know.")
        
        # Read the yaml input
        self.name = config["name"]
        # Inputs part (tests are there within input config as well!)
        self.inputs = {}
        self.tests = []
        for input_dict in config["inputs"]:
            input = df.InputFactory.createInputFromDict(input_dict, params_dict)
            self.inputs[input.name] = input
            test_configs  = []
            # check what tests are there in config
            # this double for loop section below is ... ugly :( need some redesign when time allows. 
            if "must" in input_dict:
                for critical_test in input_dict["must"]:
                    test_configs.append({"string_with_definition":critical_test, "isCritical":True})
            if "would_be_nice_for_it_to" in input_dict: 
                for nice_to_have_test in input_dict["would_be_nice_for_it_to"]:    
                    test_configs.append({"string_with_definition":nice_to_have_test, "isCritical":False})
            # and now create the tests, both critical and not critical
            for test_config in test_configs:
                test = None
                if test_config["string_with_definition"] == "be_present":
                    test = df.TestFactory.createTestFromDict(input.name,"be_present",None,test_config["isCritical"])
                else:
                    test_type = list(test_config["string_with_definition"].keys())[0]
                    test_definition = list(test_config["string_with_definition"].values())[0]
                    test = df.TestFactory.createTestFromDict(input.name,test_type,
                                test_definition, is_critical=test_config["isCritical"])
                if test:
                    self.tests.append(test)
                else:
                    raise ConfigUninteligibleException()
                    
        # some output so I can see what was loaded    
        self.logger.logMessage(f"Inputs count: {len(self.inputs)}")            
        self.logger.logMessage(f"Tests count: {len(self.tests)}")

        # Over an out!
        self.logger.logMessage("TestLibrary Constructor completed") 

    def run(self):
        run_uuid = uuid.uuid4()
        self.logger.logMessage(f"Running '{self.name}' Run ID {run_uuid}")
        for input in self.inputs.values():
            input.testRunID = run_uuid # set the testRunID in the input so it has a reference where to store tmp files if needed
            input._df = None #invalidate any previous DataFrames being loaded
        # run all tests (forget parallel runs for now)
        for test in self.tests:
            test.status = dt.TestResult.IN_PROGRESS    
            if type(test) is dt.PresenceTest:
                test.status = self.inputs[test.inputName].runPresenceTest()
            elif type(test) is dt.FreshEnoughTest:
                test.status = self.inputs[test.inputName].runFreshEnoughTest(test)
            elif type(test) is dt.FormatTest:
                test.status = self.inputs[test.inputName].runFormatTest(test)
            elif type(test) is dt.UniquenessTest:
                test.status = self.inputs[test.inputName].runUniquenessTest(test)
            elif type(test) is dt.SumDeltaWithinLimitsTest:
                test.status = self.inputs[test.inputName].runDeltaWithinLimitsTest(test)
            else:
                raise dt.UnknownTestTypeException(type(test))
            self.logger.logTest(test,test.status)