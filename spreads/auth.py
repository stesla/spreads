from authlib.integrations.flask_client import OAuth
from flask import redirect, session, url_for
from flask_login import LoginManager, login_required, login_user, logout_user
from sqlalchemy.exc import NoResultFound

from spreads import app, db
from spreads.models import User

oauth = OAuth(app)
oauth.register(
    'google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid profile email'},
)

login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login')
def login():
    redirect_uri = url_for('authorize', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/authorize')
def authorize():
    token = oauth.google.authorize_access_token()
    userinfo = token['userinfo']

    social_id = f'{userinfo["iss"]}|{userinfo["sub"]}'
    try:
        user = User.query.where(social_id == social_id).one()
    except NoResultFound:
        user = User(social_id=social_id)
        db.session.add(user)
    user.given_name = userinfo['given_name']
    user.family_name = userinfo['family_name']
    user.name = userinfo['name']
    user.email = userinfo['email']
    db.session.commit()
    login_user(user)
    session.permanent = True
    return redirect(url_for('index'))
