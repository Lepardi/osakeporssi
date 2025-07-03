import db

def get_users():
    sql = "SELECT id, username FROM users"
    return db.query(sql)

