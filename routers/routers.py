from flask import Blueprint, render_template, redirect, url_for, session, request, jsonify, Response
import requests
from app import db
from datetime import datetime
from models.historyPir_models import History_Pir
from models.user_models import userManager
from middleware.middleware import auth

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
@auth
def home():
    if session and session.get('username') == 'admin':
        return redirect(url_for('main.mainpage'))
    return redirect(url_for('main.login'))


@main_bp.route('/login')
def login():
    return render_template('login.html')


@main_bp.route('/signup')
def signup():
    return render_template('signup.html')


@main_bp.route('/main')
@auth
def mainpage():
    if session and session['username'] == 'admin':
        return render_template('home.html', username=session['username'], Id=session['id'][-4:])
    else:
        return render_template('Page404.html')


@main_bp.route('/main/device')
@auth
def device():
    return render_template('device.html', username=session['username'], Id=session['id'][-4:])


@main_bp.route('/main/history/delete', methods=['DELETE'])
def delete_history():
    data = request.get_json()
    timestamps = data.get('timestamps', [])

    if timestamps:
        for timestamp in timestamps:
            print("Received timestamp:", timestamp)
            try:
                timestamp_obj = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
                entry_to_delete = History_Pir.query.filter_by(timestamp=timestamp_obj).first()

                if entry_to_delete:
                    db.session.delete(entry_to_delete)
            except ValueError:
                return jsonify({"message": f"Timestamp {timestamp} không hợp lệ."}), 400

        db.session.commit()
        return jsonify({"message": "Xóa thành công!"}), 200

    return jsonify({"message": "Không có dữ liệu nào để xóa."}), 400


@main_bp.route('/main/history', methods=['GET', 'POST'])
@auth
def history():
    filtered_data = History_Pir.query.all()

    if request.method == 'POST':
        data = request.json
        start_date = datetime.strptime(data['startDate'], '%Y-%m-%d')
        end_date = datetime.strptime(data['endDate'], '%Y-%m-%d')

        filtered_data = History_Pir.query.filter(History_Pir.timestamp >= start_date,
                                                 History_Pir.timestamp <= end_date).all()

        results = [{'timestamp': entry.timestamp.strftime('%d/%m/%Y %H:%M:%S')} for entry in filtered_data]

        return jsonify(results)

    return render_template('history.html', data=filtered_data, username=session['username'], Id=session['id'][-4:])


@main_bp.route('/api/history')
@auth
def api_history():
    filtered_data = History_Pir.query.all()
    data = [obj.to_dict() for obj in filtered_data]
    return jsonify(data)


@main_bp.route('/main/changepass', methods=['GET', 'POST'])
@auth
def changepass():
    return render_template('changepass.html', username=session['username'])


@main_bp.route('/main/profile', methods=['GET', 'POST'])
@auth
def profile():
    username = session['username']
    name, email, gender, birthday, phone, address = userManager.findUser(username)
    gender = 'Nam' if gender == 1 else 'Nữ'

    if request.method == "POST":
        print(request.form)
    return render_template('updateProfile.html', username=username, name=name, email=email, gender=gender,
                           birthday=birthday, phone=phone, address=address)