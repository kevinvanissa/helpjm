from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import os
from flask.ext.login import LoginManager
from config import basedir, ADMINS, MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD
from flask.ext.mail import Mail
from momentjs import momentjs

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

# render phone number
def create_phone(phoneNumber):
    g = phoneNumber[:3]
    f = phoneNumber[3:]
    return g+'-'+f

app.jinja_env.globals['create_phone'] = create_phone

# datetime rendering
app.jinja_env.globals['momentjs'] = momentjs

#Emails
mail = Mail(app)

from app import views, viewAdmin
