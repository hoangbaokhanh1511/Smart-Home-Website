from flask import request, Blueprint, redirect, url_for, flash, session
from flask_restful import Resource, Api
from datetime import datetime
from Controller.TaiKhoan import userController
from werkzeug.security import generate_password_hash, check_password_hash #hash password

auth_bp = Blueprint('auth', __name__)
auth_api = Api(auth_bp)

class dangKy(Resource):
    def post(self):
        data = request.form
        success, msg = userController.dangKy(data)
        if success:
            flash(msg,'success')
            return redirect(url_for('main.signup'))
            
        flash(msg,'danger')
        return redirect(url_for('main.signup'))

class dangNhap(Resource):
    def post(self):
        data = request.form
        success, msg = userController.dangNhap(data)
        if success:
            return redirect(url_for('main.mainpage'))
        flash(msg, 'danger')
        return redirect(url_for('main.login'))

class dangXuat(Resource):
    def get(self):
        success, msg = userController.dangXuat()
        if success:
            session.pop('username', None)
            session.pop('id', None)
            flash(msg,'success')
            return redirect(url_for('main.login'))
        return {"message": msg}, 404

class doiMatKhau(Resource):
    def post(self):
        receive = request.form
        success, msg = userController.doiMatKhau(receive)
        if success:
            flash(msg,'success')
            return redirect(url_for('main.changepass'))
        
        flash(msg,'danger')
        return redirect(url_for('main.changepass'))

class capNhatHoSo(Resource):
    def post(self):
        receive = request.form
        success, msg = userController.capNhatHoSo(receive)
        if success:
            flash(msg,'success')
            return redirect(url_for('main.profile'))
        
        flash(msg,'danger')
        return redirect(url_for('main.profile'))
    
auth_api.add_resource(capNhatHoSo, '/api/auth/changeProfile')
auth_api.add_resource(doiMatKhau, '/api/auth/changePassword')
auth_api.add_resource(dangXuat, '/api/auth/logout')
auth_api.add_resource(dangNhap, '/api/auth/login')
auth_api.add_resource(dangKy, '/api/auth/signup')
