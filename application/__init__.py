from flask import Flask
from config import Config
from flask_mongoengine import MongoEngine

app = Flask(__name__)
# pulling the config class to app
app.config.from_object(Config)

# db setup and initialization
db = MongoEngine()
db.init_app(app)

from application import routes

