from flask_restful import reqparse, Resource, Api
from sqlalchemy import and_
from werkzeug.exceptions import HTTPException
import json
from flask import make_response
from models.module import *
import re
from datetime import datetime, timedelta


def timeConstraint(curShow, curVenue, time, edit=False, sv_id=None):
    curTime = datetime.now()
    curTime = curTime.replace(second=0, microsecond=0)
    currentTimeplus15 = curTime + timedelta(minutes=15)

    expectedStartTime = generatedateTime(time)
    expectedEndTime = expectedStartTime + timedelta(minutes=curShow.duration)
    if expectedStartTime < currentTimeplus15:
        raise BuisnessValidationError(
            400, "ALLOC006",
            "Allocation can be done from current time + 15 mins")
    if edit:

        allShowInCurrentVenue = ShowVenue.query.filter(
            ShowVenue.sv_id != sv_id,
            ShowVenue.venue_id == curVenue.venue_id).order_by(
                (ShowVenue.time)).all()
    else:
        allShowInCurrentVenue = ShowVenue.query.filter_by(
            venue_id=curVenue.venue_id).order_by((ShowVenue.time)).all()
    conflict = True
    if (len(allShowInCurrentVenue) == 0):
        conflict = False
    for i in range(len(allShowInCurrentVenue)):
        ss = Show.query.get(allShowInCurrentVenue[i].show_id)
        durationSS = ss.duration
        if (i == 0):
            if (expectedEndTime <=
                    allShowInCurrentVenue[i].time - timedelta(minutes=15)):
                conflict = False
                break
        if (i == len(allShowInCurrentVenue) - 1):
            if (expectedStartTime >= allShowInCurrentVenue[i].time +
                    timedelta(minutes=durationSS) + timedelta(minutes=15)):
                conflict = False
                break
        else:
            if (expectedEndTime <=
                    allShowInCurrentVenue[i + 1].time - timedelta(minutes=15)
                    and expectedStartTime >= allShowInCurrentVenue[i].time +
                    timedelta(minutes=durationSS) + timedelta(minutes=15)):
                conflict = False
                break
    if (conflict):
        raise BuisnessValidationError(
            400, "ALLOC007",
            "There is some other show blocking this time. please choose differnt time"
        )


def isvalidDate(time):
    dateRegExp = "^(19|20)\d\d(-)(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01]) ([01][1-9]|2[0-3])\:[0-5][0-9]$"
    return re.fullmatch(dateRegExp, time) != None


def generatedateTime(time):
    return datetime(
        int(time[0:4]),
        int(time[5:7]),
        int(time[8:10]),
        int(time[11:13]),
        int(time[14:16]),
    )


class NotFoundError(HTTPException):

    def __init__(self, statusCode):
        self.response = make_response("", statusCode)


class BuisnessValidationError(HTTPException):

    def __init__(self, statusCode, errorCode, errorMessage):
        error = {"error_code": errorCode, "error_message": errorMessage}
        self.response = make_response(json.dumps(error), statusCode)


parser = reqparse.RequestParser()
parser.add_argument("show_name")
parser.add_argument("venue_name")
parser.add_argument("venue_location")
parser.add_argument("time")


def allocValidation(type):
    args = parser.parse_args()
    show_name = args.get("show_name", None)
    venue_name = args.get("venue_name", None)
    venue_location = args.get("venue_location", None)
    time = args.get("time", None)
    if (show_name is None and type == 'post') or show_name == '':
        raise BuisnessValidationError(400, "SHOW001", "Show name is required")
    if (venue_name is None and type == 'post') or venue_name == '':
        raise BuisnessValidationError(400, "VENUE001",
                                      "Venue name is required")
    if (time is None and type == 'post') or time == '':
        raise BuisnessValidationError(400, "ALLOC001", "time is required")
    if (venue_location is None and type == 'post') or venue_location == '':
        raise BuisnessValidationError(400, "VENUE002",
                                      "location is required")

    if time is not None and not isvalidDate(time):
        raise BuisnessValidationError(
            400, "ALLOC002",
            "Either given time is invalid time or it is Wrong Format. It should be of format YYYY-MM-DD HH:MM"
        )
    if ((venue_name is None or venue_name == '') and venue_location
            is not None) or ((venue_location is None or venue_location == '')
                             and venue_name is not None):
        raise BuisnessValidationError(
            400, "ALLOC003",
            "Venue name and location should be come as combination")


