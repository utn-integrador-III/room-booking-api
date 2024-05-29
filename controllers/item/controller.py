from flask_restful import Resource

from utils.server_response import *
from utils.message_codes import *
from models.item.model import ItemModel
from controllers.item.parser import query_parser
import logging


class Item(Resource):
    route = '/booking_api/item'

    """
    Get all items
    """
    def get(self):        
        try:
            items = ItemModel.get_all()
            data = [c.to_dict() for c in items]
            return ServerResponse(data, status=StatusCode.OK)
        except Exception as ex:
            logging.exception(ex)
            return ServerResponse(status=StatusCode.INTERNAL_SERVER_ERROR)

    """
    Create new item
    """
    def post(self):
        data = query_parser().parse_args()      
        try:
            # Validate unique name
            item_exists = ItemModel.get_by_name(data["name"], data["category_id"])
            if item_exists:
                return ServerResponse(message='Item aready exist for selected category', 
                                          message_code=ITEM_ALREADY_EXIST, status=StatusCode.CONFLICT)
            item = ItemModel(**data)
            item.insert()
            item = ItemModel.get_by_id(item._id)
            return ServerResponse(item.to_dict(), message="Item successfully created", 
                                  message_code=ITEM_SUCCESSFULLY_CREATED, status=StatusCode.CREATED)
        except Exception as ex:
            logging.exception(ex)
            return ServerResponse(status=StatusCode.INTERNAL_SERVER_ERROR)


  
