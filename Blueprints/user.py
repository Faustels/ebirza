from flask import Blueprint, session, Response, request
from Services.Database.database import MySQLGet, MySQLExecute
from Models.user import User
from hashlib import sha256
import re
import random as r
from string import ascii_lowercase

userBlueprint = Blueprint('userBlueprint', __name__, template_folder="../templates", static_folder="../static")
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'


def ValidEmail(email):
    if len(email) > 100:
        return False
    if re.fullmatch(regex, email):
        return True
    return False


def RightPassword(enteredPassword, salt, hashedPassword):
    combinedHash = sha256((enteredPassword + salt).encode('utf-8')).hexdigest()
    if combinedHash == hashedPassword:
        return True
    return False


def GetRoles(data):
    ans = {"Producer": False, "Consumer": False}
    for i in data:
        if i == "Producer":
            ans["Producer"] = True
        elif i == "Consumer":
            ans["Consumer"] = True
    return ans


@userBlueprint.route('/login', methods=["POST"])
def login():
    if "user" in session:
        return Response('{"ANS":"NO", "ERROR":"Jau prisijungęs"}')
    else:
        email = request.form.get("loginMail")
        if not ValidEmail(email):
            return Response('{"ANS":"NO", "ERROR":"Blogas pašto adresas"}')

        user = MySQLGet("Select password, id, address, salt from user where email = %s", (email,))
        if len(user) == 0:
            return Response('{"ANS":"NO", "ERROR":"Naudotojas neegzistuoja"}')

        if not RightPassword(request.form.get("loginPassword"), user[0]['salt'], user[0]['password']):
            print()
            return Response('{"ANS":"NO", "ERROR":"Blogas slaptažodis"}')

        sessionUser = User(user[0]["id"], email, user[0]["address"])
        session["user"] = sessionUser

        return Response('{"ANS":"YES"}')


@userBlueprint.route('/logout', methods=["POST"])
def logout():
    if "user" in session:
        session.pop("user", None)
        return Response('{"ANS":"YES"}')
    return Response('{"ANS":"NO"}')


@userBlueprint.route('/register', methods=["POST"])
def register():
    if "user" in session:
        return Response('{"ANS":"NO", "ERROR":"Jau prisijungęs"}')
    else:
        email = request.form.get("registerMail")
        if not ValidEmail(email):
            return Response('{"ANS":"NO", "ERROR":"Blogas pašto adresas"}')

        user = MySQLGet("Select id from user where email = %s", (email,))
        if len(user) != 0:
            return Response('{"ANS":"NO", "ERROR":"Vartotojas jau egzistuoja"}')

        name = request.form.get("registerName")
        lastName = request.form.get("registerLastname")

        if len(name) > 30 or len(lastName) > 30:
            return Response('{"ANS":"NO", "ERROR":"Vardas ir pavardė gali būti tik 30 simbolių ilgio"}')

        address = request.form.get("registerAddress")

        if len(address) > 100:
            return Response('{"ANS":"NO", "ERROR":"Adresas netinka"}')

        roles = GetRoles(request.form.getlist("registerRole"))

        if not roles["Producer"] and not roles["Consumer"]:
            return Response('{"ANS":"NO", "ERROR":"Reikia pasirinkti bent vieną rolę"}')

        salt = ''.join([r.choice(ascii_lowercase) for _ in range(32)])
        password = sha256((request.form.get("registerPassword") + salt).encode('utf-8')).hexdigest()

        producerID = None
        consumerID = None

        if roles["Producer"]:
            producerID = MySQLExecute("Insert into producer(amount,price) values \n(%s, %s)",
                                      (0, 0))

        if roles["Consumer"]:
            consumerID = MySQLExecute("Insert into consumer(amount) values \n(%s)",
                                      (0,))

        userId = MySQLExecute("Insert into user(name, lastName, email, address, password, salt, producer, consumer)values \n(%s, %s, %s, %s, %s, %s, %s, %s)",
                     (name, lastName, email, address, password, salt, producerID, consumerID))

        session["user"] = User(userId, email, address)

        return Response('{"ANS": "YES"}')
