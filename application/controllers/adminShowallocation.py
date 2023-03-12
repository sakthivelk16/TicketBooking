from flask import Flask, redirect, render_template, request, url_for
from models.module import *
from flask import current_app as app
from datetime import datetime


@app.route("/admin/<int:a_id>/venue/<int:venue_id>/allocate",
           methods={"GET", "POST"})
def allocation(a_id, venue_id):
    if request.method == "POST":
        print(request.form)
        showTime = request.form['showTime']
        st = datetime(int(showTime[0:4]), int(showTime[5:7]),
                      int(showTime[8:10]), int(showTime[11:13]),
                      int(showTime[14:16]))
        sv1 = ShowVenue(show_id=request.form['selectShow'],
                        venue_id=venue_id,
                        time=st)
        db.session.add(sv1)
        db.session.commit()
        return redirect("/admin/" + str(a_id) + "/home")
    s1 = Show.query.all()
    return render_template('allocation.html', show=s1)
