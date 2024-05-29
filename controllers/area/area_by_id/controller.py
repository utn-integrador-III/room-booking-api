import logging
from flask_restful import Resource
from bson.objectid import ObjectId
from models.category.model import CategoryModel
from utils.server_response import *
from controllers.area.area_by_id.parser import update_parser
from models.area.model import AreaModel
from utils.message_codes import *


class AreaById(Resource):
    route = '/booking_api/area/<string:_id>'
   
    """
    Get one area by id
    """
    def get(self, _id):
        try:
            # Validate object id
            if not ObjectId.is_valid(_id):
                return ServerResponse(message='Invalid Id', message_code=INVALID_ID, status=StatusCode.UNPROCESSABLE_ENTITY)
            # Check if area exists
            area = AreaModel.get_by_id(_id)
            if not area:
                return ServerResponse(message='Area not found', 
                                      message_code=AREA_ITEM_NOT_FOUND, status=StatusCode.NOT_FOUND)
            return ServerResponse(area.to_dict(), status=StatusCode.OK)
        except Exception as ex:
            logging.exception(ex)
            return ServerResponse(status=StatusCode.INTERNAL_SERVER_ERROR)

    """
    Update one area
    """
    def put(self, _id):
        data = update_parser().parse_args()
        
        try:
            # Validate object id
            if not ObjectId.is_valid(_id):
                return ServerResponse(message='Invalid Id', message_code=INVALID_ID, status=StatusCode.UNPROCESSABLE_ENTITY)
            # Check if area exists
            area = AreaModel.get_by_id(_id)
            if not area:
                return ServerResponse(message='Area not found', 
                                      message_code=AREA_ITEM_NOT_FOUND, status=StatusCode.NOT_FOUND)
            # Validate unique name
            if "name" in data:
                site_id = area.site._id
                if "site_id" in data:
                    site_id = data["site_id"]
                area_exists = AreaModel.get_by_name(data["name"], site_id)
                if area_exists and _id != str(area_exists._id):
                    return ServerResponse(message='Area aready exists for the selected site', 
                                      message_code=AREA_ALREADY_EXIST, status=StatusCode.CONFLICT)

            area.update_area(data)
            area = AreaModel.get_by_id(area._id)
            return ServerResponse(area.to_dict(), message='Area successfully updated', 
                                  message_code=AREA_SUCCESSFULLY_UPDATED, status=StatusCode.OK)
        except Exception as ex:
            logging.exception(ex)
            return ServerResponse(status=StatusCode.INTERNAL_SERVER_ERROR)

    """
    Delete an area
    """
    def delete(self, _id):
        try:
            # Validate object id
            if not ObjectId.is_valid(_id):
                return ServerResponse(message='Invalid Id', message_code=INVALID_ID, status=StatusCode.UNPROCESSABLE_ENTITY)
            # Check if area exists
            area = AreaModel.get_by_id(_id)
            if not area:
                return ServerResponse(message='Area not found', 
                                      message_code=AREA_ITEM_NOT_FOUND, status=StatusCode.NOT_FOUND)
            # Check if area has relationships with categories
            count = CategoryModel.get_count_records_by_area(_id)
            if count > 0:
                return ServerResponse(message='Area cannot be deleted, has relationships with some categories', 
                                      message_code=AREA_DELETE_HAS_RELATIONS, status=StatusCode.CONFLICT)        
            area.delete_area()
            return ServerResponse(message='Area successfully deleted', message_code=AREA_SUCCESSFULLY_DELETED, status=StatusCode.OK)
        except Exception as ex:
            logging.exception(ex)
            return ServerResponse(status=StatusCode.INTERNAL_SERVER_ERROR)