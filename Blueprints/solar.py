from flask import Blueprint, render_template, session
from Services.Database.database import MySQLGet
solarBlueprint = Blueprint('solarBlueprint', __name__, template_folder="../templates", static_folder="../static")

@solarBlueprint.route('/spinduliuote')
def index():
    return render_template("saule.html",)