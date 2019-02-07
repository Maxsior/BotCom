import MySQLdb
import logging
from config import db_info

db = None
cursor = None


def _init():
    global db, cursor
    if db is None:
        db = MySQLdb.connect(**db_info)
        cursor = db.cursor()


def get_column(data, column_name):
    struct = ['id', 'uid', 'current', 'vk', 'telegram']
    index = struct.index(column_name)
    return data[index]


def get_real_id(uid, social):
    _init()
    cursor.execute(f"SELECT {social} FROM uids WHERE uid = '{uid}'")
    return cursor.fetchone()[0]


def get_uid(real_id, social):
    _init()
    cursor.execute(f"SELECT uid FROM uids WHERE {social} = '{real_id}'")
    return cursor.fetchone()[0]


def add_user(real_id, social):
    _init()
    cursor.query(f"SELECT uid FROM uids WHERE {social} = '{real_id}'")
    if cursor.rownumber == 0:
        # TODO генерировать uid
        uid = '_new_uid_'
        cursor.execute(f"INSERT INTO uids (uid, {social}) VALUES ('{uid}', '{real_id}')")
        db.commit()
        logging.info('зарегистрирован новый пользователь')
