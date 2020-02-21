from flask_cors import CORS
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
db = SQLAlchemy(app)

migrate = Migrate(app, db)
socketio = SocketIO(app)

from app import routes, models
