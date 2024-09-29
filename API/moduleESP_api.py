from flask import request, Blueprint,jsonify
from flask_restful import Resource, Api
from models.historyPir_models import History_Pir
import os,requests
from datetime import datetime
from app import db

module_bp = Blueprint('module', __name__)
module_api = Api(module_bp)

data_sensor_dht11 = {
    'temperature': None,
    'humidity': None
}

status_pir = {
    'status': None
}

data_check_mqt2 = {
    "value": 0
}

light = {
    'status': False
}

fan = {
    'fan1': False,
    'fan2': False
}

warningTemperature = {
    'temp': None,
    'status': False
}

warningGas = {
    'value': None,
    'status': False
}

class dht11(Resource):
    def get(self):
        return data_sensor_dht11
    def put(self):
        data = request.get_json()
        data_sensor_dht11.update(data)
        if data:
            return data, 200
        else:
            return {message: "Not Found The Data"}, 404

class motionPir(Resource):
    def get(self):
        return status_pir, 200
    def put(self):
        data = request.get_json()
        status_pir.update(data)
        
        if data.get('status') == True:
            detected = History_Pir()
            db.session.add(detected)
            db.session.commit()

        if data:
            return data, 201
        else:
            return {message: "No Data"}, 404

class mqt2_api(Resource):
    def get(self):
        return data_check_mqt2, 200
    def put(self):
        data = request.get_json()
        if data:
            data_check_mqt2.update(data)
            return data_check_mqt2, 201
        else:
            return {message: "No Data"}, 404

class history_data_pir_5(Resource):
    def get(self):
        result = {}
        size = History_Pir.query.count()
        
        if size <= 5:
            data_pir = History_Pir.query.all()

        else:
            start = size - 4
            end = size
            data_pir = History_Pir.query.filter(History_Pir.id >= start, History_Pir.id <= end).all()
        
        data_time_to_dict = [data.timestamp.strftime('%d/%m/%Y %H:%M:%S') for data in data_pir]
        result.update({
            'time': data_time_to_dict
        })
        return result, 200

class weather_forecast(Resource):
    def get(self):
        API_KEY = os.getenv('API_KEY')
        response = requests.get(
            f'http://api.openweathermap.org/data/2.5/forecast?q=Hue&appid={API_KEY}&units=metric&lang=vi')
        data = response.json()
        list_data = data.get('list')

        weather = [
            {"Day1": {}},
            {"Day2": {}},
            {"Day3": {}},
            {"Day4": {}},
            {"Day5": {}}
        ]
        current_date = None
        day_counter = 0
        ob = {
            'Times': [],
            'Weather': {
                'Temperature': [],
                'Humidity': [],
                'Icon': [],
                'Icon_title': [],
                'Description': []
            },
            'Wind': {
                'Speed': []
            },
            'Day': ''
        }
        Date_in_week = {
            "Monday": "Thứ Hai",
            "Tuesday": "Thứ Ba",
            "Wednesday": "Thứ Tư",
            "Thursday": "Thứ Năm",
            "Friday": "Thứ Sáu",
            "Saturday": "Thứ Bảy",
            "Sunday": "Chủ Nhật"
        }

        for index in list_data:
            Date, time = index.get('dt_txt').split(' ')
            timestamp = index.get('dt_txt')
            date = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
            day_of_week = date.strftime('%A')

            if current_date is None:
                current_date = Date

            if Date != current_date:
                weather[day_counter][f'Day{day_counter + 1}'] = ob
                ob = {
                    'Times': [],
                    'Weather': {
                        'Temperature': [],
                        'Humidity': [],
                        'Icon': [],
                        'Icon_title': [],
                        'Description': []
                    },
                    'Wind': {
                        'Speed': []
                    },
                    'Day': ''
                }
                current_date = Date
                day_counter += 1
                if day_counter >= 5:  # Chỉ lấy dữ liệu của 5 ngày đầu tiên
                    break

            ob['Times'].append(time)
            ob['Weather']['Temperature'].append(index['main']['temp'])
            ob['Weather']['Humidity'].append(index['main']['humidity'])
            ob['Weather']['Icon'].append(f'https://openweathermap.org/img/wn/{index["weather"][0]["icon"]}.png')
            ob['Weather']['Icon_title'].append(
                f'https://openweathermap.org/img/wn/{index["weather"][0]["icon"]}@2x.png')
            ob['Wind']['Speed'].append(int(index['wind']['speed'] * 3.6))
            ob['Day'] = Date_in_week.get(day_of_week)
            ob['Weather']['Description'].append(index['weather'][0]['description'])

        if ob and day_counter < 5:
            weather[day_counter][f'Day{day_counter + 1}'] = ob

        if not weather:
            return {message: "Data not found"}, 404
        else:
            return weather, 200

class Light(Resource):
    def get(self):
        return light, 201
    def put(self):
        data = request.get_json()
        if data:
            light['status'] = data['status']
            return light, 201
        else:
            return {message: "No Data"}, 404

class Fan(Resource):
    def get(self):
        return fan, 201
    def put(self):
        data = request.get_json()
        print(data)
        if data:
            fan.update(data)
            return fan, 201
        else:
            return {message: "No Data"}, 404

class WarningTemperature(Resource):
    def get(self):
        return warningTemperature, 201
    def put(self):
        data = request.get_json()
        if data:
            warningTemperature.update(data)
            return warningTemperature, 201
        else:
            return {message: "No Data"}, 404

class WarningGas(Resource):
    def get(self):
        return warningGas, 201
    def put(self):
        data = request.get_json()
        if data:
            warningGas.update(data)
            return warningGas, 201
        else:
            return {message: "No Data"}, 404

class history_data_pir(Resource):
    def get(self):
        result = {}
        data = History_Pir.query.all()
        data_time = [element.timestamp.strftime('%d/%m/%Y %H:%M:%S') for element in data]
            
        result.update({'time': data_time})
        
        return result, 200
        
module_api.add_resource(dht11, '/api/dht11')
module_api.add_resource(motionPir, '/api/motion')
module_api.add_resource(mqt2_api, '/api/mqt2')
module_api.add_resource(Light, '/api/light')
module_api.add_resource(Fan, '/api/fan')
module_api.add_resource(WarningTemperature, '/api/warningTemperature')
module_api.add_resource(WarningGas, '/api/warningGas')
module_api.add_resource(weather_forecast, '/api/weather_forecast')
module_api.add_resource(history_data_pir_5, '/api/data_pir_5')
module_api.add_resource(history_data_pir, '/api/data_pir')