"""
Author      : Mauricio Tabares
Author_email: matabares@netactica.com
License     : MIT
"""
import os
import pathlib
from google.cloud.storage import storage
from nos_parser.persistence_handler import PersistenceHandler


class GCSPersistence(PersistenceHandler):
    def __init__(self, blob_path, bucket_path):
        client = storage.Client()
        self.blob_path = blob_path
        self.bucket_path = bucket_path
        self.bucket=client.get_bucket(self.bucket_path);  
        
        
    def save_state(self,state):
        if storage.Blob(bucket=self.bucket, name=self.blob_path).exists(client):
            self.blob = self.bucket.get_blob(self.blob_path)
            pathlib.Path('state.bin').write_bytes(state)
            self.blob.upload_from_filename('state.bin')
            
        self.blob=self.bucket.blob(self.blob_path)
        pathlib.Path('state.bin').write_bytes(state)
        self.blob.upload_from_filename('state.bin')

    def load_state(self):
        if storage.Blob(bucket=self.bucket, name=self.blob_path).exists(client):
            self.blob = self.bucket.get_blob(self.blob_path)
            self.blob.download_to_filename('state.bin')
            return pathlib.Path('state.bin').read_bytes()

        return None
