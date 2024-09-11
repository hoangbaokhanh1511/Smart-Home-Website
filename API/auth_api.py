from flask import request, Blueprint, session
from flask_restful import Resource, Api
from datetime import datetime
from Controller.TaiKhoan import userController

auth_bp = Blueprint('auth', __name__)
auth_api = Api(auth_bp)

class dangKy(Resource):
    def post(self):
        data = request.get_json()
        success, msg = userController.dangKy(data)
        if success:
            return {"message": msg}, 201
        return {"message": msg}, 400

class dangNhap(Resource):
    def post(self):
        data = request.get_json()
        success, msg = userController.dangNhap(data)
        if success:
            return {"message": msg}, 201
        return {"message": msg}, 400

class dangXuat(Resource):
    def get(self):
        success, msg = userController.dangXuat()
        if success:
            return {"message": msg}, 201
        return {"message": msg}, 400

class doiMatKhau(Resource):
    def post(self):
        receive = request.get_json()
        success, msg = userController.doiMatKhau(receive)
        if success:
            return {"message": msg}, 201
        return {"message": msg}, 400

class capNhatHoSo(Resource):
    def post(self):
        receive = request.get_json()
        success, msg = userController.doiMatKhau(receive)
        if success:
            return {"message": msg}, 201
        return {"message": msg}, 400
    
auth_api.add_resource(capNhatHoSo, '/api/auth/changeProfile')
auth_api.add_resource(doiMatKhau, '/api/auth/changePassword')
auth_api.add_resource(dangXuat, '/api/auth/logout')
auth_api.add_resource(dangNhap, '/api/auth/login')
auth_api.add_resource(dangKy, '/api/auth/signup')
