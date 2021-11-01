from entity.observation import Observation
import json
import uuid
from tabulate import tabulate
import os

import entity.kraken_json as kr_json


class Observations:
    """ Class to store and manage Observation.

    Converts and manage schema records into series of observations to manage credibility. 

    ATTRIBUTES:
    record_ids (list): Returns all the record_ids present in storage
    keys (list): Returns all the keys present in storage

    
    METHODS:
        Entity:
            dump (list): Returns list of observations in dict form
            load (None): Ingest a list of observations in dict form into observations
            
        I/O
            save (Bool): Saves given object
            load (bool): Load given object
        
    """

    def __init__(self):
        """ Initialization of class
        """
        self._observations = []


    """
    Class operators override
    """

    def __repr__(self):


        return self._record()

    

    def __str__(self):

        return json.dumps(self._record(), indent = 4, default = str)


    def _record(self):
        data = []

        for i in self._observations:
            data.append(i._record()) 

        return data

    def _valid(self, obs):
        # Checks if observation is of class observation

        if not isinstance(obs, Observation):
            return False
        else: 
            return True



    def __eq__(self, other):

        test_equal = True

        for i in self._observations:
            if i not in other:
                test_equal = False

        for i in other._observations:
            if i not in self:
                test_equal = False

        return test_equal



    def __ne__(self, other):

        if self.__eq__(other):
            return False
        else: 
            return True


    def __contains__(self, other):

        for i in self._observations:

            if other.is_duplicate(i):
                return True
        
        return False
                
    
    def __getitem__(self, key):

        return self.get(key)

    def __len__(self):

        return len(self._observations)

    def __bool__(self):

        return len(self._observations) > 0

    def __add__(self, other):
        """Add 2 observations object
        """
        new_obs = Observations()

        for i in self._observations:
            if i not in new_obs:
                new_obs.post_observation(i)

        if isinstance(other, Observation): 
            new_obs.post_observation(other)

        elif isinstance(other, Observations): 

            for i in other._observations:
                if i not in new_obs:
                    new_obs.post_observation(i)

        return new_obs

    def __ipost_observation__(self, other): 
        
        if isinstance(other, Observation): 
            self.post_observation(other)

        for i in other._observations:
            if i not in self:
                self.post_observation(i)
        return self


    def __sub__(self, other):

        new_obs = Observations()

        for i in self._observations:
            if i not in new_obs:
                new_obs.post_observation(i)

        if isinstance(other, Observation): 
            new_obs.remove(other)

        elif isinstance(other, Observations): 
            for i in other._observations:
                new_obs.remove(i)

        return self





    """
    Class Properties
    """
    @property
    def record_ids(self):
        # Retrieve list of all record_ids 
        
        values = []

        for i in self._observations:
            if i.record_id not in values:
                values.append(i.record_id)

        values = sorted(values, key = lambda i: (i.get('record_type', None), i.get('record_id', None)))

        return values
        
    def keys(self, record_type = None, record_id = None):
        # Returns list of keys for a given object if record-id. Else returns all keys.

        keys = []
        for i in self._observations:
            if i.key not in keys:
                if i.record_type == record_type or record_type == None:
                    if i.record_id == record_id or record_id == None:
                        keys.append(i.key)

        return sorted(keys)



    """""""""""""""""""""""""""""""""""""""
    Class APIs
    """""""""""""""""""""""""""""""""""""""

    """
    Observations
    """

    def get(self, record_type = None, record_id = None, key = None):
        # Return observations for a given key

        if key:
            return self.get_observations(record_type, record_id, key)
        else:
            return self.get_entity(record_id, key)


    def get_observations(self, record_type, record_id, key):
        # Return observations for a given key

        obs = []
        for i in self._observations:
            if i.record_type == record_type and i.record_id == record_id and i.key == key:
                obs.append(i)
        
        obs.sort(reverse=True)
        return obs


    def get_min(self, record_type, record_id, key):
        # Return minimum observation for given object and key

        values = self.get_observations(record_type, record_id, key)

        if len(values) > 0:
            value = values[-1]
        else:
            value = None

        return value

    def get_max(self, record_type, record_id, key):
        # Return maximum observation for given object and key
        
        values = self.get_observations(record_type, record_id, key)

        if len(values) > 0:
            value = values[0]
        else:
            value = None

        return value


    def post_observation2(self, observation):
        return self.post_observation(observation)

    def post_observation2(self, observation):
        return self.post_observation(observation)

    def post_observation(self, observation):
        # post_observation an observation to the list

        if isinstance(observation, list): 
            for o in observation:
                self.post_observation(o)
            return

        # Check integrity
        if not self._valid(observation):
            return False

        # Check if already in list
        if self.__contains__(observation):
            return True

        # post_observation to list
        self._observations.append(observation)

        return True





    def remove2(self, observation):

        return self.delete_observation(observation)


    def delete_observation(self, observation):
        # Remove observation

        new_observations = []

        for i in self._observations:
            if not i.is_duplicate(observation):
                new_observations.append(i)

        self._observations = new_observations

        return

    def update_record_id(self, record_type, old_record_id, new_record_id):
        """Change the record_id and all references to this record_id
        Useful when a record has uuid as record_id and then it is later found.
        """
        for i in self._observations:
            i.update_record_id(record_type, old_record_id, new_record_id)
            
        return

    """
    Entities
    """



    def get_entity(self, record_type, record_id):
        # Return all observations for a given object

        observations = []

        for key in self.keys(record_type, record_id):
            observations += self.get_observations(record_type, record_id, key)

        return observations



    def delete_entity(self, record_id):
        # Removes all observations for a given object

        observations = self.get_entity(record_id)

        for i in observations:
            self.delete_observation(i)

        return


    def dump(self, record_type, record_id):
        """Dump the object into json list
        """

        obs = self.get_entity(record_type, record_id)

        values = []
        for i in obs:
            values.append(i.dump())

        return values



    def load(self, observations):
        """Load observations in json into storage
        """
        for i in observations:
            o = Observation()
            o.load(i)
            self.post_observation(o)
        return
    
    
    
    # 
    # JSON
    #


    def get_json_entity(self, record_type, record_id, expanded = False, full = False):
        """Retrieve an object and format as dict
        """

        record = {
            '@type': record_type,
            '@id': record_id
        }

        # Get values for each keys
        for k in self.keys(record_type, record_id):
            value = self.get_json_value_from_key(record_type, record_id, k, expanded, full)
            if value:
                record[k] = value

        return record



    def post_json_entity(self, record_type = None, record_id = None, key = None, value = None, credibility = None, date = None):
        """Load a json entity into storage
        """

        values = kr_json.flatten(value)

        for value in values:
            observation = Observation(
                value.get('@type', record_type),
                value.get('@id', record_id), 
                value.get('key', key),
                value.get('value', None),
                credibility,
                date)

            self.post_observation(observation)

        return




    def get_json_value_from_key(self, record_type, record_id, key, expanded = False, full = False):
        """Return observations for a key as json
        
        Args:
            expanded: returns nested records as well
            full: returns observations schemas
        
        Returns:
            list of observations dict
        
        """

        values = []
        full_values = []

        obs = self.get_observations(record_type, record_id, key)
        
        for o in obs:

            value = o.value
            full_value = o.record

            # Retrieve object if expanded true
            if isinstance(value, dict):
                child_record_type = value.get('@type', None)
                child_record_id = value.get('@id', None)
                
                if child_record_type and child_record_id:
                    
                    if expanded == True:
                        value = self.get_json_entity(child_record_type, child_record_id, expanded, full)
                        full_value['value'] = value
                    else:
                        value = {
                            '@type': child_record_type,
                            '@id': child_record_id
                        }

            # post_observation
            if value not in values:
                values.append(value)
                full_values.append(full_value)

        # Convert back from list if only one value
        if len(values) == 0:
            values = None
            full_values = None
        elif len(values) == 1:
            values = values[0]    
            full_values = full_values[0]   

        if full == True:
            return full_values
        else:
            return values




    def json(self):
        # Exports all objects

        records = []

        for record_id in self.record_ids:

            record = self.get_json(record_id)
            records.append(record)
            
        return records


    """
    Text
    """

    def get_text_entity(self, record_type = None, record_id = None, key = None):

        records = []

        obj = self.get_entity(record_type, record_id)

        for i in obj:
            records.append(i.record)
        

        # Clean dataset
        for i in records:
            # @id
            record_id = i.get('@id', "")
            if len(record_id) > 15:
                i['@id'] = record_id[0:4] + "..." + record_id[-4:-1] 

            # Object
            obs_object = i.get('object', "")
            obs_type = obs_object.get('@type', '')
            obs_id = obs_object.get('@id', '')
            if len(obs_id) > 15:
                obs_id = obs_id[0:4] + "..." + obs_id[-4:-1] 

            i['object'] = obs_type + '/' + obs_id

            # value
            value = i.get('value', '')
            if isinstance(value, dict):
                val_object = value
                val_type = val_object.get('@type', '')
                val_id = val_object.get('@id', '')
                if len(obs_id) > 15:
                    val_id = val_id[0:4] + "..." + val_id[-4:-1] 

                i['value'] = val_type + '/' + val_id



        # Print
        dataset = records

        if len(dataset)> 0:
            header = dataset[0].keys()
            rows =  [x.values() for x in dataset]
            print(tabulate(rows, header))
        

        return


    """
    I/O
    """

    def read(self, record_type, record_id): 
        """Read an entity from file
        """
        file_path = 'data/' + record_type + '/'
        file_name = record_id + '.json'
        file_full_path = file_path + '/' + file_name

        with open(file_full_path, 'r') as f:
            data = kr_json.load(f)
        
        self.load(data)

        return



    def write(self, record_type, record_id):
        """Save an entity to file
        """
        # Save record to file

        file_path = 'data/' + record_type + '/'
        file_name = record_id + '.json'
        file_full_path = file_path + '/' + file_name

        if not os.path.exists(file_path):
            os.makedirs(file_path)

        data = self.dump(record_type, record_id)
        print(data)
        with open(file_full_path, 'w', encoding='utf-8') as f:
            kr_json.dump(data, f)
            
        return


    def write_all(self):
        """Save an entity to file
        """
        # Save record to file

        for i in self._observations:


            file_path = 'data/' + i.record_type + '/'
            file_name = i.record_id + '.json'
            file_full_path = file_path + '/' + file_name

            if not os.path.exists(file_path):
                os.makedirs(file_path)

            data = self.dump(i.record_type, i.record_id)
            print(data)
            with open(file_full_path, 'w', encoding='utf-8') as f:
                kr_json.dump(data, f)
                
        return