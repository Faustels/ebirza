from flask import Blueprint, session, Response, request
from database import MySQLGet
from Models.user import User
from hashlib import sha256
import re

userBlueprint = Blueprint('userBlueprint', __name__, template_folder="../templates", static_folder="../static")
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'


def ValidEmail(email):
    if re.fullmatch(regex, email):
        return True
    return False

def RightPassword(enteredPassword, salt, hashedPassword):
    combinedHash = sha256((enteredPassword + salt).encode('utf-8')).hexdigest()
    if combinedHash == hashedPassword: return True
    return False

@userBlueprint.route('/login', methods=["POST"])
def login():
    if "user" in session:
        return Response('{"ANS":"NO", "ERROR":"Jau prisijungęs"}')
    else:
        email = request.form.get("loginMail")
        if not ValidEmail(email):
            return Response('{"ANS":"NO", "ERROR":"Blogas pašto adresas"}')

        user = MySQLGet("Select password,id, address, salt from user where email = \"" + email + "\"")

        if len(user) == 0:
            return Response('{"ANS":"NO", "ERROR":"Naudotojas neegzistuoja"}')

        if not RightPassword(request.form.get("loginPassword"), user[0]['salt'], user[0]['password']):
            print()
            return Response('{"ANS":"NO", "ERROR":"Blogas slaptažodis"}')

        sessionUser = User(user[0]["id"], email, user[0]["address"])
        session["user"] = sessionUser

        return Response('{"ANS":"YES"}')
