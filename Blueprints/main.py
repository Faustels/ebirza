from flask import Blueprint, render_template

mainBlueprint = Blueprint('mainBlueprint', __name__, template_folder="../templates", static_folder="../static")

@mainBlueprint.route('/pagrindinis')
def index():
    return render_template("pagrindinis.html")