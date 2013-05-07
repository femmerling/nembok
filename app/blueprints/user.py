from flask import Blueprint
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask import session

from ..database import db
from ..models import User
from app import github

########### user data model controllers area ###########

user_view = Blueprint('user_view', __name__)


@user_view.route('/user/', methods=['GET'], defaults={'id': None})
@user_view.route('/user/<id>', methods=['GET', 'PUT'])
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
        else:
            return 'Method Not Allowed'


@user_view.route('/user/edit/<id>')
def user_edit_controller(id):
    #this is the controller to edit model entries
    user_item = User.query.get(id)
    return render_template(
        'user/user_edit.html', user_item=user_item, title="Edit Entries")


@user_view.route('/login/')
def user_login_controller():
    if session.get('user') is not None:
        return redirect(url_for('index'))

    redirect_uri = url_for(
        '.user_login_github_controller',
        next=request.args.get('next') or request.referrer or None,
        _external=True,
        )
    params = {'redirect_uri': redirect_uri}
    return redirect(github.get_authorize_url(**params))


@user_view.route('/login/github/')
def user_login_github_controller():
    if session.get('user') is not None:
        return redirect(url_for('index'))

    if not 'code' in request.args:
        return 'Access denied: error=%s' % (request.args['error'])

    redirect_uri = url_for('.user_login_github_controller', _external=True)
    data = dict(code=request.args['code'], redirect_uri=redirect_uri)

    gh_session = github.get_auth_session(data=data)
    user_data = gh_session.get('user').json()

    user = User()

    # GitHub uses unique username, what we need to do is matching
    # the imported GitHub user with our existing user.
    # If we already have a matched user, simply skip the user data insertion.
    existing_user = user.find_by_username(user_data['login'])

    if existing_user is None:
        try:
            user.username = user_data['login']
            user.full_name = user_data['name']
            user.mini_profile = user_data['bio']
            user.email = user_data['email']
            db.session.add(user)
            db.session.commit()

            session['user'] = {
                'id': user.id,
                'username': user.username,
                'full_name': user.full_name,
            }
        except Exception:
            db.session.rollback()
            raise
    else:
        session['user'] = {
            'id': existing_user.id,
            'username': existing_user.username,
            'full_name': existing_user.full_name,
        }

    return redirect(url_for('index'))


@user_view.route('/logout/')
def user_logout_controller():
    if session.get('user') is not None:
        session['user'] = None
    return redirect(url_for('index'))
