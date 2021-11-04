
import re

class CLASS_NAME:
    """ Class to cleanup keys from schema

    LONG DESCRIPTION OF CLASS

    ATTRIBUTES:
    ATTRIBUTE1(type): Description
    ATTRIBUTE2(type): Description
    """

    def __init__(self, key = None):
        self.key = key


    def clean(self):
        """ Clean the key name
        """

        self.clean_key = self.key

        # Remove spaces
        self.clean_key = self.clean_key.strip()
        
        # convert to lowercase
        self.clean_key = self.clean_key.lower()

        # Remove special characters
        re.sub('[^A-Za-z0-9]+', '', self.clean_key)

        # Find equivalent
        self.clean_key = self.convert()




    def convert(self):
        # Find equivalent key

        key_db = {
            "firstname": "givenname",
            "lastname": "familyname"
        }

        return key_db.get(self.clean_key, self.clean_key)

