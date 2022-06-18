from datetime import timedelta
import os

from spreads import app

SECRET_KEY = b'pick a card'

database_path = os.path.join(app.instance_path, f'{app.env}.db')

SQLALCHEMY_DATABASE_URI = f'sqlite:///{database_path}'
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = False
