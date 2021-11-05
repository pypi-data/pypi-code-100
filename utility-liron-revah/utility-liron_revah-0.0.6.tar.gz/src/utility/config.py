from os import environ

class Config(object):
    env: str = environ.get('ENV') or "Development"
    name: str = environ.get('NAME')
    service_type: str = environ.get('TYPE')
    db_uri: str = environ.get('DB_URI')
    elastic_url: str = environ.get('Elastic_URL') or 'localhost'
    elastic_port: str = environ.get('ELASTIC_PORT') or 9200
