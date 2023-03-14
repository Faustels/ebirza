from flask import Blueprint, render_template, request, session, redirect
from database import MySQLGet
from Models.user import User
import MySQLdb.cursors

indexBlueprint = Blueprint('indexBlueprint', __name__, template_folder="../templates", static_folder="../static")

@indexBlueprint.route('/')
def index():
    if request.method == "GET":
        return render_template("index.html")
