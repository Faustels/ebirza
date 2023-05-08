from flask import Blueprint, render_template, session, redirect, request
from Services.Database.database import MySQLGet, MySQLExecute
import threading

lock = threading.Lock()
moneyTaken = 0.02

mainBlueprint = Blueprint('mainBlueprint', __name__, template_folder="../templates", static_folder="../static")

@mainBlueprint.route('/pagrindinis')
def index():
    if "user" not in session:
        return redirect("../", code = 302)
    return render_template("pagrindinis.html", user = session["user"])

@mainBlueprint.route('/pagrindinis/updatePrice', methods = ["POST"])
def updatePrice():
    if "user" not in session:
        return [None]
    if session["user"].produced == None:
        return [None]

    newPrice = float(request.get_json())
    if newPrice < 0 or newPrice > 1:
        return [None]

    producer = MySQLGet("Select producer from user where id = %s", (session["user"].id,))
    MySQLExecute("update producer set price = %s where id = %s", (newPrice, producer[0]["producer"]))
    session["user"].setPrice = newPrice

    return [None]

@mainBlueprint.route('/pagrindinis/getOffers')
def getData():
    if "user" not in session:
        return [None]
    if session["user"].consumed == None:
        return [None]
    if "price" not in request.args or "amount" not in request.args:
        return [None]

    try:
        float(request.args.get("price"))
        int(request.args.get("amount"))
    except ValueError:
        return [None]

    price = float(request.args.get("price"))
    amount = int(request.args.get("amount"))

    res = MySQLGet("select name, lastName, price, amount, producer.id as id from producer inner join user on user.producer = producer.id" +
                          " where price > 0 and amount > 0 and price < %s and amount < %s", (price, amount))

    if len(res) == 0:
        return [None]

    result = []
    for user in res:
        tempRes = {}
        tempRes["name"] = user["name"] + " " + user["lastName"]
        tempRes["price"] = user["price"]
        tempRes["amount"] = user["amount"]
        tempRes["id"] = user["id"]
        result.append(tempRes)

    return result

@mainBlueprint.route('/pagrindinis/buyEnergy', methods = ["POST"])
def buyEnergy():
    if "user" not in session:
        return [None]
    if session["user"].consumed == None:
        return [None]

    lock.acquire()

    producerId = int(request.get_json())
    res = MySQLGet("select id from producer, amount, price where id = %s", (producerId,))

    if len(res) == 0:
        lock.release()
        return [None]

    amountBought = res[0]["amount"]
    price = amountBought * res[0]["price"]
    if amountBought <= 0:
        lock.release()
        return [None]

    MySQLExecute("update user set balance = balance + %s, amount = 0 where producer = %s",
                 (price - amountBought * moneyTaken, producerId))

    MySQLExecute("update user set balance = balance - %s where id = %s", (price, session["user"]["id"]))

    consumerId = MySQLGet("select consumer from user where id = %s", (session["user"]["id"],))

    MySQLExecute("update consumer set amount = amount + %s where id = %s", (amountBought, consumerId))

    lock.release()

    return [True]






