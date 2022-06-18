from flask import render_template, url_for
from flask_login import login_required

from spreads import app

@app.route('/')
def index():
    return render_template('index.html')
