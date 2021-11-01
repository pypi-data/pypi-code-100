import logging
import os
from datetime import datetime

from pipictureframe.picdb import get_db, Database
from pipictureframe.picdb.DbObjects import PictureData
from pipictureframe.utils.PictureReader import read_pictures_from_disk

log = logging.getLogger(__name__)


def update_pictures_in_db(pic_dir: str, connections_str: str):
    try:
        log.info(f"Starting update of db {connections_str} from directory {pic_dir}")
        pic_file_gen = read_pictures_from_disk(pic_dir)
        # Separate db instance created here since this runs a separate process
        db = get_db(connections_str)

        # Update needs to be executed before clean to catch moved pictures
        db_changed = _add_and_update_pics(pic_file_gen, db)
        db_changed = _clean_db(db) or db_changed
        if db_changed:
            log.debug("Changes to db detected. Updated last_db_update in db.")
            db.set_last_update_time(datetime.now())

        db.close_current_session()
    except Exception as e:
        log.fatal("Unexpected exception in picture update process.", exc_info=e)


def _clean_db(db: Database) -> bool:
    all_pics = db.get_all_pictures()
    num_deleted = 0
    for pic in all_pics:
        if not os.path.exists(pic.absolute_path):
            db.delete_picture(pic, close_session=False)
            num_deleted += 1
            log.debug(f"Deleted {pic.absolute_path} from db.")
    log.info(
        f"Checked {len(all_pics)} pictures and deleted {num_deleted} entries from db."
    )
    return num_deleted > 0


def _add_and_update_pics(pic_file_gen, db: Database) -> bool:
    num_changed = 0
    num_checked = 0
    for pic_file in pic_file_gen:
        num_checked += 1
        try:
            pic_by_path = db.get_pic_by_path(pic_file, close_session=False)
            # Is present
            if pic_by_path:
                # Has been modified
                if pic_by_path.mtime < pic_file.mtime:
                    log.debug(f"Updated timestamp detected for {pic_file.path}")
                    pic_data = PictureData.from_picture_file(pic_file)
                    pic_by_hash = db.get_pic_by_hash(
                        pic_data.hash_id, close_session=False
                    )
                    # If modified but hash has not changed
                    if pic_by_hash:
                        log.debug(
                            f"Metadata but not hash has changed for {pic_file.path}"
                        )
                        # Preserving number of times shown as picture has not changed
                        pic_data.times_shown = pic_by_hash.times_shown
                        db.merge_picture(pic_data, close_session=False)
                    # If hash has changed
                    else:
                        log.debug(f"Hash has changed for {pic_file.path}")
                        db.delete_picture(pic_by_path, close_session=False)
                        db.add_picture(pic_data, close_session=False)
                else:
                    log.debug(f"File {pic_file.path} present in db and unchanged.")
                    continue
            # If not present
            else:
                pic_data = PictureData.from_picture_file(pic_file)
                pic_by_hash = db.get_pic_by_hash(pic_data.hash_id, close_session=False)
                if pic_by_hash:
                    log.debug(
                        f"Picture has moved from {pic_by_hash.absolute_path} to {pic_data.absolute_path}"
                    )
                    # Preserving number of times shown as picture has not changed
                    pic_data.times_shown = pic_by_hash.times_shown
                    db.merge_picture(pic_data, close_session=False)
                else:
                    log.debug(f"Picture {pic_file.path} will be added to the database.")
                    db.add_picture(pic_data, close_session=False)
            num_changed += 1
        except Exception as e:
            log.error(
                f"Exception while trying to update db with {pic_file.path}.", exc_info=e
            )
    log.info(
        f"Checked {num_checked} files and {num_changed} pics added or updated to/in db."
    )
    return num_changed > 0
