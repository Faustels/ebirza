from flask import Blueprint, render_template, session, redirect

mainBlueprint = Blueprint('mainBlueprint', __name__, template_folder="../templates", static_folder="../static")

@mainBlueprint.route('/pagrindinis', methods = ["GET", "POST"])
def index():
    if "user" not in session:
        return redirect("../", code = 302)
    return render_template("pagrindinis.html", user = session["user"])