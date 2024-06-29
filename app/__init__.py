#THis is going to be the initialization file to pull all the wonderful things we need to use for the application
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from config import Config

db = SQLAlchemy()
csrf = CSRFProtect()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    csrf.init_app(app)

    app.secret_key = 'usingtostoresessions'

    from app import routes, models
    app.register_blueprint(routes.bp)

    return app