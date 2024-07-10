from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

data_sensor_dht11 = {
    'temperature': None,
    'humidity': None
}

status_pir = {
    'status': None
}

led = {
    'Led_Main': False,
    'Led_D7': False,
    'Led_D8': False
}


@app.route('/')
def home():
    return render_template('index.html')


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
        new_status = data.get('state')
        if led_name in led:
            led[led_name] = new_status
            print(led)
            return jsonify({led_name: new_status}), 200
        else:
            return jsonify({'error': 'Đèn không tồn tại'}), 404
    else:
        return jsonify(led)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')