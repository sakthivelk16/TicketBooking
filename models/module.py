from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Venue(db.Model):
    venue_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    venue_name = db.Column(db.String(), nullable=False)
    place = db.Column(db.String())
    location = db.Column(db.String(), nullable=False)
    max_capacity = db.Column(db.Integer, nullable=False)
    fare2D = db.Column(db.Integer, nullable=False)
    fare3D = db.Column(db.Integer, nullable=False)
    venueShows = db.relationship("Show",
                                 backref="venues",
                                 secondary="show_venue")


class Show(db.Model):
    show_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    show_name = db.Column(db.String(), unique=True, nullable=False)
    min_fare = db.Column(db.Integer, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    is3d = db.Column(db.Boolean, nullable=False)
    tags = db.relationship("Showtag", backref="shows")


class ShowVenue(db.Model):
    sv_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    show_id = db.Column(db.Integer,
                        db.ForeignKey("show.show_id"),
                        nullable=False)
    venue_id = db.Column(db.Integer,
                         db.ForeignKey("venue.venue_id"),
                         nullable=False)
    time = db.Column(db.DateTime, nullable=False)


class Showtag(db.Model):
    st_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    show_id = db.Column(db.Integer,
                        db.ForeignKey("show.show_id"),
                        nullable=False)
    tags = db.Column(db.String(), nullable=False)


class Users(db.Model):
    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    first_name = db.Column(db.String(), nullable=False)
    last_name = db.Column(db.String())
    phone_number = db.Column(db.String())
    email_id = db.Column(db.String())
    username = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    mybookings = db.relationship("ShowVenue",
                                 backref="bookedUser",
                                 secondary="booking_details")
    myratings = db.relationship("Show",
                                backref="shoRatings",
                                secondary="rating")


class Admincode(db.Model):
    admin_code_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    admin_code = db.Column(db.String(), unique=True, nullable=False)


class Admin(db.Model):
    admin_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    first_name = db.Column(db.String(), nullable=False)
    last_name = db.Column(db.String(), nullable=False)
    phone_number = db.Column(db.String(), unique=True, nullable=False)
    email_id = db.Column(db.String(), unique=True, nullable=False)
    username = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)


class Rating(db.Model):
    rating_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.user_id"),
                        nullable=False)
    show_id = db.Column(db.Integer,
                        db.ForeignKey("show.show_id"),
                        nullable=False)
    rating = db.Column(db.Integer, nullable=False)


class BookingDetails(db.Model):
    booking_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.user_id"),
                        nullable=False)
    sv_id = db.Column(db.Integer,
                      db.ForeignKey("show_venue.sv_id"),
                      nullable=False)
    ticket_count = db.Column(db.Integer, nullable=False)
    ticket_fare = db.Column(db.Integer, nullable=False)
