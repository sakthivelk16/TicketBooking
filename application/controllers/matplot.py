import sqlite3
import matplotlib.pyplot as plt
from flask import Flask, redirect, render_template, request, url_for
from models.module import *
from flask import current_app as app


def subplot():
    try:
        conn = sqlite3.connect('instance/database.sqlite3')
        cur = conn.cursor()
        res = cur.execute(
            'SELECT total(totalprice),venue_name from(SELECT ticket_count*ticket_fare as totalprice,Venue_name from booking_details natural join show_venue natural join venue) group By(Venue_name) limit 5;'
        )
        valu, txt = [], []
        for each in res.fetchall():
            valu.append(each[0])
            txt.append(each[1])

        plt.bar(txt, valu, color='maroon', width=0.4)
        plt.xlabel("Venue Name")
        plt.ylabel("Revenue")
        plt.title("Venue with Highest Collection")
        plt.savefig('static/venueCollection.png')

        # if val=="maxPercentBooking":
        # # Show with maximum percent of booking in particular venue
        #     a = cur.execute(
        #     'SELECT sum(ticket_count)/(max_capacity*1.0) as percent_book,time,show_name,venue_name,sv_id from booking_details natural join show_venue natural join venue natural join show  group by sv_id having time between "2023-03-18 00:00:00" and "2023-03-18 23:59:59"and venue_name="abc" order by percent_book desc '
        # )

        # if val == 'byRating':
        # average rating of each show

        res = cur.execute(
            'SELECT avg(rating),show_name from rating natural JOIN show group by show_id limit 5'
        )
        valu, txt = [], []

        for each in res.fetchall():
            valu.append(each[0])
            txt.append(each[1])

        plt.clf()
        plt.bar(txt, valu, color='maroon', width=0.4)
        plt.xlabel("Show Name")
        plt.ylabel("Average Rating")
        plt.title("Top rated Shows")
        plt.savefig('static/topRating.png')

        # if val == 'tagcount':
        # tatal show per tags

        res = cur.execute(
            'SELECT count(*),tags from showtag group by tags limit 5')
        valu, txt = [], []
        for each in res.fetchall():
            valu.append(each[0])
            txt.append(each[1])

        plt.clf()
        plt.bar(txt, valu, color='maroon', width=0.4)
        plt.xlabel("Tags")
        plt.ylabel("total count")
        plt.title("Frequently used Tags")
        plt.savefig('static/tags.png')

        # if val == 'showRevenue':
        # each show revenue

        res = cur.execute(
            'SELECT total(totalprice),show_name from(SELECT ticket_count*ticket_fare as totalprice,show_name from booking_details natural join show_venue natural join show) group By(show_name) limit 5;'
        )
        valu, txt = [], []
        for each in res.fetchall():
            valu.append(each[0])
            txt.append(each[1])

        plt.clf()
        plt.bar(txt, valu, color='maroon', width=0.4)
        plt.xlabel("Show Name")
        plt.ylabel("Revenue")
        plt.title("Shows with most Revenue")
        plt.savefig('static/showRevenue.png')

        res = cur.execute(
            'SELECT sum(ticket_count)/(sum(max_capacity)*1.0) as fillPercent,show_name from booking_details natural JOIN show natural join show_venue natural join venue group by show_name order by fillPercent desc limit 5'
        )
        valu, txt = [], []
        for each in res.fetchall():
            valu.append(each[0])
            txt.append(each[1])

        plt.clf()
        plt.bar(txt, valu, color='maroon', width=0.4)
        plt.xlabel("Show Name")
        plt.ylabel("% booked")
        plt.title("% of Ticket booked")
        plt.savefig('static/bookPercent.png')
    except:
        print('error')
    finally:
        cur.close()
        conn.close()


@app.route("/admin/<int:adminId>/summary", methods={"GET", "POST"})
def summary(adminId):
    subplot()
    return render_template('summary.html', adminId=adminId)


@app.route("/admin/<int:adminId>/summary/advanced", methods={"GET", "POST"})
def summaryAdvanced(adminId):
    if request.method == "POST":

        if 'venueSubmit' in request.form:
            query = 'SELECT sum(ticket_count)/(max_capacity*1.0) as percent_book,time,show_name,venue_name,sv_id from booking_details natural join show_venue natural join venue natural join show  group by sv_id'
            query = query + ' having  venue_name="' + request.form[
                'venue'] + '" '
            if request.form['startTime'] != '':
                query = query + ' and time >= "' + request.form[
                    'startTime'] + '"'
            if request.form['endTime'] != '':
                query = query + ' and time <= "' + request.form['endTime'] + '"'
            query = query + '  order by percent_book desc;'

            return query
            # having time between "2023-03-18 00:00:00" and "2023-03-18 23:59:59"and venue_name="abc" order by percent_book desc'
    allVen = Venue.query.all()
    allShow = Show.query.all()
    print(allVen)
    return render_template('summaryAdvanced.html',
                           adminId=adminId,
                           show=allShow,
                           venue=allVen)
