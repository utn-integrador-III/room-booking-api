import json

from bson.objectid import ObjectId
from models.area.db_queries import __area__
from models.site.model import SiteModel

class AreaModel():

    __site_lookup = {
        'from': 'site',
        'localField': 'site_id',
        'foreignField': '_id',
        'as': 'site_id'
    }
    
    __country_lookup = {
        'from': 'country',
        'localField': 'site_id.country_id',
        'foreignField': '_id',
        'as': 'site_id.country_id'
    }
    
    __relations_lookups_list = [__site_lookup, __country_lookup]

    def __init__(self, floor, name, site_id, is_active=True, _id=0):
        self._id = str(_id)
        self.floor = floor
        self.name = name
        self.site = SiteModel.site_factory(site_id)
        self.is_active = is_active
    
    def to_dict(self):
        return {
            **vars(self),
            "site": {
                **self.site.__dict__,
                "country": self.site.country.to_dict()
            } if self.site else None 
        }

    @classmethod
    def get_all(cls):
        list_areas = []
        response = __area__.get_all_data(lookups=AreaModel.__relations_lookups_list, 
                                         with_unwind=True, with_preserve=False)
        for area in response:
            try:
                list_areas.append(cls(**area))
            except:
                pass
        return list_areas

    @classmethod
    def get_all_by_filters(cls, dict_match):
        list_items = []
        match_values = dict()
                
        if dict_match.get("site_ids"):
            match_values["site_id._id"] = ObjectId(dict_match["site_ids"])

        if dict_match.get("country_id"):
            match_values["site_id.country_id._id"] = ObjectId(dict_match["country_id"])

        match_values["is_active"] = True

        response = __area__.get_all_data(values_dict=match_values, lookups=AreaModel.__relations_lookups_list, 
                                         with_unwind=True, with_preserve=False)
        for item in response:
            try:
                list_items.append(cls(**item))
            except:
                pass
        return list_items
    
    @classmethod
    def delete_by_id(self, id):
        __area__.delete_by_id({
            "id": ObjectId(id)
        })
        return True
    
    @classmethod
    def get_by_id(cls, id):
        values_dict = {"id":ObjectId(id)}
        response = __area__.get_data(values_dict=values_dict,lookups=AreaModel.__relations_lookups_list, 
                                     with_unwind=True, with_preserve=False)
        if response is None: 
            return None
        area = cls(**response)
        return area

    @classmethod
    def get_by_name(cls, name, site_id=None):
        match_dict = {"name": name}
        # Unique name by site relationship
        if site_id:
            match_dict['site_id._id']=ObjectId(site_id)
        response = __area__.get_data(values_dict=match_dict, lookups=AreaModel.__relations_lookups_list, 
                                     with_unwind=True, with_preserve=False)
        if response is None: 
            return None
        area = cls(**response)
        return area

    def insert(self):
        data = {
            "floor": self.floor,
            "name": self.name,
            "site_ids": ObjectId(self.site),
            "is_active": bool(self.is_active)
        }
        response = __area__.insert_data(values_dict=data)
        self._id = response.inserted_id

    def update_area(self, area):
        self.__dict__.update(**area)
        return __area__.update_data(
            {
                "id": ObjectId(self._id)
            },
            {
                "floor": self.floor,
                "name": self.name,
                "site_ids": ObjectId(area.site_id),
                "is_active": self.is_active
            }
        )

    def delete_area(self):
        return __area__.delete_data(
            {
                "id": ObjectId(self._id)
            }
        )

    @staticmethod
    def area_factory(area):
        try:
            return AreaModel(**area)
        except:
            if type(area) == ObjectId:
                area = str(area)
            return area

    @staticmethod
    def get_count_records_by_site(site_id):
        result = __area__.get_all_data(values_dict={'site_id': ObjectId(site_id)}, only_count=True)
        try:
            count = list(result)[-1]['total_records']
        except:
            count = 0
        return count

    
    