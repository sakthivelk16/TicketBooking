from flask import Flask, redirect, render_template, request, url_for
from models.module import *
from flask import current_app as app

@app.route("/", methods={"GET", "POST"})
def login():
    if request.method == "POST":
        username = request.form['loginId']
        password = request.form['password']
        u1 = Users.query.filter_by()
        u1 = Users.query.filter_by(username=username,
                                   password=password).first()
        if u1 is None:
            return render_template("login/login.html", error=True)

        return redirect("/user/" + str(u1.user_id) + "/home")

    return render_template("login/login.html")


@app.route("/admin/login", methods={"GET", "POST"})
def adminLogin():
    if request.method == "POST":
        username = request.form['loginId']
        password = request.form['password']
        u1 = Admin.query.filter_by(username=username,
                                   password=password).first()
        if u1 is None:
            return render_template("login/adminlogin.html", error=True)

        return redirect("/admin/" + str(u1.admin_id) + "/home")

    return render_template("login/adminlogin.html")
