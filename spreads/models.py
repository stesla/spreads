from sqlalchemy import event
from sqlalchemy.engine import Engine

from flask_login import UserMixin

from spreads import db

@event.listens_for(Engine, 'connect')
def set_sqlite_pragma(conn, _):
    cursor = conn.cursor()
    cursor.execute('PRAGMA foreign_keys=ON')
    cursor.close()

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    social_id = db.Column(db.String, nullable=False, unique=True)
    given_name = db.Column(db.String)
    family_name = db.Column(db.String)
    name = db.Column(db.String)
    email = db.Column(db.String)
    picture_url = db.Column(db.String)

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return f'<User {self.id} "{self.name}">'
