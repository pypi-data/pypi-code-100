import time
import json

def SayHello(name):
   return 'me'

def address_config():
   data = {
    "src" : {
      "stateprovince": {
        "folder": "stateprovince",
        "column_mappings": {},
        "transform_mappings": {},
        "filter_mappings": {}
      },
      "address": {
        "folder": "address",
        "column_mappings": {},
        "transform_mappings": {},
        "filter_mappings": {}
      }
    },
    "hub": {
      "$staging_schema.hub_address": {
        "src": "address",
        "columns": [ "postalcode", "addressline1", "addressline2" ],
        "key_name": "hkey_address"
      }
    },
    "link_satlink": {
        "$dv_schema.link_address_stateprovince": { 
            "src": {
                "name": "address"
            },
            "link_key": "link_addresshashkey",
            "record_source": "address",
            "link" : {
                "table": "link_address_stateprovince",
                "cols": [ "modifieddate", "postalcode", "addressline1", "addressline2", "addressline2", "stateprovincecode", "countryregioncode"],
                "hub_key_mappings": {
                    "hkey_address": ["postalcode", "addressline1", "addressline2" ],
                    "hkey_stateprovince": ["stateprovincecode", "countryregioncode"],
                    "hkey_address_stateprovince": [ "postalcode", "addressline1", "addressline2", "stateprovincecode", "countryregioncode"]
                },
                "final_col_list": [ "link_addresshashkey", "load_dtm", "record_source", "hkey_address", "hkey_stateprovince", "hkey_address_stateprovince"],
                "target": "link_address_stateprovince",
                "write_mode": "append"
            },
            "satlink": {
              "table": "$dv_schema.sat_address",
              "cols": [
                  "addressid",
                  "city",
                  "spatiallocation"
              ],
              "final_col_list": [
                  "link_addresshashkey",
                  "load_dtm",
                  "load_end_dtm",
                  "record_source",
                  "addressid",
                  "city",
                  "spatiallocation"
              ],
              "target": "sat_address",
              "write_mode": "append"
            }
        }
      }  
   }
   return data
