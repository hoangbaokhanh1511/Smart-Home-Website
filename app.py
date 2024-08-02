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

# Database của users làm database chính
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'  # Tạo database có tên là users
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # theo dõi các sửa đổi object và phát tín hiệu
# database của pir HC-SR501
app.config['SQLALCHEMY_BINDS'] = {
    'pir': 'sqlite:///pir.sqlite3',
    'pending': 'sqlite:///pendingUsers.sqlite3'
}

db = SQLAlchemy(app)  # Khởi tạo database (cả database chình và phụ)


class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("username", db.String(100))
    password = db.Column("password", db.String(100))

    def __init__(self, name, password):
        self.name = name
        self.password = password

    def __repr__(self):
        return f"Name: {self.name}, Password: {self.password}"


class History_Pir(db.Model):
    __bind_key__ = 'pir'
    _id = db.Column("id", db.Integer, primary_key=True)
    timestamp = db.Column("Timestamp", db.DateTime,
                          default=None)  # lấy thời gian hiện với với múi giờ tương ứng

    def __init__(self):
        now = datetime.now()
        self.timestamp = now.replace(microsecond=0)  # bỏ phần microsecond chỉ lấy ngang hh:mm:ss

    def __repr__(self):
        return f"{self.timestamp}"


class pendingUsers(db.Model):
    __bind_key__ = 'pending'
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('Username', db.String(100))
    password = db.Column('Password', db.String(100))

    def __init__(self, name, password):
        self.name = name
        self.password = password

    def __repr__(self):
        return f"Name: {self.name}, Password: {self.password}"


@app.route('/')
def home():
    return redirect(url_for('login'))


@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        handle = request.form['handle']
        if handle == "Login":

            username = request.form['username']  # lấy username vào phiên làm việc
            password = request.form['password']  # lấy password vào phiên làm việc

            found_user = users.query.filter_by(name=username, password=password).first()

            if found_user:

                session['username'] = found_user.name

                return redirect(url_for('user_dashboard'))

            else:
                flash("Sai tài khoản mật khẩu !", "error")
                return render_template('login.html')

        else:
            return redirect(url_for('signup'))

    else:
        if 'username' in session:
            return redirect(url_for('user_dashboard'))
        return render_template('login.html')


@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "POST":

        user = request.form['username']
        pas = request.form['password']

        found_user = users.query.filter_by(name=user).first()

        if user and pas:

            if not found_user:

                # Thêm thông tin vào database
                new_user = pendingUsers(user, pas)
                db.session.add(new_user)
                db.session.commit()

                flash("Đăng ký thành công", "success")
                return redirect(url_for('login'))

            else:
                flash("Tài Khoản đã tồn tại")

        else:

            flash("Vui lòng nhập đủ thông tin")

    return render_template('signup.html')


username = ""


@app.route('/user_dashboard', methods=["GET", "POST"])
def user_dashboard():
    global username
    if request.method == "GET":

        print(pendingUsers.query.all())

        username = session['username']
        start = 0
        end = 0
<<<<<<< HEAD

        if History_Pir.query.count() > 0:
            start = History_Pir.query.first().timestamp.date()
            end = History_Pir.query.order_by(History_Pir.timestamp.desc()).first().timestamp.date()
=======
        if History_Pir.query.count() > 0:

            start = History_Pir.query.first().timestamp.date()
            end = History_Pir.query.order_by(History_Pir.timestamp.desc()).first().timestamp.date()

            two_days = start + timedelta(days=2)  # Lấy thời gian

            while (end - two_days).days >= 2:

                dell = History_Pir.query.filter(History_Pir.timestamp.between(start, two_days)).all()

                for data in dell:
                    db.session.delete(data)
                db.session.commit()

                start = two_days
                two_days = two_days + timedelta(days=2)

            # Nếu có xóa thì phải cập nhật lại ID
            all_pir = History_Pir.query.all()
            for index, data in enumerate(all_pir, start=1):
                data._id = index
            db.session.commit()
>>>>>>> backend

        if 'username' in session:
            return render_template('userpage.html', username=username, start=start, end=end)


        else:
            flash("Bạn cần phải đăng nhập trước", "error")
            return redirect(url_for('login'))


    else:
        handle = request.form.get('button')
        if handle == "Logout":
            session.pop('username', None)
            flash("Đăng xuất thành công", "success")
            return redirect(url_for('login'))

        elif handle == "Date":

            start = request.form.get('startDate')
            end = request.form.get('endDate')

            start_date = datetime.strptime(start, '%Y-%m-%d')
            end_date = datetime.strptime(end, '%Y-%m-%d')

            result = History_Pir.query.filter(History_Pir.timestamp.between(start_date, end_date)).all()

            return render_template('userpage.html', username=username, result=result, status="OFF")

        elif handle == "Overal":
            return render_template('userpage.html', status="ON", username=username)

        else:
            username = session['username']
            return redirect(url_for('change'))


@app.route('/change', methods=['GET', 'POST'])
def change():
    found_user = users.query.filter_by(name=session['username']).first()
    if request.method == "GET":
        return render_template('change.html')
    else:
        oldpass = request.form['oldPassword']
        newpass = request.form['newPassword']
        repeat = request.form['repeatPassword']
        if not oldpass or not newpass or not repeat:
            flash('Vui lòng điền đầy đủ thông tin', 'error')
        else:
            if found_user.password != oldpass:
                flash('Password cũ không đúng', 'error')
            if newpass != repeat:
                flash('Password repeat không trùng', 'error')
            if newpass == oldpass:
                flash('Trùng với password cũ', 'error')

        if found_user.password == oldpass and newpass == repeat and newpass != oldpass:
            flash('Thay đổi thành công', 'success')
            found_user.password = newpass
            db.session.commit()
        return render_template('change.html', key=found_user.name)

    # Ở phía qtv


