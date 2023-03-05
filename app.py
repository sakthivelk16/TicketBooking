from flask import Flask, redirect, render_template, request
from models.module import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.sqlite3"

db.init_app(app)
app.app_context().push()

# db.session.execute(db.select(ShowVenue).order_by(ShowVenue.venue_id)).scalars() 
@app.route("/", methods={'GET', 'POST'})
def login():
    if request.method == 'POST':
        v = Venue.query.all()
        list = []
        for e in v:
            if len(e.venueShows) > 0:
                eachjson = {}
                eachjson['venue_id'] = e.venue_id
                eachjson['venue_name'] = e.venue_name
                eachjson['place'] = e.place
                eachjson['location'] = e.location
                eachjson['max_capacity'] = e.max_capacity
                eachjson['shows'] = []
                for ee in e.venueShows:
                    
                    print(ee.show_id)
                    innerjson = {}
                    innerjson['show_id'] = ee.show_id
                    innerjson['show_name'] = ee.show_name
                    innerjson['min_fare'] = ee.min_fare
                    BookingDetails.query.filter_by()
                    eachjson['shows'].append(innerjson)
                
                list.append(eachjson)
        print(list)

        return render_template('showDetails.html', list=list)
    return render_template('login.html')


@app.route("/user/register", methods={'GET', 'POST'})
def login1():
    if request.method == 'POST':
        fname = request.form['username']
        lmane = request.form['lname']
        mobile = request.form['mobile']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        print(request.form)
        if False:  # verify user name exist in login table
            return render_template('userRegistration.html',
                                   fname='qq',
                                   lname='ss')

        return redirect('/user/register/success')
    return render_template('userRegistration.html', fname='', lname='')


@app.route("/user/register/success", methods={'GET', 'POST'})
def login3():
    print(request.form)
    return render_template('registrationSuccessful.html')


@app.route("/admin/login", methods={'GET', 'POST'})
def adminLogin():
    return render_template('adminlogin.html')


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
