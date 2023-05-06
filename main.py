from flask import Flask
from flask_session import Session
import os
import sys
from Services.Price.PriceController import SetData, SetHour
from datetime import datetime

#Temporary for now
SetHour(datetime.now().hour)
SetData()

#Reading private configuration
if not os.path.exists("privateConfig.ini"):
    newPrivateConfigFile = open("privateConfig.ini", "w")
    newPrivateConfigFile.write("[locationAPI]\nLOCATION_KEY = RAKTAS_CIA")
    print("Buvo sukurtas privateConfig.ini failas, nes jis neegzistuoja. Reikia jį papildyti su privačiais geoapify raktais.")
    print("Darbas baigiamas")
    sys.exit()

import configparser
privateConfig = configparser.ConfigParser()
privateConfig.read("privateConfig.ini")
locationKey = privateConfig["locationAPI"]["LOCATION_KEY"]
if locationKey == "RAKTAS_CIA":
    print("Reikia papildyti privateConfig.ini failą su privačiais raktais.")
    print("Darbas baigiamas")
    sys.exit()

import Services.Location.locationAPI as location
location.key = locationKey

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

from Blueprints.locationAPI import locationAPIBlueprint
app.register_blueprint(locationAPIBlueprint)

from Blueprints.assistant import assistantBlueprint
app.register_blueprint(assistantBlueprint)


# Page setup
from Blueprints.index import indexBlueprint
app.register_blueprint(indexBlueprint)

from Blueprints.main import mainBlueprint
app.register_blueprint(mainBlueprint)

from Blueprints.orai import oraiBlueprint
app.register_blueprint(oraiBlueprint)

from Blueprints.price import priceBlueprint
app.register_blueprint(priceBlueprint)

from Blueprints.solar import solarBlueprint
app.register_blueprint(solarBlueprint)


if __name__ == "__main__":
    app.run()