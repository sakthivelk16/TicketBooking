from flask import Flask, redirect
from flask_restful import Api
from flask_cors import CORS
from flask_login import LoginManager, login_required, logout_user

from models.module import *

from application.api.venue import VenueAPI
from application.api.show import ShowAPI
from application.api.allocation import AllocationAPI
from application.api.ShowVenue import (
    ShowAtVenueAPI,
    AllShowAtVenueAPI,
    ShowAtAllVenueAPI,
)


app = Flask(__name__)
app.secret_key = "abc"

login_manager = LoginManager()
login_manager.init_app(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.sqlite3"
api = Api()
CORS(app)
db.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return Users.query.filter_by(user_id=user_id).first()


@app.route("/logout")
@login_required
def user_logout():
    logout_user()
    return redirect("user/login")


api.add_resource(ShowAPI, "/api/show", "/api/show/<int:showId>")
api.add_resource(VenueAPI, "/api/venue", "/api/venue/<int:venueId>")
api.add_resource(AllocationAPI, "/api/allocation", "/api/allocation/<int:allocId>")
api.add_resource(ShowAtVenueAPI, "/api/venue/<int:venueId>/show/<int:showId>")
api.add_resource(AllShowAtVenueAPI, "/api/venue/<int:venueId>/show")
api.add_resource(ShowAtAllVenueAPI, "/api/show/<int:showId>/venue")

api.init_app(app)

app.app_context().push()


from application.controllers.login import *
from application.controllers.register import *
from application.controllers.userBookings import *
from application.controllers.venueAdmin import *
from application.controllers.showAdmin import *
from application.controllers.adminShowallocation import *
from application.controllers.rate import *
from application.controllers.search import *
from application.controllers.matplot import *
from application.controllers.adminProfile import *
from application.controllers.userProfile import *
from application.controllers.userHome import *
from application.controllers.adminHome import *
from application.controllers.excel import *

if __name__ == "__main__":
    app.debug = True
    app.run()
