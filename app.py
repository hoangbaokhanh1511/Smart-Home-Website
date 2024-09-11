from flask import Flask, render_template, url_for, jsonify, redirect, session, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, abort
from datetime import datetime
import requests, os
from dotenv import load_dotenv
load_dotenv()

db = SQLAlchemy() 
api = Api()

def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE')  # Tạo database có tên là users
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # theo dõi các sửa đổi object và phát tín hiệu
    
    db.init_app(app)
    api.init_app(app)
    
    from models.user_models import userManager
    from routers.routers import main_bp
    from API.auth_api import auth_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    
    with app.app_context():
        db.create_all()  
    
    return app