from flask import Blueprint, render_template, session

indexBlueprint = Blueprint('indexBlueprint', __name__, template_folder="../templates", static_folder="../static")

@indexBlueprint.route('/')
def index():
    if session.get("user"):
        return render_template("index.html", user=session["user"])
    return render_template("index.html")
