import sqlite3
import matplotlib
import matplotlib.pyplot as plt
from flask import flash, redirect, render_template, request, url_for
from models.module import *
from flask import current_app as app
import os
import sys
from datetime import datetime, timedelta

matplotlib.use("Agg")


def subplot():
    try:
        conn = sqlite3.connect("instance/database.sqlite3")
        cur = conn.cursor()
        res = cur.execute(
            "SELECT sum(ticket_count*ticket_fare) as tot,Venue_name from booking_details natural join show_venue natural join venue group By(Venue_name) order by tot desc limit 5"
        )
        valu, txt = [], []
        for each in res.fetchall():
            valu.append(each[0])
            txt.append(each[1].capitalize())

        plt.clf()
        plt.bar(txt, valu, color="maroon", width=0.4)
        plt.xlabel("Venue Name")
        plt.ylabel("Revenue")
        plt.title("Venue with Highest Collection")
        plt.savefig("static/venueCollection.png")

        res = cur.execute(
            "SELECT avg(rating) as aver,show_name from rating natural JOIN show group by show_id order by aver desc limit 5"
        )
        valu, txt = [], []

        for each in res.fetchall():
            valu.append(each[0])
            txt.append(each[1].capitalize())

        plt.clf()
        plt.bar(txt, valu, color="maroon", width=0.4)
        plt.xlabel("Show Name")
        plt.ylabel("Average Rating")
        plt.title("Top rated Shows")
        plt.savefig("static/topRating.png")

        # if val == 'tagcount':
        # tatal show per tags

        res = cur.execute(
            "SELECT count(*) as ct,tags from showtag group by tags order by ct desc limit 5"
        )
        valu, txt = [], []
        for each in res.fetchall():
            valu.append(each[0])
            txt.append(each[1].capitalize())

        plt.clf()
        plt.bar(txt, valu, color="maroon", width=0.4)
        plt.xlabel("Tags")
        plt.ylabel("total count")
        plt.title("Frequently used Tags")
        plt.savefig("static/tags.png")

        # if val == 'showRevenue':
        # each show revenue

        res = cur.execute(
            "SELECT total(totalprice) as tp,show_name from(SELECT ticket_count*ticket_fare as totalprice,show_name from booking_details natural join show_venue natural join show) group By(show_name) order by tp desc limit 5;"
        )
        valu, txt = [], []
        for each in res.fetchall():
            valu.append(each[0])
            txt.append(each[1].capitalize())

        plt.clf()
        plt.bar(txt, valu, color="maroon", width=0.4)
        plt.xlabel("Show Name")
        plt.ylabel("Revenue")
        plt.title("Shows with most Revenue")
        plt.savefig("static/showRevenue.png")

        res = cur.execute(
            "SELECT sum(ticket_count)/(sum(max_capacity)*1.0) as fillPercent,show_name from booking_details natural JOIN show natural join show_venue natural join venue group by show_name order by fillPercent desc limit 5"
        )
        valu, txt = [], []
        for each in res.fetchall():
            valu.append(each[0] * 100)
            txt.append(each[1].capitalize())

        plt.clf()
        plt.bar(txt, valu, color="maroon", width=0.4)
        plt.xlabel("Show Name")
        plt.ylabel("% booked")
        plt.title("% of Ticket booked")
        plt.savefig("static/bookPercent.png")
    except:
        e = sys.exc_info()[0]
        print(e)
    finally:
        cur.close()
        conn.close()


