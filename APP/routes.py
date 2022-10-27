from App import app
from flask import render_template, redirect, url_for, flash, get_flashed_messages, request
from flask_login import login_user, logout_user, login_required, current_user
from App.models import Concert, User
# from App.forms import RegisterForm, LoginForm, PurchaseForm
from App import db


@app.route('/')
@app.route('/home')
def home():
    print('called home')
    return render_template('home.html')
