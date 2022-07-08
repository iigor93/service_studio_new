from flask import Flask
from config import Config
from db_config import db
from implemented import user_service

# Blueprints
from views.auth.login import login_logout
from views.email.main import email
from application.views.account import account
from application.views.complaint import complaint
from application.views.detail_compl import detail_compl
from application.views.prints import prints
from application.views.telegram import tg


def create_app(config_obj):
    flask_app = Flask(__name__)
    flask_app.config.from_object(config_obj)
    register_blueprints(flask_app)
    register_extensions(flask_app)
    return flask_app


def register_blueprints(flask_app):
    flask_app.register_blueprint(login_logout)
    flask_app.register_blueprint(email, url_prefix='/email')
    flask_app.register_blueprint(account, url_prefix='/account')
    flask_app.register_blueprint(complaint, url_prefix='/complaint')
    flask_app.register_blueprint(detail_compl, url_prefix='/detail_compl')
    flask_app.register_blueprint(prints, url_prefix='/prints')
    flask_app.register_blueprint(tg, url_prefix='/AAHKbwD_BtK91grjBlmhmIEjPfGHyBxbyxE/')


def register_extensions(flask_app):
    db.init_app(flask_app)
    create_data(flask_app, db)


def create_data(flask_app, database):
    with flask_app.app_context():
        database.create_all()


app = create_app(Config())


if __name__ == '__main__':
    app.run()


@app.route('/')
def index():
    return "Ok", 200
