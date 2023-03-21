from flask import Blueprint, Response, request
from Services.Location.locationAPI import GetLocations

locationAPIBlueprint = Blueprint('locationAPIBlueprint', __name__, template_folder="../templates", static_folder="../static")

@locationAPIBlueprint.route('/location/autocomplete', methods=["POST"])
def getAutocomplete():
    return Response(GetLocations(request.json.get("address")).text)
