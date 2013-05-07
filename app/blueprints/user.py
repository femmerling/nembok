from flask import Blueprint
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask import session

from flask.ext.wtf import Form
from wtforms import TextField
from wtforms import TextAreaField
from wtforms.validators import Email

from app.database import db
from app.models import User
from app import github

user_view = Blueprint('user_view', __name__)


class EditUserForm(Form):
    full_name = TextField('Full Name')
    email = TextField('Email', validators=[Email()])
    mini_profile = TextAreaField('Bio')


@user_view.route('/user/', defaults={'id': None})
@user_view.route('/user/<id>')
def user_controller(id):
    if id:
        user = User.query.get(id)
        if user:
            user = user.dto()
        if request.values.get('json'):
            return jsonify(dict(user=user))
        return render_template('user/user_view.html', user=user)

    user_list = User.query.all()
    entries = [user.dto() for user in user_list]

    if request.values.get('json'):
        return jsonify(dict(user=entries))

    return render_template(
        'user/user.html', user_entries=entries, title="User List")


@user_view.route('/user/edit/<id>', methods=['GET', 'POST'])
def user_edit_controller(id):
    user = User.query.get(id)
    form = EditUserForm(obj=user)

    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('.user_controller'))

    return render_template(
        'user/user_edit.html', form=form, title="Edit Entries")


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
