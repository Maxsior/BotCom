from config import db_info
import MySQLdb


def get_real_id(uid, social):
    db = MySQLdb.connect(**db_info)
    db.query(f"SELECT {social} FROM uids WHERE uid = '{uid}'")
    result = db.use_result()
    return result.fetch_row()[0][0]
