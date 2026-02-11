import os
import errno
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__, static_folder="static", instance_relative_config=True)

    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = ("sqlite:///realjam.db")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    db.init_app(app)
    Migrate(app, db)

    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # セッションリーク防止（超重要）
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()

    # user_login
    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))
    
    # Blueprint
    from .auth.route import auth_bp
    app.register_blueprint(auth_bp)

    from .home.route import home_bp
    app.register_blueprint(home_bp)

    from .driver.route import driver_bp
    app.register_blueprint(driver_bp)

    from .passenger.route import passenger_bp
    app.register_blueprint(passenger_bp)

    from .matching.route import matching_bp
    app.register_blueprint(matching_bp)

    from .history.route import history_bp
    app.register_blueprint(history_bp)

    return app
