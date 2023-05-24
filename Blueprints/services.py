from flask import Blueprint, render_template, session

servicesBlueprint = Blueprint('servicesBlueprint', __name__, template_folder="../templates", static_folder="../static")

@servicesBlueprint.route('/paslaugos')
def index():
    if session.get("user"):
        return render_template("services.html", user=session["user"])
    return render_template("services.html")
