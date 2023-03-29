from flask import render_template, flash, request, redirect
from flask_login import current_user, login_required
from models.module import *
from flask import current_app as app


@app.route("/user/profile", methods={"GET", "POST"})
@login_required
def userProfile():
    user = Users.query.get(current_user.user_id)
    json = {}
    json["first_name"] = user.first_name
    json["last_name"] = user.last_name if user.last_name else ""
    json["phone_number"] = user.phone_number if user.phone_number else ""
    json["email_id"] = user.email_id if user.email_id else ""
    json["username"] = user.username
    return render_template("profile.html", user=json)


@app.route("/user/resetpassword", methods={"GET", "POST"})
@login_required
def userPassword():
    user = Users.query.get(current_user.user_id)
    if request.method == "POST":
        if request.form["newpassword"] != request.form["cnewpassword"]:
            flash("New password and confirm new password should be same", "danger")
            return render_template("resetPassword.html", username=user.username)
        if not user.is_password_correct(request.form["password"]):
            flash(
                "Your entered wrong current password. Enter correct one to proceed",
                "danger",
            )
            return render_template("resetPassword.html", username=user.username)
        if len(request.form["password"]) < 8 or len(request.form["password"]) > 32:
            flash("Password should be 8 to 32 character", "warning")
            return render_template("resetPassword.html", username=user.username)
        user.password = user.generate_password(request.form["newpassword"])
        db.session.commit()
        return redirect("/user/profile")
    return render_template("resetPassword.html", username=user.username)
