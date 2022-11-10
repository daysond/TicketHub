from APP import app
from flask import render_template, redirect, url_for, flash, get_flashed_messages, request
from flask_login import login_user, logout_user, login_required, current_user
from APP.models import Concert, User, Venue, Event, Ticket, Seating
from APP.forms import PurchaseForm, LoginForm, RegisterForm
from APP import db
from collections import namedtuple

@app.route('/')
@app.route('/home')
def home():
    feat_venues = Venue.query.filter_by(featured=True)
    feat_events = Event.query.filter_by(featured=True)
    
    return render_template('home.html', venues = feat_venues, events = feat_events)


@app.route('/venues')
def venues():
    all_venues = Venue.query.all() 
    return render_template('venues.html', events = all_venues)

@app.route('/events')
def events():
    all_events = Event.query.all()
    return render_template('events.html', events = all_events)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(name=form.username.data).first()
        if attempted_user and attempted_user.check_password(form.password.data):
            login_user(attempted_user)
            flash(f'Login successfully. Welcome {attempted_user.name}' , category = 'success')
            return redirect(url_for('home'))
        else:
            flash(f'Wrong username or password. Please try again!' , category = 'danger')
        
    return render_template('login.html', form = form)


@app.route('/logout', methods = ['GET', 'POST'])
def logout():
    logout_user()
    flash(f'Log out successfully.' , category = 'info') 
    return redirect(url_for('home'))


@app.route('/register', methods = ['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(name=form.username.data,
                        email=form.email_address.data,
                        password=form.password.data)
        print("creating new user")
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        flash(f'Welcome {new_user.name}!' , category = 'success')
        
        return redirect(url_for('home'))
    if form.errors != {}:
        for err in form.errors.values():
            print(f'Error: {err}')
            flash(f'Error: {err}')
            
    return render_template('register.html', form = form)


@app.route('/purchase_ticket/<event_id>', methods=['GET', 'POST'])
def purchase_ticket(event_id):
    
    purchase_form = PurchaseForm()
    event = Event.query.filter_by(id=event_id).first()
    
    if request.method == 'POST':
        can_purchase = True
        for seating in event.seatings:
            seating_qty = int(request.form.get(str(seating.id)))
            if seating.seats_available < seating_qty:
                can_purchase = False
                flash(f'Not enough ticket available.' , category = 'danger')  
                break 
        if can_purchase:
            Item = namedtuple("Item", 'seating qty')
            items = [Item(seating, int(request.form.get(str(seating.id)))) for seating in event.seatings]
            make_purchases(items, current_user.id)
        
    return render_template('ticket.html', purchase_form = purchase_form, event = event)
    
def make_purchases(items, user_id):
    cart = [] #list of tickets
    for (seating, qty) in items:
        for i in range(0, qty):
            cart.append(Ticket(seating_id = seating.id, user_id = current_user.id))
        seating.seats_sold += qty
    db.session.add_all(cart)
    db.session.commit()

@app.route('/checkout', methods=['GET','POST'])
def checkout():
    return render_template('checkout.html')
"""
implement a shopping cart, check out, payment,  ect 

    for(let i = 0; i<numSeats;i++) {
        const minusButton = document.getElementById('minus_'.concat({{event.seatings[i].id|safe}}));
        const plusButton = document.getElementById('plus_'.concat({{event.seatings[i].id|safe}}));
        const inputField = document.getElementById({{event.seatings[i].id|safe}});

        minusButton.addEventListener('click', event => {
            event.preventDefault();
            const currentValue = Number(inputField.value) || 0;
            if(currentValue>0)
                inputField.value = currentValue - 1;
            });
    
        plusButton.addEventListener('click', event => {
            event.preventDefault();
            const currentValue = Number(inputField.value) || 0;
            if(currentValue<4)
                inputField.value = currentValue + 1;
            });
    }
"""
