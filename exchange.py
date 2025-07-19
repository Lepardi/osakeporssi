import db

def get_companies():
    sql = """SELECT id, name, stock_amount, last_price, owner, industry
            FROM companies """
    return db.query(sql)

def get_company(company_id):
    sql = """SELECT id, name, stock_amount, last_price, owner, industry
            FROM companies WHERE id = ?"""
    return db.query(sql, [company_id])

def get_company_owners(company_id):
    sql = """SELECT username FROM portfolios p, users u WHERE company_id = ? AND p.user_id = u.id"""
    return db.query(sql, [company_id])

def new_listing(company_name, stock_amount, lister_name, industry):
    sql = """INSERT INTO companies (name, stock_amount, last_price, owner, industry) 
            VALUES (?, ?, ?, ?, ?)"""
    db.execute(sql, [company_name, stock_amount, 0, lister_name, industry])
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
    sql = """SELECT name, stock_amount, last_price, owner, industry
             FROM companies 
             WHERE name OR industry LIKE ?"""
    return db.query(sql, ["%" + query + "%"])

def update_company(company_id, company_name, industry):
    sql = "UPDATE companies SET name = ?, industry = ? WHERE id = ?"
    db.execute(sql, [company_name, industry, company_id])

def remove_company(company_id):
    remove_company_from_portfolio(company_id)
    sql = "DELETE FROM companies WHERE id = ?"
    db.execute(sql, [company_id])

def remove_company_from_portfolio(company_id):
    sql = "DELETE FROM portfolios WHERE company_id = ?"
    db.execute(sql, [company_id])