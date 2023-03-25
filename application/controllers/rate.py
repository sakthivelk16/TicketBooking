from flask import Flask, redirect, render_template, request, url_for, session
from flask_login import current_user, login_required
from models.module import *
from flask import current_app as app
from datetime import datetime
from sqlalchemy import func
from sqlalchemy.sql import label


@app.route("/user/book/details/<int:bookId>", methods={"GET", "POST"})
@login_required
def bookingdetails(bookId):
    curBooking = BookingDetails.query.get(bookId)
    curallocation = ShowVenue.query.get(curBooking.sv_id)
    curShow = Show.query.get(curallocation.show_id)
    curVenue = Venue.query.get(curallocation.venue_id)
    json = {}
    json["showName"] = curShow.show_name
    json["venueName"] = curVenue.venue_name
    json["duration"] = curShow.duration
    json["showTime"] = curallocation.time.strftime("%Y-%m-%d %I:%M %p")
    json["bookedTicket"] = curBooking.ticket_count
    json["ticketCost"] = curBooking.ticket_fare

    json["totalTicketCost"] = json["ticketCost"] * json["bookedTicket"]
    return render_template("user/bookingDetails.html", json=json)


@app.route("/user/rate/<int:showId>", methods={"GET", "POST"})
@login_required
def ratePage(showId):
    if request.method == "POST":
        request.form["ratevalue"]
        r1 = Rating(
            user_id=current_user.user_id,
            show_id=showId,
            rating=request.form["ratevalue"],
        )
        db.session.add(r1)
        db.session.commit()
        return redirect("/user/bookings")

    rate1 = Rating.query.filter_by(user_id=current_user.user_id, show_id=showId).all()
    show1 = Show.query.get(showId)
    json = {}

    json["rated"] = True if len(rate1) > 0 else False
    json["showName"] = show1.show_name
    json["movieType"] = "3D" if show1.is3d else "2D"
    json["showId"] = showId

    return render_template("user/rate.html", show=json)
