from flask import Flask, redirect, render_template, request, url_for
from models.module import *
from flask import current_app as app
from datetime import datetime, timedelta


@app.route("/user/<int:userID>/bookings", methods={"GET", "POST"})
def myBookings(userID):
    currentUser = Users.query.get(userID)
    userBooking = BookingDetails.query.filter_by(user_id=userID)
    print(userBooking)
    final = []
    for eachBooking in userBooking:
        currentShowVenue = ShowVenue.query.get(eachBooking.sv_id)
        currentShow = Show.query.get(currentShowVenue.show_id)
        currentVenue = Venue.query.get(currentShowVenue.venue_id)
        json = {}
        json['venue_name'] = currentVenue.venue_name
        json['show_id'] = currentShow.show_id
        json['bookingID'] = eachBooking.booking_id  # having issue need a fix
        json['show_name'] = currentShow.show_name
        json['time'] = currentShowVenue.time
        json['showStatus'] = 'completed' if currentShowVenue.time + timedelta(
            minutes=currentShow.duration) <= datetime.now() else 'notCompleted'
        final.append(json)
        print(final)
    return render_template('allBooking.html', userId=userID, bookings=final)


@app.route("/user/<int:userID>/book/<int:svId>", methods={"GET", "POST"})
def bookTicket(userID, svId):
    if request.method == "POST":
        ticketCount = request.form['ticketCount']
        b1 = BookingDetails(user_id=userID,
                            sv_id=svId,
                            ticket_count=ticketCount)
        db.session.add(b1)
        db.session.commit()
        return render_template('bookingSuccessful.html', userId=userID)
    currentVenueShow = ShowVenue.query.get(svId)
    currentShow = Show.query.filter_by(
        show_id=currentVenueShow.show_id).first()
    currentVenue = Venue.query.filter_by(
        venue_id=currentVenueShow.venue_id).first()
    allBookings = BookingDetails.query.all()
    soldTick = {}
    for each in allBookings:
        if each.sv_id in soldTick:
            soldTick[each.sv_id] = soldTick[each.sv_id] + each.ticket_count
        else:
            soldTick[each.sv_id] = each.ticket_count
    availabelTicket = currentVenue.max_capacity - soldTick[
        currentVenueShow.
        sv_id] if currentVenueShow.sv_id in soldTick else currentVenue.max_capacity
    return render_template('bookingPage.html',
                           userId=userID,
                           show=currentShow,
                           venue=currentVenue,
                           currentVenueShow=currentVenueShow,
                           availabelTicket=availabelTicket)
