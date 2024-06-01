from datetime import datetime
from bson.objectid import ObjectId
from models.category.db_queries import __category__
from models.area.model import AreaModel
import datetime

class CategoryModel():

    __area_lookup = {
        'from': 'area',
        'localField': 'area_id',
        'foreignField': '_id',
        'as': 'area_id'
    }

    __site_lookup = {
        'from': 'site',
        'localField': 'area_id.site_id',
        'foreignField': '_id',
        'as': 'area_id.site_id'
    }

    __country_lookup = {
        'from': 'country',
        'localField': 'area_id.site_id.country_id',
        'foreignField': '_id',
        'as': 'area_id.site_id.country_id'
    }
    
    __relations_lookup_list = [__area_lookup, __site_lookup, __country_lookup]
    
    __area_group = {
        "$group":{
            "_id": "$_id",
            "area_ids": {
                "$push":"$area_id"
            },
            "document": {
                "$first":"$$ROOT"
            }
        }
    }
    
    __area_replaceRoot = {
        "$replaceRoot":{
            "newRoot": {
                "$mergeObjects": [
                    "$document",
                    {"area_id": "$area_id"}
                ]
            }
        }
    }
    
    __extra_params = [__area_group, __area_replaceRoot]
    
    days_of_week = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']

    def __init__(self, name, is_active, close_time="", open_time="", time_span=0, available_days=[], area_id=[], _id=0):
        # Create properti es
        self._id = str(_id)
        self.name = name
        self.is_active = is_active
        self.close_time = close_time
        self.open_time = open_time
        self.time_span = time_span
        self.available_days = available_days
        self.area_id = [AreaModel.area_factory(area) for area in area_id]
        
    def to_dict(self):
        data =  {
            **vars(self),
            "area": [{
                **a.__dict__, 
                "site": a.site.to_dict()} for a in self.area_id] if self.area_id else None
        }
        data.pop('area_id')
        return data
        
    @classmethod
    def get_all(cls):
        list_categories = []
        response = __category__.get_all_data(lookups=CategoryModel.__relations_lookup_list, 
                                             with_unwind=True, with_preserve=False, extra_params=CategoryModel.__extra_params)
        for category in response:
            try:
                list_categories.append(cls(**category))
            except:
                pass
        return list_categories

    @classmethod
    def get_all_by_filters(cls, dict_match):
        list_items = []
        match_values = dict()
        match_values["$and"] = [{}]
        area_value = dict()
       
        if dict_match.get("area_ids"):
            if len(dict_match.get("area_ids")) > 1:
                area_value["$or"] = []
                for area in dict_match.get("area_ids"):
                    area_tmp = area_value["$or"]
                    area_tmp.append({"area_id._id": ObjectId(area)})
                    area_value["$or"] = area_tmp
                match_values['$and'].append(area_value)
            else:
                match_values["area_id._id"] = ObjectId(
                    dict_match["area_ids"][0])

        if dict_match.get("site_id"):
           match_values["area_id.site_id._id"] = ObjectId(dict_match["site_id"]) 
        
        # if dict_match.get("area_ids"):
        #     match_values["area_id._id"] = ObjectId(dict_match["area_ids"])

        if dict_match.get("country_id"):
            match_values["area_id.site_id.country_id._id"] = ObjectId(dict_match["country_id"])
            
        match_values["is_active"] = True

        response = __category__.get_all_data(values_dict=match_values, lookups=CategoryModel.__relations_lookup_list, 
                                             with_unwind=True, with_preserve=False, extra_params=CategoryModel.__extra_params)
        for item in response:
            try:
                list_items.append(cls(**item))
            except:
                pass
        return list_items

    @classmethod
    def get_by_id(cls, _id):
        values_dict = {"_id":ObjectId(_id)}
        response = __category__.get_data(values_dict=values_dict,lookups=CategoryModel.__relations_lookup_list, 
                                         with_unwind=True, with_preserve=False, extra_params=CategoryModel.__extra_params)
        if response is None: 
            return None
        category = cls(**response)
        return category
    
    @classmethod
    def get_by_name(cls, name, area_id=None):
        match_dict = {"name": name, "area_id._id":{"$in":[]}}
        # Unique name by area relationship
        if area_id:
            in_match = {
                "$in": [ObjectId(_id) for _id in area_id]
            }
            match_dict["area_id._id"] = in_match
        response = __category__.get_data(values_dict=match_dict, lookups=CategoryModel.__relations_lookup_list, 
                                         with_unwind=True, with_preserve=False, extra_params=CategoryModel.__extra_params)
        if response is None: 
            return None
        category = cls(**response)
        return category

    def insert_category(self):
        response = __category__.insert_data(values_dict={
            "name": self.name,
            "is_active": self.is_active,
            "close_time": self.close_time,
            "open_time": self.open_time,
            "area_ids": [ObjectId(area) for area in self.area_id],
            "time_span": self.time_span,
            "available_days": self.available_days
        })
        self._id = response.inserted_id

    def update_category(self, category):
        self.__dict__.update(**category)
        return __category__.update_data(
            {
                "_id": ObjectId(self._id)
            },
            {
                "name": self.name,
                "is_active": self.is_active,
                "close_time": self.close_time,
                "open_time": self.open_time,
                "area_ids": [ObjectId(_id) for _id in self.area_id],
                "time_span": self.time_span,
                "available_days": self.available_days
            }
        )

    def delete_category(self):
        return __category__.delete_data(
            {
                "_id": ObjectId(self._id)
            }
        )

    def get_category_time_span_list(self):
        list_available = [] 

        time_creation = datetime.datetime(2021, 12, 30, int(self.open_time.split(":")[0]), 0)
        evaluation = time_creation.strftime("%H")+":"+time_creation.strftime("%M")

        while evaluation < self.close_time:
            time_change = datetime.timedelta(minutes=self.time_span)
            current_time = time_creation.strftime("%H")+":"+time_creation.strftime("%M")
            time_creation = time_creation + time_change
            to_list_time = current_time+"-"+time_creation.strftime("%H")+":"+time_creation.strftime("%M")
            list_available.append(to_list_time)
            evaluation = time_creation.strftime("%H")+":"+time_creation.strftime("%M")

        return list_available

    @staticmethod
    def category_factory(category):
        try:
            return CategoryModel(**category)
        except:
            if type(category) == ObjectId:
                category = str(category)
            return category

    @staticmethod
    def get_count_records_by_area(area_id):
        result = __category__.get_all_data(values_dict={'area_id': ObjectId(area_id)}, only_count=True)
        try:
            count = list(result)[-1]['total_records']
        except:
            count = 0
        return count

