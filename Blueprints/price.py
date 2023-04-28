from flask import Blueprint, render_template, request
from Services.Price.PriceController import GetData

priceBlueprint = Blueprint('priceBlueprint', __name__, template_folder="../templates", static_folder="../static")

@priceBlueprint.route("/kaina")
def index():
    return render_template("kaina.html")

@priceBlueprint.route("/kaina/getPrice", methods = ["POST"])
def price():
    mWh = float(request.get_json())
    graph, price = GetData(mWh)
    data = {"Graph" : graph, "Price" : price}
    return data