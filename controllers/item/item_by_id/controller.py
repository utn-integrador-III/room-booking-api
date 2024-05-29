from flask_restful import Resource
from bson.objectid import ObjectId
from utils.server_response import *
from utils.message_codes import *
from controllers.item.item_by_id.parser import query_parser
from models.item.model import ItemModel
import logging


class ItemById(Resource):
    route = '/booking_api/item/<string:_id>'
   
    """
    Get one item by id
    """
    def get(self, _id):
        try:
            # Validate object id
            if not ObjectId.is_valid(_id):
                return ServerResponse(message='Invalid Id', message_code=INVALID_ID, status=StatusCode.UNPROCESSABLE_ENTITY)
            # Validate if item exists
            item = ItemModel.get_by_id(_id)
            if not item:
                return ServerResponse(message='Item not found', 
                                      message_code=ITEM_NOT_FOUND, status=StatusCode.NOT_FOUND)
            
            return ServerResponse(item.to_dict(), status=StatusCode.OK)
        except Exception as ex:
            logging.exception(ex)
            return ServerResponse(status=StatusCode.INTERNAL_SERVER_ERROR)

    """
    Update one country
    """
    def put(self, _id):
        data = query_parser().parse_args()
        try:
            # Validate object id
            if not ObjectId.is_valid(_id):
                return ServerResponse(message='Invalid Id', message_code=INVALID_ID, status=StatusCode.UNPROCESSABLE_ENTITY)
            # Validate if item exists
            item = ItemModel.get_by_id(_id)
            if not item:
                return ServerResponse(message='Item not found', 
                                      message_code=ITEM_NOT_FOUND, status=StatusCode.NOT_FOUND)
            # Validate unique name
            item_exists = ItemModel.get_by_name(data["name"], data["category_id"])
            if item_exists and _id != str(item_exists._id):
                return ServerResponse(message='Item aready exists for the selected category', 
                                        message_code=ITEM_ALREADY_EXIST, status=StatusCode.CONFLICT)

            item.update_item(data)
            item = ItemModel.get_by_id(item._id)
            return ServerResponse(item.to_dict(), message='Item successfully updated', 
                              message_code=ITEM_SUCCESSFULLY_UPDATED, status=StatusCode.OK)
        except Exception as ex:
            logging.exception(ex)
            return ServerResponse(status=StatusCode.INTERNAL_SERVER_ERROR)

    """
    Delete one country
    """
    def delete(self, _id):
        try:
            # Validate object id
            if not ObjectId.is_valid(_id):
                return ServerResponse(message='Invalid Id', message_code=INVALID_ID, status=StatusCode.UNPROCESSABLE_ENTITY)
            # Validate item exists
            item = ItemModel.get_by_id(_id)
            if not item:
                return ServerResponse(message='Item not found', 
                                      message_code=ITEM_NOT_FOUND, status=StatusCode.NOT_FOUND)
            item.delete_item()
            return ServerResponse(item.to_dict(), message='Item successfully deleted', 
                                  message_code=ITEM_SUCCESSFULLY_DELETED, status=StatusCode.OK)
        except Exception as ex:
            logging.exception(ex)
            return ServerResponse(status=StatusCode.INTERNAL_SERVER_ERROR)