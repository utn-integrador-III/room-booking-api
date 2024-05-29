import json

from bson.objectid import ObjectId
from models.site.db_queries import __site__
from models.country.model import CountryModel


class SiteModel():

    __country_lookup = {
        'from': 'country',
        'localField': 'country_id',
        'foreignField': '_id',
        'as': 'country_id'
    }

    def __init__(self, name, country_id=None, is_active=True, _id=0):
        self._id = str(_id)
        self.name = name
        self.country = CountryModel.country_factory(country_id)
        self.is_active = is_active
    
    def to_dict(self):
        return {
            **vars(self),
            'country': self.country.__dict__ if self.country else None
        }

    @classmethod
    def get_by_id(cls, id):
        values_dict = {"id":ObjectId(id)}
        response = __site__.get_data(values_dict=values_dict, lookups=[SiteModel.__country_lookup], with_unwind=True, with_preserve=False)
        if response is None: 
            return None
        competitor = cls(**response)
        return competitor

   
    @classmethod
    def get_all(cls):
        list_sites = []
        response = __site__.get_all_data(lookups=[SiteModel.__country_lookup], with_unwind=True, with_preserve=False)
        for site in response:
            try:
                list_sites.append(cls(**site))
            except Exception as ex:
                pass
        return list_sites

    @classmethod
    def get_all_by_filters(cls, dict_match):
        list_items = []
        match_values = dict()
        
        if dict_match.get("country_ids"):
            match_values["country_id._id"] = ObjectId(dict_match["country_ids"])
            
        match_values["is_active"] = True

        response = __site__.get_all_data(values_dict=match_values, lookups=[SiteModel.__country_lookup], with_unwind=True, with_preserve=False)
        for item in response:
            try:
                list_items.append(cls(**item))
            except:
                pass
        return list_items
    

    @classmethod
    def get_by_name(cls, name, country_id=None):
        match_dict = {"name": name}
        if country_id:
            match_dict["country_id._id"] = ObjectId(country_id)
        response = __site__.get_data(values_dict=match_dict, lookups=[SiteModel.__country_lookup], with_unwind=True, with_preserve=False)
        if response is None: 
            return None
        site = cls(**response)
        return site

    def insert(self):
        data = {
            "name": self.name,
            "country_ids": ObjectId(self.country),
            "is_active": self.is_active 
        }
        response = __site__.insert_data(values_dict=data)
        self._id = response.inserted_id
       


    def update_site(self, site):
        self.__dict__.update(**site)
        return __site__.update_data(
            {
                "id": ObjectId(self._id)
            },
            {
                "name": self.name,
                "country_ids": ObjectId(site.country_id),
                "is_active": self.is_active
            }
        )

    def delete_site(self):
        return __site__.delete_data(
            {
                "id": ObjectId(self._id)
            }
        )

    @classmethod
    def find_by_filter(cls, data):
        
        values_dict = dict()
        
        if  data.get("name"):
            query = {
                '$elemMatch': {
                    '$in': data["name"]
                }
            }
            values_dict["name"] = query

        if  data.get("country_ids"):
            query = {
                '$elemMatch': {
                    '$in': data["country_ids"]
                }
            }
            values_dict["country_ids"] = query

        if  data.get("is_active"):
            query = {
                '$in': data["is_active"]
            }
            values_dict["is_active"] = query

        result = __site__.get_all_data(values_dict=values_dict)
        site = list()
        for dist in result:
            try:
                site.append(cls(**dist))
            except Exception as x:
                pass
        
        return site
    
    @staticmethod
    def site_factory(site):
        try:
            return SiteModel(**site)
        except:
            if type(site) == ObjectId:
                site = str(site)
            return site

    @staticmethod
    def get_count_records_by_country(country_id):
        result = __site__.get_all_data(values_dict={'country_id': ObjectId(country_id)}, only_count=True)
        try:
            count = list(result)[-1]['total_records']
        except:
            count = 0
        return count

   