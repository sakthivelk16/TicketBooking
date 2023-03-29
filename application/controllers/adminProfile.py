from flask import render_template, flash, request, redirect
from models.module import *
from flask import current_app as app
import string
import random


@app.route("/admin/<int:adminId>/profile", methods={"GET", "POST"})
def adminProfile(adminId):
    admin = Admin.query.get(adminId)
    json = {}
    json["first_name"] = admin.first_name
    json["last_name"] = admin.last_name if admin.last_name else ""
    json["phone_number"] = admin.phone_number if admin.phone_number else ""
    json["email_id"] = admin.email_id if admin.email_id else ""
    json["username"] = admin.username
    return render_template("profile.html", user=json, admin=True, userId=adminId)


@app.route("/admin/<int:adminId>/resetpassword", methods={"GET", "POST"})
def adminPassword(adminId):
    user = Admin.query.get(adminId)
    if request.method == "POST":
        if request.form["newpassword"] != request.form["cnewpassword"]:
            flash("New password and confirm new password should be same", "danger")
            return render_template(
                "resetPassword.html", username=user.username, userId=adminId, admin=True
            )
        if not user.is_password_correct(request.form["password"]):
            flash(
                "Your entered wrong current password. Enter correct one to proceed",
                "danger",
            )
            return render_template(
                "resetPassword.html", username=user.username, userId=adminId, admin=True
            )
        if len(request.form["password"]) < 8 or len(request.form["password"]) > 32:
            flash("Password should be 8 to 32 character", "warning")
            return render_template(
                "resetPassword.html", username=user.username, userId=adminId, admin=True
            )
        user.password = user.generate_password(request.form["newpassword"])
        db.session.commit()
        return redirect("/admin/" + str(adminId) + "/profile")
    user = Admin.query.get(adminId)
    return render_template(
        "resetPassword.html", username=user.username, userId=adminId, admin=True
    )


@app.route("/admin/<int:adminId>/generete", methods={"GET", "POST"})
def GenerateCode(adminId):
    N = 10
    res = "".join(random.choices(string.ascii_letters, k=N))
    ac1 = Admincode(admin_code=res)
    db.session.add(ac1)
    db.session.commit()
    return render_template("admin/adminCode.html", code=str(res), adminId=adminId)
