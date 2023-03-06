from flask import Flask
from flask_session import Session

app = Flask(__name__)
app.config["SECRET_KEY"] = "1"
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Reading configuration
import configparser
config = configparser.ConfigParser()
config.read("config.ini")

# Database setup
from database import mysql

database = config["database"]

app.config['MYSQL_HOST'] = database['MYSQL_HOST']
app.config['MYSQL_USER'] = database['MYSQL_USER']
app.config['MYSQL_PASSWORD'] = database['MYSQL_PASSWORD']
app.config['MYSQL_DB'] = database['MYSQL_DB']

mysql.init_app(app)

# Page setup
from Blueprints.index import indexBlueprint
app.register_blueprint(indexBlueprint)

from Blueprints.main import mainBlueprint
app.register_blueprint(mainBlueprint)
app.run()