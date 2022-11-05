import os
from dotenv import load_dotenv
if os.path.exists("./.env"):
    load_dotenv()
from flask import Flask, render_template, url_for, flash, redirect, request
from sqlalchemy.ext.automap import automap_base
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from db_coms.db import DB_connector
from flask import session, flash


LOGGED_IN_USER_ID = 17

# init app and DB
app = Flask(__name__)
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["DB_URI"]
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'asdssd'
database = SQLAlchemy()
database.init_app(app)
db_connector = DB_connector()
with app.app_context():
    Base = automap_base()
    Base.prepare(database.engine, reflect=True)
    db_connector.initialize_connector(database, Base)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/browse", methods=["GET", "POST"])
def browse():
    # session["user"] = db_connector.get_user(LOGGED_IN_USER_ID).name
    session["user"] = "Jozko"
    if request.method == "POST":
        if not request.form["yearTo"] and not request.form["make"] and not request.form["yearFrom"]:
            print("Not enough arguments")
        else:
            return redirect(url_for("browse", make=request.form["make"], yfrom=request.form["yearFrom"], yto=request.form["yearTo"]))
    make = request.args.get("make", default=None, type=str) or None
    year_from = request.args.get("yfrom", default=None, type=str) or None
    year_to = request.args.get("yto", default=None, type=str) or None
    return render_template("browse.html", records=db_connector.get_all_cars(filter_make=make, filter_year_from=year_from, filter_year_to=year_to))


@app.route("/browse/<carID>", methods=["GET"])
def car_detail(carID):
    car_details = db_connector.get_car_details(carID)
    transactions = db_connector.get_car_owners(carID)
    return render_template("car.html", details=car_details, transactions=transactions)


@app.route("/transaction", methods=["GET", "POST"])
def transaction():
    if request.method == "POST":
        car_details = db_connector.get_car_details(request.form["car"])
        new_owner = db_connector.get_user_by_name(request.form["owner"])
        if not new_owner:
            flash("User does not exist!", "danger")
        else:
            db_connector.transfer_vehicle(LOGGED_IN_USER_ID, new_owner.id, car_details.id, request.form["price"])
            flash("Success! Please wait for evaluation", "success")
            return redirect(url_for("transaction"))
    user_cars = db_connector.get_user_cars(LOGGED_IN_USER_ID)
    return render_template("transaction.html", cars=user_cars)

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        action, transactionID = request.form["submit"].split("|")
        if action == "approve":
            db_connector.approve_transaction(transactionID)
        if action == "deny":
            db_connector.deny_transaction(transactionID)
        return redirect(url_for("admin"))
    
    if request.method == "GET":
        transactions = db_connector.get_all_pending_transactions()
        return render_template("admin.html", transactions=transactions)



if __name__ == '__main__':
    app.run()