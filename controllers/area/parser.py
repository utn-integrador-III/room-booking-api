from bson.objectid import ObjectId
from flask_restful import reqparse


def query_parser_save():
    parser = reqparse.RequestParser()
    parser.add_argument('floor', type=str, required=True, help="This field cannot be blank")
    parser.add_argument('name', type=str, required=True, help="This field cannot be blank")
    parser.add_argument('site_id', type=lambda x: ObjectId(x), required=True, help='The field is blank or invalid')
    parser.add_argument('is_active', type=bool)
    return parser