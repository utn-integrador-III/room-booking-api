from flask import request

def filter_parser():
    data = dict()
    data["country_id"] = request.args.get("country_id")
    data["site_id"] = request.args.get("site_id")
    data["area_id"] = request.args.getlist("area_id")
    return data