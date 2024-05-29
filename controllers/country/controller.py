from flask_restful import Resource

from utils.server_response import *
from models.country.model import CountryModel as CountryModel
from controllers.country.parser import query_parser_save
from utils.auth_manager import auth_required
import logging


class Country(Resource):
    route = '/booking_api/country'

    """
    Get all countries
    """

    def get(self):
        try:
            countries = CountryModel.get_all()
            data = [c.to_dict() for c in countries]
            return ServerResponse(data, status=StatusCode.OK)
        except Exception as ex:
            logging.exception(ex)
            return ServerResponse(status=StatusCode.INTERNAL_SERVER_ERROR)

    """
    Create new country
    """

    def post(self):
        data = query_parser_save().parse_args()
        try:
            # Validate unique name
            country_exists = CountryModel.get_by_name(data["name"])
            code_exists = CountryModel.get_by_code(data["code"])
            if country_exists or code_exists:
                return ServerResponse(message='Country aready exist',
                                      message_code=COUNTRY_ALREADY_EXIST, status=StatusCode.CONFLICT)
            country = CountryModel(**data)
            country.insert()
            country = CountryModel.get_by_id(country._id)
            return ServerResponse(country.to_dict(), message="Country successfully created",
                                  message_code=COUNTRY_SUCCESSFULLY_CREATED, status=StatusCode.CREATED)
        except Exception as ex:
            logging.exception(ex)
            return ServerResponse(status=StatusCode.INTERNAL_SERVER_ERROR)
