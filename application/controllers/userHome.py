from flask_login import current_user, login_required
from flask import render_template, flash, request, redirect
from flask_login import current_user, login_required
from sqlalchemy import func, label
from models.module import *
from flask import current_app as app
from datetime import datetime

@app.route("/user/home", methods={"GET", "POST"})
@login_required
def userHome():
    if request.method == "POST":
        return redirect("/user/book/" + request.form["book"].replace("book-", ""))
    v = Venue.query.all()
    allBookings = BookingDetails.query.all()
    soldTick = {}
    for each in allBookings:
        if each.sv_id in soldTick:
            soldTick[each.sv_id] = soldTick[each.sv_id] + each.ticket_count
        else:
            soldTick[each.sv_id] = each.ticket_count
    # print(soldTick)
    avgRatings = (
        db.session.query(Rating.show_id, label("members", func.avg(Rating.rating)))
        .group_by(Rating.show_id)
        .all()
    )
    allRatings = {}
    for each in avgRatings:
        allRatings[each[0]] = each[1]

    tags = Showtag.query.all()
    allTags = {}
    for each in tags:
        if each.show_id in allTags:
            allTags[each.show_id] = allTags[each.show_id] + ";" + each.tags
        else:
            allTags[each.show_id] = each.tags

    list = []
    currentTime = datetime.now()
    for e in v:
        allVenueShow = (
            ShowVenue.query.filter(
                ShowVenue.venue_id == e.venue_id, ShowVenue.time > currentTime
            )
            .order_by(ShowVenue.time)
            .all()
        )
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
                innerjson["time"] = ee.time.strftime("%Y-%m-%d %I:%M %p")
                innerjson["show_id"] = currentShow.show_id
                innerjson["show_name"] = currentShow.show_name
                innerjson["is3d"] = currentShow.is3d
                innerjson["tag"] = (
                    allTags[currentShow.show_id]
                    if currentShow.show_id in allTags
                    else "No Tags"
                )
                innerjson["rating"] = (
                    allRatings[currentShow.show_id]
                    if currentShow.show_id in allRatings
                    else "Not Rated"
                )
                innerjson["available_ticket"] = (
                    e.max_capacity - soldTick[ee.sv_id]
                    if ee.sv_id in soldTick
                    else e.max_capacity
                )
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
    return render_template("user/showDetails.html", list=list)
