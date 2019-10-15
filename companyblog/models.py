from companyblog import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    profile_image = db.Column(db.String(20), nullable=False, default='default_profile.png')
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64),unique=True, index=True)
    password_hash = db.Column(db.String(128))

    posts = db.relationship('BlogPost', backref='author', lazy=True)
    comments = db.relationship('Comment', backref='author', lazy=True)

    def __init__(self,email,username,password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return "Username {}".format(self.username)


post_tag = db.Table('post_tag',
    db.Column('blogpost_id', db.Integer, db.ForeignKey('blogpost.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)  
)


class BlogPost(db.Model):

    __tablename__ = 'blogpost'

    users = db.relationship(User)

    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    comments = db.relationship('Comment', backref='post', lazy=True)

    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    title = db.Column(db.String(140),nullable=False, unique=True)
    text = db.Column(db.Text,nullable=False)
    slug = db.Column(db.String(140), nullable=False)

    tags = db.relationship(
        'Tag', secondary=post_tag,
        backref=db.backref('posts', lazy='dynamic'), lazy='dynamic'
    )

    def __init__(self,title,text,user_id, slug):
        self.title = title
        self.text = text
        self.user_id = user_id
        self.slug = slug

    def __repr__(self):
        return "Post ID: {}".format(self.id)

    def tag(self, tag):
        if not self.tagged(tag):
            self.tags.append(tag)

    def untag(self, tag):
        if self.tagged(tag):
            self.tags.remove(tag)

    def tagged(self, tag):
        return self.tags.filter(
            post_tag.c.tag_id == tag.id).count() > 0


class Tag(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    tag = db.Column(db.String(64), nullable=False, unique=True)


    def __init__(self,tag):
        self.tag = tag

    def __repr__(self):
        return "Tag: {}".format(self.tag)



class Comment(db.Model):

    __tablename__ = 'comments'

    users = db.relationship(User)

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('blogpost.id'), nullable=False)
    text = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime(), default=datetime.utcnow, index=True)