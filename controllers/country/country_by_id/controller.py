from flask_restful import Resource
from bson.objectid import ObjectId
from models.site.model import SiteModel
from utils.auth_manager import auth_required
from utils.server_response import *
from flask import jsonify
from controllers.country.country_by_id.parser import query_parser
from models.country.model import CountryModel
from utils.message_codes import *
import logging


class CountryById(Resource):
    route = '/booking_api/country/<string:_id>'
    
    """
    Get one country by id
    """
    def get(self, _id):
        try:
            # Validate object id
            if not ObjectId.is_valid(_id):
                return ServerResponse(message='Invalid Id', message_code=INVALID_ID, status=StatusCode.UNPROCESSABLE_ENTITY)
            # Validate if country exists
            country = CountryModel.get_by_id(_id)
            if not country:
                return ServerResponse(message='Country not found', 
                                      message_code=COUNTRY_ITEM_NOT_FOUND, status=StatusCode.NOT_FOUND)
            
            return ServerResponse(country.to_dict(), status=StatusCode.OK)
        except:
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
            # Validate if country exists
            country = CountryModel.get_by_id(_id)
            if not country:
                return ServerResponse(message='Country not found', 
                                      message_code=COUNTRY_ITEM_NOT_FOUND, status=StatusCode.NOT_FOUND)
            # Validate if name is unique
            if "name" in data:
                country_exists = CountryModel.get_by_name(data["name"])
                if country_exists and _id != str(country_exists._id):
                    return ServerResponse(message='Country aready exist', 
                                          message_code=COUNTRY_ALREADY_EXIST, status=StatusCode.CONFLICT)

            country.update_country(data)
            country = CountryModel.get_by_id(country._id)
            return ServerResponse(country.to_dict(), message='Country successfully updated', 
                              message_code=COUNTRY_SUCCESSFULLY_UPDATED, status=StatusCode.OK)
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
            # Validate country exists
            country = CountryModel.get_by_id(_id)
            if not country:
                return ServerResponse(message='Country not found', 
                                      message_code=COUNTRY_ITEM_NOT_FOUND, status=StatusCode.NOT_FOUND)

            # Check if country has relationships with site
            count = SiteModel.get_count_records_by_country(_id)

            if count > 0:
                return ServerResponse(message='Country cannot be deleted, has relationships with some sites', 
                                      message_code=COUNTRY_DELETE_HAS_RELATIONS, status=StatusCode.CONFLICT)  

            country.delete_country()
            return ServerResponse(country.to_dict(), message='Country successfully deleted', 
                              message_code=COUNTRY_SUCCESSFULLY_DELETED, status=StatusCode.OK)
        except Exception as ex:
            logging.exception(ex)
            return ServerResponse(status=StatusCode.INTERNAL_SERVER_ERROR)