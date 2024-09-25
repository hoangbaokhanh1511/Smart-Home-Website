from flask import Blueprint, render_template, redirect, url_for, session

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    return redirect(url_for('main.login'))

@main_bp.route('/main')
def mainpage():
    if session and session['username'] == 'admin':
        return render_template('home.html')
    else:
        return render_template('Page404.html')

@main_bp.route('/login')
def login():
    return render_template('login.html')

@main_bp.route('/main/device')
def device():
    return render_template('device.html')

@main_bp.route('/signup')
def signup():
    return render_template('signup.html')
