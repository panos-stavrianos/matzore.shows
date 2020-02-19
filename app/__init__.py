from gevent import monkey

monkey.patch_all()
from flask import Flask
from flask_migrate import Migrate
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy

from app.config import Config

app = Flask(__name__, template_folder="templates")
app.config.from_object(Config)
db = SQLAlchemy(app)
#db = SQLAlchemy(session_options={"autoflush": False})

migrate = Migrate(app, db)
socketio = SocketIO(app)

from app import routes, models
