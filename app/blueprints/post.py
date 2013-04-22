from flask import Blueprint
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import request

from ..database import db
from ..models import Post


########### post data model controllers area ###########

post_view = Blueprint('post_view', __name__)


@post_view.route('/post/', methods=['GET', 'POST'], defaults={'id': None})
@post_view.route('/post/<id>', methods=['GET', 'PUT', 'DELETE'])
def post_controller(id):
    title = request.values.get('title')
    content = request.values.get('content')
    user_id = request.values.get('user_id')

    if id:
        if request.method == 'GET':
            post = Post.query.get(id)
            if post:
                post = post.dto()
            if request.values.get('json'):
                return jsonify(dict(post=post))
            else:
                return render_template('post/post_view.html', post=post)
        elif request.method == 'PUT':
            post_item = Post.query.get(id)
            post_item.title = title
            post_item.content = content
            post_item.user_id = user_id
            db.session.add(post_item)
            db.session.commit()
            return 'updated'
        elif request.method == 'DELETE':
            post_item = Post.query.get(id)
            db.session.delete(post_item)
            db.session.commit()
            return 'deleted'
        else:
            return 'Method Not Allowed'
    else:
        if request.method == 'GET':
            post_list = Post.query.all()
            if post_list:
                entries = [post.dto() for post in post_list]
            else:
                entries = None
            if request.values.get('json'):
                return jsonify(dict(post=entries))
            else:
                return render_template(
                    'post/post.html', post_entries=entries, title="Post List")
        elif request.method == 'POST':
            new_post = Post(
                            title=title,
                            content=content,
                            user_id=user_id
                            )

            db.session.add(new_post)
            db.session.commit()
            if request.values.get('json'):
                url = '/post/json=true'
            else:
                url = '/post/'
            return redirect(url)
        else:
            return 'Method Not Allowed'


@post_view.route('/post/add/')
def post_add_controller():
    #this is the controller to add new model entries
    return render_template('post/post_add.html', title="Add New Entry")


@post_view.route('/post/edit/<id>')
def post_edit_controller(id):
    #this is the controller to edit model entries
    post_item = Post.query.get(id)
    return render_template(
        'post/post_edit.html', post_item=post_item, title="Edit Entries")
