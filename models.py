"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
import datetime

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

    @property
    def full_name(self):
        full_name = f"{self.first_name} {self.last_name}"
        return full_name
    

class Post(db.Model):
    """post model"""

    __tablename__ = "posts"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    title = db.Column(db.String(50),
                        nullable=False)
    content = db.Column(db.Text)
    @property
    def friendly_date(self):
        """Return nicely-formatted date."""
        return self.created_on.strftime("%a %b %-d  %Y, %-I:%M %p")

    created_on = db.Column(db.DateTime, default=datetime.datetime.now)

    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'),
                        nullable=False)
    tags = db.relationship('Tag', secondary='tagged_post', backref='posts', cascade="delete")


class Tag(db.Model):
    """tag model"""

    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, unique=True)

class PostTag(db.Model):
    """through table for tags and posts"""

    __tablename__ = "tagged_post"

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)