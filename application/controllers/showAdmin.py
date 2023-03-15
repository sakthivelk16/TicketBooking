from flask import Flask, session, redirect, render_template, request, url_for
from models.module import *
from flask import current_app as app

app.secret_key = "abc"


@app.route("/admin/<int:a_id>/show/create", methods={"GET", "POST"})
def showCreate(a_id):
    if request.method == "POST":
        print(request.form)
        name = request.form['showName']
        show1 = Show.query.filter_by(show_name=name).first()
        if show1 is not None:
            return render_template("createShow.html", adminId=a_id, error=True)
        tags = request.form['tags']
        duration = request.form['duration']
        price = request.form['price']
        is3D = False

        if 'is3D' in request.form:
            is3D = True
        s1 = Show(show_name=name, min_fare=price, is3d=is3D, duration=duration)
        db.session.add(s1)
        db.session.commit()
        show1 = Show.query.filter_by(show_name=name, min_fare=price,
                                     is3d=is3D).first()
        for each in tags.split(';'):
            st1 = Showtag(show_id=show1.show_id, tags=each)
            db.session.add(st1)
            db.session.commit()
        return redirect("/admin/" + str(a_id) + "/show")
    show = {}
    return render_template("createShow.html", adminId=a_id, show=show)


@app.route("/admin/<int:a_id>/show", methods={"GET", "POST"})
def showHome(a_id):
    error = None if ('showError' not in session) else 'NotDelete'
    session.clear()
    allShow = Show.query.all()
    finalShow = []
    for eachShow in allShow:
        innerjson = {}
        innerjson['show_id'] = eachShow.show_id
        innerjson['show_name'] = eachShow.show_name
        innerjson['min_fare'] = eachShow.min_fare
        innerjson['is3d'] = eachShow.is3d
        alltags = Showtag.query.filter_by(show_id=eachShow.show_id).all()
        a = ''
        for each in alltags:
            a = a + each.tags + ';'
        innerjson['tags'] = a[:-1]
        finalShow.append(innerjson)

    return render_template("showAdmin.html",
                           allShow=finalShow,
                           adminId=a_id,
                           error=error)


@app.route("/admin/<int:a_id>/show/<int:showId>/delete",
           methods={"GET", "POST"})
def deleteShow(a_id, showId):
    sv = ShowVenue.query.filter_by(show_id=showId).all()
    if len(sv) > 0:
        session['showError'] = True
        return redirect(url_for('showHome', a_id=a_id))
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
        print(request.form)
        showjson = {}
        showjson['name'] = request.form['showName']
        showjson['tags'] = request.form['tags']
        showjson['duration'] = request.form['duration']
        showjson['price'] = request.form['price']
        showjson['is3D'] = False

        if 'is3D' in request.form:
            showjson['is3D'] = True
        show1 = Show.query.filter_by(show_name=showjson['name']).all()
        for each in show1:
            if each.show_id != showId:
                return render_template(
                    "createShow.html",
                    error=True,
                    adminId=a_id,
                    show=showjson,
                )
        s1 = Show.query.get(showId)
        s1.show_name = showjson['name']
        s1.min_fare = showjson['price']
        s1.duration = showjson['duration']
        s1.is3d = showjson['is3D']
        db.session.add(s1)
        db.session.commit()
        st = Showtag.query.filter_by(show_id=showId)
        for each in st:
            db.session.delete(each)
            db.session.commit()
        for each in showjson['tags'].split(';'):
            st1 = Showtag(show_id=showId, tags=each)
            db.session.add(st1)
            db.session.commit()
        return redirect("/admin/" + str(a_id) + "/show")
    currentShow = Show.query.get(showId)
    alltags = Showtag.query.filter_by(show_id=showId).all()
    a = ''
    for each in alltags:
        a = a + each.tags + ';'
    showjson = {}
    showjson['name'] = currentShow.show_name
    showjson['tags'] = a[:-1]
    showjson['duration'] = currentShow.duration
    showjson['price'] = currentShow.min_fare
    showjson['is3D'] = currentShow.is3d
    return render_template("createShow.html", adminId=a_id, show=showjson)
