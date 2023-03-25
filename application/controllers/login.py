from flask import Flask,  redirect, render_template, request, session, url_for, flash
from flask_login import login_user
from models.module import *
from flask import current_app as app

@app.route("/", methods={"GET", "POST"})
def intialPage():
    return redirect('/user/login')

@app.route("/user/login", methods={"GET", "POST"})
def login():
    if request.method == "POST":
        username = request.form['loginId'].lower()
        password = request.form['password']
        u1 = Users.query.filter_by()
        u1 = Users.query.filter_by(username=username,
                                   password=password).first()
        if u1 is None:
            flash('Invalid Login details', "danger")
            return render_template("login/login.html", error=True)
        login_user(u1)
        return redirect("/user/home")
    session.clear()
    return render_template("login/login.html")


@app.route("/admin/login", methods={"GET", "POST"})
def adminLogin():
    if request.method == "POST":
        username = request.form['loginId'].lower()
        password = request.form['password']
        u1 = Admin.query.filter_by(username=username,
                                   password=password).first()
        if u1 is None:
            flash('Invalid Login details', "danger")
            return render_template("login/adminlogin.html", error=True)

        return redirect("/admin/" + str(u1.admin_id) + "/home")

    return render_template("login/adminlogin.html")
