from flask_restful import reqparse

def query_parser():
    parser = reqparse.RequestParser()
    parser.add_argument('status', type=str, required=True, help="The date field cannot be blanks")
    parser.add_argument('booking_time', type=list, location="json", required=True, help="The date field cannot be blanks")
    return parser