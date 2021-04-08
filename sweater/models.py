from sweater import db
from datetime import *
from flask_login import LoginManager, UserMixin
from sweater import manager


class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    mik = db.Column(db.String(20), unique=True, nullable=False)
    time = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return '<users %r>' % self.id


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(25), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.id


@manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
