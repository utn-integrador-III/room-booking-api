from flask_restful import Resource

from utils.server_response import *
from models.item.model import ItemModel
from controllers.item.item_by_filters.parser import filter_parser
import logging
from models.booking.model import BookingModel

class ItemByFilters(Resource):
    route = '/booking_api/item_by_all_filters'

    """
    Filter by the different DB relations
    """

    def get(self):
        data = filter_parser()
        try:
            items = ItemModel.get_all_by_filters(data)
            itemsAvailable = []
            for item in items:
                bookings = BookingModel.get_relation_booking_item_date_by_item_id(
                    item._id, data["booking_date"])
                available_times_res = BookingModel.get_available_times_list_with_booking(
                    item.category_id.get_category_time_span_list(), bookings)
                if available_times_res:
                    itemsAvailable.append(item)
            all_items = [c.to_dict() for c in itemsAvailable]
            return ServerResponse(all_items, status=StatusCode.OK)
        except Exception as ex:
            logging.exception(ex)
            return ServerResponse(status=StatusCode.INTERNAL_SERVER_ERROR)
