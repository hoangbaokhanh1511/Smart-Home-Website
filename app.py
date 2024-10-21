from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_mail import Mail
import os
from dotenv import load_dotenv
load_dotenv()

db = SQLAlchemy() 
api = Api()
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE') 
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  
    app.config['SQLALCHEMY_BINDS'] = {
        'pir': os.getenv('DATABASE_PIR') ,
    }
    
    #Mail
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME','')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD', '')
    
    db.init_app(app)
    api.init_app(app)
    mail.init_app(app)
    
    from models.user_models import userManager
    from models.historyPir_models import History_Pir
    
    from routers.routers import main_bp
    from API.auth_api import auth_bp
    from API.moduleESP_api import module_bp
    from API.gmail_api import mail_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(module_bp)
    app.register_blueprint(mail_bp)
    
    
    with app.app_context():
        db.create_all()
    
    return app