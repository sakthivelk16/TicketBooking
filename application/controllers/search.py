from flask import Flask, flash, redirect, render_template, request, url_for, session
from models.module import *
from flask import current_app as app
from datetime import datetime
from sqlalchemy import func
from sqlalchemy.sql import label


@app.route("/user/<int:user_id>/search/result", methods={"GET", "POST"})
def filterResult(user_id):
    if request.method == "POST":
        return redirect('/user/' + str(user_id) + '/book/' +
                        request.form['book'].replace('book-', ''))

    if 'venue' not in session:
        return redirect('/user/' + str(user_id) + '/search')
    filterVenue = session['venue']
    session.clear()
    allBookings = BookingDetails.query.all()
    soldTick = {}
    for each in allBookings:
        if each.sv_id in soldTick:
            soldTick[each.sv_id] = soldTick[each.sv_id] + each.ticket_count
        else:
            soldTick[each.sv_id] = each.ticket_count
    avgRatings = db.session.query(Rating.show_id,
                                  label('members',
                                        func.avg(Rating.rating))).group_by(
                                            Rating.show_id).all()
    allRatings = {}
    for each in avgRatings:
        allRatings[each[0]] = each[1]

    tags = Showtag.query.all()
    allTags = {}
    for each in tags:
        if each.show_id in allTags:
            allTags[each.show_id] = allTags[each.show_id] + ';' + each.tags
        else:
            allTags[each.show_id] = each.tags

    list = []
    currentTime = datetime.now()
    for e in filterVenue:
        currentVenue = Venue.query.get(e)
        if 'show' in session:
            allVenueShow = ShowVenue.query.filter(
                ShowVenue.venue_id == currentVenue.venue_id,
                ShowVenue.time > currentTime,
                ShowVenue.show_id.in_(session['show'])).order_by(
                    ShowVenue.time).all()
        else:
            allVenueShow = ShowVenue.query.filter(
                ShowVenue.venue_id == currentVenue.venue_id,
                ShowVenue.time > currentTime).order_by(ShowVenue.time).all()
        if len(allVenueShow) > 0:
            eachjson = {}
            eachjson["venue_id"] = currentVenue.venue_id
            eachjson["venue_name"] = currentVenue.venue_name
            eachjson["place"] = currentVenue.place
            eachjson["location"] = currentVenue.location
            eachjson["max_capacity"] = currentVenue.max_capacity
            eachjson["price2D"] = currentVenue.fare2D
            eachjson["price3D"] = currentVenue.fare3D
            eachjson["shows"] = []

            for ee in allVenueShow:
                currentShow = Show.query.get(ee.show_id)
                innerjson = {}
                innerjson["sv_id"] = ee.sv_id
                innerjson["time"] = ee.time
                innerjson["show_id"] = currentShow.show_id
                innerjson["show_name"] = currentShow.show_name
                innerjson["is3d"] = currentShow.is3d
                innerjson["tag"] = allTags[
                    currentShow.
                    show_id] if currentShow.show_id in allTags else 'No Tags'
                innerjson['rating'] = allRatings[
                    currentShow.
                    show_id] if currentShow.show_id in allRatings else 'Not Rated'
                innerjson[
                    "available_ticket"] = currentVenue.max_capacity - soldTick[
                        ee.
                        sv_id] if ee.sv_id in soldTick else currentVenue.max_capacity

                if currentShow.is3d and currentShow.min_fare > currentVenue.fare3D:
                    innerjson["min_fare"] = currentShow.min_fare
                elif currentShow.is3d:
                    innerjson["min_fare"] = currentVenue.fare3D
                elif currentShow.min_fare > currentVenue.fare2D:
                    innerjson["min_fare"] = currentShow.min_fare
                else:
                    innerjson["min_fare"] = currentVenue.fare2D
                eachjson["shows"].append(innerjson)
            list.append(eachjson)
    return render_template("user/showDetails.html",
                           userId=user_id,
                           list=list,
                           search='searchpage')