def generateResult(alloc):

    curShow = Show.query.get(alloc.show_id)
    curVenue = Venue.query.get(alloc.venue_id)
    inner = {}
    inner['alloc_id'] = alloc.sv_id
    inner['show_name'] = curShow.show_name
    inner['venue_name'] = curVenue.venue_name
    inner['venue_location'] = curVenue.location
    inner['time'] = alloc.time.strftime("%Y-%m-%d %H:%M")
    return (inner)


class AllocationAPI(Resource):

    def get(self, allocId):
        currentAlloc = ShowVenue.query.get(allocId)
        if currentAlloc:
            return generateResult(currentAlloc)
        else:
            raise NotFoundError(statusCode=404)

    def post(self):
        allocValidation('post')
        args = parser.parse_args()
        show_name = args.get("show_name", None)
        venue_name = args.get("venue_name", None)
        venue_location = args.get("venue_location", None)
        time = args.get("time", None)

        curShow = Show.query.filter_by(show_name=show_name).first()
        curVenue = Venue.query.filter_by(venue_name=venue_name,
                                         location=venue_location).first()
        if not curShow:
            raise BuisnessValidationError(400, "ALLOC004",
                                          "Show name not Found")
        if not curVenue:
            raise BuisnessValidationError(
                400, "ALLOC005",
                "Venue name and venue location combination not found")

        timeConstraint(curShow, curVenue, time)
        newAlloc = ShowVenue(show_id=curShow.show_id,
                             venue_id=curVenue.venue_id,
                             time=generatedateTime(time))
        db.session.add(newAlloc)
        db.session.commit()

        curAlloc = ShowVenue.query.filter_by(
            show_id=curShow.show_id,
            venue_id=curVenue.venue_id,
            time=generatedateTime(time)).first()

        return generateResult(curAlloc), 201

    def put(self, allocId):
        currentalloc = ShowVenue.query.get(allocId)
        if not currentalloc:
            raise NotFoundError(404)
        allocValidation(None)

        args = parser.parse_args()
        show_name = args.get("show_name", None)
        venue_name = args.get("venue_name", None)
        venue_location = args.get("venue_location", None)
        time = args.get("time", None)

        if show_name is None:
            curShow = Show.query.get(currentalloc.show_id)
        else:
            curShow = Show.query.filter_by(show_name=show_name).first()

        if venue_name is None:
            curVenue = Venue.query.get(currentalloc.venue_id)
        else:
            curVenue = Venue.query.filter_by(venue_name=venue_name,
                                             location=venue_location).first()
        if not curShow:
            raise BuisnessValidationError(400, "ALLOC004",
                                          "Show name not Found")
        if not curVenue:
            raise BuisnessValidationError(
                400, "ALLOC005",
                "Venue name and venue location combination not found")

        if time:
            timeConstraint(curShow, curVenue, time, True, allocId)

        if show_name is not None: currentalloc.show_id = curShow.show_id
        if venue_name is not None: currentalloc.venue_id = curVenue.venue_id
        if time is not None: currentalloc.show_id = generatedateTime(time)

        db.session.commit()
        curAlloc = ShowVenue.query.get(allocId)

        return generateResult(curAlloc)

    def delete(self, allocId):
        currentAlloc = ShowVenue.query.get(allocId)

        if currentAlloc:
            curBooking=BookingDetails.query.filter_by(sv_id=allocId).all()
            for each in curBooking:
                db.session.delete(each)
                db.session.commit()
            db.session.delete(currentAlloc)
            db.session.commit()
            raise NotFoundError(200)
        else:
            raise NotFoundError(404)
