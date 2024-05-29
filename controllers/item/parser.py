from flask_restful import reqparse


def query_parser():
    parser = reqparse.RequestParser()
    parser.add_argument('capacity', type=int, required=True, help="This field cannot be blank")
    parser.add_argument('category_id', type=str, required=True, help='This field cannot be blank')
    parser.add_argument('area_id', type=str, required=True, help='This field cannot be blank')
    parser.add_argument('is_active', type=bool)
    parser.add_argument('name', type=str, required=True, help="This field cannot be blank")
    return parser