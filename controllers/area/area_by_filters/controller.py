import logging
from flask_restful import Resource
from utils.server_response import *
from models.area.model import AreaModel as AreaModel
from controllers.area.area_by_filters.parser import filter_parser

class AreaByFilters(Resource):
    route = '/booking_api/area_by_all_filters'

    """
    Filter by the different DB relations
    """
    def get(self):
        data = filter_parser()
        try:  
            areas = AreaModel.get_all_by_filters(data)
            all_areas = [c.to_dict() for c in areas]
            return ServerResponse(all_areas, status=StatusCode.OK)
        except Exception as ex:
            logging.exception(ex)
            return ServerResponse(status=StatusCode.INTERNAL_SERVER_ERROR)