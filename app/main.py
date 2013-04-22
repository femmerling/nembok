# do not change or move the following lines
# if you still want to use the box.py auto generator
from app import app
# from models import Jempol

# you can freely change the lines below
from flask import render_template
# from flask import json
# from flask import session
# from flask import url_for
# from flask import redirect
# from flask import request
# from flask import abort
# from flask import Response
# import logging
# from helpers import generate_key

from blueprints import user_view
from blueprints import post_view
from blueprints import comment_view
from blueprints import tag_view
from blueprints import jempol_view


app.register_blueprint(user_view)
app.register_blueprint(post_view)
app.register_blueprint(comment_view)
app.register_blueprint(tag_view)
app.register_blueprint(jempol_view)

# define global variables here


# home root controller
@app.route('/')
def index():
    # define your controller here
    return render_template('welcome.html')
