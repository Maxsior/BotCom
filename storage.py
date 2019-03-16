import MySQLdb
import MySQLdb.cursors
import logging
from config import db_info
import utils
from social import vk


class _StableCursor(MySQLdb.cursors.Cursor):
    def execute(self, query, args=None):
        try:
            super().execute(query, args)
        except MySQLdb.OperationalError as e:
            if e.args[0] not in (2006, 2013):
                raise e

            _init(True)
            cursor.execute(query, args)
        return self


db: MySQLdb.Connection = None
cursor: _StableCursor = None


def _init(force=False):
    global db, cursor
    if force or db is None:
        db = MySQLdb.connect(**db_info)
        cursor = db.cursor(_StableCursor)


def get_name(id_):
    cursor.execute("SELECT name FROM uids WHERE id = %s", (id_,))
    result = cursor.fetchone()
    if result is not None:
        return result[0]
    else:
        return None


def get_id(id_, social=None):
    if social is None:
        cursor.execute("SELECT id FROM uids WHERE uid = %s", (id_,))
    else:
        cursor.execute(
            "SELECT id FROM uids WHERE real_id = %s and social = %s",
            (id_, social)
        )

    result = cursor.fetchone()
    if result is not None:
        return result[0]
    else:
        return None


def get_real_id(id_):
    cursor.execute("SELECT real_id, social FROM uids WHERE id = %s", (id_,))
    return cursor.fetchone()


def get_uid(id_):
    cursor.execute("SELECT uid FROM uids WHERE id = %s", (id_,))
    if cursor.rowcount == 0:
        return None
    else:
        return cursor.fetchone()[0]


def get_cur_con(id_):
    if id_ is None:
        return None
    cursor.execute("SELECT current FROM uids WHERE id = %s", (id_,))
    return cursor.fetchone()[0]


def user_exists(id_, social=None):
    if social is None:
        cursor.execute(
            "SELECT COUNT(*) FROM uids WHERE uid = %s",
            (id_,)
        )
    else:
        cursor.execute(
            "SELECT COUNT(*) FROM uids WHERE real_id = %s and social = %s",
            (id_, social)
        )
    return bool(cursor.fetchone()[0])


def get_msgs(id_from, id_to):
    cursor.execute(
        "SELECT text FROM msgs WHERE id_from = %s and id_to = %s",
        (id_from, id_to)
    )

    msgs = tuple(map(lambda msg: msg[0], cursor.fetchall()))

    cursor.execute(
        "DELETE FROM msgs WHERE id_from = %s and id_to = %s",
        (id_from, id_to)
    )
    db.commit()

    return msgs


def get_others(id_to):
    if id_to is None:
        return ()
    cursor.execute("SELECT name, uid FROM uids WHERE current = %s", (id_to,))
    return cursor.fetchall()


def add_msg(id_from, id_to, msg):
    if id_to is None:
        return False

    cursor.execute(
        "INSERT INTO msgs (id_from, id_to, text) values (%s, %s, %s)",
        (id_from, id_to, msg)
    )
    db.commit()
    return True


def add_user(real_id, social, name, nick):
    if user_exists(real_id, social):
        logging.debug(f"пользователь уже существует -- ({real_id}, {social})")
        return None

    uid = utils.generate_uid()

    cursor.execute(
        "INSERT INTO uids (uid, real_id, social, name, nick)"
        "VALUES (%s, %s, %s, %s, %s)",
        (uid, real_id, social, name, nick)
    )
    db.commit()
    logging.info('зарегистрирован новый пользователь')
    logging.debug(f"имя нового пользователя = {uid}")
    return cursor.lastrowid


def set_current(id_from, id_to):
    cursor.execute(
        "UPDATE uids SET current = %s WHERE id = %s",
        (id_to, id_from)
    )
    db.commit()


def update_uid(real_id, social):
    if user_exists(real_id, social):
        uid = utils.generate_uid()
        cursor.execute(
            "UPDATE uids SET uid = %s WHERE real_id = %s and social = %s",
            (uid, real_id, social)
        )
        db.commit()
        return uid


def delete_user(id_):
    cursor.execute("DELETE FROM uids WHERE id = %s", (id_,))
    db.commit()


_init()
