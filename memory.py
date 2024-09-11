
class dht11(Resource):
    def get(self):
        return data_sensor_dht11

    def post(self):
        data = request.get_json()
        data_sensor_dht11.update(data)
        if data:
            return data, 200
        else:
            return abort("data of dht11_sensor not found"), 400


api.add_resource(dht11, '/api/weather')


# api pir HC-SR501 (database)
class dataPir(Resource):

    def get(self):
        p = {'data': []}
        size = History_Pir.query.count()

        if size <= 5:
            data_pir = History_Pir.query.all()

        else:
            start = size - 4
            end = size
            data_pir = History_Pir.query.filter(History_Pir._id >= start, History_Pir._id <= end).all()

            data_time_to_dict = [data.timestamp.strftime('%d/%m/%Y %H:%M:%S') for data in data_pir]
            data_area_to_dict = [data.area for data in data_pir]

        p['data'].append({'time': data_time_to_dict, 'area': data_area_to_dict})

        return p, 200


api.add_resource(dataPir, '/data_pir')


# api motion của pir
class motionPir(Resource):
    def get(self):
        return status_pir, 200

    def post(self):
        data = request.get_json()
        status_pir.update(data)

        if data['Bathroom'] == True:
            detected = History_Pir('Phòng Tắm')
            db.session.add(detected)
            db.session.commit()

        if data['Area2'] == True:
            detected = History_Pir('Area2')
            db.session.add(detected)
            db.session.commit()

        if data:
            return data, 200
        else:
            return abort("No data"), 400


api.add_resource(motionPir, '/api/motion')


# api mqt135
class mqt135_api(Resource):
    def get(self):
        return data_check_mqt135, 200

    def post(self):

        data = request.get_json()
        data_check_mqt135.update(data)

        if data:
            return data_check_mqt135, 200
        else:
            return abort('No data'), 400


api.add_resource(mqt135_api, '/api/mqt135')


# api weather-forecast
class weather_forecast(Resource):
    def get(self):
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
            ob['Weather']['Icon_title'].append(
                f'https://openweathermap.org/img/wn/{index["weather"][0]["icon"]}@2x.png')
            ob['Wind']['Speed'].append(int(index['wind']['speed'] * 3.6))
            ob['Day'] = Date_in_week.get(day_of_week)
            ob['Weather']['Description'].append(index['weather'][0]['description'])

        if ob and day_counter < 5:
            weather[day_counter][f'Day{day_counter + 1}'] = ob

        if not weather:
            return abort(404, "Data not found")

        else:
            return weather, 200

api.add_resource(weather_forecast, '/api/weather_forecast')


# api của đèn
class toggleLed(Resource):
    def get(self):
        return led, 200

    def put(self, led_name, status):

        if led_name not in led:
            return abort(404, description='LED not found')

        try:

            if led_name != "Led_Main":
                if status == 'On':
                    led[led_name] = 1023
                else:
                    led[led_name] = 0

            else:
                if status == 'On':
                    led[led_name] = 0
                else:
                    led[led_name] = 1023
        except:
            abort(400, description='Error status')

        return led, 200

    def post(self):
        data = request.get_json()

        led.update(data)

        return data, 200


api.add_resource(toggleLed, '/api/change_status_led', '/api/change_status_led/<string:led_name>/<string:status>')

# Phần này xử lý thao tác module => => => => =>
data_sensor_dht11 = {
    'temperature': None,
    'humidity': None
}

status_pir = {
    'Bathroom': None,
    'Area2': None
}

led = {
    'Led_Main': 1023,
    'Led_D7': 0,
    'Led_D8': 0
}

data_check_mqt135 = {'value': 0}
