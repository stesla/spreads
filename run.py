import os

import flask_migrate
import waitress

from spreads import app

with app.app_context():
    flask_migrate.upgrade()

host = os.getenv('HOST', '0.0.0.0')
port = int(os.getenv('PORT', '5000'))

waitress.serve(app, host=host, port=port)
