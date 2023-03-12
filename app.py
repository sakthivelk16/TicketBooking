from flask import Flask, redirect, render_template, request, url_for
from models.module import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.sqlite3"

db.init_app(app)
app.app_context().push()


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
    print(soldTick)
    list = []
    for e in v:
        allVenueShow = ShowVenue.query.filter_by(venue_id=e.venue_id).all()
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
                innerjson["available_ticket"] = e.max_capacity - soldTick[
                    ee.sv_id] if ee.sv_id in soldTick else e.max_capacity

                innerjson["min_fare"] = currentShow.min_fare
                eachjson["shows"].append(innerjson)
            list.append(eachjson)
    print(list)
    return render_template("showDetails.html", userId=userID, list=list)


# db.session.execute(db.select(ShowVenue).order_by(ShowVenue.venue_id)).scalars()


@app.route("/admin/<int:a_id>/home", methods={"GET", "POST"})
def adminHome(a_id):
    if request.method == "POST":
        username = request.form['loginId']
        password = request.form['password']
        u1 = Admin.query.filter_by(username=username,
                                   password=password).first()
        if u1 is None:
            return render_template("login/adminlogin.html", error=True)

        return redirect("/admin/" + str(u1.admin_id) + "/home")

    v = Venue.query.all()
    list = []
    for e in v:
        allVenueShow = ShowVenue.query.filter_by(venue_id=e.venue_id).all()
        if len(allVenueShow) > 0:
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

if __name__ == "__main__":
    app.debug = True
    app.run()
