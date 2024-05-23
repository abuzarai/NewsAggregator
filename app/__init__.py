from flask import Flask
from flask_login import LoginManager
from .routes import main_bp
from .models import db, User 
from .auth import auth_bp  
import os
import secrets

secret_key = secrets.token_hex(16)

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = secret_key 
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    
    db.init_app(app)
    
    login_manager = LoginManager(app)
    login_manager.login_view = 'auth.login' 
    login_manager.login_message_category = 'info'
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth') 
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app
