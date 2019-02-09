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


def get_real_id(id_):
    _init()
    cursor.execute(f"SELECT real_id, social FROM uids WHERE id = {id_}")
    return cursor.fetchone()


def get_uid(id_):
    _init()
    cursor.execute(f"SELECT uid FROM uids WHERE id = {id_}")
    if cursor.rowcount == 0:
        return None
    else:
        return cursor.fetchone()[0]


def user_exists(id_, social=None):
    _init()
    if social is None:
        cursor.execute(
            "SELECT COUNT(*) FROM uids WHERE uid = '{}'"
            .format(id_)
        )
    else:
        cursor.execute(
            "SELECT COUNT(*) FROM uids WHERE real_id = '{}' and social = '{}'"
            .format(id_, social)
        )
    return bool(cursor.fetchone()[0])


def get_id(id_, social=None):
    _init()
    if social is None:
        cursor.execute(f"SELECT id FROM uids WHERE uid = '{id_}'")
    else:
        cursor.execute(
            "SELECT id FROM uids WHERE real_id = '{}' and social = '{}'"
            .format(id_, social)
        )
    return cursor.fetchone()[0]


def get_cur_con(id_):
    _init()
    cursor.execute(f"SELECT current FROM uids WHERE id = {id_}")
    return cursor.fetchone()[0]


def add_msg(id_from, id_to, msg):
    _init()
    cursor.execute(
        "INSERT INTO msgs (id_from, id_to, text) values ({}, {}, '{}')"
        .format(id_from, id_to, msg)
    )
    db.commit()


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
        logging.debug(f"имя нового пользователя = {uid}")
