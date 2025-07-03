import db

def get_companies():
    sql = """SELECT name, stock_amount, last_price, owner
            FROM companies """
    return db.query(sql)

def new_listing(company_name, stock_amount, lister_name):
    sql = """INSERT INTO companies (name, stock_amount, last_price, owner) 
            VALUES (?, ?, ?, ?)"""
    db.execute(sql, [company_name, stock_amount, 0, lister_name])
