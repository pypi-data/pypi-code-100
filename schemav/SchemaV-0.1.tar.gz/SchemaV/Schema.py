class Validator():

    def __init__(self, schema):
        self.__schema = schema

    def validate(self, input):
        """
        Validates an input against it's schema
        :param input: the input dict
        :return: the validated input with default values (in case)
        """
        validated_output = {}
        for _ in self.__validate(input, validated_output, self.__schema): pass
        return validated_output

    def generate(self, input):
        """
        Generates a schema from an Input, the field is mandatory when its checkIn is None
        :param input: The input dict
        :return: The corresponding Schema to be used (CheckIns to be replaced in case)
        """
        schema = {}
        for _ in self.__generate(input, schema): pass
        return schema

    def __validate_value(self, value, checkIn):
        """
        Validates a value or a structure (dict or list) using a function
        :param value: a value or a structure
        :param checkIn: the CheckIn object with function validator
        :return: the same value if it's valid, otherwise it throws an Exception
        :raises: ValueError if the value is incorrect or a SchemaError
        """

        value_validator_func = checkIn.value_validator_func()

        if value_validator_func is None:

            return value

        else:

            try:
                result = value_validator_func(value)
            except Exception as e:
                raise SchemaError("SCHEMA ERROR - An Exception occurred in the validator function: " + str(e))

            if isinstance(result, bool) and result == True:
                return value

            elif isinstance(result, bool) and result == False:
                raise ValueError("incorrect value: " + str(value))

            else:
                # result is not bool type
                raise SchemaError("SCHEMA ERROR - Validator function should return a boolean result")

    def __validate(self, input_config, validated_config, schema):
        """
        A Generator function to validate the input_config against its schema
        :param input_config:
        :param validated_config:
        :param schema:
        :return:
        """

        try:
            checkNext = schema["checkNext"]
        except:
            raise SchemaError("SCHEMA ERROR - checkNext is missing in: " + str(schema))

        if isinstance(checkNext, dict):

            if isinstance(input_config, dict):

                # check if there is an extra key in the input config that is not handled by the schema and generate error in case
                for key in input_config.keys():
                    if not key in checkNext.keys():
                        raise SpecError("SPEC ERROR - Key: " + str(key) + " in " + str(
                            input_config) + " is not recognized by the schema: " + str(checkNext))

                for key, value_schema in checkNext.items():

                    try:
                        checkIn = checkNext[key]["checkIn"]
                    except:
                        raise SchemaError(
                            "SCHEMA ERROR - Need to checkIn first and make checkNext=" + str(checkNext[key]))

                    try:
                        # if key is not found, we need to check if it is a mandatory/required key
                        input_value = input_config[key]

                        # check if it is a simple final value like int, str, float, ... and not a structure like dict or list
                        if not isinstance(input_value, dict) and not isinstance(input_value, list):

                            if not checkIn is None:

                                try:
                                    validated_config[key] = self.__validate_value(input_value, checkIn)
                                except ValueError:
                                    raise SpecError("SPEC ERROR - Key: " + str(key) + ", incorrect value: " + str(
                                        input_config[key]) + " in: " + str(input_config))
                            else:
                                validated_config[key] = input_value

                            yield input_value

                        # if input_value is a structure (dict or list)
                        else:

                            if isinstance(checkNext[key]["checkNext"], dict):
                                validated_config[key] = {}

                            elif isinstance(checkNext[key]["checkNext"], list):
                                validated_config[key] = []

                            else:
                                raise SchemaError(
                                    "SCHEMA ALGO ERROR - Structure type not recognized: " + str(type(
                                        input_value)) + ", please report the bug by sending the input and the used schema")

                            yield from self.__validate(input_value, validated_config[key], checkNext[key])

                            # validate the structure
                            try:
                                if not checkIn is None: self.__validate_value(validated_config[key], checkIn)
                            except ValueError:
                                raise SpecError("SPEC ERROR - Key: " + str(key) + ", incorrect value: " + str(
                                    validated_config[key]) + " in: " + str(validated_config))


                    # check if the key is mandatory or optional
                    except KeyError:

                        if not checkIn is None:

                            if checkIn.isRequired():
                                raise SpecError(
                                    "SPEC ERROR - Required field: " + str(key) + " not found in: " + str(input_config))

                            # insert the default value and validate it
                            else:

                                if isinstance(checkNext[key]["checkNext"], dict):

                                    next_validated_conf = {}
                                    yield from self.__validate(checkIn.default_value(), next_validated_conf,
                                                               checkNext[key])
                                    validated_config[key] = next_validated_conf

                                elif isinstance(checkNext[key]["checkNext"], list):

                                    next_validated_conf = []
                                    yield from self.__validate(checkIn.default_value(), next_validated_conf,
                                                               checkNext[key])
                                    validated_config[key] = next_validated_conf

                                else:
                                    # in case the CheckNext is the End (a None value)
                                    pass

                                try:
                                    self.__validate_value(validated_config[key], checkIn)
                                except ValueError:

                                    raise SpecError("SPEC ERROR - Key: " + str(key) + ", incorrect value: " + str(
                                        validated_config[key]) + " in: " + str(validated_config))
                        else:
                            raise SpecError(
                                "SPEC ERROR - Required field: " + str(key) + " not found in: " + str(input_config))

            else:
                raise SpecError("SPEC ERROR - Incorrect structure type: " + str(type(input_config)) + " of: " + str(
                    input_config) + ", should be: " + str(type(checkNext)))


        elif isinstance(checkNext, list):

            if isinstance(input_config, list):

                try:
                    checkIn = checkNext[0]["checkIn"]
                except:
                    raise SchemaError("SCHEMA ERROR - Need to checkIn first and make checkNext=" + str(checkNext[0]))

                if len(input_config) == 0:

                    if not checkIn is None:

                        if checkIn.isRequired():

                            raise SpecError(
                                "SPEC ERROR - Required fields in the list: " + str(input_config))
                        else:
                            # an empty list is possible in this case
                            if checkIn.default_value() is None:
                                pass
                            # use the default list structure in the schema and validate it
                            else:

                                if isinstance(checkNext[0]["checkNext"], dict):

                                    next_validated_conf = {}
                                    yield from self.__validate(checkIn.default_value(), next_validated_conf,
                                                               checkNext[0])

                                elif isinstance(checkNext[0]["checkNext"], list):
                                    next_validated_conf = []
                                    yield from self.__validate(checkIn.default_value(), next_validated_conf,
                                                               checkNext[0])

                                else:
                                    raise SchemaError(
                                        "SCHEMA ALGO ERROR - Structure type not recognized when validating the default value: " + str(
                                            type(checkNext[0][
                                                     "checkNext"])) + ", please report the bug with input value and the used schema")

                                try:
                                    self.__validate_value(next_validated_conf, checkIn)
                                except ValueError:
                                    raise SpecError("SPEC ERROR - Incorrect value: " + str(next_validated_conf))

                                validated_config.append(next_validated_conf)

                    else:
                        raise SpecError(
                            "SPEC ERROR - Required fields, list cannot be empty" + str(input_config))

                else:

                    for item in input_config:

                        try:
                            next_checkNext = checkNext[0]["checkNext"]
                        except:
                            raise SchemaError("SCHEMA ALGO ERROR - checkNext is missing in: " + str(checkNext[0]))

                        if isinstance(next_checkNext, dict):

                            new_config = {}
                            yield from self.__validate(item, new_config, checkNext[0])
                            validated_config.append(new_config)

                        elif isinstance(next_checkNext, list):

                            new_config = []
                            yield from self.__validate(item, new_config, checkNext[0])
                            validated_config.append(new_config)

                        elif isinstance(next_checkNext, type(None)):

                            validated_config.append(item)

                        else:
                            raise SchemaError(
                                "SPEC ERROR - Schema Error, please report the bug with input value and the used schema")

                        try:
                            if not checkIn is None: self.__validate_value(item, checkIn)
                        except ValueError:
                            raise SpecError("SPEC ERROR - Incorrect value: " + str(item))

            else:
                raise SpecError("SPEC ERROR - Incorrect structure: " + str(input_config))

        else:
            raise SchemaError(
                "SCHEMA ALGO ERROR - Structure type not recognized, please report the bug with the input data and the deployed schema")

    def __generate(self, input, schema):
        """
        Schema Generator function
        :param input: The input dict
        ;:param: the schema object
        :return: The corresponding Schema to be used
        """

        if isinstance(input, dict):

            if len(input) > 0:

                schema["checkIn"] = None
                schema["checkNext"] = {}

                for key in input:
                    dict_tree = {}
                    yield from self.__generate(input[key], dict_tree)
                    schema["checkNext"][key] = dict_tree

            else:
                raise SchemaError("SCHEMA GENERATION ERROR: Cannot create a schema from an empty list ")

        elif isinstance(input, list):

            schema["checkIn"] = None
            schema["checkNext"] = []

            if len(input) > 0:

                list_tree = {}
                yield from self.__generate(input[0], list_tree)
                schema["checkNext"].append(list_tree)

            else:
                raise SchemaError("SCHEMA GENERATION ERROR: Cannot create a schema from an empty list ")

        else:

            schema["checkIn"] = None
            schema["checkNext"] = None

            yield schema


class SpecError(Exception):

    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return self.message

class SchemaError(Exception):

    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return self.message
