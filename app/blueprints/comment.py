from flask import Blueprint
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import request

from ..database import db
from ..models import Comment

########### comment data model controllers area ###########

comment_view = Blueprint('comment_view', __name__)


@comment_view.route(
    '/comment/', methods=['GET', 'POST'], defaults={'id': None})
@comment_view.route('/comment/<id>', methods=['GET', 'PUT', 'DELETE'])
def comment_controller(id):
    user_id = request.values.get('user_id')
    post_id = request.values.get('post_id')
    comment = request.values.get('comment')
    comment_time = request.values.get('comment_time')

    if id:
        if request.method == 'GET':
            comment = Comment.query.get(id)
            if comment:
                comment = comment.dto()
            if request.values.get('json'):
                return jsonify(dict(comment=comment))
            else:
                return render_template(
                    'comment/comment_view.html', comment=comment)
        elif request.method == 'PUT':
            comment_item = Comment.query.get(id)
            comment_item.user_id = user_id
            comment_item.post_id = post_id
            comment_item.comment = comment
            comment_item.comment_time = comment_time
            db.session.add(comment_item)
            db.session.commit()
            return 'updated'
        elif request.method == 'DELETE':
            comment_item = Comment.query.get(id)
            db.session.delete(comment_item)
            db.session.commit()
            return 'deleted'
        else:
            return 'Method Not Allowed'
    else:
        if request.method == 'GET':
            comment_list = Comment.query.all()
            if comment_list:
                entries = [comment.dto() for comment in comment_list]
            else:
                entries = None
            if request.values.get('json'):
                return jsonify(dict(comment=entries))
            else:
                return render_template(
                    'comment/comment.html',
                    comment_entries=entries,
                    title="Comment List",
                    )
        elif request.method == 'POST':
            new_comment = Comment(
                            user_id=user_id,
                            post_id=post_id,
                            comment=comment,
                            comment_time=comment_time,
                            )

            db.session.add(new_comment)
            db.session.commit()
            if request.values.get('json'):
                url = '/comment/json=true'
            else:
                url = '/comment/'
            return redirect(url)
        else:
            return 'Method Not Allowed'


@comment_view.route('/comment/add/')
def comment_add_controller():
    #this is the controller to add new model entries
    return render_template(
        'comment/comment_add.html', title="Add New Entry")


@comment_view.route('/comment/edit/<id>')
def comment_edit_controller(id):
    #this is the controller to edit model entries
    comment_item = Comment.query.get(id)
    return render_template(
        'comment/comment_edit.html',
        comment_item=comment_item,
        title="Edit Entries",
        )
