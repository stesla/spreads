from flask import render_template, session, url_for
from flask_login import login_required

from spreads import app, oauth

@app.route('/')
def index():
    try:
        token = session['token']
        img_url = token['userinfo']['picture']
    except KeyError:
        img_url = None
    return render_template('index.html', img_url=img_url)
