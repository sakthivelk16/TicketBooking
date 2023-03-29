import sqlite3
from flask import  flash, session, redirect, render_template, request, url_for
from sqlalchemy import func
from models.module import *
from flask import current_app as app
from datetime import  timedelta


def showValidating(show):
    if show.show_name is None or show.show_name == "":
        return (True, "show Name should not be empty")
    if len(show.show_name) > 64:
        return (True, "show Name Should be less than  or equal to 64 character")

    if show.duration is None or show.duration == "":
        return (True, "show duration should not be empty")
    try:
        int(show.duration)
    except ValueError:
        return (True, "duration should be not include any charcter")
    if int(show.duration) < 30 or int(show.duration) > 200:
        return (True, "max_capacity should between 30 and 200")

    if show.min_fare is None or show.min_fare == "":
        return (True, "show min_fare should not be empty")
    try:
        int(show.min_fare)
    except ValueError:
        return (True, "min_fare should be not include any charcter")
    if int(show.min_fare) < 50 or int(show.min_fare) > 300:
        return (True, "min_fare should between 50 and 300")

    return (False,None)


@app.route("/admin/<int:a_id>/show/create", methods={"GET", "POST"})
def showCreate(a_id):
    if request.method == "POST":
        name = request.form["showName"].lower()
        show1 = Show.query.filter_by(show_name=name).first()
        if show1 is not None:
            flash(
                " Another Show exists with same Name. please choose different Name",
                "danger",
            )
            showjson = {}
            showjson["tags"] = request.form["tags"].lower()
            showjson["duration"] = request.form["duration"]
            showjson["price"] = request.form["price"]
            showjson["is3D"] = True if "is3D" in request.form else False

            return render_template("admin/createShow.html", adminId=a_id, show=showjson)
        tags = request.form["tags"].lower()
        duration = request.form["duration"]
        price = request.form["price"]
        is3D = True if "is3D" in request.form else False

        s1 = Show(show_name=name, min_fare=price, is3d=is3D, duration=duration)
        validateResult = showValidating(s1)
        if validateResult[0]:
            flash(validateResult[1], "warning")
            return render_template("admin/createShow.html", adminId=a_id, show=showjson)
        if tags is None or tags == "":
            flash("Tags dhould not be empty", "warning")
            return render_template("admin/createShow.html", adminId=a_id, show=showjson)
        db.session.add(s1)
        db.session.commit()
        show1 = Show.query.filter_by(
            show_name=name.lower(), min_fare=price, is3d=is3D
        ).first()
        for each in tags.split(";"):
            if each !='':
                st1 = Showtag(show_id=show1.show_id, tags=each.lower())
                db.session.add(st1)
                db.session.commit()
        return redirect("/admin/" + str(a_id) + "/show")
    show = {}
    return render_template("admin/createShow.html", adminId=a_id, show=show)


@app.route("/admin/<int:a_id>/show", methods={"GET", "POST"})
def showHome(a_id):
    if "showError" in session:
        flash(
            "There is Still this show allocated to some Venue. So you are not allowed to delete the show",
            "danger",
        )
        session.pop("showError")

    allShow = Show.query.all()
    finalShow = []
    for eachShow in allShow:
        innerjson = {}
        innerjson["show_id"] = eachShow.show_id
        innerjson["show_name"] = eachShow.show_name
        innerjson["min_fare"] = eachShow.min_fare
        innerjson["duration"] = eachShow.duration
        innerjson["is3d"] = eachShow.is3d
        alltags = Showtag.query.filter_by(show_id=eachShow.show_id).all()
        a = ""
        for each in alltags:
            a = a + each.tags + ";"
        innerjson["tags"] = a[:-1]
        finalShow.append(innerjson)

    return render_template("admin/showAdmin.html", allShow=finalShow, adminId=a_id)


@app.route("/admin/<int:a_id>/show/<int:showId>/delete", methods={"GET", "POST"})
def deleteShow(a_id, showId):
    sv = ShowVenue.query.filter_by(show_id=showId).all()

    if len(sv) > 0:
        session["showError"] = True
        return redirect(url_for("showHome", a_id=a_id))
    allRating = Rating.query.filter_by(show_id=showId).all()
    for each in allRating:
        db.session.delete(each)
        db.session.commit()
    s = Show.query.get(showId)
    st = Showtag.query.filter_by(show_id=showId)
    for each in st:
        db.session.delete(each)
        db.session.commit()

    db.session.delete(s)
    db.session.commit()

    return redirect("/admin/" + str(a_id) + "/show")