@app.route("/user/<int:user_id>/search", methods={"GET", "POST"})
def search(user_id):
    if request.method == "POST":
        if 'venue' in request.form:
            if request.form['venue'] == '1':
                v1 = Venue.query.filter(
                    Venue.venue_name.like(request.form['venueSearch'])).all()
            elif request.form['venue'] == '2':
                v1 = Venue.query.filter(
                    Venue.venue_name.like(request.form['venueSearch'] +
                                          '%')).all()
            elif request.form['venue'] == '3':
                v1 = Venue.query.filter(
                    Venue.venue_name.like('%' +
                                          request.form['venueSearch'])).all()
            elif request.form['venue'] == '4':
                v1 = Venue.query.filter(
                    Venue.venue_name.like('%' + request.form['venueSearch'] +
                                          '%')).all()
        if 'LocationSearch' in request.form:
            v1 = Venue.query.filter_by(
                location=request.form['LocationSearch']).all()
        if 'LocationSearch' in request.form or 'venue' in request.form:

            if len(v1) == 0:
                flash(
                    'There is no venue found with provided search details. Try different combination',
                    'danger')
                return render_template('user/search.html', userId=user_id)

            ven = []
            for v in v1:
                ven.append(v.venue_id)
            allVenueShow = ShowVenue.query.filter(
                ShowVenue.venue_id.in_(ven),
                ShowVenue.time > datetime.now()).all()
            if len(allVenueShow) == 0:
                flash(
                    "There is  venue found with provided search details. But there is no scheduled show to book Tickets",
                    'warning')
                return render_template(
                    'user/search.html',
                    userId=user_id,
                )
            session['venue'] = ven
            return redirect(url_for('filterResult', user_id=user_id))
        if 'show' in request.form:
            if request.form['show'] == '1':
                s1 = Show.query.filter(
                    Show.show_name.like(request.form['showSearch'])).all()
            elif request.form['show'] == '2':
                s1 = Show.query.filter(
                    Show.show_name.like(request.form['showSearch'] +
                                        '%')).all()
            elif request.form['show'] == '3':
                s1 = Show.query.filter(
                    Show.show_name.like('%' +
                                        request.form['showSearch'])).all()
            elif request.form['show'] == '4':
                s1 = Show.query.filter(
                    Show.show_name.like('%' + request.form['showSearch'] +
                                        '%')).all()
            if len(s1) == 0:
                flash(
                    "There is no show found with provided search details. Try different combination",
                    'danger')
                return render_template('user/search.html', userId=user_id)
            shows = []
            ven = []
            for s in s1:
                shows.append(s.show_id)
                for v in s.venues:
                    ven.append(v.venue_id)
            allVenueShow = ShowVenue.query.filter(
                ShowVenue.time > datetime.now(),
                ShowVenue.show_id.in_(shows)).all()
            if len(allVenueShow) == 0:
                flash(
                    "There is show found with provided search details but there is no show schdule to book tickets",
                    "warning")
                return render_template('user/search.html', userId=user_id)
            ven = [*set(ven)]
            session['venue'] = ven
            session['show'] = shows
            return redirect(url_for('filterResult', user_id=user_id))

        if 'tagSearch' in request.form:
            st1 = Showtag.query.filter(
                Showtag.tags == request.form['tagSearch']).all()
            if len(st1) == 0:
                flash(
                    "There is no tag found with provided search details. Try different combination",
                    'danger')
                return render_template('user/search.html', userId=user_id)
            shows = []
            ven = []
            for st in st1:
                shows.append(st.shows.show_id)
                for v in st.shows.venues:
                    ven.append(v.venue_id)
            allVenueShow = ShowVenue.query.filter(
                ShowVenue.time > datetime.now(),
                ShowVenue.show_id.in_(shows)).all()
            if len(allVenueShow) == 0:
                flash(
                    "There is show found with provided search details but there is no show schdule to book tickets",
                    'warning')
                return render_template('user/search.html', userId=user_id)
            ven = [*set(ven)]
            session['venue'] = ven
            session['show'] = shows
            return redirect(url_for('filterResult', user_id=user_id))

        if 'ratingSearch' in request.form:
            avgRatings = db.session.query(
                Rating.show_id,
                label('members',
                      func.avg(Rating.rating))).group_by(Rating.show_id).all()
            shows = []
            ven = []
            for each in avgRatings:
                if each[1] >= int(request.form['ratingSearch']):
                    shows.append(each[0])
                    s = Show.query.get(each[0])
                    for v in s.venues:
                        ven.append(v.venue_id)
            if len(shows) == 0:
                flash(
                    "There is no show found with provided search details. Try different Combination",
                    'danger')
                return render_template('user/search.html', userId=user_id)
            allVenueShow = ShowVenue.query.filter(
                ShowVenue.time > datetime.now(),
                ShowVenue.show_id.in_(shows)).all()
            if len(allVenueShow) == 0:
                flash(
                    "There is show found with provided search details but there is no show schdule to book tickets",
                    'warning')
                return render_template('user/search.html', userId=user_id)
            ven = [*set(ven)]
            session['venue'] = ven
            session['show'] = shows
            return redirect(url_for('filterResult', user_id=user_id))

    return render_template('user/search.html', userId=user_id)
