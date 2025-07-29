import sqlite3
from flask import Flask
from flask import redirect, render_template, request, session
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
import config
import db
import exchange
import user

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    companies = exchange.get_companies()
    return render_template("index.html", companies = companies)

@app.route("/new_listing", methods = ["POST"])
def new_listing():

    company_name = request.form["company_name"]
    stock_amount = request.form["stock_amount"]
    industry = request.form["industry"]
    lister_name = session["username"]

    exchange.new_listing(company_name, stock_amount, lister_name, industry)
    return redirect("/")

@app.route("/new_buy_order/<int:company_id>", methods = ["POST"])
def new_buy_order(company_id):

    stock_buy_amount = request.form["stock_buy_amount"]
    buy_price = request.form["stock_buy_price"]
    user_id = user.get_user_id(session["username"])[0]["id"]

    exchange. add_buy_order(user_id, company_id, stock_buy_amount, buy_price)
    return redirect("/")

@app.route("/new_sell_order/<int:company_id>", methods = ["POST"])
def new_sell_order(company_id):

    stock_sell_amount = request.form["stock_sell_amount"]
    sell_price = request.form["stock_sell_price"]
    user_id = user.get_user_id(session["username"])[0]["id"]

    if len(user.get_owned_stock_amount(session["username"], company_id)) == 0:
        amount_of_stock_owned = 0
    else:
        amount_of_stock_owned = user.get_owned_stock_amount(session["username"], company_id)[0]["amount"]

    if int(amount_of_stock_owned) < int(stock_sell_amount):
        return "Yrität myydä " + str(stock_sell_amount) + " osaketta yrityksestä josta omistat vain " + str(amount_of_stock_owned) +" osaketta."

    exchange. add_buy_order(user_id, company_id, stock_sell_amount, sell_price)
    return redirect("/")

@app.route("/users")
def show_users():
    users = user.get_users()
    return render_template("users.html", users=users)

@app.route("/users/<string:username>")
def show_user(username):
    portfolio = user.get_portfolio(username)
    companies = user.get_listed_companies(username)
    return render_template("user.html", portfolio = portfolio,
                            username = username, companies = companies)

@app.route("/search")
def search():
    query = request.args.get("query")
    results = exchange.search(query) if query else []
    return render_template("search.html", query=query, results=results)

@app.route("/edit/<int:company_id>", methods=["GET", "POST"])
def edit_company(company_id):
    company = exchange.get_company(company_id)

    if company[0]["owner"] != session["username"]:
        abort(403)

    if request.method == "GET":
        return render_template("edit.html", company=company[0])

    if request.method == "POST":
        name = request.form["company_name"]
        industry = request.form["industry"]
        exchange.update_company(company[0]["id"], name, industry)
        return redirect("/")

@app.route("/remove/<int:company_id>", methods=["GET", "POST"])
def remove_company(company_id):
    company = exchange.get_company(company_id)
    if company[0]["owner"] != session["username"]:
        abort(403)

    if request.method == "GET":
        owners = exchange.get_company_owners(company_id)
        if session["username"] == owners[0]["username"] and len(owners) == 1:
            return render_template("remove.html", company=company[0])
            
        else:
            return "Et voi poistaa yritystä jonka osakkeita on myös muiden hallussa!"
        
    if request.method == "POST":
        if "continue" in request.form:
            exchange.remove_company(company[0]["id"])
            return redirect("/")
        return redirect("/")


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return "VIRHE: salasanat eivät ole samat"
    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        return "VIRHE: tunnus on jo varattu"

    return "Tunnus luotu"

@app.route("/login", methods=["POST", "GET"])
def login():

    if request.method == "GET":
        return render_template("login.html")
    
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        sql = "SELECT password_hash FROM users WHERE username = ?"
        password_hash = db.query(sql, [username])[0][0]

        if check_password_hash(password_hash, password):
            session["username"] = username
            return redirect("/")
        else:
            return "VIRHE: väärä tunnus tai salasana"

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

