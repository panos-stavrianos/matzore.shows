from flask_cors import CORS
from flask_googlemaps import GoogleMaps
from gevent import monkey

monkey.patch_all()
from flask_socketio import SocketIO

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from app.config import Config

app = Flask(__name__, template_folder="templates")

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

app.config.from_object(Config)
GoogleMaps(app)

db = SQLAlchemy(app)

migrate = Migrate(app, db)
socketio = SocketIO(app)

from app import models
from app.routes import members, routes, shows, api, traffic, pilot, login, articles, events, categories
