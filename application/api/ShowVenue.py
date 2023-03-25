from flask_restful import Resource
from werkzeug.exceptions import HTTPException
from flask import make_response
from models.module import *


class NotFoundError(HTTPException):

    def __init__(self, statusCode):
        self.response = make_response("", statusCode)


def generateResult(alloc):
    final = []
    for each in alloc:
        curShow = Show.query.get(each.show_id)
        curVenue = Venue.query.get(each.venue_id)
        inner = {}
        inner['alloc_id'] = each.sv_id
        inner['show_name'] = curShow.show_name.capitalize()
        inner['venue_name'] = curVenue.venue_name.capitalize()
        inner['venue_location'] = curVenue.location.capitalize()
        inner['time'] = each.time.strftime("%Y-%m-%d %I:%M %p")
        final.append(inner)
    return final


class ShowAtAllVenueAPI(Resource):

    def get(self, showId):
        currentAlloc = ShowVenue.query.filter_by(show_id=showId).order_by(
            ShowVenue.time).all()
        if currentAlloc:
            return generateResult(currentAlloc)
        else:
            raise NotFoundError(statusCode=404)


class ShowAtVenueAPI(Resource):

    def get(self, venueId, showId):
        currentAlloc = ShowVenue.query.filter_by(venue_id=venueId,
                                                 show_id=showId).order_by(
                                                     ShowVenue.time).all()
        if currentAlloc:
            return generateResult(currentAlloc)
        else:
            raise NotFoundError(statusCode=404)


class AllShowAtVenueAPI(Resource):

    def get(self, venueId):
        currentAlloc = ShowVenue.query.filter_by(venue_id=venueId).order_by(
            ShowVenue.time).all()
        if currentAlloc:
            return generateResult(currentAlloc)
        else:
            raise NotFoundError(statusCode=404)
