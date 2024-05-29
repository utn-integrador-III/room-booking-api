import logging
from flask_restful import Resource
from models.category.model import CategoryModel
from utils.server_response import *
from .parser import query_parser

class CategoryController(Resource):
    route = '/booking_api/category'
    
    """
    Get all categories
    """
    def get(self):        
        try:
            categories = CategoryModel.get_all()
            data = [c.to_dict() for c in categories]
            return ServerResponse(data, status=StatusCode.OK)
        except Exception as ex:
            logging.exception(ex)
            return ServerResponse(status=StatusCode.INTERNAL_SERVER_ERROR)

    """
    Create a new category
    """
    def post(self):
        data = query_parser().parse_args()
        try:
            # Validate if days prefix are valid
            for day in data['available_days']:
                if day not in CategoryModel.days_of_week:
                    return ServerResponse(message='One or more days are invalid', 
                                            message_code=CATEGORY_DAYS_INVALID, status=StatusCode.UNPROCESSABLE_ENTITY) 
            # Validate unique name
            category_exists = CategoryModel.get_by_name(data["name"], data["area_id"])
            if category_exists:
                return ServerResponse(message='Category already exists for the selected area', 
                                       message_code=CATEGORY_ALREADY_EXIST, status=StatusCode.CONFLICT) 
            # Validate open time is lower than close time
            if data["open_time"] > data["close_time"]:
                return ServerResponse(message='Open time can not be higher than close_time', 
                                          message_code=CATEGORY_OPEN_TIME_HIGHER, status=StatusCode.UNPROCESSABLE_ENTITY)  

            category = CategoryModel(**data)
            category.insert_category()
            category = category.get_by_id(category._id)
            return ServerResponse(category.to_dict(), message='Category created successfully',
                                  message_code=CATEGORY_SUCCESSFULLY_CREATED)
            
        except Exception as ex:
            logging.exception(ex)
            return ServerResponse(status=StatusCode.INTERNAL_SERVER_ERROR)
