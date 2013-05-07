from database import db

tag_table = db.Table('post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(50))
    username = db.Column(db.String(20))
    email = db.Column(db.String(50))
    mini_profile = db.Column(db.Text)
    posts = db.relationship('Post', backref='user', lazy='dynamic')
    jempols = db.relationship('Jempol', backref='user', lazy='dynamic')
    comments = db.relationship('Comment', backref='user', lazy='dynamic')

    # data transfer object to form JSON
    def dto(self):
        return dict(
            id=self.id,
            full_name=self.full_name,
            username=self.username,
            email=self.email,
            mini_profile=self.mini_profile,
            )

    def find_by_username(self, username):
        return self.query.filter_by(username=username).limit(1).first()


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tags = db.relationship(
        'Tag',
        secondary=tag_table,
        backref=db.backref('post_tags'),
        lazy='dynamic',
        )
    jempols = db.relationship('Jempol', backref='post', lazy='dynamic')
    comments = db.relationship('Comment', backref='post', lazy='dynamic')

    # data transfer object to form JSON
    def dto(self):
        return dict(
            id=self.id,
            title=self.title,
            content=self.content,
            user_id=self.user_id,
            )


class Jempol(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    jempol_time = db.Column(db.DateTime)

    # data transfer object to form JSON
    def dto(self):
        return dict(
            id=self.id,
            user_id=self.user_id,
            post_id=self.post_id,
            jempol_time=self.jempol_time,
            )


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    desc = db.Column(db.String(100))
    tags = db.relationship(
        'Post',
        secondary=tag_table,
        backref=db.backref('post_tags'),
        lazy='dynamic',
        )

    # data transfer object to form JSON
    def dto(self):
        return dict(
            id=self.id,
            desc=self.desc,
            )


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    comment = db.Column(db.Text)
    comment_time = db.Column(db.DateTime)

    # data transfer object to form JSON
    def dto(self):
        return dict(
            id=self.id,
            user_id=self.user_id,
            post_id=self.post_id,
            comment=self.comment,
            comment_time=self.comment_time,
            )