def venuePlot(endQuery):
    try:
        conn = sqlite3.connect("instance/database.sqlite3")
        cur = conn.cursor()

        plt.clf()
        res = cur.execute(
            "SELECT count(*) as total_show, show_name from venue natural join show natural join show_venue where "
            + endQuery
            + "group by show_name order by total_show desc limit 5"
        )

        valu, txt = [], []
        for each in res.fetchall():
            valu.append(each[0])
            txt.append(each[1].capitalize())

        plt.bar(txt, valu, color="maroon", width=0.4)
        plt.xlabel("Show Name")
        plt.ylabel("Count")
        plt.title("Total Show Count in Filtered Date")
        plt.savefig("static/showCountVenue.png")

        res = cur.execute(
            "SELECT sum(ticket_count*ticket_fare) as sumTicket,show_name from booking_details natural join show_venue natural join show natural join venue where  "
            + endQuery
            + " group by show_name order by sumTicket desc limit 5"
        )
        valu, txt = [], []
        for each in res.fetchall():
            valu.append(each[0])
            txt.append(each[1].capitalize())

        plt.clf()
        plt.bar(txt, valu, color="maroon", width=0.4)
        plt.xlabel("Show Name")
        plt.ylabel("Revenue")
        plt.title("Shows with most Revenue")
        plt.savefig("static/showRevenueatVenueMax.png")

        res = cur.execute(
            "SELECT sum(ticket_count*ticket_fare) as sumTicket,show_name from booking_details natural join show_venue natural join show natural join venue where  "
            + endQuery
            + " group by show_name order by sumTicket limit 5"
        )
        valu, txt = [], []
        for each in res.fetchall():
            valu.append(each[0])
            txt.append(each[1].capitalize())

        plt.clf()
        plt.bar(txt, valu, color="maroon", width=0.4)
        plt.xlabel("Show Name")
        plt.ylabel("Revenue")
        plt.title("Shows with minimum Revenue")
        plt.savefig("static/showRevenueatVenueMin.png")

        res = cur.execute(
            "SELECT sum(ticket_count)/(sum(max_capacity)*1.0) as book_percent,show_name from booking_details natural join show_venue natural join show natural join venue where "
            + endQuery
            + " group by show_name order by book_percent desc limit 5"
        )
        valu, txt = [], []
        for each in res.fetchall():
            valu.append(each[0] * 100)
            txt.append(each[1].capitalize())

        plt.clf()
        plt.bar(txt, valu, color="maroon", width=0.4)
        plt.xlabel("Show Name")
        plt.ylabel("BookingPercent")
        plt.title("Shows with maximum  booking Percent")
        plt.savefig("static/showBookPercentMax.png")

        res = cur.execute(
            "SELECT sum(ticket_count)/(sum(max_capacity)*1.0) as book_percent,show_name from booking_details natural join show_venue natural join show natural join venue where "
            + endQuery
            + " group by show_name order by book_percent limit 5"
        )
        valu, txt = [], []
        for each in res.fetchall():
            valu.append(each[0] * 100)
            txt.append(each[1].capitalize())

        plt.clf()
        plt.bar(txt, valu, color="maroon", width=0.4)
        plt.xlabel("Show Name")
        plt.ylabel("BookingPercent")
        plt.title("Shows with minimum  booking Percent")
        plt.savefig("static/showBookPercentMin.png")

    except:
        e = sys.exc_info()[0]
        print(e)
        pass
    finally:
        cur.close()
        conn.close()


def showPlot(endQuery):
    try:
        conn = sqlite3.connect("instance/database.sqlite3")
        cur = conn.cursor()

        plt.clf()
        res = cur.execute(
            "SELECT count(*) as total_venue, venue_name from venue natural join show natural join show_venue where "
            + endQuery
            + "group by venue_name order by total_venue desc limit 5"
        )
        valu, txt = [], []
        for each in res.fetchall():
            valu.append(each[0])
            txt.append(each[1].capitalize())

        plt.bar(txt, valu, color="maroon", width=0.4)
        plt.xlabel("Venue Name")
        plt.ylabel("Count")
        plt.title("Total Venue Count of Show")
        plt.savefig("static/VenueCountShow.png")

        res = cur.execute(
            "SELECT sum(ticket_count*ticket_fare) as sumTicket,venue_name from booking_details natural join show_venue natural join show natural join venue where  "
            + endQuery
            + " group by venue_name order by sumTicket desc limit 5"
        )
        valu, txt = [], []
        for each in res.fetchall():
            valu.append(each[0])
            txt.append(each[1].capitalize())

        plt.clf()
        plt.bar(txt, valu, color="maroon", width=0.4)
        plt.xlabel("Venue Name")
        plt.ylabel("Revenue")
        plt.title("Venue with most Revenue")
        plt.savefig("static/venueRevenueForShowMax.png")

        res = cur.execute(
            "SELECT sum(ticket_count*ticket_fare) as sumTicket,venue_name from booking_details natural join show_venue natural join show natural join venue where  "
            + endQuery
            + " group by venue_name order by sumTicket limit 5"
        )
        valu, txt = [], []
        for each in res.fetchall():
            valu.append(each[0])
            txt.append(each[1].capitalize())

        plt.clf()
        plt.bar(txt, valu, color="maroon", width=0.4)
        plt.xlabel("Venue Name")
        plt.ylabel("Revenue")
        plt.title("Venue with min Revenue")
        plt.savefig("static/venueRevenueForShowMin.png")

        res = cur.execute(
            "SELECT sum(ticket_count)/(sum(max_capacity)*1.0) as book_percent,venue_name from booking_details natural join show_venue natural join show natural join venue where "
            + endQuery
            + " group by venue_name order by book_percent desc limit 5"
        )
        valu, txt = [], []
        for each in res.fetchall():
            valu.append(each[0] * 100)
            txt.append(each[1].capitalize())

        plt.clf()
        plt.bar(txt, valu, color="maroon", width=0.4)
        plt.xlabel("Venue Name")
        plt.ylabel("BookingPercent")
        plt.title("Venues with maximum booking Percent")
        plt.savefig("static/venueBookPercentMax.png")

        res = cur.execute(
            "SELECT sum(ticket_count)/(sum(max_capacity)*1.0) as book_percent,venue_name from booking_details natural join show_venue natural join show natural join venue where "
            + endQuery
            + " group by venue_name order by book_percent limit 5"
        )
        valu, txt = [], []
        for each in res.fetchall():
            valu.append(each[0] * 100)
            txt.append(each[1].capitalize())

        plt.clf()
        plt.bar(txt, valu, color="maroon", width=0.4)
        plt.xlabel("Show Name")
        plt.ylabel("BookingPercent")
        plt.title("Venue with minimum  booking Percent")
        plt.savefig("static/venueBookPercentMin.png")
    except:
        e = sys.exc_info()[0]
        print(e)
        pass
    finally:
        cur.close()
        conn.close()


