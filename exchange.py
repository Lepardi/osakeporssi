import db

def get_companies():
    sql = """SELECT name, stock_amount, last_price, owner
            FROM companies """
    return db.query(sql)

def new_listing(company_name, stock_amount, lister_name):
    sql = """INSERT INTO companies (name, stock_amount, last_price, owner) 
            VALUES (?, ?, ?, ?)"""
    db.execute(sql, [company_name, stock_amount, 0, lister_name])
    add_to_portfolio(lister_name, company_name, stock_amount)

def add_to_portfolio(username, company_name, stock_amount):
    sql = "SELECT id FROM companies WHERE name = ?" 
    company_id = db.query(sql, [company_name])

    sql = "SELECT id FROM users WHERE username = ?" 
    user_id = db.query(sql, [username])

    sql = """INSERT INTO portfolios (user_id, company_id, amount) 
            VALUES (?, ?, ?)"""
    db.execute(sql, [user_id[0]["id"], company_id[0]["id"], stock_amount])

def search(query):
    sql = """SELECT name, stock_amount, last_price, owner
             FROM companies 
             WHERE name LIKE ?"""
    return db.query(sql, ["%" + query + "%"])
