from flask import Blueprint, render_template, session, redirect, request, Response
from Services.Database.database import MySQLGet

mainBlueprint = Blueprint('mainBlueprint', __name__, template_folder="../templates", static_folder="../static")

@mainBlueprint.route('/pagrindinis')
def index():
    if "user" not in session:
        return redirect("../", code = 302)
    return render_template("pagrindinis.html", user = session["user"])
@mainBlueprint.route('/pagrindinis/getOffers')
def getData():
    if "user" not in session:
        return redirect("../../", code=302)
    if "price" not in request.args or "amount" not in request.args:
        return [None]

    try:
        float(request.args.get("price"))
        int(request.args.get("amount"))
    except ValueError:
        return [None]

    price = float(request.args.get("price"))
    amount = int(request.args.get("amount"))

    res = MySQLGet("select name, lastName, price, amount from producer inner join user on user.producer = producer.id" +
                          " where price > 0 and amount > 0 and price < %s and amount < %s", (price, amount))

    if len(res) == 0:
        return [None]

    result = []
    for user in res:
        tempRes = {}
        tempRes["name"] = user["name"] + " " + user["lastName"]
        tempRes["price"] = user["price"]
        tempRes["amount"] = user["amount"]
        result.append(tempRes)

    return result
