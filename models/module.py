from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class Venue(db.Model):
    venue_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    venue_name = db.Column(db.String(32), nullable=False)
    place = db.Column(db.String(32))
    location = db.Column(db.String(32), nullable=False)
    max_capacity = db.Column(db.Integer, nullable=False)
    fare2D = db.Column(db.Integer, nullable=False)
    fare3D = db.Column(db.Integer, nullable=False)
    venueShows = db.relationship("Show", backref="venues", secondary="show_venue")


class Show(db.Model):
    show_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    show_name = db.Column(db.String(64), unique=True, nullable=False)
    min_fare = db.Column(db.Integer, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    is3d = db.Column(db.Boolean, nullable=False)
    tags = db.relationship("Showtag", backref="shows")


class ShowVenue(db.Model):
    sv_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    show_id = db.Column(db.Integer, db.ForeignKey("show.show_id"), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey("venue.venue_id"), nullable=False)
    time = db.Column(db.DateTime, nullable=False)


class Showtag(db.Model):
    st_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    show_id = db.Column(db.Integer, db.ForeignKey("show.show_id"), nullable=False)
    tags = db.Column(db.String(), nullable=False)


class Users(db.Model, UserMixin):
    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    first_name = db.Column(db.String(32), nullable=False)
    last_name = db.Column(db.String(32), nullable=False)
    phone_number = db.Column(db.String(10))
    email_id = db.Column(db.String(32))
    username = db.Column(db.String(32), unique=True, nullable=False)
    password = db.Column(db.String(32), nullable=False)
    mybookings = db.relationship(
        "ShowVenue", backref="bookedUser", secondary="booking_details"
    )
    myratings = db.relationship("Show", backref="shoRatings", secondary="rating")

    def __init__(
        self, first_name, last_name, email_id, phone_number, username, password
    ):
        self.username = username
        self.password = self.generate_password(password)
        self.first_name = first_name    
        self.last_name = last_name
        self.email_id = email_id
        self.phone_number = phone_number

    def get_id(self):
        return self.user_id

    def is_password_correct(self, password_plaintext: str):
        return check_password_hash(self.password, password_plaintext)

    def generate_password(self, password_plaintext: str):
        return generate_password_hash(password_plaintext)


class Admincode(db.Model):
    admin_code_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    admin_code = db.Column(db.String(10), unique=True, nullable=False)


class Admin(db.Model):
    admin_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    first_name = db.Column(db.String(32), nullable=False)
    last_name = db.Column(db.String(32), nullable=False)
    phone_number = db.Column(db.String(10), unique=True, nullable=False)
    email_id = db.Column(db.String(32), unique=True, nullable=False)
    username = db.Column(db.String(32), unique=True, nullable=False)
    password = db.Column(db.String(32), nullable=False)
   
    def __init__(
        self, first_name, last_name, email_id, phone_number, username, password
    ):
        self.username = username
        self.password = self.generate_password(password)
        self.first_name = first_name    
        self.last_name = last_name
        self.email_id = email_id
        self.phone_number = phone_number


    def is_password_correct(self, password_plaintext: str):
        return check_password_hash(self.password, password_plaintext)

    def generate_password(self, password_plaintext: str):
        return generate_password_hash(password_plaintext)


class Rating(db.Model):
    rating_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    show_id = db.Column(db.Integer, db.ForeignKey("show.show_id"), nullable=False)
    rating = db.Column(db.Integer, nullable=False)


class BookingDetails(db.Model):
    booking_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    sv_id = db.Column(db.Integer, db.ForeignKey("show_venue.sv_id"), nullable=False)
    ticket_count = db.Column(db.Integer, nullable=False)
    ticket_fare = db.Column(db.Integer, nullable=False)
