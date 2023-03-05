from flask import Flask, render_template
from Blueprints.index import indexBlueprint

app = Flask(__name__)

app.register_blueprint(indexBlueprint)
app.run()