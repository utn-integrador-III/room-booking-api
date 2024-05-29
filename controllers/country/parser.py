from flask_restful import reqparse

def query_parser_save():
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True, help="This field cannot be blank")
    parser.add_argument('code', type=str, required=True, help="This field cannot be blank")
    parser.add_argument('is_active', action='append', required=False)
    return parser