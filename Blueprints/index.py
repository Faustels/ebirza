from flask import Blueprint, render_template, request, session, redirect
from database import MySQLGet
from Models.user import User
import MySQLdb.cursors

indexBlueprint = Blueprint('indexBlueprint', __name__, template_folder="../templates", static_folder="../static")

@indexBlueprint.route('/', methods = ["POST", "GET"])
def index():
    if request.method == "GET":
        return render_template("index.html")
    elif request.method == "POST":
        if "loginMail" in request.form:
            temp = MySQLGet('Select * FROM user')
            tempUser = User(temp[0]['id'], temp[0]['address'])
            session['user'] = tempUser
            return redirect("/pagrindinis", code=302)
        else:
            return "LOGIN nebaigtas ivesk tik egzistuojancius"
