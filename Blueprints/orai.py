from flask import Blueprint, render_template, session, redirect
from database import mysql
import Models.user

oraiBlueprint = Blueprint('oraiBlueprint', __name__, template_folder="../templates", static_folder="../static")

@oraiBlueprint.route('/orai')
def index():
    return render_template("orai.html")