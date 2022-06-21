from flask import abort, redirect, request, session, url_for
from flask_login import LoginManager, login_required, login_user, logout_user
from sqlalchemy.exc import NoResultFound
from urllib.parse import urlparse, urljoin

from spreads import app, db, oauth
from spreads.models import User

oauth.register(
    'google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid profile email'},
)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login')
def login():
    session['next'] = get_redirect_target()
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
        user = User.query.where(User.social_id == social_id).one()
    except NoResultFound:
        user = User(social_id=social_id)
        db.session.add(user)
    user.email = userinfo['email']
    user.name = userinfo.get('name')
    user.given_name = userinfo.get('given_name')
    user.family_name = userinfo.get('family_name')
    user.picture_url = userinfo.get('picture')
    db.session.commit()
    login_user(user)
    session.permanent = True
    session['token'] = token
    nextUrl = session['next'] or url_for('index')
    return redirect(nextUrl)

def get_redirect_target():
    for target in request.values.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return target

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
        ref_url.netloc == test_url.netloc
