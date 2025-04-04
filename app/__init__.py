from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    
    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path, mode=0o755, exist_ok=True)
    except OSError:
        pass

    # Configure the app
    app.config['SECRET_KEY'] = os.urandom(24)
    
    # Set the database path to be in the instance folder
    db_path = os.path.join(app.instance_path, 'crm.db')
    
    # Ensure the database file exists with proper permissions
    if not os.path.exists(db_path):
        open(db_path, 'a').close()
        os.chmod(db_path, 0o644)
    
    # Configure SQLite to handle concurrent writes
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}?timeout=15&check_same_thread=False'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from app.routes import auth, customers, dashboard
    app.register_blueprint(auth.bp)
    app.register_blueprint(customers.bp)
    app.register_blueprint(dashboard.bp)

    with app.app_context():
        db.create_all()

    return app 