from dummit.inputs import AzureBlobInput, LocalFileInput, VersionedLocalFileInput
from dummit.tests import PresenceTest,FreshEnoughTest,FormatTest, UniquenessTest, SumDeltaWithinLimitsTest
from dummit.locations import ExactLocation, VersionedByDateAzureBlobLocation, VersionedByDateLocalFileLocation

class UnknownInputTypeException(Exception):
    pass

class UnknownTestTypeException(Exception):
    pass

class UnknownLocationTypeException(Exception):
    pass

class InputFactory():
    @staticmethod
    def createInputFromDict(data_dict: dict, params_dict:dict):
        input_type = data_dict.get("input_type")
        if input_type == "local_file":
            return LocalFileInput(data_dict, params_dict)
        elif input_type == "local_versioned_file":
            return VersionedLocalFileInput(data_dict,params_dict)
        elif input_type == "azure_blob":
            return AzureBlobInput(data_dict, params_dict)
        else:
            raise UnknownInputTypeException(input_type)

class TestFactory():
    @staticmethod
    def createTestFromDict(input_name,test_type, test_definition, is_critical=False):
        if test_type=="be_present":
            return PresenceTest(input_name,is_critical) # test definition is a dummy here 
        elif test_type=="be_modified_at_least_x_hours_ago":
            return FreshEnoughTest(input_name,test_definition,is_critical)
        elif test_type=="be_well_formated":
            return FormatTest(input_name,test_definition,is_critical)
        elif test_type=="have_no_duplicates_for_a_key_of":
            return UniquenessTest(input_name,test_definition,is_critical)
        elif test_type=="have_sum_delta_within_limits":
            return SumDeltaWithinLimitsTest(input_name,test_definition,is_critical)
        else:
            raise UnknownTestTypeException(test_type)

class LocationFactory():
    @staticmethod
    def createLocationFromDict(input,data_string):
        values = data_string.split(",")
        location_type = values[0].replace(" ","")
        location_value = values[1].replace(" ","")
        if location_type=="exact":
            return ExactLocation(location_value) # this one takes no params (i.e. run_date)
        elif location_type=="versioned_by_date":
            if input.type=="local_file":
                return VersionedByDateLocalFileLocation(input.params,location_value) 
            elif input.type=="azure_blob":
                return VersionedByDateAzureBlobLocation(input.params,location_value) 
            else:
                raise UnknownLocationTypeException(f"{input.type}, {location_type}")
        else:
            raise UnknownLocationTypeException(f"{input.type}, {location_type}")