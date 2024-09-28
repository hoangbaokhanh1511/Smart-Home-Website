from flask import Blueprint, render_template, redirect, url_for, session
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

@main_bp.route('/main/history')
def history():
    return render_template('history.html')

@main_bp.route('/signup')
def signup():
    return render_template('signup.html')

@main_bp.route('/demo')
def demo():
    data = History_Pir.query.all()
    return render_template('demo.html', data = data)