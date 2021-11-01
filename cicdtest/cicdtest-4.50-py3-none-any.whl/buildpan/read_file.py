"""
    Title: read_file
    Author: Kushagra A.
    Language: Python
    Date Created: 23-09-2021
    Date Modified: 23-09-2021
    Description:
        ###############################################################
        ##   Read a file for refresh token ## 
         ###############################################################
"""

from buildpan import encrypt
import json

def read_file(path, project_id):
    enc_key = b'CgOc_6PmZq8fYXriMbXF0Yk27VT2RVyeiiobUd3DzR4='

    enc = encrypt.Encryptor()
    enc.decrypt_file(enc_key, path + f"/{project_id}.json.enc")

    with open(path + f"/{project_id}.json") as file:
        data = json.load(file)
        token = data["refresh_token"]
    
    enc.encrypt_file(enc_key, path + f"/{project_id}.json")

    return token

