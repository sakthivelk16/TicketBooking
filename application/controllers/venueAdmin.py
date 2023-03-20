from flask import Flask, flash, session, redirect, render_template, request, url_for
from models.module import *
from flask import current_app as app

app.secret_key = "abc"


@app.route("/admin/<int:a_id>/venue/create", methods={"GET", "POST"})
def venueCreate(a_id):
    if request.method == "POST":
        name = request.form['venue_name']
        place = request.form['place']
        location = request.form['location']
        capacity = request.form['max_capacity']
        fare2D = request.form['fare2D']
        fare3D = request.form['fare3D']
        v1 = Venue(venue_name=name,
                   place=place,
                   location=location,
                   max_capacity=capacity,
                   fare2D=fare2D,
                   fare3D=fare3D)
        db.session.add(v1)
        db.session.commit()
        return redirect("/admin/" + str(a_id) + "/venue")
    venue = {}
    return render_template("createVenue.html", adminId=a_id, venue=venue)


@app.route("/admin/<int:a_id>/venue", methods={"GET", "POST"})
def venueHome(a_id):
    error = None if ('venueError' not in session) else 'NotDelete'
    session.clear()
    allVenue = Venue.query.all()
    return render_template("venueHome.html",
                           allVenue=allVenue,
                           adminId=a_id,
                           error=error)


@app.route("/admin/<int:a_id>/venue/<int:venue_id>/delete",
           methods={"GET", "POST"})
def deleteVenue(a_id, venue_id):
    sv = ShowVenue.query.filter_by(venue_id=venue_id).all()
    if len(sv) > 0:
        session['venueError'] = True
        return redirect(url_for('venueHome', a_id=a_id))
    s = Venue.query.get(venue_id)
    db.session.delete(s)
    db.session.commit()
    return redirect("/admin/" + str(a_id) + "/venue")


@app.route("/admin/<int:a_id>/venue/<int:venueId>/edit",
           methods={"GET", "POST"})
def editVenue(a_id, venueId):
    if request.method == "POST":
        name = request.form['venue_name']
        place = request.form['place']
        location = request.form['location']
        capacity = request.form['max_capacity']
        fare2D = request.form['fare2D']
        fare3D = request.form['fare3D']
        venue1 = Venue.query.filter_by(venue_name=name).all()
        for each in venue1:
            flash(
                'There is Still some show allocated to this Venue. Please delete allocation from Venue before Deleting this Venue',
                'danger')
            if each.venue_id != venueId:
                return render_template(
                    "createVenue.html",
                    adminId=a_id,
                    venue=request.form,
                )
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

    return render_template("createVenue.html",
                           adminId=a_id,
                           venue=currentVenue)
