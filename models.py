"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class User(db.Model):
    """User Model"""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.String(50),
                     nullable=False)
    last_name = db.Column(db.String(50),
                     nullable = False)
    image_url = db.Column(db.String(100))

    posts = db.relationship('Post', backref='users', cascade="delete")

class Post(db.Model):
    """post model"""

    __tablename__ = "posts"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    title = db.Column(db.String(50),
                        nullable=False)
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'),
                        nullable=False)
    tags = db.relationship('Tag', secondary='tagged_post', backref='posts', cascade="delete")

class Tag(db.Model):
    """tag model"""

    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, unique=True)

    # posts = db.relationship('Post', secondary='tagged_post', backref='tags')

class PostTag(db.Model):
    """through table for tags and posts"""

    __tablename__ = "tagged_post"

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)