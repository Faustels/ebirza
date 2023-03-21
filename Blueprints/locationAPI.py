from flask import Blueprint, Response, request
from Services.Location.autocomplete import GetAutocomplete
import requests

locationAPIBlueprint = Blueprint('locationAPIBlueprint', __name__, template_folder="../templates", static_folder="../static")

@locationAPIBlueprint.route('/location/autocomplete', methods=["POST"])
def getAutocomplete():
    return Response(GetAutocomplete(request.json.get("address")).text)
