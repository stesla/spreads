import os
import logging.config

import flask_migrate
import waitress

from spreads import app
from werkzeug.middleware.proxy_fix import ProxyFix

app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_host=1, x_proto=1)

with app.app_context():
    flask_migrate.upgrade()

logging.config.dictConfig({
    'version': 1,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(levelname)s:%(name)s: %(message)s',
        },
    },
    'handlers': {
        'stderr': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stderr',
            'formatter': 'default',
        },
    },
    'loggers': {
        'spreads': { 'level': 'INFO'},
    },
    'root': {
        'level': 'INFO',
        'handlers': ['stderr'],
    },
})

host = os.getenv('HOST', '0.0.0.0')
port = int(os.getenv('PORT', '5000'))

waitress.serve(app, host=host, port=port)
