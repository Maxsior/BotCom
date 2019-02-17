import MySQLdb
import MySQLdb.cursors
import logging
from config import db_info
import utils

db = None
cursor = None


class _StableDictCursor(MySQLdb.cursors.Cursor):
    def execute(self, query, args=None):
        try:
            super().execute(query, args)
        except (AttributeError, MySQLdb.OperationalError):
            _init(True)
            super().execute(query, args)
        return self


def _init(force=False):
    global db, cursor
    if force or db is None:
        db = MySQLdb.connect(**db_info)
        cursor = db.cursor(_StableDictCursor)


def get_id(id_, social=None):
    _init()
    if social is None:
        cursor.execute(f"SELECT id FROM uids WHERE uid = '{id_}'")
    else:
        cursor.execute(
            "SELECT id FROM uids WHERE real_id = {} and social = '{}'"
            .format(id_, social)
        )
    return cursor.fetchone()[0]


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


def get_cur_con(id_):
    _init()
    if id_ is None:
        return None
    cursor.execute(f"SELECT current FROM uids WHERE id = {id_}")
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
            "SELECT COUNT(*) FROM uids WHERE real_id = {} and social = '{}'"
            .format(id_, social)
        )
    return bool(cursor.fetchone()[0])


def add_msg(id_from, id_to, msg):
    if id_to is None:
        return False

    _init()
    cursor.execute(
        "INSERT INTO msgs (id_from, id_to, text) values ({}, {}, '{}')"
            .format(id_from, id_to, msg)
    )
    db.commit()
    return True


def add_user(real_id, social):
    _init()

    if user_exists(real_id, social):
        logging.debug(f"пользователь уже существует -- ({real_id}, {social})")
        return None

    uid = utils.generate_uid()
    cursor.execute(
        "INSERT INTO uids (uid, real_id, social) VALUES ('{}', {}, '{}')"
        .format(uid, real_id, social)
    )
    db.commit()
    logging.info('зарегистрирован новый пользователь')
    logging.debug(f"имя нового пользователя = {uid}")
    return cursor.lastrowid


def set_current(id_from, id_to):
    _init()
    cursor.execute(
        "UPDATE uids SET current = {} WHERE id = {}"
        .format(id_to, id_from)
    )
    db.commit()


def update_uid(real_id, social):
    _init()
    if user_exists(real_id, social):
        uid = utils.generate_uid()
        cursor.execute(
            "UPDATE uids SET uid = '{}' WHERE real_id = {} and social = '{}'"
            .format(uid, real_id, social)
        )
        db.commit()
        return uid


def delete_user(id_):
    _init()
    cursor.execute(f"DELETE FROM uids WHERE id = {id_}")
