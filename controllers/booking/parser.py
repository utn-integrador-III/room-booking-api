from datetime import datetime
from flask_restful import reqparse
from flask import request

def filter_parser():
    data = dict()
    if request.args.get("status") is not None:
        data["status"] = request.args.get("status", type=str)
    return data

def filter_parser_user():
    data = {}
    if request.args.get("status") is not None:
        data["status"] = request.args.get("status", type=str)
    if request.args.get("user_email") is not None:
        data["user_email"] = request.args.get("user_email", type=str)
    return data

def query_parser_avilable_times():
    data = {}
    data['id'] = request.args.get('id')
    data['date'] = datetime.strptime(request.args.get('date'), '%Y-%m-%d')
    return data

def query_parser_create_booking():
    parser = reqparse.RequestParser()
    parser.add_argument('booking_date', type=lambda x: datetime.strptime(x,'%Y-%m-%d'), required=True, help="The id field cannot be blanks")
    parser.add_argument('booking_time', action="append", required=True, help="The date field cannot be blanks")
    parser.add_argument('comment', type=str, required=True, help="The id field cannot be blanks")
    parser.add_argument('item_id', type=str, required=True, help="The item id cannot be blanks")
    parser.add_argument('user_email', type=str, required=True, help="The user email cannot be blanks")
    parser.add_argument('user_name', type=str, required=True, help="The user name cannot be blanks")
    parser.add_argument('timezone', type=str, required=True, help="The timezone field cannot be blanks") 
    return parser