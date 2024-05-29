import logging
from flask_restful import Resource
from bson.objectid import ObjectId
from models.item.model import ItemModel
from utils.server_response import *
from controllers.category.category_by_id.parser import query_parser
from models.category.model import CategoryModel


class CategoryByIdController(Resource):
    route = '/booking_api/category/<id>'
    
    """
    Get one category by id
    """   
    def get(self, id):
        try:
            # Validate object id
            if not ObjectId.is_valid(id):
                return ServerResponse(message='Invalid Id', message_code=INVALID_ID,
                                      status=StatusCode.UNPROCESSABLE_ENTITY)
            # Validate category exists
            category = CategoryModel.get_by_id(id)
            if not category:
                return ServerResponse(message='Category not found', message_code=CATEGORY_ITEM_NOT_FOUND,
                                      status=StatusCode.NOT_FOUND)
            
            return ServerResponse(category.to_dict(), status=StatusCode.OK)
        except Exception as ex:
            logging.exception(ex)
            return ServerResponse(status=StatusCode.INTERNAL_SERVER_ERROR)
    """
    Update one category
    """
    def put(self, id):
        data = query_parser().parse_args()
        try:
            # Validate object id
            if not ObjectId.is_valid(id):
                return ServerResponse(message='Invalid Id', message_code=INVALID_ID,
                                      status=StatusCode.UNPROCESSABLE_ENTITY)
            # Validate category exists
            category = CategoryModel.get_by_id(id)
            if not category:
                return ServerResponse(message='Category not found', message_code=CATEGORY_ITEM_NOT_FOUND,
                                      status=StatusCode.NOT_FOUND)
            # Validate if days prefix are valid
            for day in data['available_days']:
                if day not in CategoryModel.days_of_week:
                    return ServerResponse(message='One or more days are invalid', 
                                        message_code=CATEGORY_DAYS_INVALID, status=StatusCode.UNPROCESSABLE_ENTITY) 
            # Validate unique name
            category_exists = CategoryModel.get_by_name(data["name"], data["area_id"])
            if category_exists and id != str(category_exists._id):
                return ServerResponse(message='Category already exists for the selected area', message_code=CATEGORY_ALREADY_EXIST,
                                    status=StatusCode.CONFLICT)

            # Validate initial time is lower that end time
            aux_open_time = data["open_time"] if "open_time" in data else category.open_time
            aux_close_time = data["close_time"] if "close_time" in data else category.close_time
            if aux_open_time > aux_close_time:
                return ServerResponse(message='Open time can not be higher than close time', 
                                    message_code=CATEGORY_OPEN_TIME_HIGHER, status=StatusCode.UNPROCESSABLE_ENTITY)

            category.update_category(data)
            category = CategoryModel.get_by_id(category._id)
            return ServerResponse(category.to_dict(), message='Category updated successfully', 
                                  message_code=CATEGORY_SUCCESSFULLY_UPDATED ,status=StatusCode.OK)
        except Exception as ex:
            logging.exception(ex)
            return ServerResponse(status=StatusCode.INTERNAL_SERVER_ERROR)
        
    """
    Delete one category
    """
    def delete(self, id):
        try:
            # Validate object id
            if not ObjectId.is_valid(id):
                return ServerResponse(message='Invalid Id', message_code=INVALID_ID,
                                      status=StatusCode.UNPROCESSABLE_ENTITY)
            # Validate category exists
            category = CategoryModel.get_by_id(id)
            if not category:
                return ServerResponse(message='Category not found', message_code=CATEGORY_ITEM_NOT_FOUND,
                                      status=StatusCode.NOT_FOUND)

            # Check if category has relationships with items
            count = ItemModel.get_count_records_by_category(id)

            if count > 0:
                return ServerResponse(message='Category cannot be deleted, has relationships with some items', 
                                      message_code=AREA_DELETE_HAS_RELATIONS, status=StatusCode.CONFLICT)  

            category.delete_category()

            return ServerResponse(message='Category deleted successfully', message_code=CATEGORY_SUCCESSFULLY_DELETED,
                                  status=StatusCode.OK)
            
        except Exception as ex:
            logging.exception(ex)
            return ServerResponse(StatusCode.INTERNAL_SERVER_ERROR)