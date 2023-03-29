from flask import Flask, redirect, render_template, request, url_for, flash
from models.module import *
from flask import current_app as app


def userValidating(user):
    if user.first_name is None or user.first_name == "":
        return (True, "first_name should not be empty")
    if len(user.first_name) > 32:
        return (True, "first_name Should be less than  or equal to 32 character")

    if user.last_name is None or user.last_name == "":
        return (True, "last_name should not be empty")
    if len(user.last_name) > 32:
        return (True, "last_name Should be less than  or equal to 32 character")

    if (
        user.phone_number is not None
        and user.phone_number != ""
        and len(str(user.phone_number)) != 10
    ):
        return (True, "phone_number Should be empty or exactly 10 character")

    if (
        user.email_id is not None
        and user.email_id != ""
        and (len(user.email_id) > 32 or len(user.email_id) < 3)
    ):
        return (True, "email_id Should be 3 to 32 character")

    if user.username is None or user.username == "":
        return (True, "username should not be empty")
    if len(user.username) > 32 or len(user.username) < 3:
        return (True, "username Should be 3 to 32 character")

    if user.password is None or user.password == "":
        return (True, "password should not be empty")
    if  len(user.password) < 8:
        return (True, "password Should greater than 8  character")

    return (False, None)


def adminValidating(user):
    if user.first_name is None or user.first_name == "":
        return (True, "first_name should not be empty")
    if len(user.first_name) > 32:
        return (True, "first_name Should be less than  or equal to 32 character")

    if user.last_name is None or user.last_name == "":
        return (True, "last_name should not be empty")
    if len(user.last_name) > 32:
        return (True, "last_name Should be less than  or equal to 32 character")

    if user.phone_number is None or user.phone_number == "":
        return (True, "phone_number should not be empty")
    if len(str(user.phone_number)) != 10:
        return (True, "phone_number Should be exactly 10 character")

    if user.email_id is None or user.email_id == "":
        return (True, "email_id should not be empty")
    if len(user.email_id) > 32 or len(user.email_id) < 3:
        return (True, "email_id Should be 3 to 32 character")

    if user.username is None or user.username == "":
        return (True, "username should not be empty")
    if len(user.username) > 32:
        return (True, "username Should be 3 to 32 character")

    if user.password is None or user.password == "":
        return (True, "password should not be empty")
    if  len(user.password) < 8:
        return (True, "password Should greater than 8  character")


    return (False, None)


@app.route("/user/register", methods={"GET", "POST"})
def register():
    if request.method == "POST":
        fname = request.form["fname"].lower()
        lname = request.form["lname"].lower()
        mobile = request.form["mobile"]
        email = request.form["email"].lower()
        username = request.form["username"].lower()
        password = request.form["password"]
        isexist = Users.query.filter_by(username=username).all()
        if len(isexist) > 0:  # verify user name exist in login table
            flash(
                "This username is already exist. Please choose differnt one", "danger"
            )
            return render_template(
                "registration/userRegistration.html",
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
        validateResult = userValidating(u1)
        if validateResult[0]:
            flash(validateResult[1], "warning")
            return render_template(
                "registration/userRegistration.html",
                first_name=fname,
                last_name=lname,
                phone_number=mobile,
                email_id=email,
            )

        db.session.add(u1)
        db.session.commit()
        flash("User Registration Successfull", "success")
        return redirect("/")
    return render_template("registration/userRegistration.html")


@app.route("/admin/register", methods={"GET", "POST"})
def adminRegister():
    if request.method == "POST":
        fname = request.form["fname"].lower()
        lname = request.form["lname"].lower()
        mobile = request.form["mobile"]
        email = request.form["email"].lower()
        username = request.form["username"].lower()
        password = request.form["password"]
        adminCode = request.form["code"]
        isCodeExist = Admincode.query.filter_by(admin_code=adminCode).all()
        if len(isCodeExist) == 0:
            # This Code is Generated by register Admin. Get Valid code from Admin before Registration. <br> If you have valid code check case as Code feild is CASE SENSITIVE
            flash("This is not valid code. Code feild is Case-sensitive", "danger")
            flash("If you do not have a valid code. Get from current Admin", "info")
            return render_template(
                "registration/adminRegistration.html",
                fname=fname,
                lname=lname,
                mobile=mobile,
                email=email,
                username=username,
            )
        db.session.delete(isCodeExist[0])
        db.session.commit()
        isexist = Admin.query.filter_by(username=username).all()
        if len(isexist) > 0:  # verify user name exist in login table
            flash(
                "This username is already exist. Please choose differnt one", "danger"
            )
            return render_template(
                "registration/adminRegistration.html",
                fname=fname,
                lname=lname,
                mobile=mobile,
                email=email,
            )
        
        u1 = Admin(
            first_name=fname,
            last_name=lname,
            phone_number=mobile,
            email_id=email,
            username=username,
            password=password,
        )
        validateResult = adminValidating(u1)
        if validateResult[0]:
            flash(validateResult[1], "warning")
            return render_template(
                "registration/adminRegistration.html",
                fname=fname,
                lname=lname,
                mobile=mobile,
                email=email,
            )
        db.session.add(u1)
        db.session.commit()
        flash("Admin Registration Successfull", "success")
        return redirect("/admin/login")
    flash("If you do not have a valid code. Get from current Admin", "info")
    return render_template("registration/adminRegistration.html")
