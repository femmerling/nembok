from flask import Blueprint
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import request

from ..database import db
from ..models import User

########### user data model controllers area ###########

user_view = Blueprint('user_view', __name__)


@user_view.route('/user/', methods=['GET', 'POST'], defaults={'id': None})
@user_view.route('/user/<id>', methods=['GET', 'PUT', 'DELETE'])
def user_controller(id):
    full_name = request.values.get('full_name')
    username = request.values.get('username')
    email = request.values.get('email')
    mini_profile = request.values.get('mini_profile')

    if id:
        if request.method == 'GET':
            user = User.query.get(id)
            if user:
                user = user.dto()
            if request.values.get('json'):
                return jsonify(dict(user=user))
            else:
                return render_template('user/user_view.html', user=user)
        elif request.method == 'PUT':
            user_item = User.query.get(id)
            user_item.full_name = full_name
            user_item.username = username
            user_item.email = email
            user_item.mini_profile = mini_profile
            db.session.add(user_item)
            db.session.commit()
            return 'updated'
        elif request.method == 'DELETE':
            user_item = User.query.get(id)
            db.session.delete(user_item)
            db.session.commit()
            return 'deleted'
        else:
            return 'Method Not Allowed'
    else:
        if request.method == 'GET':
            user_list = User.query.all()
            if user_list:
                entries = [user.dto() for user in user_list]
            else:
                entries = None
            if request.values.get('json'):
                return jsonify(dict(user=entries))
            else:
                return render_template(
                    'user/user.html',
                    user_entries=entries,
                    title="User List",
                    )
        elif request.method == 'POST':
            new_user = User(
                full_name=full_name,
                username=username,
                email=email,
                mini_profile=mini_profile,
                )

            db.session.add(new_user)
            db.session.commit()
            if request.values.get('json'):
                url = '/user/json=true'
            else:
                url = '/user/'
            return redirect(url)
        else:
            return 'Method Not Allowed'


@user_view.route('/user/add/')
def user_add_controller():
    # this is the controller to add new model entries
    return render_template('user/user_add.html', title="Add New Entry")


@user_view.route('/user/edit/<id>')
def user_edit_controller(id):
    #this is the controller to edit model entries
    user_item = User.query.get(id)
    return render_template(
        'user/user_edit.html', user_item=user_item, title="Edit Entries")
