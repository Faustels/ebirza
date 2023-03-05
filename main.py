from flask import Flask, render_template
from Blueprints.index import indexBlueprint
from Blueprints.main import mainBlueprint

app = Flask(__name__)

app.register_blueprint(indexBlueprint)
app.register_blueprint(mainBlueprint)
app.run()