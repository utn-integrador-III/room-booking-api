import logging
from flask_restful import Resource

from utils.server_response import *
from models.category.model import CategoryModel
from controllers.category.category_by_filters.parser import filter_parser
from flask import request

class CategoryByFilters(Resource):
    route = '/booking_api/category_by_all_filters'

    """
    Filter by the different DB relations
    """
    def get(self): 
        data = filter_parser()       
        try:
            categories = CategoryModel.get_all_by_filters(data)
            all_categories = [c.to_dict() for c in categories]
            return ServerResponse(all_categories, status=StatusCode.OK) 
        except Exception as ex:
            logging.exception(ex)
            return ServerResponse(status=StatusCode.INTERNAL_SERVER_ERROR)