import pandas
from models.module import *
from flask import current_app as app, redirect,flash
import os


def gettags(show_id):
    tags = Showtag.query.filter_by(show_id=show_id).all()
    a = ""
    for each in tags:
        a += ";" + each.tags.capitalize()
    return a[1:]

@app.route("/admin/<int:adminId>/venue/download", methods={"GET", "POST"})
def downloadVenue(adminId):
    path = "static"
    isExist = os.path.exists(path)
    if not isExist:
        os.makedirs(path)
    allVenue = Venue.query.all()
    res = []
    for e in allVenue:
        eachjson = {}
        eachjson["Id"] = e.venue_id
        eachjson["Name"] = e.venue_name.capitalize()
        eachjson["Place"] = e.place.capitalize()
        eachjson["Location"] = e.location.capitalize()
        eachjson["Capacity"] = e.max_capacity
        eachjson["2D Price"] = e.fare2D
        eachjson["3D Price"] = e.fare2D

        res.append(eachjson)
    df = pandas.DataFrame(res)
    df.to_csv("static/venue.csv",index=False)
    flash('Venue Download success. File stored in Static/venue','success')
    return redirect("/admin/" + str(adminId) + "/venue")


@app.route("/admin/<int:adminId>/show/download", methods={"GET", "POST"})
def downloadShow(adminId):
    path = "static"
    isExist = os.path.exists(path)
    if not isExist:
        os.makedirs(path)
    allShow = Show.query.all()
    res = []
    for e in allShow:
        eachjson = {}
        eachjson["Id"] = e.show_id
        eachjson["Name"] = e.show_name.capitalize()
        eachjson["Movie Basic Fare"] = e.min_fare
        eachjson["Duration"] = e.duration
        eachjson["is 3D"] = e.is3d
        eachjson['Tags']=gettags(e.show_id)

        res.append(eachjson)
    df = pandas.DataFrame(res)
    df.to_csv("static/Show.csv",index=False)
    flash('Show Download success. File stored in Static/Show','success')
    return redirect("/admin/" + str(adminId) + "/show")
