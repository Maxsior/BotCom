import MySQLdb
import logging
from config import db_info
import utils

db = None
cursor = None


def _init():
    global db, cursor
    if db is None:
        db = MySQLdb.connect(**db_info)
        cursor = db.cursor()


def get_real_id(uid):
    _init()
    cursor.execute(f"SELECT real_id, social FROM uids WHERE uid = '{uid}'")
    return cursor.fetchone()


def get_uid(real_id, social):
    _init()
    cursor.execute(
        "SELECT uid FROM uids WHERE real_id = '{}' and social = '{}'"
        .format(real_id, social)
    )
    return cursor.fetchone()[0]


def user_exists(id_, social=None):
    _init()
    if social is None:
        cursor.execute(
            "SELECT COUNT(*) FROM uids WHERE uid = '{}'"
            .format(id_)
        )
        return bool(cursor.fetchone()[0])
    else:
        cursor.execute(
            "SELECT COUNT(*) FROM uids WHERE real_id = '{}' and social = '{}'"
            .format(id_, social)
        )
        return bool(cursor.fetchone()[0])


def add_user(real_id, social):
    _init()
    if not user_exists(real_id, social):
        uid = utils.generate_uid()
        cursor.execute(
            "INSERT INTO uids (uid, real_id, social) VALUES ('{}', '{}', '{}')"
            .format(uid, real_id, social)
        )
        db.commit()
        logging.info('зарегистрирован новый пользователь')
        logging.debug(f"имя нового пользователя = {uid}")
        return True
    else:
        return False


def update_uid(real_id, social):
    _init()
    if not user_exists(real_id, social):
        uid = utils.generate_uid()
        cursor.execute(
            "UPDATE uids SET uid = '{}' WHERE real_id = '{}' and social = '{}'"
            .format(uid, real_id, social)
        )
        db.commit()
        logging.info('зарегистрирован новый пользователь')
        logging.debug(f"имя новго пользователя = {uid}")
