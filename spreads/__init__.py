import os

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(
    __name__,
    instance_path=os.getenv('FLASK_INSTANCE_PATH'),
    instance_relative_config=True,
)
app.config.from_object('spreads.default_settings')
app.config.from_pyfile('config.py', silent=True)
app.config.from_envvar('FLASK_SETTINGS', silent=True)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

import spreads.models
import spreads.routes
import spreads.auth
