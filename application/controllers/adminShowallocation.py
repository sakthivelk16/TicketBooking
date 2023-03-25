import sqlite3
from flask import Flask, flash, redirect, render_template, request, url_for
from application.api.allocation import generatedateTime
from models.module import *
from flask import current_app as app
from datetime import datetime, timedelta


@app.route("/admin/<int:a_id>/venue/<int:venue_id>/allocate", methods={"GET", "POST"})
def allocation(a_id, venue_id):
    if request.method == "POST":
        s1 = Show.query.all()
        allShowInCurrentVenue = (
            ShowVenue.query.filter_by(venue_id=venue_id)
            .order_by((ShowVenue.time))
            .all()
        )
        currentShow = Show.query.get(request.form["selectShow"])
        showTime = request.form["showTime"]
        expectedStartTime = datetime(
            int(showTime[0:4]),
            int(showTime[5:7]),
            int(showTime[8:10]),
            int(showTime[11:13]),
            int(showTime[14:16]),
        )
        expectedEndTime = expectedStartTime + timedelta(minutes=currentShow.duration)
        currentTime = datetime.now()
        currentTime = currentTime.replace(second=0, microsecond=0)
        currentTimeplus15 = currentTime + timedelta(minutes=15)
        if expectedStartTime < currentTimeplus15:
            flash("The show can be created present time +15 mins", "warning")

            return render_template(
                "admin/allocation.html", adminId=a_id, show=s1, sv=None
            )
        conflict = True
        if len(allShowInCurrentVenue) == 0:
            conflict = False
        for i in range(len(allShowInCurrentVenue)):
            ss = Show.query.get(allShowInCurrentVenue[i].show_id)
            durationSS = ss.duration
            if i == 0:
                if expectedEndTime <= allShowInCurrentVenue[i].time - timedelta(
                    minutes=15
                ):
                    conflict = False
                    break
            if i == len(allShowInCurrentVenue) - 1:
                if expectedStartTime >= allShowInCurrentVenue[i].time + timedelta(
                    minutes=durationSS
                ) + timedelta(minutes=15):
                    conflict = False
                    break
            else:
                if expectedEndTime <= allShowInCurrentVenue[i + 1].time - timedelta(
                    minutes=15
                ) and expectedStartTime >= allShowInCurrentVenue[i].time + timedelta(
                    minutes=durationSS
                ) + timedelta(
                    minutes=15
                ):
                    conflict = False
                    break
        if conflict:
            flash(
                "There is some other show blocking this time. Please choose differnt time",
                "warning",
            )
            return render_template(
                "admin/allocation.html", adminId=a_id, show=s1, sv=None
            )
        else:
            sv1 = ShowVenue(
                show_id=request.form["selectShow"],
                venue_id=venue_id,
                time=expectedStartTime,
            )
            db.session.add(sv1)
            db.session.commit()
            return redirect("/admin/" + str(a_id) + "/home")
    s1 = Show.query.all()
    if len(s1) == 0:
        flash(
            "No shows are available to allocate. Please create New show before adding Show ro venue",
            "danger",
        )
        return redirect("/admin/" + str(a_id) + "/home")
    return render_template("admin/allocation.html", adminId=a_id, show=s1, sv=None)


@app.route("/admin/<int:a_id>/delete/<int:sv_id>", methods={"GET", "POST"})
def deleteAllocation(a_id, sv_id):
    bd = BookingDetails.query.filter_by(sv_id=sv_id).all()
    for each in bd:
        db.session.delete(each)
        db.session.commit()
    sv1 = ShowVenue.query.get(sv_id)
    db.session.delete(sv1)
    db.session.commit()
    # flash('Show allocated to venue is delete successfully')
    return redirect("/admin/" + str(a_id) + "/home")


