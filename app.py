from flask import Flask, render_template, url_for, jsonify, redirect, session, request, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "HelloWorld!!"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'  # Tạo database có tên là users
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # theo dõi các sửa đổi object và phát tín hiệu

db = SQLAlchemy(app)  # khai báo


class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("username", db.String(100))
    password = db.Column("password", db.String(100))

    def __init__(self, name, password):
        self.name = name
        self.password = password


@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == "POST":
        return redirect(url_for('login'))
    else:
        return render_template('home.html')


@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":

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
                new_user = users(user, pas)
                db.session.add(new_user)
                db.session.commit()

                flash("Đăng ký thành công", "success")
                return redirect(url_for('login'))

            else:
                flash("Tài Khoản đã tồn tại")

        else:

            flash("Vui lòng nhập đủ thông tin")

    return render_template('signup.html')


@app.route('/user_dashboard', methods=["GET", "POST"])
def user_dashboard():
    if request.method == "GET":

        if 'username' in session:
            username = session['username']
            return render_template('userpage.html', username=username)
        else:
            flash("Bạn cần phải đăng nhập trước", "error")
            return redirect(url_for('login'))


    else:  # log out xóa data khỏi phiên làm việc

        session.pop('username', None)
        flash("Đăng xuất thành công", "success")
        return redirect(url_for('login'))


@app.route('/view/database')
def data():
    return render_template('view.html', data=users.query.all())


# Phần này xử lý thao tác module => => => => =>
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
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0')