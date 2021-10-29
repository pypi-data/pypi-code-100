import sys
import hashlib

if sys.version_info < (3, 6):
    import sha3

from datetime import datetime

from mdb_bp.const import CONST_SALT_BYTE_LENGTH
from mdb_bp.utils import random_bytes, bytes_to_string


class config:
    def __init__(
            self,
        username="",
        password="",
        connection_protocol="tcp",
        server_address="0.0.0.0",
        server_port=8080,
        database_name="master",
        parameters={},
    ):
        self.username = username
        self.password = password

        self.connection_protocol = connection_protocol

        self.server_address = server_address
        self.server_port    = server_port

        self.database_name = database_name

        # TODO: Update this config to include loc based stuff for timestamp testing
        # TODO: Update this config to include text encoding information
        self.parameters = parameters

    def Format(self):
        # Initialize the response
        resp = ""

        #  Check to see if the login credentials were defined
        if self.username == "" or self.passowrd == "":
            resp = "{}:{}@".format(self.username, self.passowrd,)

        # Concatenate the main portion of the string
        resp += "{}({}:{})/{}".format(
            self.connection_protocol,
            self.server_address, self.server_port,
            self.database_name,
        )

        # Add the parameters
        for key in self.parameters:
            resp += "?{}={}".format(key, self.parameters[key])
        return resp

    def get_address(self):
        return "{}:{}".format(self.server_address, self.server_port)

    def interpolate_params(self, query, params):
        # Check for valid inputs
        assert query.count("?") == len(params), \
            "the query received {} parameters, but received {}".format(query.count("?"), len(params))

        # Initialize basic variables
        params_pos = 0
        resp = ""

        # Loop through the characters in the string and fill in the parameters in params
        for char in query:
            if char == '?':
                # Grab the param
                param = params[params_pos]

                # Switch on the type of the input parameter
                if type(param) is datetime:
                    # Grab the location from the cfg and format accordingly
                    # datetime.
                    raise Exception("datetime not supported")
                # elif data_type == "json":
                #     raise Exception("json not supported")
                elif type(param) is str:
                    resp += "\"{}\"".format(param)
                elif type(param) is bytes or type(param) is bytearray:
                    if len(param) == 0:
                        resp += "[]"
                    else:
                        resp += "[{}".format(param[0])
                        for index in range(1, len(param)):
                            resp += " {}".format(param[index])
                        resp += "]"
                else:
                    resp += "{}".format(param)

                # Increment the pos
                params_pos += 1
            else:
                # Add current char to the response
                resp += char

        return resp

    def hash_password(self, password):
        """Hash a password for storing."""

        # The salt is used to prevent the use of a hash table lookup attack
        # The salt should never be less than 32 bytes
        salt = random_bytes(CONST_SALT_BYTE_LENGTH)

        # A MAC with 32 bytes of output has 256-bit security strength -- if you use at least a 32-byte-long key.
        d = hashlib.sha3_256()

        # Write the salt to the hash
        d.update(salt)

        # Write the password to the hash
        # TODO: Update encoding to reference the config
        d.update(password.encode('utf-8'))

        # Read the output of the hash
        pw_hash = d.digest()

        return salt, pw_hash