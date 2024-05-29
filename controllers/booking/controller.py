from datetime import datetime
from pytz import timezone
import pytz
from flask_restful import Resource
from bson.objectid import ObjectId
from models.item.model import ItemModel
from models.user.model import UserModel
from utils.server_response import ServerResponse, StatusCode
from controllers.booking.parser import query_parser_create_booking, query_parser_avilable_times, filter_parser, filter_parser_user
from models.booking.model import BookingModel
from utils.message_codes import *
import re
import logging

class BookingController(Resource):
    route = '/booking_api/booking'
    """
    Get all bookings
    """

    def get(self): 
        try:
            data = filter_parser_user()
            if data['user_email']:
                bookings = BookingModel.get_all_by_email(data['user_email'], data['status'])
                data = [c.to_dict() for c in bookings]
                return ServerResponse(data=data, status=StatusCode.OK)
        except Exception as ex:
            logging.exception(ex)
            return ServerResponse(status=StatusCode.INTERNAL_SERVER_ERROR)

    """
    Create a booking
    """

    def post(self):
        data = query_parser_create_booking().parse_args()
        try:
            # Validate object Id
            if not ObjectId.is_valid(data["item_id"]):
                return ServerResponse(message='Invalid Item Id', message_code=INVALID_ID, status=StatusCode.UNPROCESSABLE_ENTITY)
            
            item = ItemModel.get_by_id(data['item_id'])

            # Item exists
            if not item:
                return ServerResponse(message='Item not found',
                                      message_code=BOOKING_ITEM_NOT_FOUND, status=StatusCode.NOT_FOUND)
            

            # Map the ids from item
            try:
                data['details'] = dict()
                data['details']['item_id'] = item._id
                data['details']['category_id'] = item.category_id._id
                data['details']['area_id'] = item.area_id._id
                data['details']['site_id'] = item.area_id.site._id
                data['details']['country_id'] = item.area_id.site.country._id
            except Exception as ex:
                logging.exception(ex)
                return ServerResponse(message="Item has conflicts with parent relationships",
                                      message_code=BOOKING_ITEM_RELATION_CONFLICT, status=StatusCode.CONFLICT)

            # Validate Day is in available days
            if data['booking_date'].strftime('%a') not in item.category_id.available_days:
                return ServerResponse(message='Item is not available in the selected day',
                                      message_code=BOOKING_ITEM_NOT_AVAIL_DAY, status=StatusCode.CONFLICT)

            # Date equal or greater than today
            if data['booking_date'] < datetime.strptime(datetime.now().strftime('%Y-%m-%d'), '%Y-%m-%d'):
                return ServerResponse(message='Date must be equal or greater than today',
                                      message_code=BOOKING_DATE_INVALID, status=StatusCode.UNPROCESSABLE_ENTITY)

            # Times format
            regex_time = re.compile(
                r"([01][0-9]|2[0-3]):([0-5][0-9])-([01][0-9]|2[0-3]):([0-5][0-9])")
            for time in data['booking_time']:
                if not regex_time.match(time):
                    return ServerResponse(message="One or more time ranges do not have the correct format",
                                          message_code='BOOKING_INVALID_TIME_RANGE', status=StatusCode.UNPROCESSABLE_ENTITY)
                else:
                    time_arr = time.split('-')
                    if time_arr[0] > time_arr[1]:
                        return ServerResponse(message="One or more time ranges do not have the correct format",
                                              message_code='BOOKING_INVALID_TIME_RANGE', status=StatusCode.UNPROCESSABLE_ENTITY)

            # Validate times if date is equal to now
            str_date = data['booking_date'].strftime('%Y-%m-%d')
            if str_date == datetime.now().strftime('%Y-%m-%d'):
                for time in data['booking_time']:
                    time_arr = time.split('-')
                    start_date_time = datetime.strptime(
                        f"{str_date} {time_arr[0]}", '%Y-%m-%d %H:%M')
                    end_date_time = datetime.strptime(
                        f"{str_date} {time_arr[1]}", '%Y-%m-%d %H:%M')
                    current_time = datetime.now(tz=pytz.utc).astimezone(timezone(data['timezone']))
                    current_time = datetime(current_time.year, current_time.month, current_time.day, current_time.hour, current_time.minute)
                    if (start_date_time < current_time or end_date_time < current_time) and not BookingModel.checkTimeAvailability(time, current_time):
                        return ServerResponse(message=f"One or more times are lower than the current time",
                                              message_code='BOOKING_TIME_LOWER_THAN_ACTUAL', status=StatusCode.CONFLICT)

            bookings = BookingModel.get_relation_booking_item_date_by_item_id(
                item._id, data["booking_date"])
            # Times conflict validation
            available_times_res = BookingModel.get_available_times_list_with_booking(
                item.category_id.get_category_time_span_list(), bookings)

            conflict_times = []
            for time in data["booking_time"]:
                if time not in available_times_res:
                    conflict_times.append(time)

            if len(conflict_times):
                return ServerResponse(message="Some selected times are not available", data=conflict_times,
                                      message_code='BOOKING_TIMES_NOT_AVAIL', status=StatusCode.CONFLICT)

            booking = BookingModel(**data)
            booking.insert_booking()
            booking = BookingModel.get_by_id(booking._id)

            return ServerResponse(message="Booking created successfully",
                                          message_code='BOOKING_CREATED', status=StatusCode.CREATED)
        except Exception as ex:
            logging.exception(ex)
            return ServerResponse(status=StatusCode.INTERNAL_SERVER_ERROR)


class BookingAvailableTimesController(Resource):
    route = '/booking_api/booking_available_times'
    """
    Get available times for the item
    """

    def get(self):
        data = query_parser_avilable_times()
        try:
            # Validate object id
            if not ObjectId.is_valid(data["id"]):
                return ServerResponse(message='Invalid Id', message_code=INVALID_ID, status=StatusCode.UNPROCESSABLE_ENTITY)
            # Validate if item exists
            item = ItemModel.get_by_id(data['id'])
            if not item:
                return ServerResponse(message='Item not found',
                                      message_code=BOOKING_ITEM_NOT_FOUND, status=StatusCode.NOT_FOUND)

            bookings = BookingModel.get_relation_booking_item_date_by_item_id(
                data["id"], data["date"])

            # Validate the day to return available days
            available_times_res = []
            if data['date'].strftime('%a') in item.category_id.available_days:
                available_times_res = BookingModel.get_available_times_list_with_booking(
                    item.category_id.get_category_time_span_list(), bookings)

            data = {'times': available_times_res}
            return ServerResponse(data=data, status=StatusCode.OK)
        except Exception as ex:
            logging.exception(ex)
            return ServerResponse(status=StatusCode.INTERNAL_SERVER_ERROR)
