from flask import render_template, flash, request, redirect
from models.module import *
from flask import current_app as app


@app.route("/user/<int:userId>/profile", methods={"GET", "POST"})
def userProfile(userId):
    user = Users.query.get(userId)
    json = {}
    json["first_name"] = user.first_name
    json["last_name"] = user.last_name if user.last_name else ""
    json["phone_number"] = user.phone_number if user.phone_number else ""
    json["email_id"] = user.email_id if user.email_id else ""
    json["username"] = user.username
    return render_template("profile.html", user=json, userId=userId)


@app.route("/user/<int:userId>/resetpassword", methods={"GET", "POST"})
def userPassword(userId):
    user = Users.query.get(userId)
    if request.method == "POST":
        if request.form["newpassword"] != request.form["cnewpassword"]:
            flash("New password and confirm new password should be same", "danger")
            return render_template(
                "resetPassword.html", username=user.username, userId=userId
            )
        if request.form["password"] != user.password:
            flash(
                "Your entered wrong current password. Enter correct one to proceed",
                "danger",
            )
            return render_template(
                "resetPassword.html", username=user.username, userId=userId
            )
        user.password = request.form["newpassword"]
        db.session.commit()
        return redirect("/user/" + str(userId) + "/profile")
    user = Users.query.get(userId)
    return render_template("resetPassword.html", username=user.username, userId=userId)
