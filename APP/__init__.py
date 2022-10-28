
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'cf2ad42be998f16d0c0e6596'
db.init_app(app)

#Routes and model
from App import routes
from App import models

def insertDummyData():
    with app.app_context():
        db.drop_all()
        print('All tables dropped')
        db.create_all()
        print('Successfully created database')
        objects = [
            models.User(name='TestUser', email='test@test.com',
                        password_hash='123456'),

            models.EMC(name='INK EVENTS', balance=0),
            models.EMC(name='GTA EVENTS', balance=0),

            models.Venue(name='Air Canada Center',
                         address='40 Bay St., Toronto'),
            models.Venue(name='Sony Center', address='1 Front St E, Toronto'),
            models.Venue(name='Rogers Center',
                         address='1 Blue Jays Way, Toronto'),

            models.Concert(name='Ed Sheeran + - = ÷ x Tour',
                           artist='Ed Sheeran'),
            models.Concert(name='World War Joy Tour',
                           artist='The Chainsmokers'),
            models.Concert(name='Walkerverse The Tour', artist='Alan Walker')]

        db.session.add_all(objects)
        print('Successfully add objects')
        db.session.commit()

        events = [
            models.Event(date=datetime.date(2023, 6, 17),
                         concert_id=models.Concert.query.filter_by(
                             name='Ed Sheeran + - = ÷ x Tour').first().id,
                         venue_id=models.Venue.query.filter_by(
                             name='Rogers Center').first().id,
                         description='Sat 6:00pm',
                         image_url = 'https://readdork.com/wp-content/uploads/2022/10/Ed-Sheeran-Tour-Cropped-2023.jpg',
                         emc_id=models.EMC.query.filter_by(name='INK EVENTS').first().id),

            models.Event(date=datetime.date(2023, 6, 18), concert_id=models.Concert.query.filter_by(
                            name='Ed Sheeran + - = ÷ x Tour').first().id,
                         venue_id=models.Venue.query.filter_by(
                             name='Rogers Center').first().id,
                         description='Sun 6:00pm',
                         image_url = 'https://readdork.com/wp-content/uploads/2022/10/Ed-Sheeran-Tour-Cropped-2023.jpg',
                         emc_id=models.EMC.query.filter_by(name='INK EVENTS').first().id),

            models.Event(date=datetime.date(2023, 5, 18),
                         concert_id=models.Concert.query.filter_by(
                             name='Walkerverse The Tour').first().id,
                         venue_id=models.Venue.query.filter_by(
                             name='Sony Center').first().id,
                         description='Fri 8:00pm',
                         image_url = 'https://rebeltoronto.com/wp-content/uploads/2022/05/Alan_Walker_Post.jpg',
                         emc_id=models.EMC.query.filter_by(
                name='INK EVENTS').first().id
            ),
            models.Event(date=datetime.date(2022, 12, 18),
                         concert_id=models.Concert.query.filter_by(
                name='World War Joy Tour').first().id,
                venue_id=models.Venue.query.filter_by(
                name='Air Canada Center').first().id,
                description='Sat 8:00pm',
                image_url = 'https://newsroom.mohegansun.com/wp-content/uploads/2019/02/Chainsmokers_ADMAT_COLOR_crop-300x292.jpg',
                emc_id=models.EMC.query.filter_by(
                name='GTA EVENTS').first().id
            )
        ]

        db.session.add_all(events)
        print('Successfully added events')
        sections = [
            models.Venue_Section(venue_id=models.Venue.query.filter_by(name='Air Canada Center').first().id,
                                 num_of_seats=500,
                                 sec_name='floor'),
            models.Venue_Section(venue_id=models.Venue.query.filter_by(name='Air Canada Center').first().id,
                                 num_of_seats=600,
                                 sec_name='lower level'),
            models.Venue_Section(venue_id=models.Venue.query.filter_by(name='Air Canada Center').first().id,
                                 num_of_seats=800,
                                 sec_name='club level'),
            models.Venue_Section(venue_id=models.Venue.query.filter_by(name='Air Canada Center').first().id,
                                 num_of_seats=1000,
                                 sec_name='upper level'),
            models.Venue_Section(venue_id=models.Venue.query.filter_by(name='Sony Center').first().id,
                                 num_of_seats=500,
                                 sec_name='Premium Seats'),
            models.Venue_Section(venue_id=models.Venue.query.filter_by(name='Sony Center').first().id,
                                 num_of_seats=500,
                                 sec_name='Gold Seats'),
            models.Venue_Section(venue_id=models.Venue.query.filter_by(name='Sony Center').first().id,
                                 num_of_seats=800,
                                 sec_name='Silver Seats'),
            models.Venue_Section(venue_id=models.Venue.query.filter_by(name='Rogers Center').first().id,
                                 num_of_seats=500,
                                 sec_name='A Seats'),
            models.Venue_Section(venue_id=models.Venue.query.filter_by(name='Rogers Center').first().id,
                                 num_of_seats=500,
                                 sec_name='B Seats'),
            models.Venue_Section(venue_id=models.Venue.query.filter_by(name='Rogers Center').first().id,
                                 num_of_seats=800,
                                 sec_name='C Seats'),
        ]

        db.session.add_all(sections)

        seatings = [
            models.Seating(event_id=1, venue_section_id=8, price=220),
            models.Seating(event_id=1, venue_section_id=9, price=300),
            models.Seating(event_id=1, venue_section_id=10, price=200),
            models.Seating(event_id=2, venue_section_id=8, price=220),
            models.Seating(event_id=2, venue_section_id=9, price=300),
            models.Seating(event_id=2, venue_section_id=10, price=200),
            models.Seating(event_id=3, venue_section_id=5, price=150),
            models.Seating(event_id=3, venue_section_id=6, price=500),
            models.Seating(event_id=3, venue_section_id=7, price=400),
            models.Seating(event_id=4, venue_section_id=1, price=150),
            models.Seating(event_id=4, venue_section_id=2, price=500),
            models.Seating(event_id=4, venue_section_id=3, price=400),
            models.Seating(event_id=4, venue_section_id=4, price=300),
        ]

        db.session.add_all(seatings)
        db.session.commit()
        print('Finished populating data')


# insertDummyData()
