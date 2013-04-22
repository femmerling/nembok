# do not change or move the following lines
# if you still want to use the box.py auto generator
from app import app, db
from models import Post, Jempol, Tag, Comment

# you can freely change the lines below
from flask import render_template
from flask import json
from flask import session
from flask import url_for
from flask import redirect
from flask import request
from flask import abort
from flask import Response
import logging
from helpers import generate_key

from user import user_view


app.register_blueprint(user_view)

# define global variables here


# home root controller
@app.route('/')
def index():
    # define your controller here
    return render_template('welcome.html')


########### post data model controllers area ###########

@app.route('/post/',methods=['GET','POST'],defaults={'id':None})
@app.route('/post/<id>',methods=['GET','PUT','DELETE'])
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
                return json.dumps(dict(post=post))
            else:
                return render_template('post_view.html', post = post)
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
                entries=None
            if request.values.get('json'):
                return json.dumps(dict(post=entries))
            else:
                return render_template('post.html',post_entries = entries, title = "Post List")
        elif request.method == 'POST':
            new_post = Post(
                            title = title,
                            content = content,
                            user_id = user_id
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

@app.route('/post/add/')
def post_add_controller():
    #this is the controller to add new model entries
    return render_template('post_add.html', title = "Add New Entry")

@app.route('/post/edit/<id>')
def post_edit_controller(id):
    #this is the controller to edit model entries
    post_item = Post.query.get(id)
    return render_template('post_edit.html', post_item = post_item, title = "Edit Entries")



########### jempol data model controllers area ###########

@app.route('/jempol/',methods=['GET','POST'],defaults={'id':None})
@app.route('/jempol/<id>',methods=['GET','PUT','DELETE'])
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
                return json.dumps(dict(jempol=jempol))
            else:
                return render_template('jempol_view.html', jempol = jempol)
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
                entries=None
            if request.values.get('json'):
                return json.dumps(dict(jempol=entries))
            else:
                return render_template('jempol.html',jempol_entries = entries, title = "Jempol List")
        elif request.method == 'POST':
            new_jempol = Jempol(
                            user_id = user_id,
                            post_id = post_id,
                            jempol_time = jempol_time
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

@app.route('/jempol/add/')
def jempol_add_controller():
    #this is the controller to add new model entries
    return render_template('jempol_add.html', title = "Add New Entry")

@app.route('/jempol/edit/<id>')
def jempol_edit_controller(id):
    #this is the controller to edit model entries
    jempol_item = Jempol.query.get(id)
    return render_template('jempol_edit.html', jempol_item = jempol_item, title = "Edit Entries")



########### tag data model controllers area ###########

@app.route('/tag/',methods=['GET','POST'],defaults={'id':None})
@app.route('/tag/<id>',methods=['GET','PUT','DELETE'])
def tag_controller(id):
    desc = request.values.get('desc')

    if id:
        if request.method == 'GET':
            tag = Tag.query.get(id)
            if tag:
                tag = tag.dto()
            if request.values.get('json'):
                return json.dumps(dict(tag=tag))
            else:
                return render_template('tag_view.html', tag = tag)
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
                entries=None
            if request.values.get('json'):
                return json.dumps(dict(tag=entries))
            else:
                return render_template('tag.html',tag_entries = entries, title = "Tag List")
        elif request.method == 'POST':
            new_tag = Tag(
                            desc = desc
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

@app.route('/tag/add/')
def tag_add_controller():
    #this is the controller to add new model entries
    return render_template('tag_add.html', title = "Add New Entry")

@app.route('/tag/edit/<id>')
def tag_edit_controller(id):
    #this is the controller to edit model entries
    tag_item = Tag.query.get(id)
    return render_template('tag_edit.html', tag_item = tag_item, title = "Edit Entries")



########### comment data model controllers area ###########

@app.route('/comment/',methods=['GET','POST'],defaults={'id':None})
@app.route('/comment/<id>',methods=['GET','PUT','DELETE'])
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
                return json.dumps(dict(comment=comment))
            else:
                return render_template('comment_view.html', comment = comment)
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
                entries=None
            if request.values.get('json'):
                return json.dumps(dict(comment=entries))
            else:
                return render_template('comment.html',comment_entries = entries, title = "Comment List")
        elif request.method == 'POST':
            new_comment = Comment(
                            user_id = user_id,
                            post_id = post_id,
                            comment = comment,
                            comment_time = comment_time
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

@app.route('/comment/add/')
def comment_add_controller():
    #this is the controller to add new model entries
    return render_template('comment_add.html', title = "Add New Entry")

@app.route('/comment/edit/<id>')
def comment_edit_controller(id):
    #this is the controller to edit model entries
    comment_item = Comment.query.get(id)
    return render_template('comment_edit.html', comment_item = comment_item, title = "Edit Entries")
