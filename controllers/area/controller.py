from flask_restful import Resource
from utils.server_response import *
from models.area.model import AreaModel
from controllers.area.parser import query_parser_save
from utils.message_codes import  *
import logging
class Area(Resource):
    route = '/booking_api/area'

    """
    Get all areas
    """
    def get(self):        
        try:
            areas = AreaModel.get_all()
            data = [c.to_dict() for c in areas]
            return ServerResponse(data, status=StatusCode.OK)
        except Exception as ex:
            logging.exception(ex)
            return ServerResponse(status=StatusCode.INTERNAL_SERVER_ERROR)

    """
    Create a new area
    """
    def post(self):
        data = query_parser_save().parse_args()
        try:
            # Validate unique name
            area_exists = AreaModel.get_by_name(data["name"], data["site_id"])
            if area_exists:
                return ServerResponse(message='Area aready exist for the selected site', 
                                      message_code=AREA_ALREADY_EXIST, status=StatusCode.CONFLICT)
            area = AreaModel(**data)
            area.insert()
            area = AreaModel.get_by_id(area._id)
            return ServerResponse(area.to_dict(), message='Area successfully created', 
                                  message_code= AREA_SUCCESSFULLY_CREATED, status=StatusCode.CREATED)
        except Exception as ex:
            logging.exception(ex)
            return ServerResponse(status=StatusCode.INTERNAL_SERVER_ERROR)


  
