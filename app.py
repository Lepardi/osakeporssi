import sqlite3
import secrets
from flask import Flask
from flask import abort, redirect, render_template, request, session, flash, g
from werkzeug.security import generate_password_hash, check_password_hash
import config
import db
import exchange
import user
import math
import time

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
@app.route("/<int:page>")
def index(page=1):
    page_size = 5
    company_count = exchange.get_company_count()
    page_count = math.ceil(company_count / page_size)
    page_count = max(page_count, 1)

    if page < 1:
        return redirect("/1")
    if page > page_count:
        return redirect("/" + str(page_count))

    companies = exchange.get_companies(page, page_size)
    return render_template("index.html", page=page, page_count=page_count, companies=companies)

@app.route("/search")
@app.route("/search/<int:page>")
def search(page=1):
    query = request.args.get("query")
    page_size = 5
    results = exchange.search(query, page, page_size) if query else []
    company_count = exchange.get_search_row_count(query)

    page_count = math.ceil(company_count / page_size)
    page_count = max(page_count, 1)

    if page < 1:
        return redirect("/search?query="+query)
    if page > page_count:
        return redirect("/search/"+str(page_count)+"?query="+query)

    return render_template("search.html", page=page, page_count=page_count, query=query, results=results)

@app.route("/new_listing", methods = ["POST"])
def new_listing():
    check_csrf()
    company_name = request.form["company_name"]
    stock_amount = int(request.form["stock_amount"])
    industry = request.form["industry"]
    lister_name = session["username"]

    if not company_name or len(company_name ) > 100 or stock_amount > 1000000 or stock_amount < 1:
        abort(403)

    try:
        exchange.new_listing(company_name, stock_amount, lister_name, industry)
        return redirect("/")
    except sqlite3.IntegrityError:
        flash("Tämän niminen yritys on jo listattu!")
        return redirect("/")

@app.route("/new_buy_order/<int:company_id>", methods = ["POST"])
def new_buy_order(company_id):
    check_csrf()
    stock_buy_amount = int(request.form["stock_buy_amount"])
    buy_price = int(request.form["stock_buy_price"])
    user_id = user.get_user_id(session["username"])[0]["id"]

    if not buy_price or not stock_buy_amount:
        abort(403)
    if buy_price > 1000000 or buy_price < 1 or stock_buy_amount > 1000000 or stock_buy_amount < 1:
        abort(403)

    exchange.add_buy_order(user_id, company_id, stock_buy_amount, buy_price)
    return redirect("/buy_orders")

@app.route("/new_sell_order/<int:company_id>", methods = ["POST"])
def new_sell_order(company_id):
    check_csrf()
    stock_sell_amount = int(request.form["stock_sell_amount"])
    sell_price = int(request.form["stock_sell_price"])
    user_id = user.get_user_id(session["username"])[0]["id"]

    if not sell_price or not stock_sell_amount:
        abort(403)
    if sell_price > 1000000 or sell_price < 1 or stock_sell_amount > 1000000 or stock_sell_amount < 1:
        abort(403)

    if len(user.get_owned_stock_amount(session["username"], company_id)) == 0:
        amount_of_stock_owned = 0
    else:
        amount_of_stock_owned = user.get_owned_stock_amount(session["username"], company_id)[0]["amount"]

    if int(amount_of_stock_owned) < int(stock_sell_amount):
        flash("Yrität myydä " + str(stock_sell_amount) + " osaketta yrityksestä josta omistat vain " 
                + str(amount_of_stock_owned) +" osaketta.")
        return redirect("/")

    exchange.add_sell_order(user_id, company_id, stock_sell_amount, sell_price)
    return redirect("/sell_orders")

@app.route("/buy_orders")
@app.route("/buy_orders/<int:page>")
def show_buy_orders(page=1):
    page_size = 20
    buy_order_count = exchange.get_buy_order_count()
    page_count = math.ceil(buy_order_count / page_size)
    page_count = max(page_count, 1)

    if page < 1:
        return redirect("/buy_orders")
    if page > page_count:
        return redirect("/buy_orders/" + str(page_count))

    buy_orders = exchange.get_buy_orders(page, page_size)
    return render_template("buy_orders.html", buy_orders=buy_orders, page=page, page_count=page_count)

@app.route("/sell_orders")
@app.route("/sell_orders/<int:page>")
def show_sell_orders(page=1):
    page_size = 20
    sell_order_count = exchange.get_sell_order_count()
    page_count = math.ceil(sell_order_count / page_size)
    page_count = max(page_count, 1)

    if page < 1:
        return redirect("/sell_orders")
    if page > page_count:
        return redirect("/sell_orders/" + str(page_count))

    sell_orders = exchange.get_sell_orders(page, page_size)
    return render_template("sell_orders.html", sell_orders=sell_orders, page=page, page_count=page_count)

@app.route("/users")
def show_users():
    users = user.get_users()
    return render_template("users.html", users=users)

@app.route("/users/<string:username>")
def show_user(username):
    portfolio = user.get_portfolio(username)
    companies = user.get_listed_companies(username)
    sell_order_amount = user.get_user_sell_orders_amount(username)
    buy_order_amount = user.get_user_buy_orders_amount(username)
    print(buy_order_amount)
    return render_template("user.html", portfolio=portfolio,
                            username=username, companies=companies,
                            sell_order_amount=sell_order_amount,
                            buy_order_amount=buy_order_amount)

@app.route("/edit/<int:company_id>", methods=["GET", "POST"])
def edit_company(company_id):
    company = exchange.get_company(company_id)

    if company[0]["owner"] != session["username"]:
        abort(403)

    if request.method == "GET":
        return render_template("edit.html", company=company[0])

    if request.method == "POST":
        check_csrf()
        name = request.form["company_name"]
        industry = request.form["industry"]

        if not name or len(name ) > 100:
            abort(403)

        try:
            exchange.update_company(company[0]["id"], name, industry)
            return redirect("/")
        except sqlite3.IntegrityError:
            flash("Tämän niminen yritys on jo listattu!")
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
            flash("Et voi poistaa yritystä jonka osakkeita on myös muiden hallussa!")
            return redirect("/")
        
    if request.method == "POST":
        check_csrf()
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
    if not username.strip():
        flash("VIRHE: Kirjoita käyttäjätunnus.")
        return redirect("/register")
    if password1 != password2:
        flash("VIRHE: Salasanat eivät ole samat.")
        return redirect("/register")
    if not password1.strip() and not password2.strip():
        flash("VIRHE: Kirjoita salasana.")
        return redirect("/register")
    
    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        flash("VIRHE: Tunnus on jo varattu")
        return redirect("/register")

    flash("Tunnus luotu. Palaa etusivulle missä voit kirjautua sisään.")
    return redirect("/register")


@app.route("/login", methods=["POST", "GET"])
def login():

    if request.method == "GET":
        return render_template("login.html")
    
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        sql = "SELECT password_hash FROM users WHERE username = ?"
        result = db.query(sql, [username])
        if len(result) == 0:
            flash("VIRHE: Väärä tunnus tai salasana")
            return redirect("/login")
        password_hash = result[0][0]

        if check_password_hash(password_hash, password):
            session["username"] = username
            session["csrf_token"] = secrets.token_hex(16)
            return redirect("/")
        else:
            flash("VIRHE: Väärä tunnus tai salasana")
            return redirect("/login")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

def check_csrf():
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)

@app.before_request
def before_request():
    g.start_time = time.time()

@app.after_request
def after_request(response):
    elapsed_time = round(time.time() - g.start_time, 2)
    print("elapsed time:", elapsed_time, "s")
    return response