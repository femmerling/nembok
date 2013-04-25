from flask import Flask
from rauth.service import OAuth2Service

from database import db

app = Flask(__name__)
app.config.from_object('config')
db.init_app(app)

github = OAuth2Service(
    name='github',
    authorize_url='https://github.com/login/oauth/authorize',
    access_token_url='https://github.com/login/oauth/access_token',
    client_id=app.config['GITHUB_CLIENT_ID'],
    client_secret=app.config['GITHUB_CLIENT_SECRET'],
    base_url='https://api.github.com/',
    )

import main  # NOQA
