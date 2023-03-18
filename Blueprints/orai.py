from flask import Blueprint, render_template, session, redirect
from database import MySQLGet
import Models.user

oraiBlueprint = Blueprint('oraiBlueprint', __name__, template_folder="../templates", static_folder="../static")

def ToJSDictionary(data):
    ans = "const sunHours = {\n"
    for i in data:
        ans += i["name"] + ": " + str(i["sunshineHours"]) + ",\n"
    ans += "};"
    return(ans)

@oraiBlueprint.route('/orai')
def index():
    sun = MySQLGet('Select name, sunshineHours FROM county', None)
    return render_template("orai.html", sunShineDict = ToJSDictionary(sun))