from APP import db
from flask_login import UserMixin


class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column('name', db.String, nullable=False, unique=True)
    email = db.Column('email', db.String, nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)

    tickets = db.relationship("Ticket", back_populates="user")

    def __repr__(self):
        return f'Username: {self.name}'


# Event manaement company
class EMC(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column('name', db.String, nullable=False, unique=True)
    balance = db.Column(db.Numeric(
        precision=2, asdecimal=False), nullable=False, default=0)

    events = db.relationship('Event', back_populates='emc')


class Concert(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=64), nullable=False, unique=True)
    artist = db.Column(db.String(length=64), nullable=False)

    events = db.relationship("Event", back_populates="concert")

    def __repr__(self):
        return f'Username: {self.name}'


class Venue(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=64), nullable=False, unique=True)
    address = db.Column(db.String(length=255), nullable=False, unique=True)

    sections = db.relationship('Venue_Section', back_populates='venue')
    events = db.relationship('Event', back_populates='venue')

    def __repr__(self):
        return f'Username: {self.name}'


class Event(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    description = db.Column(db.String(length=1024),
                            nullable=False, unique=True)
    availablePercentage = db.Column(db.Integer, nullable=True, default=100)
    image_url = db.Column(db.String(length=1024), nullable=False)
    
    venue_id = db.Column(db.Integer, db.ForeignKey(Venue.id))
    venue = db.relationship("Venue", back_populates='events')

    emc_id = db.Column(db.String(length=30), db.ForeignKey(EMC.id))
    emc = db.relationship("EMC", back_populates='events')

    concert_id = db.Column(db.Integer, db.ForeignKey(Concert.id))
    concert = db.relationship("Concert", back_populates="events")

    seatings = db.relationship("Seating", back_populates='event')


    def __repr__(self):
        return f'Event: {self.description} {self.concert.name}'


class Venue_Section(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    num_of_seats = db.Column(db.Integer, nullable=False)
    sec_name = db.Column(db.String(length=60), nullable=False)

    venue_id = db.Column(db.Integer, db.ForeignKey(Venue.id))
    venue = db.relationship("Venue", back_populates='sections')

    seatings = db.relationship("Seating", back_populates='venue_section')


class Seating(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Numeric(precision=2, asdecimal=False),
                      nullable=False, default=0)
    seats_sold = db.Column(db.Integer, nullable=False, default=0)

    event_id = db.Column(db.Integer, db.ForeignKey(Event.id))
    event = db.relationship("Event", back_populates="seatings")

    venue_section_id = db.Column(db.Integer, db.ForeignKey(Venue_Section.id))
    venue_section = db.relationship("Venue_Section", back_populates="seatings")

    tickets = db.relationship("Ticket", back_populates="seating")

class Ticket(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    seating_id = db.Column(db.Integer, db.ForeignKey(Seating.id))
    seating = db.relationship("Seating", back_populates="tickets")

    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship("User", back_populates="tickets")
