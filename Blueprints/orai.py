from flask import Blueprint, render_template, session
from Services.Database.database import MySQLGet
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
    if session.get("user"):
        return render_template("orai.html", sunShineDict = ToJSDictionary(sun) , user=session["user"])
    return render_template("orai.html", sunShineDict=ToJSDictionary(sun))