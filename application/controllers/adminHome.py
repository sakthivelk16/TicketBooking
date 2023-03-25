from flask import render_template
from models.module import *
from flask import current_app as app
from datetime import datetime


@app.route("/admin/<int:a_id>/archive", methods={"GET", "POST"})
def adminarchive(a_id):
    v = Venue.query.all()
    list = []
    total = 0
    for e in v:
        allVenueShow = ShowVenue.query.filter(
            ShowVenue.venue_id == e.venue_id, ShowVenue.time <= datetime.now()
        ).order_by(ShowVenue.time).all()

        eachjson = {}
        eachjson["venue_id"] = e.venue_id
        eachjson["venue_name"] = e.venue_name
        eachjson["place"] = e.place
        eachjson["location"] = e.location
        eachjson["shows"] = []
        total += len(allVenueShow)
        for ee in allVenueShow:
            currentShow = Show.query.filter_by(show_id=ee.show_id).first()
            innerjson = {}
            innerjson["sv_id"] = ee.sv_id
            innerjson["time"] = ee.time.strftime("%Y-%m-%d %I:%M %p")
            innerjson["show_name"] = currentShow.show_name

            eachjson["shows"].append(innerjson)
        list.append(eachjson)
    return render_template("admin/archive.html", Venue=list, adminId=a_id, total=total)


@app.route("/admin/<int:a_id>/home", methods={"GET", "POST"})
def adminHome(a_id):
    v = Venue.query.all()
    list = []
    for e in v:
        allVenueShow = ShowVenue.query.filter(
            ShowVenue.venue_id == e.venue_id, ShowVenue.time > datetime.now()
        ).order_by(ShowVenue.time).all()

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
            innerjson["time"] = ee.time.strftime("%Y-%m-%d %I:%M %p")
            innerjson["show_name"] = currentShow.show_name

            eachjson["shows"].append(innerjson)
        list.append(eachjson)
    return render_template("admin/adminHome.html", Venue=list, adminId=a_id)
