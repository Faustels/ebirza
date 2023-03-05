from flask import Blueprint, render_template

indexBlueprint = Blueprint('indexBlueprint', __name__, template_folder="../templates", static_folder="../static")

@indexBlueprint.route('/')
def index():
    return render_template("index.html")