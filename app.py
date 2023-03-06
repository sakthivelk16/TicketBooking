from flask import Flask, redirect, render_template, request
from models.module import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.sqlite3"

db.init_app(app)
app.app_context().push()


@app.route("/user/<int:userID>/bookings", methods={"GET", "POST"})
def myBookings(userID):
    currentUser = Users.query.get(userID)
    allBookings = BookingDetails.query.filter_by(user_id=userID)
    final=[]
    for eachShowVenue in currentUser.mybookings:
        currentShow = Show.query.get(eachShowVenue.show_id)
        currentVenue = Venue.query.get(eachShowVenue.venue_id)
        json = {}
        json['venue_name'] = currentVenue.venue_name
        json['show_name'] = currentShow.show_name
        json['time'] = eachShowVenue.time
        final.append(json)
    return render_template('allBooking.html',userId=userID, bookings=final)


@app.route("/user/<int:userID>/book/<int:svId>", methods={"GET", "POST"})
def bookTicket(userID, svId):
    if request.method == "POST":
        ticketCount = request.form['ticketCount']
        b1 = BookingDetails(user_id=userID,
                            sv_id=svId,
                            ticket_count=ticketCount)
        db.session.add(b1)
        db.session.commit()
        return render_template('bookingSuccessful.html', userId=userID)
    currentVenueShow = ShowVenue.query.get(svId)
    currentShow = Show.query.filter_by(
        show_id=currentVenueShow.show_id).first()
    currentVenue = Venue.query.filter_by(
        venue_id=currentVenueShow.venue_id).first()
    allSVID = ShowVenue.query.filter_by(show_id=currentVenueShow.show_id).all()
    soldTicketCount = 0
    for eachSV in allSVID:
        allBookingDetails = BookingDetails.query.filter_by(
            sv_id=eachSV.sv_id).all()
        for eachBD in allBookingDetails:
            soldTicketCount = soldTicketCount + eachBD.ticket_count
    availabelTicket = currentVenue.max_capacity - soldTicketCount
    return render_template('bookingPage.html',
                           userId=userID,
                           show=currentShow,
                           venue=currentVenue,
                           currentVenueShow=currentVenueShow,
                           availabelTicket=availabelTicket)


@app.route("/user/<int:userID>/home", methods={"GET", "POST"})
def userHome(userID):
    if request.method == "POST":
        return redirect('/user/' + str(userID) + '/book/' +
                        request.form['book'].replace('book-', ''))

    v = Venue.query.all()
    list = []
    for e in v:
        allVenueShow = ShowVenue.query.filter_by(venue_id=e.venue_id).all()
        if len(allVenueShow) > 0:
            eachjson = {}
            eachjson["venue_id"] = e.venue_id
            eachjson["venue_name"] = e.venue_name
            eachjson["place"] = e.place
            eachjson["location"] = e.location
            eachjson["max_capacity"] = e.max_capacity
            eachjson["price2D"] = e.fare2D
            eachjson["price3D"] = e.fare3D
            eachjson["shows"] = []

            for ee in allVenueShow:
                currentShow = Show.query.filter_by(show_id=ee.show_id).first()

                allSVID = ShowVenue.query.filter_by(show_id=ee.show_id).all()
                soldTicketCount = 0
                for eachSV in allSVID:
                    allBookingDetails = BookingDetails.query.filter_by(
                        sv_id=eachSV.sv_id).all()

                    for eachBD in allBookingDetails:
                        soldTicketCount = soldTicketCount + eachBD.ticket_count
                innerjson = {}
                innerjson["sv_id"] = ee.sv_id
                innerjson["time"] = ee.time
                innerjson["show_id"] = currentShow.show_id
                innerjson["show_name"] = currentShow.show_name
                innerjson["is3d"] = currentShow.is3d
                innerjson[
                    "available_ticket"] = e.max_capacity - soldTicketCount
                innerjson["min_fare"] = currentShow.min_fare
                eachjson["shows"].append(innerjson)
            list.append(eachjson)
    return render_template("showDetails.html", userId=userID, list=list)


# db.session.execute(db.select(ShowVenue).order_by(ShowVenue.venue_id)).scalars()
@app.route("/", methods={"GET", "POST"})
def login():
    if request.method == "POST":
        username = request.form['loginId']
        password = request.form['password']
        u1 = Users.query.filter_by()
        u1 = Users.query.filter_by(username=username,
                                   password=password).first()
        if u1 is None:
            return render_template("login.html", error=True)

        return redirect("/user/" + str(u1.user_id) + "/home")

    return render_template("login.html")


@app.route("/user/register", methods={"GET", "POST"})
def register():
    if request.method == "POST":
        fname = request.form["username"]
        lname = request.form["lname"]
        mobile = request.form["mobile"]
        email = request.form["email"]
        username = request.form["username"]
        password = request.form["password"]
        isexist = Users.query.filter_by(username=username).all()
        if len(isexist) > 0:  # verify user name exist in login table
            return render_template(
                "userRegistration.html",
                exist="True",
                first_name=fname,
                last_name=lname,
                phone_number=mobile,
                email_id=email,
            )
        u1 = Users(
            first_name=fname,
            last_name=lname,
            phone_number=mobile,
            email_id=email,
            username=username,
            password=password,
        )
        db.session.add(u1)
        db.session.commit()
        return redirect("/user/register/success")
    return render_template("userRegistration.html")


@app.route("/user/register/success", methods={"GET", "POST"})
def registerSuccess():
    return render_template("registrationSuccessful.html")


@app.route("/admin/login", methods={"GET", "POST"})
def adminLogin():
    return render_template("adminlogin.html")


# @app.route("/student/<int:student_id>", methods={'GET', 'POST'})
# def showStudent(student_id):
#     s = Student.query.get(student_id)
#     c = s.studentCourses
#     return render_template('details.html', stud=s, cour=c)

# @app.route("/student/create", methods={'GET', 'POST'})
# def createStudent():
#     if request.method == 'POST':
#         roll = request.form.get("roll")
#         current = Student.query.filter_by(roll_number=roll).all()
#         if len(current) != 0:
#             return render_template('exists.html')
#         fName = request.form.get("f_name")
#         lname = request.form.get("l_name")
#         selcourse = request.form.getlist("courses")
#         s = Student(roll_number=roll, first_name=fName, last_name=lname)
#         db.session.add(s)
#         db.session.commit()
#         for each in selcourse:
#             c1 = Course.query.get(int(each.replace('course_', '')))
#             s.studentCourses.append(c1)
#             db.session.commit()
#         return redirect('/')
#     return render_template('addStudent.html')

# @app.route("/student/<int:student_id>/update", methods={'GET', 'POST'})
# def updateStudent(student_id):
#     if request.method == 'POST':
#         current = Student.query.get(student_id)
#         fName = request.form.get("f_name")
#         lname = request.form.get("l_name")
#         selcourse = request.form.getlist("courses")
#         current.first_name = fName
#         current.last_name = lname
#         db.session.commit()
#         current.studentCourses = []
#         for each in selcourse:
#             c1 = Course.query.get(int(each.replace('course_', '')))
#             current.studentCourses.append(c1)
#             db.session.commit()
#         return redirect('/')
#     current = Student.query.get(student_id)
#     return render_template('updateStudent.html', student=current)

# @app.route("/student/<int:student_id>/delete", methods={'GET', 'POST'})
# def deleteStudent(student_id):
#     s = Student.query.get(student_id)
#     db.session.delete(s)
#     db.session.commit()
#     return redirect('/')

if __name__ == "__main__":
    app.run()
