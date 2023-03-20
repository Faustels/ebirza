from flask import Blueprint, Response, request
from Services.Location.autocomplete import GetAutocomplete

locationAPIBlueprint = Blueprint('locationAPIBlueprint', __name__, template_folder="../templates", static_folder="../static")

@locationAPIBlueprint.route('/locationAutocomplete', methods=["POST"])
def getAutocomplete():
    return Response(GetAutocomplete(request.json.get("address")))
