import logging
from datetime import datetime

import sqlalchemy
from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.orm.exc import UnmappedClassError

from pipictureframe.picdb.DbObjects import Metadata, PictureData
from pipictureframe.utils.PictureReader import PictureFile

log = logging.getLogger(__name__)

VERSION_STRING = "version"
CURRENT_DB_VERSION = 2
LAST_DB_UPDATE_KEY_STR = "last_db_update"
LAST_DB_UPDATE_FMT_STR = "%Y-%m-%d %H:%M:%S.%f"


class Database:
    def __init__(self, connection_string: str, echo=False, expire_on_commit=True):
        self.engine = sqlalchemy.create_engine(connection_string, echo=echo)
        self.connection = self.engine.connect()
        self.alchemy_metadata = sqlalchemy.MetaData(bind=self.engine)
        self.sm = sessionmaker(expire_on_commit=expire_on_commit)
        self._initialize_db_picture_mapping()
        self._initizalize_metadata_table()
        self.alchemy_metadata.create_all()
        self._create_inital_metadata_objects()
        self.version = self._get_db_version()
        self.current_session = None

    def _create_inital_metadata_objects(self):
        session = self._get_session()
        try:
            session.add(Metadata(VERSION_STRING, str(CURRENT_DB_VERSION)))
            session.add(
                Metadata(
                    LAST_DB_UPDATE_KEY_STR,
                    datetime.now().strftime(LAST_DB_UPDATE_FMT_STR),
                )
            )
            session.commit()
            log.debug("Setting up initial metadata objects successful.")
        except IntegrityError:
            log.debug("Metadata objects already set up. Probably already existing db.")
            pass
        finally:
            session.close()

    def _get_db_version(self):
        session = self._get_session()
        version_obj: Metadata = (
            session.query(Metadata).filter(Metadata.key == VERSION_STRING).one()
        )
        version = version_obj.value
        session.close()
        log.debug(f"Retrieved db version = {version}")
        return int(version)

    def _initialize_db_picture_mapping(self):
        try:
            sqlalchemy.orm.class_mapper(PictureData)
        except UnmappedClassError:  # map class as it is not yet mapped.
            pic_data_map = sqlalchemy.Table(
                "pictures",
                self.alchemy_metadata,
                Column("hash_id", String(50), primary_key=True),
                Column("absolute_path", String(256)),
                Column("mtime", Integer),
                Column("orig_date_time", DateTime),
                Column("orientation", Integer),
                Column("rating", Integer),
                Column("lat_ref", String(1)),
                Column("lat", Float),
                Column("long_ref", String(1)),
                Column("long", Float),
                Column("times_shown", Integer),
            )
            sqlalchemy.orm.mapper(PictureData, pic_data_map)

    def _initizalize_metadata_table(self):
        try:
            sqlalchemy.orm.class_mapper(Metadata)
        except UnmappedClassError:
            metadata_map = sqlalchemy.Table(
                "metadata",
                self.alchemy_metadata,
                Column("key", String(256), primary_key=True),
                Column("value", String(1024)),
            )
            sqlalchemy.orm.mapper(Metadata, metadata_map)

    def _get_session(self) -> Session:
        return self.sm()

    def set_last_update_time(
        self, update_time: datetime = None, session: Session = None
    ):
        generate_session = False if session else True
        if generate_session:
            session = self._get_session()

        update_obj = (
            Metadata(
                LAST_DB_UPDATE_KEY_STR, update_time.strftime(LAST_DB_UPDATE_FMT_STR)
            )
            if update_time
            else Metadata(
                LAST_DB_UPDATE_KEY_STR, datetime.now().strftime(LAST_DB_UPDATE_FMT_STR)
            )
        )
        session.merge(update_obj)

        if generate_session:
            session.commit()
            session.close()

    def get_last_update_time(self, session: Session = None) -> datetime:
        generate_session = False if session else True
        if generate_session:
            session = self._get_session()
        last_db_update = datetime.strptime(
            session.query(Metadata)
            .filter(Metadata.key == LAST_DB_UPDATE_KEY_STR)
            .one()
            .value,
            LAST_DB_UPDATE_FMT_STR,
        )
        if generate_session:
            session.commit()
            session.close()
        return last_db_update

    def get_all_pictures(self):
        session = self._get_session()
        res = session.query(PictureData).all()
        session.close()
        return res

    def get_filtered_pictures(self, filter_rating_below, filter_rating_above):
        session = self._get_session()
        q = session.query(PictureData)
        if filter_rating_below:
            log.info(f"Filtering for pictures with a rating >= {filter_rating_below}.")
            q = q.filter(PictureData.rating >= filter_rating_below)
        if filter_rating_above:
            log.info(f"Filtering for pictures with a rating <= {filter_rating_above}.")
            q = q.filter(PictureData.rating <= filter_rating_above)
        full_picture_list = q.all()
        log.info(f"{len(full_picture_list)} pictures loaded.")
        session.close()
        return full_picture_list

    def get_pic_by_path(self, pic_file: PictureFile, close_session=True) -> PictureData:
        session = self._setup_session()
        q = session.query(PictureData).filter(
            PictureData.absolute_path == pic_file.path
        )
        res = q.first()
        if close_session:
            self._close_session()
        return res

    def get_pic_by_hash(self, hash_id: str, close_session=True) -> PictureData:
        session = self._setup_session()
        q = session.query(PictureData).filter(PictureData.hash_id == hash_id)
        res = q.first()
        if close_session:
            self._close_session()
        return res

    def _setup_session(self):
        if not self.current_session:
            self.current_session = self._get_session()
        return self.current_session

    def _close_session(self):
        if self.current_session:
            self.current_session.close()
        self.current_session = None

    _ADD = "add"
    _MERGE = "merge"
    _DELETE = "delete"

    def _x_picture(self, action: str, pic: PictureData, close_session):
        session = self._setup_session()
        # noinspection PyBroadException
        try:
            if action == self._ADD:
                session.add(pic)
            elif action == self._MERGE:
                session.merge(pic)
            elif action == self._DELETE:
                session.delete(pic)
            session.commit()
        except Exception:
            session.rollback()
        if close_session:
            self._close_session()

    def add_picture(self, pic: PictureData, close_session=True):
        self._x_picture(self._ADD, pic, close_session)

    def merge_picture(self, pic: PictureData, close_session=True):
        self._x_picture(self._MERGE, pic, close_session)

    def delete_picture(self, pic: PictureData, close_session=True):
        self._x_picture(self._DELETE, pic, close_session)

    def close_current_session(self):
        self._close_session()

    def inc_times_shown(self, pic):
        """
        Increments the counter which counts how many times the picture has been shown.
        """
        session = self._get_session()
        pic.times_shown += 1
        session.merge(pic)
        session.commit()
        session.close()

    def close(self):
        sqlalchemy.orm.session.close_all_sessions()
        self.connection.close()
        self.engine.dispose()
        sqlalchemy.orm.clear_mappers()
