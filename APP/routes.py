from App import app
from flask import render_template, redirect, url_for, flash, get_flashed_messages, request
from flask_login import login_user, logout_user, login_required, current_user
from App.models import Concert, User, Venue, Event
# from App.forms import RegisterForm, LoginForm, PurchaseForm
from App import db


@app.route('/')
@app.route('/home')
def home():
    feat_venues = Venue.query.all() #filter by feature
    feat_events = Event.query.all()
    return render_template('home.html', venues = feat_venues, events = feat_events)

@app.route('/venues')
def venue():
    print('called venue')
    return 'Venues'

