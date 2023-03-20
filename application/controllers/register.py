from flask import Flask, redirect, render_template, request, url_for, flash
from models.module import *
from flask import current_app as app


@app.route("/user/register", methods={"GET", "POST"})
def register():
    if request.method == "POST":
        fname = request.form["fname"]
        lname = request.form["lname"]
        mobile = request.form["mobile"]
        email = request.form["email"]
        username = request.form["username"]
        password = request.form["password"]
        isexist = Users.query.filter_by(username=username).all()
        if len(isexist) > 0:  # verify user name exist in login table
            flash('This username is already exist> please choose differnt one',
                  'danger')
            return render_template(
                "userRegistration/userRegistration.html",
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
        flash('User Registration Successfull', 'success')
        return redirect("/")
        return redirect("/user/register/success")
    return render_template("userRegistration/userRegistration.html")


@app.route("/user/register/success", methods={"GET", "POST"})
def registerSuccess():
    return render_template("userRegistration/registrationSuccessful.html")


@app.route("/admin/register", methods={"GET", "POST"})
def adminRegister():
    if request.method == "POST":
        fname = request.form["fname"]
        lname = request.form["lname"]
        mobile = request.form["mobile"]
        email = request.form["email"]
        username = request.form["username"]
        password = request.form["password"]
        adminCode = request.form["code"]
        isCodeExist = Admincode.query.filter_by(admin_code=adminCode).all()
        if len(isCodeExist) == 0:
            # This Code is Generated by register Admin. Get Valid code from Admin before Registration. <br> If you have valid code check case as Code feild is CASE SENSITIVE
            flash('This is not valid code. Code feild is Case-sensitive',
                  'danger')
            flash('If you do not have a valid code. Get from current Admin',
                  'info')
            return render_template("userRegistration/adminRegistration.html",
                                   
                                   fname=fname,
                                   lname=lname,
                                   mobile=mobile,
                                   email=email,
                                   username=username)
        db.session.delete(isCodeExist[0])
        db.session.commit()
        isexist = Admin.query.filter_by(username=username).all()
        if len(isexist) > 0:  # verify user name exist in login table
            flash('This username is already exist> please choose differnt one',
                  'danger')
            return render_template(
                "userRegistration/adminRegistration.html",
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
        db.session.add(u1)
        db.session.commit()
        flash('Admin Registration Successfull', 'success')
        return redirect("/admin/login")
        return redirect("/admin/register/success")
    flash('If you do not have a valid code. Get from current Admin',
                  'info')
    return render_template("userRegistration/adminRegistration.html")


@app.route("/admin/register/success", methods={"GET", "POST"})
def adminRegisterSuccess():
    return render_template("userRegistration/adminRegistrationSuccessful.html")
