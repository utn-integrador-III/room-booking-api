from flask_restful import reqparse


def update_parser():
    parser = reqparse.RequestParser()
    parser.add_argument('floor', type=str, required=True, help="This field cannot be blank")
    parser.add_argument('name', type=str, required=True, help="This field cannot be blank")
    parser.add_argument('site_id', type=str, required=True, help='This field cannot be blank')
    parser.add_argument('is_active', type=bool)
    return parser