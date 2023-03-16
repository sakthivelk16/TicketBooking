from flask import Flask, redirect, render_template, request, url_for, session
from models.module import *
from flask import current_app as app
from datetime import datetime
from sqlalchemy import func
from sqlalchemy.sql import label


@app.route("/user/<int:user_id>/details/<int:bookId>", methods={"GET", "POST"})
def bookingdetails(user_id, bookId):
    curBooking = BookingDetails.query.get(bookId)
    curallocation = ShowVenue.query.get(curBooking.sv_id)
    curShow = Show.query.get(curallocation.show_id)
    curVenue = Venue.query.get(curallocation.venue_id)
    json = {}
    json['showName'] = curShow.show_name
    json['venueName'] = curVenue.venue_name
    json['duration'] = curShow.duration
    json['showTime'] = curallocation.time
    json['bookedTicket'] = curBooking.ticket_count
    if curShow.is3d and curShow.min_fare > curVenue.fare3D:
        json['ticketCost'] = curShow.min_fare
    elif curShow.is3d:
        json['ticketCost'] = curVenue.fare3D
    elif curShow.min_fare > curVenue.fare2D:
        json['ticketCost'] = curShow.min_fare
    else:
        json['ticketCost'] = curVenue.fare2D

    json['totalTicketCost'] = json['ticketCost'] * json['bookedTicket']
    print(curBooking.ticket_count)
    return render_template('bookingDetails.html', userId=user_id, json=json)


@app.route("/user/<int:user_id>/rate/<int:showId>", methods={"GET", "POST"})
def ratePage(user_id, showId):
    if request.method == "POST":
        request.form['ratevalue']
        r1 = Rating(user_id=user_id,
                    show_id=showId,
                    rating=request.form['ratevalue'])
        db.session.add(r1)
        db.session.commit()
        return redirect('/user/' + str(user_id) + '/bookings')
    
    rate1 = Rating.query.filter_by(user_id=user_id, show_id=showId).all()
    show1 = Show.query.get(showId)
    json = {}

    json['rated'] = True if len(rate1) > 0 else False
    json['showName'] = show1.show_name
    json['movieType'] = '3D' if show1.is3d else '2D'
    json['showId'] = showId

    return render_template('rate.html', userId=user_id, show=json)
