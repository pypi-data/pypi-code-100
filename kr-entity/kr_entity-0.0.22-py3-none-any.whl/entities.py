from entity.entity import Entity
from tabulate import tabulate

class Entities:
    """ Class to manage collections of entity

    LONG DESCRIPTION OF CLASS

    ATTRIBUTES:
    ATTRIBUTE1(type): Description
    ATTRIBUTE2(type): Description
    """

    def __init__(self, entities = []):
        """ Initialization of class
        """
        self.entities = entities


    def __len__(self):
        return len(self.entities)



    def get(self):

        return self.entities


    def get_json(self, expanded = False, full = False):

        records = []
        for i in self.entities:
            records.append(i.get_json_entity(expanded, full))

        return records

    def post(self, entities):
        """ Post a new Entity class object
        """

        if not isinstance(entities, list):
            entities = [entities]

        for e in entities:

            if isinstance(e, Entity):
                self.entities.append(e)
            else:
                self.post_json(e)
        return



    def post_json(self, records):
        """ Post a new entity in json
        """

        if not isinstance(records, list):
            records = [records]

        for r in records:
            e = Entity()
            e.post_json_entity(r)
            self.entities.append(e)
        

        return  


    def save_all(self):
        e=Entity()
        e.write_all()

    def print(self):


        records = []


        observations = []
        

        # Clean dataset
        for i in self.entities:
            observations += i.get_entity()
            
        for i in observations:
            record = {}

            record['@type'] = i.record_type
            record['@id'] = i.record_id
            record['key'] = i.key
            record['value'] = i.value
            record['cred'] = i.credibility
            record['date'] = i.date

            # format @id
            record_id = i.record_id
            if len(record_id) > 15:
                record['@id'] = record_id[0:4] + "..." + record_id[-4:-1] 


            # format value
            value = i.value
            if isinstance(value, dict):
                val_type = value.get('@type', '')
                val_id = value.get('@id', '')
                if len(val_id) > 15:
                    val_id = val_id[0:4] + "..." + val_id[-4:-1] 

                record['value'] = val_type + '/' + val_id

            records.append(record)

        # Print
        dataset = records

        if len(dataset)> 0:
            header = dataset[0].keys()
            rows =  [x.values() for x in dataset]
            print(tabulate(rows, header))
        

        return
