import db

def get_users():
    sql = "SELECT id, username FROM users"
    return db.query(sql)

def get_user_id(username):
    sql = "SELECT id FROM users WHERE username = ?"
    return db.query(sql, [username])

def get_portfolio(username):
    sql = """SELECT c.name, p.amount
            FROM companies c, portfolios p, users u
            WHERE c.id = p.company_id AND u.id = p.user_id AND u.username = ? """
    return db.query(sql, [username])

def get_listed_companies(username):
    sql = """SELECT c.name
        FROM companies c
        WHERE c.owner = ? """
    return db.query(sql, [username])

def get_owned_stock_amount(username, company_id):
    sql = """SELECT p.amount
            FROM portfolios p, users u
            WHERE p.company_id = ? AND u.id = p.user_id AND u.username = ? """
    return db.query(sql, [company_id, username])
