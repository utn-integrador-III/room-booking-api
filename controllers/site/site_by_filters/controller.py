from bson import ObjectId
from flask_restful import Resource
from utils.server_response import *
from models.site.model import SiteModel
from controllers.site.site_by_filters.parser import filter_parser
import logging

class SiteByFilters(Resource):
    route = '/booking_api/site_by_all_filters'

    """
    Filter by the different DB relations
    """
    def get(self):     
        data = filter_parser()
        
        try:
            # Validate object id
            if not ObjectId.is_valid(data["country_id"]):
                return ServerResponse(message='Invalid Id', message_code=INVALID_ID, status=StatusCode.UNPROCESSABLE_ENTITY)
            sites = SiteModel.get_all_by_filters(data)
            all_sites = [c.to_dict() for c in sites]
            return ServerResponse(all_sites, status=StatusCode.OK)
        except Exception as ex:
            logging.exception(ex)
            return ServerResponse(status=StatusCode.INTERNAL_SERVER_ERROR)