import allure


def teststep_allure_step(step_desc, request_dict, response_dict, validate_list, extract_mapping):
    @allure.step
    def request_data(**kv):
        pass

    @allure.step
    def response_data(**kv):
        pass

    def validate_allure_step(valiate_desc, validator_dict):
        @allure.step
        def validate_detail(**kv):
            pass

        @allure.step(valiate_desc)
        def assert_step(test_result):
            validate_detail(**validator_dict)

        return assert_step

    @allure.step
    def extract_values(**kv):
        pass

    @allure.step(step_desc)
    def step_function():
        request_data(**request_dict)
        response_data(**response_dict)
        with allure.step("validate_list"):
            for desc, detail, test_result in validate_list:
                validate_allure_step(desc, detail)(test_result)
        extract_values(**extract_mapping)

    step_function()

