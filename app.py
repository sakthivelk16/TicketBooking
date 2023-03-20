from flask import Flask, redirect, render_template, request, url_for
from models.module import *
from datetime import datetime
import string
import random
from flask_restful import Api
from application.api.venue import VenueAPI
from application.api.show import ShowAPI
from application.api.allocation import AllocationAPI
from application.api.ShowVenue import ShowAtVenueAPI, AllShowAtVenueAPI, ShowAtAllVenueAPI

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.sqlite3"
api = Api()
db.init_app(app)

api.add_resource(ShowAPI, "/api/show", "/api/show/<int:showId>")
api.add_resource(VenueAPI, "/api/venue", "/api/venue/<int:venueId>")
api.add_resource(AllocationAPI, "/api/allocation",
                 "/api/allocation/<int:allocId>")
api.add_resource(ShowAtVenueAPI, "/api/venue/<int:venueId>/show/<int:showId>")
api.add_resource(AllShowAtVenueAPI, "/api/venue/<int:venueId>/show")
api.add_resource(ShowAtAllVenueAPI, "/api/show/<int:showId>/venue")

api.init_app(app)
app.app_context().push()


@app.route("/user/<int:userId>/profile", methods={"GET", "POST"})
def userProfile(userId):
    user = Users.query.get(userId)
    json = {}
    json['first_name'] = user.first_name
    json['last_name'] = user.last_name if user.last_name else ''
    json['phone_number'] = user.phone_number if user.phone_number else ''
    json['email_id'] = user.email_id if user.email_id else ''
    json['username'] = user.username
    return render_template('profile.html', user=json, userId=userId)


@app.route("/admin/<int:adminId>/profile", methods={"GET", "POST"})
def adminProfile(adminId):
    admin = Admin.query.get(adminId)
    json = {}
    json['first_name'] = admin.first_name
    json['last_name'] = admin.last_name if admin.last_name else ''
    json['phone_number'] = admin.phone_number if admin.phone_number else ''
    json['email_id'] = admin.email_id if admin.email_id else ''
    json['username'] = admin.username
    return render_template('profile.html',
                           user=json,
                           admin=True,
                           userId=adminId)


@app.route("/admin/<int:userId>/generete", methods={"GET", "POST"})
def GenerateCode(userId):
    N = 10
    res = ''.join(random.choices(string.ascii_letters, k=N))
    ac1 = Admincode(admin_code=res)
    db.session.add(ac1)
    db.session.commit()
    # print("The generated random string : " + str(res))
    return render_template('adminCode.html', code=str(res))


