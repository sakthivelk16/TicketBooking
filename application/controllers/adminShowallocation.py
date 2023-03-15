from flask import Flask, redirect, render_template, request, url_for
from models.module import *
from flask import current_app as app
from datetime import datetime, timedelta


@app.route("/admin/<int:a_id>/venue/<int:venue_id>/allocate",
           methods={"GET", "POST"})
def allocation(a_id, venue_id):
    if request.method == "POST":
        s1 = Show.query.all()
        print(request.form)
        allShowInCurrentVenue = ShowVenue.query.filter_by(
            venue_id=venue_id).order_by((ShowVenue.time)).all()
        currentShow = Show.query.get(request.form['selectShow'])
        showTime = request.form['showTime']
        expectedStartTime = datetime(int(showTime[0:4]), int(showTime[5:7]),
                                     int(showTime[8:10]), int(showTime[11:13]),
                                     int(showTime[14:16]))
        expectedEndTime = expectedStartTime + timedelta(
            minutes=currentShow.duration)
        currentTime = datetime.now()
        currentTime = currentTime.replace(second=0, microsecond=0)
        currentTimeplus15 = currentTime + timedelta(minutes=15)
        if expectedStartTime < currentTimeplus15:
            return render_template("allocation.html",
                                   error='timeConflict',
                                   adminId=a_id,
                                   show=s1)
        conflict = True
        if (len(allShowInCurrentVenue) == 0):
            conflict = False
        for i in range(len(allShowInCurrentVenue)):
            ss = Show.query.get(allShowInCurrentVenue[i].show_id)
            durationSS = ss.duration
            if (i == 0):
                if (expectedEndTime <=
                        allShowInCurrentVenue[i].time - timedelta(minutes=15)):
                    conflict = False
                    break
            if (i == len(allShowInCurrentVenue) - 1):
                if (expectedStartTime >= allShowInCurrentVenue[i].time +
                        timedelta(minutes=durationSS) + timedelta(minutes=15)):
                    conflict = False
                    break
            else:
                if (expectedEndTime <= allShowInCurrentVenue[i + 1].time -
                        timedelta(minutes=15) and
                        expectedStartTime >= allShowInCurrentVenue[i].time +
                        timedelta(minutes=durationSS) + timedelta(minutes=15)):
                    conflict = False
                    break
        if (conflict):
            return render_template("allocation.html",
                                   error='scheduleConflict',
                                   adminId=a_id,
                                   show=s1)
        else:
            sv1 = ShowVenue(show_id=request.form['selectShow'],
                            venue_id=venue_id,
                            time=expectedStartTime)
            db.session.add(sv1)
            db.session.commit()
            return redirect("/admin/" + str(a_id) + "/home")
    s1 = Show.query.all()
    return render_template('allocation.html', adminId=a_id, show=s1)
