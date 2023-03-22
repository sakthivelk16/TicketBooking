from flask import Flask, flash, session, redirect, render_template, request, url_for
from models.module import *
from flask import current_app as app
from datetime import datetime

app.secret_key = "abc"


@app.route("/admin/<int:a_id>/venue/create", methods={"GET", "POST"})
def venueCreate(a_id):
    if request.method == "POST":
        name = request.form["venue_name"]
        place = request.form["place"]
        location = request.form["location"]
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
            venue["place"] = request.form["place"]
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
        name = request.form["venue_name"]
        place = request.form["place"]
        location = request.form["location"]
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
        v1.venue_name = name
        v1.place = place
        v1.location = location
        v1.max_capacity = capacity
        v1.fare2D = fare2D
        v1.fare3D = fare3D
        db.session.add(v1)
        db.session.commit()
        return redirect("/admin/" + str(a_id) + "/venue")
    currentVenue = Venue.query.get(venueId)

    return render_template("admin/createVenue.html", adminId=a_id, venue=currentVenue)
