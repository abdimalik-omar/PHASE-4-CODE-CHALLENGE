from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

metadata = MetaData()

db = SQLAlchemy(metadata=metadata)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_approved = db.Column(db.Boolean, default=False)
    password = db.Column(db.String(128), nullable=False)

    movie = db.relationship('Movie', backref='user', lazy=True)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    director = db.Column(db.String(120), nullable=False)
    release_year = db.Column(db.Integer, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class TokenBlocklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, index=True)
    created_at = db.Column(db.DateTime, nullable=False)