@app.route("/user/<int:userID>/home", methods={"GET", "POST"})
def userHome(userID):
    if request.method == "POST":
        return redirect('/user/' + str(userID) + '/book/' +
                        request.form['book'].replace('book-', ''))

    v = Venue.query.all()
    allBookings = BookingDetails.query.all()
    soldTick = {}
    for each in allBookings:
        if each.sv_id in soldTick:
            soldTick[each.sv_id] = soldTick[each.sv_id] + each.ticket_count
        else:
            soldTick[each.sv_id] = each.ticket_count
    # print(soldTick)
    avgRatings = db.session.query(Rating.show_id,
                                  label('members',
                                        func.avg(Rating.rating))).group_by(
                                            Rating.show_id).all()
    allRatings = {}
    for each in avgRatings:
        allRatings[each[0]] = each[1]

    tags = Showtag.query.all()
    allTags = {}
    for each in tags:
        if each.show_id in allTags:
            allTags[each.show_id] = allTags[each.show_id] + ';' + each.tags
        else:
            allTags[each.show_id] = each.tags

    list = []
    currentTime = datetime.now()
    for e in v:
        allVenueShow = ShowVenue.query.filter(
            ShowVenue.venue_id == e.venue_id,
            ShowVenue.time > currentTime).order_by(ShowVenue.time).all()
        if len(allVenueShow) > 0:
            eachjson = {}
            eachjson["venue_id"] = e.venue_id
            eachjson["venue_name"] = e.venue_name
            eachjson["place"] = e.place
            eachjson["location"] = e.location
            eachjson["max_capacity"] = e.max_capacity
            eachjson["price2D"] = e.fare2D
            eachjson["price3D"] = e.fare3D
            eachjson["shows"] = []

            for ee in allVenueShow:
                currentShow = Show.query.filter_by(show_id=ee.show_id).first()

                # allSVID = ShowVenue.query.filter_by(show_id=ee.show_id).all()
                # soldTicketCount = 0
                # for eachSV in allSVID:
                #     allBookingDetails = BookingDetails.query.filter_by(
                #         sv_id=eachSV.sv_id).all()
                #     print(allBookingDetails)
                #     for eachBD in allBookingDetails:
                #         soldTicketCount = soldTicketCount + eachBD.ticket_count

                innerjson = {}
                innerjson["sv_id"] = ee.sv_id
                innerjson["time"] = ee.time
                innerjson["show_id"] = currentShow.show_id
                innerjson["show_name"] = currentShow.show_name
                innerjson["is3d"] = currentShow.is3d
                innerjson["tag"] = allTags[
                    currentShow.
                    show_id] if currentShow.show_id in allTags else 'No Tags'
                innerjson['rating'] = allRatings[
                    currentShow.
                    show_id] if currentShow.show_id in allRatings else 'Not Rated'
                innerjson["available_ticket"] = e.max_capacity - soldTick[
                    ee.sv_id] if ee.sv_id in soldTick else e.max_capacity
                if currentShow.is3d and currentShow.min_fare > e.fare3D:
                    innerjson["min_fare"] = currentShow.min_fare
                elif currentShow.is3d:
                    innerjson["min_fare"] = e.fare3D
                elif currentShow.min_fare > e.fare2D:
                    innerjson["min_fare"] = currentShow.min_fare
                else:
                    innerjson["min_fare"] = e.fare2D
                eachjson["shows"].append(innerjson)
            list.append(eachjson)
    return render_template("showDetails.html", userId=userID, list=list)


# db.session.execute(db.select(ShowVenue).order_by(ShowVenue.venue_id)).scalars()


@app.route("/admin/<int:a_id>/archive", methods={"GET", "POST"})
def adminarchive(a_id):
    v = Venue.query.all()
    list = []
    for e in v:
        allVenueShow = ShowVenue.query.filter(
            ShowVenue.venue_id == e.venue_id,
            ShowVenue.time <= datetime.now()).all()

        eachjson = {}
        eachjson["venue_id"] = e.venue_id
        eachjson["venue_name"] = e.venue_name
        eachjson["place"] = e.place
        eachjson["location"] = e.location
        eachjson["shows"] = []

        for ee in allVenueShow:
            currentShow = Show.query.filter_by(show_id=ee.show_id).first()
            innerjson = {}
            innerjson["sv_id"] = ee.sv_id
            innerjson["time"] = ee.time
            innerjson["show_name"] = currentShow.show_name

            eachjson["shows"].append(innerjson)
        list.append(eachjson)
    return render_template("adminHome.html",
                           Venue=list,
                           adminId=a_id,
                           archive="archive")


@app.route("/admin/<int:a_id>/home", methods={"GET", "POST"})
def adminHome(a_id):
    v = Venue.query.all()
    list = []
    for e in v:
        allVenueShow = ShowVenue.query.filter(
            ShowVenue.venue_id == e.venue_id,
            ShowVenue.time > datetime.now()).all()

        eachjson = {}
        eachjson["venue_id"] = e.venue_id
        eachjson["venue_name"] = e.venue_name
        eachjson["place"] = e.place
        eachjson["location"] = e.location
        eachjson["shows"] = []

        for ee in allVenueShow:
            currentShow = Show.query.filter_by(show_id=ee.show_id).first()
            innerjson = {}
            innerjson["sv_id"] = ee.sv_id
            innerjson["time"] = ee.time
            innerjson["show_name"] = currentShow.show_name

            eachjson["shows"].append(innerjson)
        list.append(eachjson)
    return render_template("adminHome.html", Venue=list, adminId=a_id)


from application.controllers.login import *
from application.controllers.register import *
from application.controllers.userBookings import *
from application.controllers.venueAdmin import *
from application.controllers.showAdmin import *
from application.controllers.adminShowallocation import *
from application.controllers.rate import *
from application.controllers.search import *
from application.controllers.matplot import *

if __name__ == "__main__":
    app.debug = True
    app.run()
