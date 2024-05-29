from flask import request
from datetime import datetime


def filter_parser():
    data = dict()
    data['country_id'] = request.args.get('country_id')
    data['site_id'] = request.args.get('site_id')
    data['area_id'] = request.args.getlist('area_id')
    data['category_id'] = request.args.getlist('category_id')
    data['booking_date'] = datetime.strptime(request.args.get('booking_date'),'%Y-%m-%d')
    return data
