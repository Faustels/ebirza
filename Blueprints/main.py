from flask import Blueprint, render_template, session, redirect
from database import mysql
import Models.user

mainBlueprint = Blueprint('mainBlueprint', __name__, template_folder="../templates", static_folder="../static")

@mainBlueprint.route('/pagrindinis', methods = ["GET", "POST"])
def index():
    if "user" not in session:
        return redirect("../", code = 302)
    return render_template("pagrindinis.html")