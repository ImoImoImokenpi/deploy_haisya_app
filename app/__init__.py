import os
import errno
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, static_folder="static")

    app.config['SECRET_KEY'] = 'secret-key-goes-here'

    # db_user = os.environ.get('DATABASE_USER')
    # db_password = os.environ.get('DATABASE_PASSWORD')
    # db_host = os.environ.get('DATABASE_HOST')
    # db_port = os.environ.get('DATABASE_PORT')
    # db_name = os.environ.get('DATABASE_NAME')
    
    app.config['SQLALCHEMY_DATABASE_URI'] = ("sqlite:///realjam.db")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    db.init_app(app)
    Migrate(app, db)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    from .auth.route import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .index import index as index_blueprint
    app.register_blueprint(index_blueprint)

    return app
