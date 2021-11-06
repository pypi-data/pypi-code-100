import json
import uuid
import datetime
import dateutil.parser

from entity.schema_org import Schema_org
from entity import normalize as n

class Observation:
    """ SHORT DESCRIPTION OF CLASS

    LONG DESCRIPTION OF CLASS

    ATTRIBUTES:
        record_type: the '@type' of the observed entity
        record_id: the '@id' of the observed entity
        key (str): The name of the field (key)
        value (tbd): The value of the field
        credibility(float): the credibility score (0 to 1)
        date(datetime): the date of the Observation
        observation_id (string): the id of the observation (uuid if blank)
        datasource (string): the system or source of the data
    
    """



    """
    Class operators override
    """

    def __init__(self, record_type = None, record_id = None, key = None, value = None, **kwargs):
        """ Initialization of class
        """

        if not kwargs.get('observation_id', None):
            observation_id = str(uuid.uuid4())

        self.record_type = record_type
        self.record_id = record_id
        self.key = key
        self.value = value
        self.credibility = kwargs.get('credibility',  kwargs.get('c', None))
        self.date = kwargs.get('date', kwargs.get('d', None))
        self.observation_id = observation_id
        self.datasource = kwargs.get('datasource', kwargs.get('ds', None))

        # Clean up data
        self._normalize_key()
        self._normalize_value()





    def __str__(self):
        return json.dumps(self._record(), default=str, indent = 4)

    def __repr__(self):
        return str(self._record())

    def _record(self): 
        record = {
            "@type": "schema:observation",
            "@id": self.observation_id,
            "object": {
                "@type": self.record_type,
                "@id": self.record_id,
                },
            "key": self.key,
            "value": self.value,
            "credibility": self.credibility,
            "date": self.date, 
            "datasource": self.datasource
        }

        return record

    @property
    def record(self):
        return self._record()

    def _same_entity(self, other):
        """Verifies if it is same entity
        """

        if not self.record_type == other.record_type:
            return False

        if not self.record_id == other.record_id:
            return False

        return True

    def _same_key(self, other):
        """ Verifies if same entity and same key
        """

        if not self._same_entity(other):
            return False
        
        if not self.key == other.key:
            return False

        return True


    def __eq__(self, other):
        """Determines equality between two observations

        Two observations are equal if it meets the following conditions:
            same type
            same id
            same key
            same value
            same credibility
            same datasource
            same date
            
        """

        if not self._same_key(other):
            return False

        if not self.value == other.value:
            return False

        if not self.credibility == other.credibility:
            return False

        if not self.datasource == other.datasource:
            return False

        if not self.date == other.date:
            return False

        return True



    def __ne__(self, other):

        if not self._same_key(other):
            return False

        if self.__eq__(other):
            return False
        else:
            return True


    def __gt__(self, other):
        """ Determines if self if greater than other
        Greater is determined with the following condition in this order:
            credibility
            date

        """

        if not self._same_key(other):
            return False

        if self.credibility and other.credibility and self.credibility > other.credibility:
            return True

        elif self.date and other.date and self.date > other.date: 
            return True

        else:
            return False

    def __ge__(self, other):
        
        if not self._same_key(other):
            return False

        if self.__eq__(other):
            return True
        elif self.__gt__(other):
            return True
        else:
            return False

    def __lt__(self, other):
        # Greater if cred is higher or date is higher

        if not self._same_key(other):
            return False

        if self.credibility and other.credibility and self.credibility < other.credibility:
            return True

        elif self.date and other.date and self.date < other.date: 
            return True

        else:
            return False

    def __le__(self, other):
        
        if not self._same_key(other):
            return False

        if self.__eq__(other):
            return True
        elif self.__lt__(other):
            return True
        else:
            return False

    def dump(self):
        # Return json version of the object
        return self.record

    def load(self, record):
        # Load json to object

        obj = record.get('object', {})

        self.record_type = obj.get('@type', None)  
        self.record_id = obj.get('@id', None)

        self.key = record.get('key', {})
        self.value = record.get('value', {})

        self.credibility = record.get('credibility', {})

        date_data = record.get('date', None)
        if date_data:
            self.date = dateutil.parser.parse(date_data)
        
        self.datasource = record.get('datasource', {})

        return



    """
    Properties
    """


    @property
    def measuredProperty(self):
        return self.key
    
    @property
    def measuredValue(self):
        return self.value

    @property
    def observedNode(self):
        return self.record_id

    @property
    def observationDate(self):
        return self.date

    @property
    def marginOfError(self):
        return self.credibility


    """
    Methods
    """
    def update_record_id(self, record_type, old_record_id, new_record_id):
        """Update the record id and/or associated links
        """

        # update links if exists
        old_link = {'@type': record_type, '@id': old_record_id}
        new_link = {'@type': record_type, '@id': new_record_id}

        if self.value == old_link:
            self.value = new_link

        # update self if needed
        if self.record_type == record_type and self.record_id == old_record_id:
            self.record_id = new_record_id

        return


    """
    Data 
    """

    @property
    def schema(self):
        # Returns dict following schema.org

        record = {
            '@type': 'schema:observation',
            '@id': self.observation_id,
            'schema:observedNode': self.observedNode,
            'schema:measuredProperty': self.measuredProperty,
            'schema:measuredValue': self.measuredValue,
            'schema:observationDate': self.observationDate,
            'schema:marginOfError': self.marginOfError
        }

        return record



    def is_duplicate(self, other):

        if self.__eq__(other):
            if self.value == other.value:
                return True
        
        return False
    

    """
    Data format manipulation
    """

    def _normalize_key(self):


        return 


    def _normalize_value(self):

        s = Schema_org()

        self.datatype = s.get_datatype(self.key)


        if 'schema:URL' in self.datatype:
            self.value = n.url(self.value) 

        if 'schema:DATE' in self.datatype:
            self.value = n.date(self.value) 
        
        if 'schema:email' in self.datatype:
            self.value = n.email(self.value) 



        return 

