"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    """Users"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)

    first_name = db.Column(db.Text, nullable = False) 

    last_name = db.Column(db.Text, nullable = False)

    image_url = db.Column(db.Text, nullable = False, unique = True)

class Post(db.Model):
    """Posts"""

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)

    title = db.Column(db.Text, nullable = False) 

    content = db.Column(db.Text, nullable = False)

    created_at = db.Column(db.Text, nullable = False, default ="01-01-2000 8:15 AM")

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
    

    user = db.relationship("User",backref ="posts")

class Tag(db.Model):
    """Tags"""

    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)

    name = db.Column(db.Text, unique = True)

    posts = db.relationship("Post", secondary = "posts_tags", backref = "tags")

class PostTag(db.Model):
    """Posts_Tags"""

    __tablename__ = "posts_tags"

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key = True)

    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key = True)
    
    