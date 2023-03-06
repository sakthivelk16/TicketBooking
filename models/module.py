from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Venue(db.Model):
    venue_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    venue_name = db.Column(db.String(), nullable=False)
    place = db.Column(db.String(), nullable=False)
    location = db.Column(db.String())
    max_capacity = db.Column(db.Integer, nullable=False)
    fare2D=db.Column(db.Integer, nullable=False)
    fare3D=db.Column(db.Integer, nullable=False)
    venueShows = db.relationship("Show", backref="venues", secondary="show_venue")


class Show(db.Model):
    show_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    show_name = db.Column(db.String(), unique=True, nullable=False)
    min_fare = db.Column(db.Integer, nullable=False)
    is3d= db.Column(db.Boolean, nullable=False)
    tags = db.relationship("Showtag", backref="shows")



class ShowVenue(db.Model):
    sv_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    show_id = db.Column(db.Integer,
                        db.ForeignKey("show.show_id"),
                        nullable=False)
    venue_id = db.Column(db.Integer,
                         db.ForeignKey("venue.venue_id"),
                         nullable=False)
    time = db.Column(db.DateTime)


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
    myratings = db.relationship("Show", backref="shoRatings", secondary="rating")


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


# db.create_all()

# d1=Director(name="direct1")
# db.session.add(d1)
# db.session.commit()
# d2=Director(name="direct2")
# m1=Movie(name="movie1")
# db.session.add_all([m1,d2])
# db.session.commit()

# Director.query.all() # return complete table
# Director.query.get(1) # return data which have id(primarykey) 1
# Director.query.filter_by(name="Director2").first() # return as element-> first data with filter details
# Director.query.filter_by(name="Director2").all() # return as list-> all data with filter details
