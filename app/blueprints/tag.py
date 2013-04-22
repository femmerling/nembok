from flask import Blueprint
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import request

from ..database import db
from ..models import Tag

########### tag data model controllers area ###########

tag_view = Blueprint('tag_view', __name__)


@tag_view.route('/tag/', methods=['GET', 'POST'], defaults={'id': None})
@tag_view.route('/tag/<id>', methods=['GET', 'PUT', 'DELETE'])
def tag_controller(id):
    desc = request.values.get('desc')

    if id:
        if request.method == 'GET':
            tag = Tag.query.get(id)
            if tag:
                tag = tag.dto()
            if request.values.get('json'):
                return jsonify(dict(tag=tag))
            else:
                return render_template('tag/tag_view.html', tag=tag)
        elif request.method == 'PUT':
            tag_item = Tag.query.get(id)
            tag_item.desc = desc
            db.session.add(tag_item)
            db.session.commit()
            return 'updated'
        elif request.method == 'DELETE':
            tag_item = Tag.query.get(id)
            db.session.delete(tag_item)
            db.session.commit()
            return 'deleted'
        else:
            return 'Method Not Allowed'
    else:
        if request.method == 'GET':
            tag_list = Tag.query.all()
            if tag_list:
                entries = [tag.dto() for tag in tag_list]
            else:
                entries = None
            if request.values.get('json'):
                return jsonify(dict(tag=entries))
            else:
                return render_template(
                    'tag/tag.html', tag_entries=entries, title="Tag List")
        elif request.method == 'POST':
            new_tag = Tag(
                            desc=desc,
                            )

            db.session.add(new_tag)
            db.session.commit()
            if request.values.get('json'):
                url = '/tag/json=true'
            else:
                url = '/tag/'
            return redirect(url)
        else:
            return 'Method Not Allowed'


@tag_view.route('/tag/add/')
def tag_add_controller():
    #this is the controller to add new model entries
    return render_template('tag/tag_add.html', title="Add New Entry")


@tag_view.route('/tag/edit/<id>')
def tag_edit_controller(id):
    #this is the controller to edit model entries
    tag_item = Tag.query.get(id)
    return render_template(
        'tag/tag_edit.html', tag_item=tag_item, title="Edit Entries")
