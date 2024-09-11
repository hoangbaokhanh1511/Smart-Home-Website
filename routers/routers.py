from flask import Blueprint, render_template, redirect, url_for

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    return redirect(url_for('main.login'))

@main_bp.route('/login')
def login():
    return render_template('home.html')

@main_bp.route('/signup')
def signup():
    return render_template('home.html')