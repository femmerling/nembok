from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(50))
    username = db.Column(db.String(20))
    email = db.Column(db.String(50))
    mini_profile = db.Column(db.Text)
    posts = db.relationship('Post',backref='user',lazy='dynamic')

    # data transfer object to form JSON
    def dto(self):
        return dict(
      id = self.id,
            full_name = self.full_name,
            username = self.username,
            email = self.email,
            mini_profile = self.mini_profile)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # data transfer object to form JSON
    def dto(self):
        return dict(
            id = self.id,
            title = self.title,
            content = self.content,
            user_id = self.user_id)
