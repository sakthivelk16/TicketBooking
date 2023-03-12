from flask import Flask, redirect, render_template, request, url_for
from models.module import *
from flask import current_app as app

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
