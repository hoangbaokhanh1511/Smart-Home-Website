from flask import request, Blueprint,jsonify,current_app
from flask_mail import Message, Mail
from flask_restful import Resource, Api
import os
from dotenv import load_dotenv
load_dotenv()
from app import mail

mail_bp = Blueprint('mail', __name__)
mail_api = Api(mail_bp)


class mailWarningTemp(Resource):
    def post(self):
        data = request.get_json()
        msg_post = data['message']
        msg = Message(
            subject='Cảnh Báo Nhiệt Độ', 
            sender=os.getenv('MAIL_USERNAME',''),  
            recipients=[os.getenv('RECEIVED_USER','')] 
        )
        msg.body = msg_post
        try:
            mail.send(msg)
            return {'message': "OK"}, 201
        except Exception as e:
            return {'message': str(e)}, 404
        
class mailWarningPir(Resource):
    def post(self):
        data = request.get_json()
        msg_post = data['message']
        msg = Message(
            subject='Cảnh Báo Chuyển Động Bất Thường', 
            sender=os.getenv('MAIL_USERNAME',''),  
            recipients=[os.getenv('RECEIVED_USER','')] 
        )
        msg.body = msg_post
        try:
            mail.send(msg)
            return {'message': "OK"}, 201
        except Exception as e:
            return {'message': str(e)}, 404

class mailWarningMQT2(Resource):
    def post(self):
        data = request.get_json()
        msg_post = data['message']
        msg = Message(
            subject='Cảnh Báo Nồng Độ Khí Gas', 
            sender=os.getenv('MAIL_USERNAME',''),  
            recipients=[os.getenv('RECEIVED_USER','')] 
        )
        msg.body = msg_post
        try:
            mail.send(msg)
            return {'message': "OK"}, 201
        except Exception as e:
            return {'message': str(e)}, 404

mail_api.add_resource(mailWarningTemp, '/api/send/dht11')
mail_api.add_resource(mailWarningPir, '/api/send/pir')
mail_api.add_resource(mailWarningMQT2, '/api/send/mqt2')