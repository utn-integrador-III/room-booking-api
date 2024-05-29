from flask import request

def filter_parser():
    data = dict()
    data["country_id"] = request.args.get('country_id')
    return data