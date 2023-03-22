from flask_restful import reqparse, Resource, Api
from werkzeug.exceptions import HTTPException
import json
from flask import make_response
from models.module import *


def verifyInterger(value, defaultcode, code, message):
    try:
        return int(value)
    except ValueError:
        raise BuisnessValidationError(defaultcode, code, message)


class NotFoundError(HTTPException):
    def __init__(self, statusCode):
        self.response = make_response("", statusCode)


class BuisnessValidationError(HTTPException):
    def __init__(self, statusCode, errorCode, errorMessage):
        error = {"error_code": errorCode, "error_message": errorMessage}
        self.response = make_response(json.dumps(error), statusCode)


def gettags(show_id):
    tags = Showtag.query.filter_by(show_id=show_id).all()
    a = ""
    for each in tags:
        a += ";" + each.tags
    return a[1:]


parser = reqparse.RequestParser()
parser.add_argument("show_name")
parser.add_argument("min_fare")
parser.add_argument("duration")
parser.add_argument("is3d")
parser.add_argument("tags")


def showValidation(type):
    args = parser.parse_args()
    show_name = args.get("show_name", None)
    min_fare = args.get("min_fare", None)
    duration = args.get("duration", None)
    is3d = args.get("is3d", None)
    tags = args.get("tags", None)

    if (show_name is None and type == "post") or show_name == "":
        raise BuisnessValidationError(400, "SHOW001", "Show name is required")
    if (min_fare is None and type == "post") or min_fare == "":
        raise BuisnessValidationError(400, "SHOW002", "minimum Fare is required")
    if (duration is None and type == "post") or duration == "":
        raise BuisnessValidationError(400, "SHOW003", "duration is required")
    if (is3d is None and type == "post") or is3d == "":
        raise BuisnessValidationError(400, "SHOW004", "is3D is required")
    if (tags is None and type == "post") or tags == "":
        raise BuisnessValidationError(400, "SHOW005", "tags is required")

    if min_fare is not None:
        min_fare = verifyInterger(
            min_fare, 400, "SHOW006", "minimum Fare should be integer"
        )

        if min_fare <= 0:
            raise BuisnessValidationError(
                400, "SHOW007", "minimum Fare should be greater than 0"
            )
    if duration is not None:
        duration = verifyInterger(
            duration, 400, "SHOW008", "duration should be integer"
        )

        if duration <= 0:
            raise BuisnessValidationError(
                400, "SHOW009", "duration should be greater than 0"
            )

    if is3d is not None:
        if not (is3d == "True" or is3d == "False"):
            raise BuisnessValidationError(
                400, "SHOW010", "is3d eithier true or false in lowercase as boolean"
            )


class ShowAPI(Resource):
    def get(self, showId):
        currentShow = Show.query.get(showId)
        if currentShow:
            return {
                "show_id": currentShow.show_id,
                "show_name": currentShow.show_name,
                "min_fare": currentShow.min_fare,
                "duration": currentShow.duration,
                "is3d": currentShow.is3d,
                "tags": gettags(showId),
            }
        else:
            raise NotFoundError(statusCode=404)

    def post(self):
        showValidation("post")
        args = parser.parse_args()
        show_name = args.get("show_name", None)
        min_fare = args.get("min_fare", None)
        duration = args.get("duration", None)
        is3d = args.get("is3d", None)
        tags = args.get("tags", None)

        currentShowId = Show.query.filter_by(show_name=show_name).first()

        if currentShowId:
            raise NotFoundError(409)
        newShow = Show(
            show_name=show_name,
            min_fare=min_fare,
            duration=duration,
            is3d=False if is3d == "False" else True,
        )
        db.session.add(newShow)
        db.session.commit()
        currentShow = Show.query.filter_by(show_name=show_name).first()
        for each in tags.split(";"):
            eachShowTag = Showtag(show_id=currentShow.show_id, tags=each)
            db.session.add(eachShowTag)
            db.session.commit()
        return {
            "show_id": currentShow.show_id,
            "show_name": currentShow.show_name,
            "min_fare": currentShow.min_fare,
            "duration": currentShow.duration,
            "is3d": currentShow.is3d,
            "tags": gettags(currentShow.show_id),
        }, 201

    def put(self, showId):
        currentShow = Show.query.get(showId)
        if not currentShow:
            raise NotFoundError(404)
        showValidation(None)
        args = parser.parse_args()
        show_name = args.get("show_name", None)
        min_fare = args.get("min_fare", None)
        duration = args.get("duration", None)
        is3d = args.get("is3d", None)
        tags = args.get("tags", None)

        currentShow = Show.query.filter_by(show_name=show_name).all()
        for each in currentShow:
            if each.show_id != showId:
                raise NotFoundError(409)

        if show_name is not None:
            currentShow.show_name = show_name
        if min_fare is not None:
            currentShow.min_fare = min_fare
        if duration is not None:
            currentShow.duration = duration
        if is3d is not None:
            currentShow.is3d = False if is3d == "False" else True

        db.session.commit()
        currentShow = Show.query.get(showId)

        st = Showtag.query.filter_by(show_id=showId)
        for each in st:
            db.session.delete(each)
            db.session.commit()
        for each in tags.split(";"):
            st1 = Showtag(show_id=showId, tags=each).all()
            db.session.add(st1)
            db.session.commit()
        return {
            "show_id": currentShow.show_id,
            "show_name": currentShow.show_name,
            "min_fare": currentShow.min_fare,
            "duration": currentShow.duration,
            "is3d": currentShow.is3d,
            "tags": gettags(currentShow.show_id),
        }

    def delete(self, showId):
        currentShow = Show.query.get(showId)

        currentShowVenue = ShowVenue.query.filter_by(show_id=showId).all()
        if len(currentShowVenue) > 0:
            raise BuisnessValidationError(
                400,
                "SHOW011",
                "Show cannot be delete where there ia allocation available in the venue",
            )
        if currentShow:
            curRating = Rating.query.filter_by(show_id=showId).all()
            for each in curRating:
                db.session.delete(each)
                db.session.commit()
            st = Showtag.query.filter_by(show_id=showId).all()
            for each in st:
                db.session.delete(each)
                db.session.commit()
            db.session.delete(currentShow)
            db.session.commit()
            raise NotFoundError(200)
        else:
            raise NotFoundError(404)