@app.route("/admin/<int:adminId>/summary", methods={"GET", "POST"})
def summary(adminId):
    # create path if doesn't exist
    path = "static"
    isExist = os.path.exists(path)
    if not isExist:
        os.makedirs(path)
    subplot()
    return render_template("admin/summary.html", adminId=adminId)


@app.route("/admin/<int:adminId>/summary/advanced", methods={"GET", "POST"})
def summaryAdvanced(adminId):
    if request.method == "POST":
        path = "static"
        isExist = os.path.exists(path)
        if not isExist:
            os.makedirs(path)
        sti = request.form["startTime"]
        eti = request.form["endTime"]

        if sti != "":
            stime = datetime.strptime(request.form["startTime"], "%Y-%m-%d")
        if eti != "":
            etime = datetime.strptime(request.form["endTime"], "%Y-%m-%d") + timedelta(
                hours=23, minutes=59
            )
        if sti != "" and eti != "" and stime > etime:
            flash(
                "start time is greater than end time ans search is not possible",
                "danger",
            )
            allVen = Venue.query.all()
            allShow = Show.query.all()
            return render_template(
                "admin/summaryAdvanced.html",
                adminId=adminId,
                show=allShow,
                venue=allVen,
            )

        if "venueSubmit" in request.form:
            v1 = Venue.query.filter(
                Venue.venue_name == request.form["venue"].split("-")[0],
                Venue.location == request.form["venue"].split("-")[1],
            ).first()
            if sti == "" and eti == "":
                s1 = ShowVenue.query.filter_by(venue_id=v1.venue_id).all()
            elif sti == "":
                s1 = ShowVenue.query.filter(
                    ShowVenue.venue_id == v1.venue_id, ShowVenue.time < etime
                ).all()
            elif eti == "":
                s1 = ShowVenue.query.filter(
                    ShowVenue.venue_id == v1.venue_id, ShowVenue.time > stime
                ).all()
            else:
                s1 = ShowVenue.query.filter(
                    ShowVenue.venue_id == v1.venue_id,
                    ShowVenue.time > stime,
                    ShowVenue.time < etime,
                ).all()
            if len(s1) == 0:
                flash(
                    "No data are avilable with filtered result",
                    "danger",
                )
                allVen = Venue.query.all()
                allShow = Show.query.all()
                return render_template(
                    "admin/summaryAdvanced.html",
                    adminId=adminId,
                    show=allShow,
                    venue=allVen,
                )
            query = (
                'venue_name="'
                + request.form["venue"].split("-")[0]
                + '" and location="'
                + request.form["venue"].split("-")[1]
                + '" '
            )
            if sti != "":
                query = query + ' and time >= "' + request.form["startTime"] + '"'
            if eti != "":
                query = query + ' and time <= "' + request.form["endTime"] + '23:59"'
            venuePlot(query)
            return render_template("admin/venueSummary.html", adminId=adminId)

        if "showSubmit" in request.form:
            filShow = Show.query.filter_by(show_name=request.form["show"]).first()
            if sti == "" and eti == "":
                s1 = ShowVenue.query.filter_by(show_id=filShow.show_id).all()
            elif sti == "":
                s1 = ShowVenue.query.filter(
                    ShowVenue.show_id == filShow.show_id, ShowVenue.time < etime
                ).all()
            elif eti == "":
                s1 = ShowVenue.query.filter(
                    ShowVenue.show_id == filShow.show_id, ShowVenue.time > stime
                ).all()
            else:
                s1 = ShowVenue.query.filter(
                    ShowVenue.show_id == filShow.show_id,
                    ShowVenue.time > stime,
                    ShowVenue.time < etime,
                ).all()
            if len(s1) == 0:
                flash(
                    "No data are avilable with filtered result",
                    "danger",
                )
                allVen = Venue.query.all()
                allShow = Show.query.all()
                return render_template(
                    "admin/summaryAdvanced.html",
                    adminId=adminId,
                    show=allShow,
                    venue=allVen,
                )
            query = 'show_name="' + request.form["show"] + '" '
            if request.form["startTime"] != "":
                query = query + ' and time >= "' + request.form["startTime"] + '"'
            if request.form["endTime"] != "":
                query = query + ' and time <= "' + request.form["endTime"] + '23:59"'
            showPlot(query)
            return render_template("admin/showSummary.html", adminId=adminId)

    allVen = Venue.query.all()
    allShow = Show.query.all()
    return render_template(
        "admin/summaryAdvanced.html", adminId=adminId, show=allShow, venue=allVen
    )
