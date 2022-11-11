
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import datetime

app = Flask(__name__)
db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'cf2ad42be998f16d0c0e6596'
app.config['STRIPE_PUBLIC_KEY'] = 'pk_test_KMCerPRQaKzAv45qvFR58Vnl00Ccaf8NiN'
app.config['STRIPE_SECRET_KEY'] = 'sk_test_Gaah29dliX1UUMIe3a6OAqqO00OQIP9EWO'
db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
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
                         address='40 Bay St., Toronto',
                         featured=True,
                         image_url = 'https://hub.musicpeaks.com/sites/default/files/Air%20Canada%20Centre%2C%20Toronto.jpeg'),
            models.Venue(name='Sony Center', address='1 Front St E, Toronto', image_url = 'https://mapio.net/images-p/12240077.jpg'),
            models.Venue(name='Rogers Center',
                         featured=True,
                         address='1 Blue Jays Way, Toronto', image_url = 'https://img.mlbstatic.com/mlb-images/image/private/t_16x9/t_w2208/mlb/i6su9anj3vijyern9bao.jpg'),

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
                         emc_id=models.EMC.query.filter_by(name='INK EVENTS').first().id,
                         featured=True),

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
                         image_url = 'https://edm.com/.image/ar_1:1%2Cc_fill%2Ccs_srgb%2Cfl_progressive%2Cq_auto:good%2Cw_1200/MTg5Mzg0MzcyODg4MDIwODg1/279912798_554688012687989_7371472378482916394_n-e1651905549299-696x522.jpg',
                         emc_id=models.EMC.query.filter_by(
                name='INK EVENTS').first().id, featured=True
            ),
            models.Event(date=datetime.date(2022, 12, 18),
                         concert_id=models.Concert.query.filter_by(
                name='World War Joy Tour').first().id,
                venue_id=models.Venue.query.filter_by(
                name='Air Canada Center').first().id,
                description='Sat 8:00pm',
                image_url = 'https://newsroom.mohegansun.com/wp-content/uploads/2019/02/Chainsmokers_ADMAT_COLOR_crop-300x292.jpg',
                emc_id=models.EMC.query.filter_by(
                name='GTA EVENTS').first().id, featured=True
            )
        ]

        db.session.add_all(events)
        print('Successfully added events')
     
        vc2 = 600
        vc3710 = 800
        vc4 = 1000
        vc15689 = 500
        sections = [
            models.Venue_Section(venue_id=models.Venue.query.filter_by(name='Air Canada Center').first().id,
                                 num_of_seats=vc15689,
                                 sec_name='floor'),
            models.Venue_Section(venue_id=models.Venue.query.filter_by(name='Air Canada Center').first().id,
                                 num_of_seats=vc2,
                                 sec_name='lower level'),
            models.Venue_Section(venue_id=models.Venue.query.filter_by(name='Air Canada Center').first().id,
                                 num_of_seats=vc3710,
                                 sec_name='club level'),
            models.Venue_Section(venue_id=models.Venue.query.filter_by(name='Air Canada Center').first().id,
                                 num_of_seats=vc4,
                                 sec_name='upper level'),
            models.Venue_Section(venue_id=models.Venue.query.filter_by(name='Sony Center').first().id,
                                 num_of_seats=vc15689,
                                 sec_name='Premium Seats'),
            models.Venue_Section(venue_id=models.Venue.query.filter_by(name='Sony Center').first().id,
                                 num_of_seats=vc15689,
                                 sec_name='Gold Seats'),
            models.Venue_Section(venue_id=models.Venue.query.filter_by(name='Sony Center').first().id,
                                 num_of_seats=vc3710,
                                 sec_name='Silver Seats'),
            models.Venue_Section(venue_id=models.Venue.query.filter_by(name='Rogers Center').first().id,
                                 num_of_seats=vc15689,
                                 sec_name='A Seats'),
            models.Venue_Section(venue_id=models.Venue.query.filter_by(name='Rogers Center').first().id,
                                 num_of_seats=vc15689,
                                 sec_name='B Seats'),
            models.Venue_Section(venue_id=models.Venue.query.filter_by(name='Rogers Center').first().id,
                                 num_of_seats=vc3710,
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
            models.Seating(event_id=4, venue_section_id=4, price=300)
        ]

        db.session.add_all(seatings)
        db.session.commit()
        print('Finished populating data')


# insertDummyData()
