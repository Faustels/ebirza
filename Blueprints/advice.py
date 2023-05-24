from flask import Blueprint, render_template, session

adviceBlueprint = Blueprint('adviceBlueprint', __name__, template_folder="../templates", static_folder="../static")

@adviceBlueprint.route('/patarimai')
def index():
    if session.get("user"):
        return render_template("advice.html", user=session["user"])
    return render_template("advice.html")
