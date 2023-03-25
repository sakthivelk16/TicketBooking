import sqlite3
from flask import Flask, flash, session, redirect, render_template, request, url_for
from models.module import *
from flask import current_app as app
from datetime import datetime



@app.route("/admin/<int:a_id>/venue/create", methods={"GET", "POST"})
def venueCreate(a_id):
    if request.method == "POST":
        name = request.form["venue_name"].lower()
        place = request.form["place"].lower()
        location = request.form["location"].lower()
        capacity = request.form["max_capacity"]
        fare2D = request.form["fare2D"]
        fare3D = request.form["fare3D"]
        exist = Venue.query.filter_by(venue_name=name, location=location).all()
        if len(exist) > 0:
            flash("This Venue already added to the  location", "danger")
            flash(
                "Venue name should be unique in one location. i.e. Venue name and location combination should be unique",
                "info",
            )
            venue = {}
            venue["place"] = request.form["place"].lower()
            venue["max_capacity"] = request.form["max_capacity"]
            venue["fare2D"] = request.form["fare2D"]
            venue["fare3D"] = request.form["fare3D"]
            return render_template("admin/createVenue.html", adminId=a_id, venue=venue)
        v1 = Venue(
            venue_name=name,
            place=place,
            location=location,
            max_capacity=capacity,
            fare2D=fare2D,
            fare3D=fare3D,
        )
        db.session.add(v1)
        db.session.commit()
        return redirect("/admin/" + str(a_id) + "/venue")
    venue = {}
    return render_template("admin/createVenue.html", adminId=a_id, venue=venue)


@app.route("/admin/<int:a_id>/venue", methods={"GET", "POST"})
def venueHome(a_id):
    if "venueError" in session:
        flash(
            "There is Still some show allocated to this Venue. So You are not allowed to delete the venue",
            "danger",
        )
        session.pop("venueError")
    allVenue = Venue.query.all()
    return render_template("admin/venueHome.html", allVenue=allVenue, adminId=a_id)


@app.route("/admin/<int:a_id>/venue/<int:venue_id>/delete", methods={"GET", "POST"})
def deleteVenue(a_id, venue_id):
    sv = ShowVenue.query.filter_by(venue_id=venue_id).all()
    if len(sv) > 0:
        session["venueError"] = True
        return redirect(url_for("venueHome", a_id=a_id))

    s = Venue.query.get(venue_id)
    db.session.delete(s)
    db.session.commit()
    return redirect("/admin/" + str(a_id) + "/venue")


@app.route("/admin/<int:a_id>/venue/<int:venueId>/edit", methods={"GET", "POST"})
def editVenue(a_id, venueId):
    if request.method == "POST":
        name = request.form["venue_name"].lower()
        place = request.form["place"].lower()
        location = request.form["location"].lower()
        capacity = request.form["max_capacity"]
        fare2D = request.form["fare2D"]
        fare3D = request.form["fare3D"]
        venue1 = Venue.query.filter(
            Venue.venue_name == name,
            Venue.location == location,
            Venue.venue_id != venueId,
        ).all()

        if len(venue1) > 0:
            flash("This Venue already present in location", "danger")
            flash(
                "Venue name should be unique in one location. (ie)Venue name and location combination should be unique",
                "info",
            )
            return render_template("admin/createVenue.html", adminId=a_id, venue=request.form)
        v1 = Venue.query.get(venueId)
        v1.venue_name = name.lower()
        v1.place = place.lower()
        v1.location = location.lower()
        v1.max_capacity = capacity
        v1.fare2D = fare2D
        v1.fare3D = fare3D
        # db.session.add(v1)
        db.session.commit()
        return redirect("/admin/" + str(a_id) + "/venue")
    currentVenue = Venue.query.get(venueId)

    return render_template("admin/createVenue.html", adminId=a_id, venue=currentVenue)


@app.route("/admin/<int:a_id>/venue/<int:venueId>/details", methods={"GET", "POST"})
def eachvenueDetails(a_id, venueId):
    query = None
    error = {}

    text = "Unfiltered Venue Details"
    query = "venue_id=" + str(venueId)
    if request.method == "POST":
        if request.form["from"] != "":
            query = query + " and time >= '" + request.form["from"] + "'"
            text = "Filtered Data from " + request.form["from"]
        if request.form["to"] != "":
            query = query + " and time <= '" + request.form["to"] + "'"
            if text == "Unfiltered Show Details":
                text = "Filtered Data upto " + request.form["to"]
            else:
                text = text + " to " + request.form["to"]
    conn = sqlite3.connect("instance/database.sqlite3")
    cur = conn.cursor()
    res0 = cur.execute(
        "SELECT sum(max_capacity) from show_venue natural join show NATURAL join venue where "
        + query
    )
    z = res0.fetchone()
    if z[0] is None:
        error["ERROR"] = "THIS VENUE HAS NO ALLOCATION"
        return render_template("admin/showDetails.html", adminId=a_id, json=error)
    json = {}
    json["availed"] = z[0]

    currentVenue = Venue.query.get(venueId)
    json["text"] = text
    json["venue"] = currentVenue.venue_name
    json["location"] = currentVenue.location

    res = cur.execute(
        "SELECT sum(ticket_count*ticket_fare) as summ, sum(ticket_count), sum(max_capacity),show_name from booking_details natural join show_venue natural join show NATURAL join venue where "
        + query
        + " group by venue_id;"
    )
    a = res.fetchone()
    if a is None:
        json["warn"] = "No Booking made for this show with details above"
        json["revenue"] = 0
        json["bookedTicket"] = 0
    else:
        json["revenue"] = a[0]
        json["bookedTicket"] = a[1]

    res1 = cur.execute("SELECT count(*) from show_venue where " + query)
    b = res1.fetchone()
    json["run"] = b[0]
    cur.close()
    conn.close()
    json["percent"] = round(json["bookedTicket"] / json["availed"] * 100)
    return render_template("admin/venueDetails.html", adminId=a_id, json=json)
