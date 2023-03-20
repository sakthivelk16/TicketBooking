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


parser = reqparse.RequestParser()
parser.add_argument("venue_name")
parser.add_argument("course_code")
parser.add_argument("place")
parser.add_argument("location")
parser.add_argument("max_capacity")
parser.add_argument("fare2D")
parser.add_argument("fare3D")


def venueValidation(type):
    args = parser.parse_args()
    venue_name = args.get("venue_name", None)
    place = args.get("place", None)
    location = args.get("location", None)
    max_capacity = args.get("max_capacity", None)
    fare2D = args.get("fare2D", None)
    fare3D = args.get("fare3D", None)
    if (venue_name is None and type == 'post') or venue_name == '':
        raise BuisnessValidationError(400, "VENUE001",
                                      "Venue name is required")
    if (location is None and type == 'post') or location == '':
        raise BuisnessValidationError(400, "VENUE002", "location is required")
    if (max_capacity is None and type == 'post') or max_capacity == '':
        raise BuisnessValidationError(400, "VENUE003",
                                      "max_capacity is required")
    if (fare2D is None and type == 'post') or fare2D == '':
        raise BuisnessValidationError(400, "VENUE004", "fare2D is required")
    if (fare3D is None and type == 'post') or fare3D == '':
        raise BuisnessValidationError(400, "VENUE005", "fare3D is required")
    if max_capacity is not None:
        max_capacity = verifyInterger(max_capacity, 400, 'VENUE006',
                                      'max_capacity should be integer')

        if max_capacity <= 0:
            raise BuisnessValidationError(
                400, "VENUE007", "max_capacity should be greater than 0")
    if fare2D is not None:
        fare2D = verifyInterger(fare2D, 400, 'VENUE008',
                                '2D Fare should be integer')

        if fare2D <= 0:
            raise BuisnessValidationError(400, "VENUE009",
                                          "fare2D should be greater than 0")

    if fare3D is not None:
        fare3D = verifyInterger(fare3D, 400, 'VENUE010',
                                '3D Fare should be integer')

        if fare3D <= 0:
            raise BuisnessValidationError(400, "VENUE011",
                                          "fare3D should be greater than 0")


class VenueAPI(Resource):

    def get(self, venueId):
        currentVenue = Venue.query.get(venueId)
        if currentVenue:
            return {
                'venue_id': currentVenue.venue_id,
                'venue_name': currentVenue.venue_name,
                'place': currentVenue.place,
                'location': currentVenue.location,
                'max_capacity': currentVenue.max_capacity,
                'fare2D': currentVenue.fare2D,
                'fare3D': currentVenue.fare3D,
            }
        else:
            raise NotFoundError(statusCode=404)

    def post(self):
        venueValidation('post')
        args = parser.parse_args()
        venue_name = args.get("venue_name", None)
        place = args.get("place", None)
        location = args.get("location", None)
        max_capacity = args.get("max_capacity", None)
        fare2D = args.get("fare2D", None)
        fare3D = args.get("fare3D", None)

        currentVenueId = Venue.query.filter_by(venue_name=venue_name,
                                               location=location).first()

        if currentVenueId:
            raise NotFoundError(409)
        newVenue = Venue(venue_name=venue_name,
                         place=place,
                         location=location,
                         max_capacity=max_capacity,
                         fare2D=fare2D,
                         fare3D=fare3D)
        db.session.add(newVenue)
        db.session.commit()
        currentVenue = Venue.query.filter_by(venue_name=venue_name,
                                             location=location).first()
        return {
            "venue_id": currentVenue.venue_id,
            "venue_name": currentVenue.venue_name,
            "place": currentVenue.place,
            "location": currentVenue.location,
            "max_capacity": currentVenue.max_capacity,
            "fare2D": currentVenue.fare2D,
            "fare3D": currentVenue.fare3D,
        }, 201

    def put(self, venueId):
        currentVenue = Venue.query.get(venueId)
        if not currentVenue:
            raise NotFoundError(404)
        venueValidation(None)
        args = parser.parse_args()
        venue_name = args.get("venue_name", None)
        place = args.get("place", None)
        location = args.get("location", None)
        max_capacity = args.get("max_capacity", None)
        fare2D = args.get("fare2D", None)
        fare3D = args.get("fare3D", None)

        if venue_name is not None: currentVenue.venue_name = venue_name
        if place is not None: currentVenue.place = place
        if location is not None: currentVenue.venue_name = location
        if max_capacity is not None: currentVenue.max_capacity = max_capacity
        if fare2D is not None: currentVenue.fare2D = fare2D
        if fare3D is not None: currentVenue.fare3D = fare3D

        db.session.commit()
        currentVenue = Venue.query.get(venueId)
        return {
            "venue_id": currentVenue.venue_id,
            "venue_name": currentVenue.venue_name,
            "place": currentVenue.place,
            "location": currentVenue.location,
            "max_capacity": currentVenue.max_capacity,
            "fare2D": currentVenue.fare2D,
            "fare3D": currentVenue.fare3D,
        }, 201

    def delete(self, venueId):
        currentVenue = Venue.query.get(venueId)
        currentShowVenue = ShowVenue.query.filter_by(venue_id=venueId).all()
        if len(currentShowVenue) > 0:
            raise NotFoundError(307)

        if currentVenue:
            db.session.delete(currentVenue)
            db.session.commit()
            raise NotFoundError(200)
        else:
            raise NotFoundError(404)
