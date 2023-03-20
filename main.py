from flask import Flask, session
from flask_session import Session
import os
import sys

#Reading private configuration
if not os.path.exists("privateConfig.ini"):
    newPrivateConfigFile = open("privateConfig.ini", "w")
    newPrivateConfigFile.write("[locationAPI]\nAUTOCOMPLETE_KEY = RAKTAS_CIA")
    print("Buvo sukurtas privateConfig.ini failas, nes jis neegzistuoja. Reikia jį papildyti su privačiais geoapify raktais.")
    print("Darbas baigiamas")
    sys.exit()

import configparser
privateConfig = configparser.ConfigParser()
privateConfig.read("privateConfig.ini")
autocompleteKey = privateConfig["locationAPI"]["AUTOCOMPLETE_KEY"]
if autocompleteKey == "RAKTAS_CIA":
    print("Reikia papildyti privateConfig.ini failą su privačiais raktais.")
    print("Darbas baigiamas")
    sys.exit()

import Services.Location.autocomplete as autocomplete
autocomplete.key = autocompleteKey

# Reading configuration
config = configparser.ConfigParser()
config.read("config.ini")



app = Flask(__name__)
app.config["SECRET_KEY"] = "1"
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Database setup
from Services.Database.database import mysql

database = config["database"]

app.config['MYSQL_HOST'] = database['MYSQL_HOST']
app.config['MYSQL_USER'] = database['MYSQL_USER']
app.config['MYSQL_PASSWORD'] = database['MYSQL_PASSWORD']
app.config['MYSQL_DB'] = database['MYSQL_DB']

mysql.init_app(app)

#Request setup
from Blueprints.user import userBlueprint
app.register_blueprint(userBlueprint)



# Page setup
from Blueprints.index import indexBlueprint
app.register_blueprint(indexBlueprint)

from Blueprints.main import mainBlueprint
app.register_blueprint(mainBlueprint)

from Blueprints.orai import oraiBlueprint
app.register_blueprint(oraiBlueprint)

app.run()