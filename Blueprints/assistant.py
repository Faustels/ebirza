from flask import Blueprint, Response, request
from Services.Assistant.assistant import Query

assistantBlueprint = Blueprint('assistantBlueprint', __name__, template_folder="../templates",
                               static_folder="../static")


@assistantBlueprint.route('/assistant')
def getAutocomplete():
    return Response(Query(request.args.get("text")))
