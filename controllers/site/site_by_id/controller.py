from flask_restful import Resource
from bson.objectid import ObjectId
from models.area.model import AreaModel
from utils.server_response import *
from utils.message_codes import *
from controllers.site.site_by_id.parser import query_parser
from models.site.model import SiteModel
import logging


class SiteById(Resource):
    route = '/booking_api/site/<string:_id>'
    """
    Get a site by id
    """
    def get(self, _id):
        try:
            # Validate object id
            if not ObjectId.is_valid(_id):
                return ServerResponse(message='Invalid Id', message_code=INVALID_ID, status=StatusCode.UNPROCESSABLE_ENTITY)
            # Validate if site exists
            site = SiteModel.get_by_id(_id)
            if not site:
                return ServerResponse(message='Site not found', 
                                      message_code=SITE_NOT_FOUND, status=StatusCode.NOT_FOUND)

            return ServerResponse(site.to_dict(), status=StatusCode.OK)
        except Exception as ex:
            logging.exception(ex)
            return ServerResponse(status=StatusCode.INTERNAL_SERVER_ERROR)

    """
    Update a site
    """
    def put(self, _id):
        try:
            # Validate object id
            if not ObjectId.is_valid(_id):
                return ServerResponse(message='Invalid Id', message_code=INVALID_ID, status=StatusCode.UNPROCESSABLE_ENTITY)
            data = query_parser().parse_args()
            # Validate if site exists
            site = SiteModel.get_by_id(_id)
            if not site:
                return ServerResponse(message='Site not found', 
                                      message_code=SITE_NOT_FOUND, status=StatusCode.NOT_FOUND)
            # Validate unique name
            if "name" in data:
                country_id = site.country._id
                if "country_id" in data:
                    country_id = data["country_id"]
                site_exists = SiteModel.get_by_name(data["name"], country_id)
                if site_exists and _id != str(site_exists._id):
                    return ServerResponse(message='Site aready exist for the selected country', 
                                          message_code=SITE_ALREADY_EXIST, status=StatusCode.CONFLICT)

            site.update_site(data)
            site = SiteModel.get_by_id(site._id)
            return ServerResponse(site.to_dict(), message='Site successfully updated', 
                              message_code=SITE_SUCCESSFULLY_UPDATED, status=StatusCode.OK)
        except Exception as ex:
            logging.exception(ex)
            return ServerResponse(status=StatusCode.INTERNAL_SERVER_ERROR)
        
    """
    Delete a site
    """
    def delete(self, _id):
        try:
            # Validate object id
            if not ObjectId.is_valid(_id):
                return ServerResponse(message='Invalid Id', message_code=INVALID_ID, status=StatusCode.UNPROCESSABLE_ENTITY)
            # Validate if site exists
            site = SiteModel.get_by_id(_id)
            if not site:
                return ServerResponse(message='Site not found', 
                                      message_code=SITE_NOT_FOUND, status=StatusCode.NOT_FOUND)
                                      
            # Check if site has relationships with areas
            count = AreaModel.get_count_records_by_site(_id)

            if count > 0:
                return ServerResponse(message='Site cannot be deleted, has relationships with some areas', 
                                      message_code=SITE_DELETE_HAS_RELATIONS, status=StatusCode.CONFLICT)

            site.delete_site()
            return ServerResponse(message='Site successfully deleted', 
                              message_code=SITE_SUCCESSFULLY_DELETED, status=StatusCode.OK)
        except Exception as ex:
            logging.exception(ex)
            return ServerResponse(status=StatusCode.INTERNAL_SERVER_ERROR)