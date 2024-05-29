import logging
from flask_restful import Resource
from bson.objectid import ObjectId
from utils.server_response import *
from utils.message_codes import *
from controllers.booking.booking_by_id.parser import query_parser
from models.booking.model import BookingModel


class BookingById(Resource):
    route = '/booking_api/booking/<string:_id>'

    
    """
    Get one booking by id
    """
    def get(self, _id):
        try:
            # Validate object id
            if not ObjectId.is_valid(_id):
                return ServerResponse(message='Invalid Id', message_code=INVALID_ID,
                                      status=StatusCode.UNPROCESSABLE_ENTITY)
            # Validate if booking exists
            booking = BookingModel.get_by_id(_id)
            if not booking:
                return ServerResponse(message='Booking not found', message_code=BOOKING_NOT_FOUND,
                                      status=StatusCode.NOT_FOUND)
            else:
                return ServerResponse(data=booking.to_dict(), status=StatusCode.OK)
        except Exception as ex:
            logging.exception(ex)
            return ServerResponse(status=StatusCode.INTERNAL_SERVER_ERROR)

    """
    Cancel a booking
    """
    def put(self, _id):
        data = query_parser().parse_args()
        try:
            # Validate object id
            if not ObjectId.is_valid(_id):
                return ServerResponse(message='Invalid Id', message_code=INVALID_ID,
                                      status=StatusCode.UNPROCESSABLE_ENTITY)
            # Validate if booking exists
            booking = BookingModel.get_by_id(_id)
            if not booking:
                return ServerResponse(message='Booking not found', message_code=BOOKING_NOT_FOUND,
                                      status=StatusCode.NOT_FOUND)

            booking.update_booking(data)
            booking = BookingModel.get_by_id(booking._id)
            return ServerResponse(data=booking.to_dict(), message='Booking updated successfully', 
                                  message_code=BOOKING_UPDATED, status=StatusCode.OK)
        except Exception as ex:
            logging.exception(ex)
            return ServerResponse(status=StatusCode.INTERNAL_SERVER_ERROR)

        

   