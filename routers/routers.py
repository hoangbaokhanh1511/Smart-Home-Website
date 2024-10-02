from flask import Blueprint, render_template, redirect, url_for, session, request, jsonify, Response
import requests
from app import db
from datetime import datetime
from models.historyPir_models import History_Pir

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    if session and session.get('username') == 'admin':
        return redirect(url_for('main.mainpage'))
    return redirect(url_for('main.login'))

@main_bp.route('/main')
def mainpage():
    if session and session['username'] == 'admin':
        return render_template('home.html', username = session['username'], Id = session['id'][-4:])
    else:
        return render_template('Page404.html')

@main_bp.route('/login')
def login():
    return render_template('login.html')


@main_bp.route('/main/device')
def device():
    return render_template('device.html')

@main_bp.route('/main/history/delete', methods=['DELETE'])
def delete_history():
    data = request.get_json()
    timestamps = data.get('timestamps', [])

    if timestamps:
        for timestamp in timestamps:
            entry_to_delete = History_Pir.query.filter_by(timestamp=datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')).first()
            if entry_to_delete:
                db.session.delete(entry_to_delete)
        db.session.commit()
        return jsonify({"message": "Xóa thành công!"}), 200
    
    return jsonify({"message": "Không có dữ liệu nào để xóa."}), 400

@main_bp.route('/main/history', methods=['GET', 'POST'])
def history():
    filtered_data = History_Pir.query.all()
    
    if request.method == 'POST':
        data = request.json
        start_date = datetime.strptime(data['startDate'], '%Y-%m-%d')
        end_date = datetime.strptime(data['endDate'], '%Y-%m-%d')
        
        filtered_data = History_Pir.query.filter(History_Pir.timestamp >= start_date, History_Pir.timestamp <= end_date).all()

        results = [{'timestamp': entry.timestamp.strftime('%d/%m/%Y %H:%M:%S')} for entry in filtered_data]
        
        return jsonify(results)

    return render_template('history.html', data = filtered_data)


@main_bp.route('/signup')
def signup():
    return render_template('signup.html')