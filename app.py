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
        username = session['username']
        if 'username' in session:

            return render_template('userpage.html', username=username)
        else:
            flash("Bạn cần phải đăng nhập trước", "error")
            return redirect(url_for('login'))


    else:  # log out xóa data khỏi phiên làm việc
        handle = request.form['handle']

        if handle == "Logout":
            session.pop('username', None)
            flash("Đăng xuất thành công", "success")
            return redirect(url_for('login'))
        else:
            username = session['username']

            return redirect(url_for('change'))


@app.route('/change', methods=['GET', 'POST'])
def change():
    found_user = users.query.filter_by(name=session['username']).first()
    if request.method == "GET":
        return render_template('change.html', key=found_user.name)
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


@app.route('/view/database')
def data():
    query = request.args.get('query')  # lấy dữ liêu từ url

    if query:
        result = users.query.filter(users.name.like(f"%{query}%")).all()  # => tìm kiếm tương đối
    else:
        result = users.query.all()

    return render_template('view.html', data=result, query=query)


# Phần này xử lý thao tác module => => => => =>
status_pir = {
    'status': None
}

led = {
    'Led_Main': False,
    'Led_D7': False,
    'Led_D8': False
}

DATA = {}
# Xử lý dht11
@app.route('/user_dashboard/api/weather', methods=['POST', 'GET'])
def get_weather():

    if request.method == 'POST':  # nhận dữ liệu từ mạch
        data = request.get_json()  # lấy dữ liệu được truyền thành file json
        DATA.update((data))
        if data:

            return jsonify({"status": "success", "data_received": data}), 200
        else:
            return jsonify({"status": "error", "message": "No data received"}), 400

    else:
        return jsonify(DATA)  # Cập nhật api json


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