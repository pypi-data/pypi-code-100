import pymongo


class Mongodb:

    def connection(self, connection_url, database_name=None):
        """
        connection function establishes a connection with mongo server

        Parameters:

        ->connection_url: connection url with password
        database_name(optional): name of the database
        """

        # Establishing a connection with mongodb
        try:
            self.client_cloud = pymongo.MongoClient(connection_url)
            if database_name is not None:
                self.database = self.client_cloud[database_name]
            print(self.client_cloud.test)
        except Exception as e:
            print(f"Error : {str(e)}")

    def create_database(self, database_name):
        """
        create_database function helps to create a new database

        Parameters:

        ->database_name: name of the database
        """

        # Creating a database
        try:
            self.database = self.client_cloud[database_name]
            print(f"{database_name}  database created")
        except Exception as e:
            print(f"Error : {str(e)}")

    def available_database(self):
        """
        available_database function returns list of all the existing database
        """

        # Checking existing database
        print(self.client_cloud.list_database_names())

    def create_collection(self, collection_name):
        """
        Function create_collection is used to create a new collection
        Parameters:

        ->collection_name: name of the collection
        """
        try:
            self.database[collection_name]
            print(f"{collection_name}  collection created")
        except Exception as e:
            print(f"Error : {str(e)}")

    def insert(self, collection_name, record):
        """
        Insert function is used to insert value in the table

        Parameters:

        ->collection_name: name of the collection
        ->record: data to be inserted
            -to insert one record datatype should be dictionary
            -to insert many record datatype should be list
        """
        try:
            if type(record) == dict:
                collection = self.database[collection_name]
                collection.insert_one(record)
            if type(record) == list:
                collection = self.database[collection_name]
                collection.insert_many(record)
            print(f"Record inserted")
        except Exception as e:
            print(f"Error : {str(e)}")

    def find(self, collection_name):
        """
        find function is used find all the records in a collection

        Parameters:

        ->collection_name: name of the collection
        """
        try:
            collection = self.database[collection_name]
            for i in collection.find():
                print(i)
        except Exception as e:
            print(f"Error : {str(e)}")

    def update(self, collection_name, present_record, new_record):
        """
        update function is used to alter/update the record

        Parameters:

        ->collection_name: collection name
        ->present_record: existing record
            -datatype as dict
        ->new_record: new record
            -datatype as dict
        """
        try:
            collection = self.database[collection_name]
            if type(new_record) == dict and type(present_record) == dict:
                collection.update_one(present_record, {"$set": new_record})
                print(f"Record Updated")
        except Exception as e:
            print(f"Error : {str(e)}")

    def delete(self, collection_name, query):
        """
        delete function is used to delete record from collection

        Parameters:

        ->collection_name: name of the collection
        ->query: any condition in that particular record
            -datatype as dictionary
        """
        try:
            collection = self.database[collection_name]
            if type(query) == dict:
                collection.delete_one(query)
                print(f"Record deleted")
        except Exception as e:
            print(f"Error : {str(e)}")

    def drop_collection(self, collection_name):
        """
        drop_collection function is used to drop the collection

        Parameters:

        ->collection_name: name of the collection
        """
        try:
            collection = self.database[collection_name]
            collection.drop()
        except Exception as e:
            print(f"Error : {str(e)}")
