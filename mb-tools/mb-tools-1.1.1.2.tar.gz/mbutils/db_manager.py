from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from . import single_instance
from mbutils import settings


@single_instance
class DBManager:
    def __init__(self, db_config):
        engine_url = r'mysql+mysqldb://{}:{}@{}:3306/{}?charset=utf8'.format(db_config['user'], db_config['password'],
                                                                             db_config['host'], db_config['database'])
        print(engine_url)
        engine_setting = dict(
            echo=settings['debug'],
            echo_pool=False,
            # 这里设置7小时是为了避免mysql默认会断开超过8小时未活跃过的连接，避免"MySQL server has gone away”错误
            pool_recycle=db_config.get("idle", 5000) / 10,
            pool_size=db_config.get("max", 30)
        )

        self.engine = create_engine(engine_url, **engine_setting)
        db_maker = scoped_session(sessionmaker(bind=self.engine))
        self.db = db_maker

    def get_db(self):
        return self.db

    def get_engine(self):
        return self.engine


@single_instance
class SubDBManager:
    def __init__(self, db_config):
        engine_url = r'mysql+mysqldb://{}:{}@{}:{}/{}?charset=utf8'.format(db_config['user'], db_config['password'],
                                                                           db_config['host'],
                                                                           db_config.get('port', 3306),
                                                                           db_config['database'])
        print(engine_url)
        engine_setting = dict(
            echo=settings['debug'],
            echo_pool=False,
            # 这里设置7小时是为了避免mysql默认会断开超过8小时未活跃过的连接，避免"MySQL server has gone away”错误
            pool_recycle=db_config.get("idle", 5000) / 1000,
            pool_size=db_config.get("max", 30)
        )

        self.engine = create_engine(engine_url, **engine_setting)
        db_maker = scoped_session(sessionmaker(bind=self.engine))
        self.db = db_maker

    def get_db(self):
        return self.db

    def get_engine(self):
        return self.engine
