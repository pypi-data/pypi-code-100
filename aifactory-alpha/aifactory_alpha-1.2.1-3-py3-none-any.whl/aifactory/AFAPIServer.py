import psycopg2
from aifactory.Authentication import AFCrypto

class AFQuery:
    crypt = None
    db = None
    cursor = None
    DUMMY_QUERY = 'select 1 from public."user" limit 1'

    def __init__(self):
        self.crypt = AFCrypto()

    def check_alive(self):
        try:
            self.cursor.execute(self.DUMMY_QUERY)
        except psycopg2.OperationalError:
            self.connect_db()
        else:
            return True
        return False

    def connect_db(self):
        db_host = os.environ.get("DB_HOST")
        db_user = os.environ.get("DB_USER")
        db_passwd = os.environ.get("DB_PASSWORD")
        db_name = os.environ.get("DB_NAME")
        self.db = psycopg2.connect(host=db_host, dbname=db_name,
                                   user=db_user, password=db_passwd, port=5432)
        self.cursor = self.db.cursor()
        # try:
        #     db_host = os.environ.get("DB_HOST")
        #     db_user = os.environ.get("DB_USER")
        #     db_passwd = os.environ.get("DB_PASSWORD")
        #     db_name = os.environ.get("DB_NAME")
        #     self.db = psycopg2.connect(host=db_host, dbname=db_name,
        #                                user=db_user, password=db_passwd, port=5432)
        #     self.cursor = self.db.cursor()
        #     return True
        # except (psycopg2.Error):
        #     return False

    def rollback(self):
        self.db.rollback()

    def close_db(self):
        self.db.commit()
        self.db.close()
        self.cursor.close()


from kafka import KafkaProducer
from json import dumps
import logging


class Topics:
    AFCONTEST_SUBMIT_PREFIX = 'afcontest.submit'
    AFCONTEST_DEFAULT_SUBMIT = 'afcontest.submit.default'


class AFPublisher:
    producer = None

    def __init__(self, bootstrap_servers='kafka.aifactory.solutions:9092',
                 value_serializer=lambda x: dumps(x).encode('utf-8'), acks=1, debug=False):
        if debug:
            logging.basicConfig(level=logging.INFO)
        self.producer = KafkaProducer(acks=acks, bootstrap_servers=bootstrap_servers,
                                      value_serializer=value_serializer)

    def publish_log(self, topic: str, log):
        self.producer.send(topic, value=log)
        self.producer.flush()

    def produce_submit(self, result, topic=Topics.AFCONTEST_DEFAULT_SUBMIT):
        self.producer.send(topic, result)
        self.producer.flush()

    def terminate(self):
        self.producer.close()

