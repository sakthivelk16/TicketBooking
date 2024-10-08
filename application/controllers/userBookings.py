from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy import func, label
from models.module import *
from flask import current_app as app
from datetime import datetime, timedelta


@app.route("/user/bookings", methods={"GET", "POST"})
@login_required
def myBookings():
    userBooking = BookingDetails.query.filter_by(user_id=current_user.user_id).order_by(BookingDetails.booking_id.desc()).all()
    final = []
    for eachBooking in userBooking:
        currentShowVenue = ShowVenue.query.get(eachBooking.sv_id)
        currentShow = Show.query.get(currentShowVenue.show_id)
        currentVenue = Venue.query.get(currentShowVenue.venue_id)
        rate1 = Rating.query.filter_by(
            user_id=current_user.user_id, show_id=currentShow.show_id
        ).all()

        json = {}
        json["venue_name"] = currentVenue.venue_name
        json["location"] = currentVenue.location
        json["show_id"] = currentShow.show_id
        json["bookingID"] = eachBooking.booking_id  # having issue need a fix
        json["show_name"] = currentShow.show_name
        json["time"] = currentShowVenue.time.strftime("%Y-%m-%d %I:%M %p")
        json["showStatus"] = (
            "completed"
            if currentShowVenue.time + timedelta(minutes=currentShow.duration)
            <= datetime.now()
            else "notCompleted"
        )
        final.append(json)
        json["rated"] = rate1[0].rating if len(rate1) > 0 else "notRated"
    return render_template("user/allBooking.html", bookings=final)


@app.route("/user/book/<int:svId>", methods={"GET", "POST"})
@login_required
def bookTicket(svId):
    if request.method == "POST":
        b1 = BookingDetails(
            user_id=current_user.user_id,
            sv_id=svId,
            ticket_count=request.form["ticketCount"],
            ticket_fare=request.form["ticketrate"],
        )
        db.session.add(b1)
        db.session.commit()
        flash(
            "Your Ticket booking is successful.",
            "success",
        )
        return redirect("/user/book/details/" + str(b1.booking_id))
    currentVenueShow = ShowVenue.query.get(svId)
    currentShow = Show.query.filter_by(show_id=currentVenueShow.show_id).first()
    currentVenue = Venue.query.filter_by(venue_id=currentVenueShow.venue_id).first()
    allBookings = BookingDetails.query.all()
    soldTick = {}
    avgRatings = (
        db.session.query(Rating.show_id, label("members", func.avg(Rating.rating)))
        .group_by(Rating.show_id)
        .all()
    )

    tags = Showtag.query.filter_by(show_id=currentShow.show_id).all()
    if len(tags) == 0:
        tag = "No tags"
    else:
        tag = ""
        for each in tags:
            tag = tag + ";" + each.tags
        tag = tag[1:]
    allRatings = {}
    for each in avgRatings:
        allRatings[each[0]] = round(each[1],1)
    for each in allBookings:
        if each.sv_id in soldTick:
            soldTick[each.sv_id] = soldTick[each.sv_id] + each.ticket_count
        else:
            soldTick[each.sv_id] = each.ticket_count
    availabelTicket = (
        currentVenue.max_capacity - soldTick[currentVenueShow.sv_id]
        if currentVenueShow.sv_id in soldTick
        else currentVenue.max_capacity
    )
    if currentShow.is3d and currentShow.min_fare > currentVenue.fare3D:
        fare = currentShow.min_fare
    elif currentShow.is3d:
        fare = currentVenue.fare3D
    elif currentShow.min_fare > currentVenue.fare2D:
        fare = currentShow.min_fare
    else:
        fare = currentVenue.fare2D
    rate = (
        allRatings[currentShow.show_id]
        if currentShow.show_id in allRatings
        else "Not rated"
    )
    json = {}
    json["venue_name"] = currentVenue.venue_name
    json["location"] = currentVenue.location
    json["show_name"] = currentShow.show_name
    json["time"] = currentVenueShow.time.strftime("%Y-%m-%d %I:%M %p")
    json["fare"] = fare
    json["rate"] = rate
    json["tags"] = tag
    json["availabelTicket"] = availabelTicket
    return render_template("user/bookingPage.html", json=json)
