import random
import sqlite3

db = sqlite3.connect("database.db")

db.execute("DELETE FROM users")
db.execute("DELETE FROM companies")
db.execute("DELETE FROM sell_orders")
db.execute("DELETE FROM buy_orders")
db.execute("DELETE FROM portfolios")

user_count = 1000
company_count = 10**6

for i in range(1, user_count + 1):
    db.execute("INSERT INTO users (username) VALUES (?)",
               ["user" + str(i)])

for i in range(1, company_count + 1):
    lister_name = "user" + str(random.randint(1, user_count))
    lister_id = db.execute("SELECT id FROM users WHERE username = ?", [lister_name]).fetchall()[0][0]
    company_name = "company" + str(i)
    db.execute("""INSERT INTO companies (name, stock_amount, last_price, owner, industry)
                    VALUES (?, 100, 0, ?, "Teollisuus")""",
                    [company_name, lister_name])
    
    db.execute("""INSERT INTO portfolios (user_id, company_id, amount)
                    VALUES (?, ?, 100)""",
                    [lister_id, i])

    for j in range(1, 10):
        db.execute("""INSERT INTO sell_orders (seller_id, company_id, amount, price)
                   VALUEs (?, ?, 1, ?)""",
                   [lister_id, i, random.randint(1, 100)])
        db.execute("""INSERT INTO buy_orders (buyer_id, company_id, amount, price)
                   VALUEs (?, ?, 1, ?)""",
                   [lister_id, i, random.randint(1, 100)])



db.commit()
db.close()

