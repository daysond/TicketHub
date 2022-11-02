from APP import app
from flask import render_template, redirect, url_for, flash, get_flashed_messages, request
from flask_login import login_user, logout_user, login_required, current_user
from APP.models import Concert, User, Venue, Event, Ticket, Seating
from APP.forms import PurchaseForm
from APP import db


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

@app.route('/purchase_ticket/<event_id>', methods=['GET', 'POST'])
def purchase_ticket(event_id):
    purchase_form = PurchaseForm()
    event = Event.query.filter_by(id=event_id).first()
    if request.method == 'POST':
        event_id = request.form.get("purchased_ticket")
        #purchase ticket logic here:
        #need to impletement seating choose.
        seating = event.seatings[0]
        user = User.query.filter_by(id=1).first()
        #mind tickets amount
        ticket = Ticket(seating_id = seating.id, user_id = user.id)
        #some other logic dealing with balance.
        db.session.add(ticket)
        seating = Seating.query.get(seating.id)
        #make sure its less than max
        seating.seats_sold = seating.seats_sold + 1
        db.session.commit()
        
    return render_template('ticket.html', purchase_form = purchase_form, event = event)
