import os

from flask import Flask

app = Flask(
    __name__,
    instance_path=os.getenv('FLASK_INSTANCE_PATH'),
    instance_relative_config=True,
)
app.config.from_object('spreads.default_settings')
app.config.from_pyfile('config.py', silent=True)
app.config.from_envvar('FLASK_SETTINGS', silent=True)

import spreads.routes