@app.route("/admin/<int:a_id>/show/<int:showId>/edit", methods={"GET", "POST"})
def editShow(a_id, showId):
    if request.method == "POST":
        showjson = {}
        showjson["name"] = request.form["showName"].lower()
        showjson["tags"] = request.form["tags"].lower()
        showjson["duration"] = request.form["duration"]
        showjson["price"] = request.form["price"]
        showjson["is3D"] = True if "is3D" in request.form else False

        show1 = Show.query.filter(
            Show.show_name == showjson["name"], Show.show_id != showId
        ).all()

        if len(show1) > 0:
            flash(
                "Another Show exists with same Name. please choose different Name",
                "danger",
            )
            return render_template("admin/createShow.html", adminId=a_id, show=showjson)
        s1 = Show.query.get(showId)
        conflict = False
        if s1.duration != showjson["duration"]:
            myVenue = s1.venues
            for eachven in myVenue:
                allShowInCurrentVenue = (
                    ShowVenue.query.filter_by(venue_id=eachven.venue_id)
                    .order_by((ShowVenue.time))
                    .all()
                )
                for i in range(len(allShowInCurrentVenue)):
                    if i == len(allShowInCurrentVenue) - 1:
                        break
                    if allShowInCurrentVenue[i].show_id == s1.show_id:
                        if (
                            allShowInCurrentVenue[i].time
                            + timedelta(minutes=15 + int(showjson["duration"]))
                            > allShowInCurrentVenue[i + 1].time
                        ):
                            conflict = True
                            # conflictShow = allShowInCurrentVenue[i + 1]
                            # print(allShowInCurrentVenue[i + 1])
                            # print(allShowInCurrentVenue[i])
        if conflict:
            showjson["duration"] = ""
            flash(
                "Edited duration for show is conflicting with booked Schedule. Try reducing show duration or stick to original duration",
                "danger",
            )
            return render_template(
                "admin/createShow.html",
                adminId=a_id,
                show=showjson,
            )
        s1.show_name = showjson["name"].lower()
        s1.min_fare = showjson["price"]
        s1.duration = showjson["duration"]
        s1.is3d = showjson["is3D"]
        # db.session.add(s1)
        validateResult = showValidating(s1)
        if validateResult[0]:
            flash(validateResult[1], "warning")
            return render_template(
                "admin/createShow.html",
                adminId=a_id,
                show=showjson,
            )
        if showjson["tags"] is None or showjson["tags"] == "":
            flash("Tags should not be empty", "warning")
            return render_template(
                "admin/createShow.html",
                adminId=a_id,
                show=showjson,
            )

        db.session.commit()
        st = Showtag.query.filter_by(show_id=showId)
        for each in st:
            db.session.delete(each)
            db.session.commit()
        for each in showjson["tags"].split(";"):
            if each !='':
                st1 = Showtag(show_id=showId, tags=each.lower())
                db.session.add(st1)
                db.session.commit()
        return redirect("/admin/" + str(a_id) + "/show")
    currentShow = Show.query.get(showId)
    alltags = Showtag.query.filter_by(show_id=showId).all()
    a = ""
    for each in alltags:
        a = a + each.tags + ";"
    showjson = {}
    showjson["name"] = currentShow.show_name
    showjson["tags"] = a[:-1]
    showjson["duration"] = currentShow.duration
    showjson["price"] = currentShow.min_fare
    showjson["is3D"] = currentShow.is3d
    return render_template("admin/createShow.html", adminId=a_id, show=showjson)


@app.route("/admin/<int:a_id>/show/<int:showId>/details", methods={"GET", "POST"})
def eachShowDetails(a_id, showId):
    query = None
    error = {}

    text = "Unfiltered Show Details"
    query = "show_id=" + str(showId)
    if request.method == "POST":
        # t = datetime.strptime(sessionTo, "%Y-%m-%d") + timedelta(
        #         hours=23, minutes=59
            # )
        if request.form["from"] != "":
            query = query + " and time >= '" + request.form["from"] + "'"
            text = "Filtered Data from " + request.form["from"]
        if request.form["to"] != "":
            query = query + " and time <= '" + request.form["to"] + "23:59'"
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
        if text == "Unfiltered Show Details":
            error["ERROR"] = "THIS SHOW DOES NOT HAVE ALLOCATION"
            return render_template("admin/showDetails.html", adminId=a_id, json=error)
        else:
            error["ERROR1"] = "THIS SHOW DOES NOT HAVE ALLOCATION WITH FILTERED TIMEW"
            return render_template("admin/showDetails.html", adminId=a_id, json=error)
    json = {}
    json["availed"] = z[0]

    currentShow = Show.query.get(showId)
    json["text"] = text
    json["showName"] = currentShow.show_name
    json["duration"] = currentShow.duration

    res = cur.execute(
        "SELECT sum(ticket_count*ticket_fare) as summ, sum(ticket_count), sum(max_capacity),show_name from booking_details natural join show_venue natural join show NATURAL join venue where "
        + query
        + " group by show_name;"
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
    showRate=Rating.query.filter(Rating.show_id==showId).with_entities(func.avg(Rating.rating)).first()
    json["rate"] = 'Not Rated yet' if showRate[0] is None else round(showRate[0],1)
    json["percent"] = round(json["bookedTicket"] / json["availed"] * 100)
    return render_template("admin/showDetails.html", adminId=a_id, json=json)
