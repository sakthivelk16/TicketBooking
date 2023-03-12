from flask import Flask, redirect, render_template, request, url_for
from models.module import *
from flask import current_app as app


@app.route("/user/<int:userID>/bookings", methods={"GET", "POST"})
def myBookings(userID):
    currentUser = Users.query.get(userID)
    final = []
    for eachShowVenue in currentUser.mybookings:
        currentShow = Show.query.get(eachShowVenue.show_id)
        currentVenue = Venue.query.get(eachShowVenue.venue_id)
        json = {}
        json['venue_name'] = currentVenue.venue_name
        json['show_name'] = currentShow.show_name
        json['time'] = eachShowVenue.time
        final.append(json)
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
        currentVenueShow.sv_id]
    return render_template('bookingPage.html',
                           userId=userID,
                           show=currentShow,
                           venue=currentVenue,
                           currentVenueShow=currentVenueShow,
                           availabelTicket=availabelTicket)

