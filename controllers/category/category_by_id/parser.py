from flask_restful import reqparse


def query_parser():
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True, help="The Name field cannot be blanks")
    parser.add_argument('is_active', type=bool, choices=[True, False],required=True, help="The is_active field cannot be blanks")
    parser.add_argument('available_days', type=list, location="json", required=True, help="The available_days field cannot be blanks")
    parser.add_argument('close_time', type=str, required=True, help="The Close time field cannot be blanks")
    parser.add_argument('open_time', type=str, required=True, help="The Open time field cannot be blanks")
    parser.add_argument('area_id', type=list, location="json", required=True, help="The Area id field cannot be blanks")
    parser.add_argument('time_span', type=int)
    return parser
