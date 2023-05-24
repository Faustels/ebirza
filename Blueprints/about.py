from flask import Blueprint, render_template, session

aboutBlueprint = Blueprint('aboutBlueprint', __name__, template_folder="../templates", static_folder="../static")

@aboutBlueprint.route('/apiemus')
def index():
    if session.get("user"):
        return render_template("about.html", user=session["user"])
    return render_template("about.html")
