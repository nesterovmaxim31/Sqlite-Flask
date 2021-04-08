from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import smtplib
from flask_mail import Mail
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'SOME secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
EMAIL_ADMIN = "workmaksim041@gmail.com"
PASSWORD_ADMIN_EMAIL = "Flask_Python"
db = SQLAlchemy(app)
manager = LoginManager(app)

from sweater import models, routes

db.create_all()