@app.route("/admin/<int:a_id>/edit/<int:sv_id>", methods={"GET", "POST"})
def editAllocation(a_id, sv_id):
    if request.method == "POST":
        s1 = Show.query.all()
        currentShowVenue = ShowVenue.query.get(sv_id)
        currentVenue = Venue.query.get(currentShowVenue.venue_id)
        venue_id = currentVenue.venue_id
        allShowInCurrentVenue = (
            ShowVenue.query.filter(
                ShowVenue.sv_id != sv_id, ShowVenue.venue_id == venue_id
            )
            .order_by((ShowVenue.time))
            .all()
        )
        currentShow = Show.query.get(request.form["selectShow"])
        showTime = request.form["showTime"]
        expectedStartTime = datetime(
            int(showTime[0:4]),
            int(showTime[5:7]),
            int(showTime[8:10]),
            int(showTime[11:13]),
            int(showTime[14:16]),
        )
        expectedEndTime = expectedStartTime + timedelta(minutes=currentShow.duration)
        currentTime = datetime.now()
        currentTime = currentTime.replace(second=0, microsecond=0)
        currentTimeplus15 = currentTime + timedelta(minutes=15)
        if expectedStartTime < currentTimeplus15:
            flash("The show can be created present time +15 mins", "warning")
            return render_template(
                "admin/allocation.html", adminId=a_id, show=s1, sv=None
            )
        conflict = True
        if len(allShowInCurrentVenue) == 0:
            conflict = False
        for i in range(len(allShowInCurrentVenue)):
            ss = Show.query.get(allShowInCurrentVenue[i].show_id)
            durationSS = ss.duration
            if i == 0:
                if expectedEndTime <= allShowInCurrentVenue[i].time - timedelta(
                    minutes=15
                ):
                    conflict = False
                    break
            if i == len(allShowInCurrentVenue) - 1:
                if expectedStartTime >= allShowInCurrentVenue[i].time + timedelta(
                    minutes=durationSS
                ) + timedelta(minutes=15):
                    conflict = False
                    break
            else:
                if expectedEndTime <= allShowInCurrentVenue[i + 1].time - timedelta(
                    minutes=15
                ) and expectedStartTime >= allShowInCurrentVenue[i].time + timedelta(
                    minutes=durationSS
                ) + timedelta(
                    minutes=15
                ):
                    conflict = False
                    break
        if conflict:
            flash(
                "There is some other show blocking this time. Please choose differnt time",
                "warning",
            )

            return render_template(
                "admin/allocation.html", adminId=a_id, show=s1, sv=None
            )
        else:
            currentShowVenue.show_id = request.form["selectShow"]
            currentShowVenue.time = expectedStartTime
            db.session.commit()
            return redirect("/admin/" + str(a_id) + "/home")

    currentShowVenue = ShowVenue.query.get(sv_id)
    show = Show.query.all()
    currentShow = Show.query.get(currentShowVenue.show_id)

    return render_template(
        "admin/allocation.html",
        adminId=a_id,
        show=show,
        sv=currentShowVenue,
        myshow=currentShow.show_name,
    )



@app.route("/admin/<int:a_id>/allocate/<int:allocId>/details", methods={"GET", "POST"})
def eachAllocateDetails(a_id, allocId):
    query = "sv_id=" + str(allocId)

    conn = sqlite3.connect("instance/database.sqlite3")
    cur = conn.cursor()
    res0 = cur.execute(
        "SELECT * from show_venue natural join show NATURAL join venue where "
        + query
    )
    z = res0.fetchone()

    res = cur.execute(
        "SELECT sum(ticket_count*ticket_fare) , sum(ticket_count) from booking_details where "
        + query    )
    a = res.fetchone()


    # return 'k'
    json = {}
    json["show"] = z[4]
    json["duration"] = z[6]
    json["venue"] = z[8]
    json["location"] = z[10]
    json["availed"] = z[11]
    json["time"] = generatedateTime(z[3]).strftime('%Y-%m-%d %I:%M %p')
    if a[0]is None:
        json["revenue"] = 0
        json["bookedTicket"] = 0
    else:
        json["revenue"] = a[0]
        json["bookedTicket"] = a[1]    

    cur.close()
    conn.close()
    json["percent"] = round(json["bookedTicket"] / json["availed"] * 100)
    return render_template("admin/allocDetails.html", adminId=a_id, json=json)
