from flask import Flask, render_template, send_file, url_for, jsonify, redirect, session, request, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import requests, io, sys, json

app = Flask(__name__)
app.secret_key = "HelloWorld!!"

"""
Một số câu lệnh query dùng cho database sqlite3 trong web framework flask
db.session.add() => thêm element vào database
db.session.add_all() => thêm nhiều element vào database
db.session.delete() => xóa element khỏi database
db.session.execute() => thực hiện câu lệnh SQL trực tiếp vd db.session.execute("Select * From Users)
db.session.query() => thực hiện truy vấn trong sql
''.query.filter() => tìm kiếm có điều kiện
''.query.filter(thuộc_tính.like('%target%')) => tìm kiếm tương đối
-> sắp xếp query.order_by(thuộc tính.asc[hoặc desc]()).all() => asc là bé > lớn, desc là lớn > bé  
db.session.commit() => lưu các thay đổi sau khi truy vấn
"""

# Database của pir làm database chính
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pir.sqlite3'  # Tạo database có tên là users
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # theo dõi các sửa đổi object và phát tín hiệu

db = SQLAlchemy(app)  # Khởi tạo database (cả database chình và phụ)


class History_Pir(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)

    timestamp = db.Column("Timestamp", db.DateTime,
                          default=None)  # lấy thời gian hiện với với múi giờ tương ứng

    def __init__(self):
        now = datetime.now()
        self.timestamp = now.replace(microsecond=0)  # bỏ phần microsecond chỉ lấy ngang hh:mm:ss

    def __repr__(self):
        return f"{self.timestamp}"


@app.route('/')
def home():


    return render_template('home.html')

@app.route('/data_pir')
def data_pir():
    size = History_Pir.query.count()

    if size <= 5:
        data_pir = History_Pir.query.all()

    else:
        start = size - 4
        end = size
        data_pir = History_Pir.query.filter(History_Pir._id >= start, History_Pir._id <= end).all()

    data_to_dict = []
    for data in data_pir:

        formatted_time = data.timestamp.strftime('%d/%m/%Y %H:%M:%S')
        data_to_dict.append(formatted_time)

    return jsonify({'data': data_to_dict})


# Phần này xử lý thao tác module => => => => =>
data_sensor_dht11 = {
    'temperature': None,
    'humidity': None
}

status_pir = {
    'status': None
}

led = {
    'Led_Main': 1023,
    'Led_D7': 0,
    'Led_D8': 0
}

mqt135 = {
    'value': 0
}


# Xử lý mqt135
@app.route('/api/mqt135', methods=['POST', 'GET'])
def get_mqt135():
    if request.method == 'POST':
        data = request.get_json()
        mqt135.update(data)
        if data:
            return jsonify({"status": "success", "data_received": data}), 200
        else:
            return jsonify({"status": "error", "message": "No data received"}), 400
    else:
        return jsonify(mqt135)


# Xử lý dht11
@app.route('/api/weather', methods=['POST', 'GET'])
def get_weather():
    if request.method == 'POST':  # nhận dữ liệu từ mạch
        data = request.get_json()  # lấy dữ liệu được truyền thành file json
        data_sensor_dht11.update(data)  # cập nhật dữ liệu
        if data:
            return jsonify({"status": "success", "data_received": data}), 200
        else:
            return jsonify({"status": "error", "message": "No data received"}), 400

    else:
        return jsonify(data_sensor_dht11)  # Cập nhật api json


# xử lý pir sensor HC-SR501
@app.route('/api/motion', methods=["POST", "GET"])
def receive_data_motion():
    if request.method == 'POST':
        data = request.get_json()
        status_pir.update(data)

        if data.get('status') == True:
            detected = History_Pir()
            db.session.add(detected)
            db.session.commit()

        if data:
            return jsonify({"status": "success", "data_received": data}), 200
        else:
            return jsonify({"status": "error", "message": "No data received"}), 400
    else:
        return jsonify(status_pir)


# Bật/Tắt Đèn
@app.route('/api/change_status_led', methods=["POST", "GET"])
def change_status_led():
    if request.method == "POST":
        data = request.json
        led_name = data.get('led_name')
        new_value = data.get('value')
        if led_name in led:
            led[led_name] = new_value
            return jsonify({led_name: new_value}), 200
        else:
            return jsonify({'error': 'Đèn không tồn tại'}), 404
    else:
        return jsonify(led)


@app.route('/api/weather_forecast')
def graph():
    response = requests.get(
        'http://api.openweathermap.org/data/2.5/forecast?q=Hue&appid=07bb5510d2576951d78b0f0b637f4716&units=metric&lang=vi')
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
        ob['Weather']['Icon_title'].append(f'https://openweathermap.org/img/wn/{index["weather"][0]["icon"]}@2x.png')
        ob['Wind']['Speed'].append(int(index['wind']['speed'] * 3.6))
        ob['Day'] = Date_in_week.get(day_of_week)
        ob['Weather']['Description'].append(index['weather'][0]['description'])

    if ob and day_counter < 5:
        weather[day_counter][f'Day{day_counter + 1}'] = ob

    return jsonify(weather)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True, host='0.0.0.0')