@app.route('/view/database', methods=['GET', 'POST'])
def data():
    if request.method == 'GET':
        query = request.args.get('query')  # lấy dữ liêu từ url

        if query:
            result = users.query.filter(users.name.like(f"%{query}%")).all()  # => tìm kiếm tương đối
        else:
            result = users.query.all()

        result2 = pendingUsers.query.all()

        return render_template('view.html', data=result, pending=result2, query=query)

    else:
        handle = request.form['handle']

        if handle == 'Add':

            username = request.form['username']
            password = request.form['password']

            if username and password:
                found_user = users.query.filter_by(name=username).first()
                if found_user:
                    flash("Tài khoản đã tồn tại", "error")
                else:

                    new_user = users(username, password)
                    db.session.add(new_user)
                    db.session.commit()

                    flash('Tài khoản đã được thêm')
            else:
                flash('Vui lòng nhập đủ thông tin', 'error')


        elif handle == 'Remove':

            username = request.form['username']
            found_user = users.query.filter_by(name=username).first()
            if found_user:
                db.session.delete(found_user)
                db.session.commit()
                flash("Xóa tài khoản thành công", 'success')

                # Tiến hành đánh số lại id
                # enumerate là một hàm trong Python được sử dụng để đánh số
                # các phần tử của một iterable (như list, tuple, hoặc string)
                # và trả về một đối tượng enumerate
                # cú pháp enumerate(iterable, start=0)

                all_user = users.query.all()
                for index, user in enumerate(all_user, start=1):
                    user._id = index
                db.session.commit()

            else:
                flash('Không tìm thấy tài khoản', 'error')

        elif handle == 'Save':
            form_data = request.form.to_dict(flat=False)  # Chuyển dữ liệu ImmutableMultiDict thành Dictionary

            size = users.query.count()  # Đếm số user trong database

            Newpass = form_data.get('newPassword')
            OldPass = form_data.get('oldPassword')
            getID = form_data.get('ID')

            for step in range(size):

                if Newpass[step] != OldPass[step]:
                    user = users.query.filter_by(_id=getID[step]).first()
                    user.password = Newpass[step]

            db.session.commit()

        elif handle == "Submit Change":

            data = request.form.to_dict(flat=False)

            user = data.get('user')
            if user == None:
                pass

            else:
                for index in user:
                    Id, status = index.split(' ')
                    Id = int(Id)

                    clone_user = pendingUsers.query.filter_by(id=Id).first()
                    if status == 'True':
                        newUser = users(clone_user.name, clone_user.password)

                        db.session.add(newUser)

                    db.session.delete(clone_user)

                all_user = pendingUsers.query.all()
                for index, user in enumerate(all_user, start=1):
                    user.id = index

                db.session.commit()

        result1 = users.query.all()
        result2 = pendingUsers.query.all()

        return render_template('view.html', data=result1, pending=result2)


@app.route('/view/history_pir')
def history_pir():
    if username == "":
        flash('Bạn phải đăng nhập trước')
        return redirect(url_for('login'))

    start = History_Pir.query.first()
    end = History_Pir.query.order_by(History_Pir.timestamp.desc()).first()
    if start and end:

        return render_template('pir.html', data=History_Pir.query.all(), startTime=start, endTime=end)

    else:

        return render_template('pir.html', data=History_Pir.query.all())


@app.route('/view/weather')
def five_days_weather():
    result = get_weather_for_five_days()
    return render_template('weather.html', result=result)


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
@app.route('/user_dashboard/api/mqt135', methods=['POST', 'GET'])
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
@app.route('/user_dashboard/api/weather', methods=['POST', 'GET'])
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
@app.route('/user_dashboard/api/motion', methods=["POST", "GET"])
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
@app.route('/user_dashboard/api/change_status_led', methods=["POST", "GET"])
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


def get_weather_for_five_days():
    data = requests.get(
        'http://api.openweathermap.org/data/2.5/forecast?q=Hue&appid=07bb5510d2576951d78b0f0b637f4716&units=metric&lang=vi').json()
    if data['cod'] != '200':
        print('Error')
        return

    data_weather = []
    for i in range(len(data['list'])):
        if data['list'][i]['dt_txt'].endswith('00:00:00'):
            temp = int(data['list'][i]['main']['temp'])
            hum = data['list'][i]['main']['humidity']
            icon = data['list'][i]['weather'][0]['icon']
            icon_url = f"http://openweathermap.org/img/wn/{icon}@2x.png"
            date = datetime.strptime(data['list'][i]['dt_txt'], '%Y-%m-%d %H:%M:%S')
            element = {
                "temp": int(temp),
                'humidity': hum,
                "icon_url": icon_url,
                "date_of_week": date.strftime("%A")
            }

            data_weather.append(element)

    return data_weather


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
<<<<<<< HEAD
    app.run(debug=True, host='0.0.0.0')
=======

    app.run(debug=True, host='0.0.0.0')
>>>>>>> backend
