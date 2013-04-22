from flask import Blueprint
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import request

from ..database import db
from ..models import Jempol

########### jempol data model controllers area ###########

jempol_view = Blueprint('jempol_view', __name__)


@jempol_view.route('/jempol/', methods=['GET', 'POST'], defaults={'id': None})
@jempol_view.route('/jempol/<id>', methods=['GET', 'PUT', 'DELETE'])
def jempol_controller(id):
    user_id = request.values.get('user_id')
    post_id = request.values.get('post_id')
    jempol_time = request.values.get('jempol_time')

    if id:
        if request.method == 'GET':
            jempol = Jempol.query.get(id)
            if jempol:
                jempol = jempol.dto()
            if request.values.get('json'):
                return jsonify(dict(jempol=jempol))
            else:
                return render_template(
                    'jempol/jempol_view.html', jempol=jempol)
        elif request.method == 'PUT':
            jempol_item = Jempol.query.get(id)
            jempol_item.user_id = user_id
            jempol_item.post_id = post_id
            jempol_item.jempol_time = jempol_time
            db.session.add(jempol_item)
            db.session.commit()
            return 'updated'
        elif request.method == 'DELETE':
            jempol_item = Jempol.query.get(id)
            db.session.delete(jempol_item)
            db.session.commit()
            return 'deleted'
        else:
            return 'Method Not Allowed'
    else:
        if request.method == 'GET':
            jempol_list = Jempol.query.all()
            if jempol_list:
                entries = [jempol.dto() for jempol in jempol_list]
            else:
                entries = None
            if request.values.get('json'):
                return jsonify(dict(jempol=entries))
            else:
                return render_template(
                    'jempol/jempol.html',
                    jempol_entries=entries,
                    title="Jempol List",
                    )
        elif request.method == 'POST':
            new_jempol = Jempol(
                            user_id=user_id,
                            post_id=post_id,
                            jempol_time=jempol_time,
                            )

            db.session.add(new_jempol)
            db.session.commit()
            if request.values.get('json'):
                url = '/jempol/json=true'
            else:
                url = '/jempol/'
            return redirect(url)
        else:
            return 'Method Not Allowed'


@jempol_view.route('/jempol/add/')
def jempol_add_controller():
    #this is the controller to add new model entries
    return render_template(
        'jempol/jempol_add.html', title="Add New Entry")


@jempol_view.route('/jempol/edit/<id>')
def jempol_edit_controller(id):
    #this is the controller to edit model entries
    jempol_item = Jempol.query.get(id)
    return render_template(
        'jempol/jempol_edit.html',
        jempol_item=jempol_item,
        title="Edit Entries",
        )
