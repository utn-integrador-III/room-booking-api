import json

from bson.objectid import ObjectId
from models.area.model import AreaModel
from models.item.db_queries import __item__
from models.category.model import CategoryModel


class ItemModel():

    __category_lookup = {
        'from': 'category',
        'localField': 'category_id',
        'foreignField': '_id',
        'as': 'category_id'
    }

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

    def __init__(self, capacity, category_id, name, area_id, is_active=True, _id=0):
        self._id = str(_id)
        self.capacity = capacity
        self.category_id = CategoryModel.category_factory(category_id)
        self.area_id = AreaModel.area_factory(area_id)
        self.is_active = is_active
        self.name = name

    def to_dict(self):
        item = {
            **vars(self),
            "category": {
                **self.category_id.__dict__,
            } if self.category_id else None,
            "area": {
                **self.area_id.to_dict(),
            } if self.area_id else None
        }
        item.pop("area_id")
        item.pop("category_id")
        return item

    @classmethod
    def get_all(cls):
        list_items = []
        response = __item__.get_all_data(lookups=[ItemModel.__category_lookup, ItemModel.__area_lookup,
                                         ItemModel.__site_lookup, ItemModel.__country_lookup], with_unwind=True, with_preserve=False)
        for item in response:
            try:
                list_items.append(cls(**item))
            except:
                pass
        return list_items

    @classmethod
    def get_all_by_filters(cls, dict_match):
        list_items = []
        match_values = dict()
        match_values["$and"] = [{}]
        category_value = dict()
        area_value = dict()

        if dict_match.get("category_id"):
            if len(dict_match.get("category_id")) > 1:
                category_value["$or"] = []
                for category in dict_match.get("category_id"):
                    category_tmp = category_value["$or"]
                    category_tmp.append({"category_id._id": ObjectId(category)})
                    category_value["$or"] = category_tmp
                match_values['$and'].append(category_value)
            else:
                match_values["category_id._id"] = ObjectId(
                    dict_match["category_id"][0])

        if dict_match.get("area_id"):
            if len(dict_match.get("area_id")) > 1:
                area_value["$or"] = []
                for area in dict_match.get("area_id"):
                    area_tmp = area_value["$or"]
                    area_tmp.append({"area_id._id": ObjectId(area)})
                    area_value["$or"] = area_tmp
                match_values['$and'].append(area_value)
            else:
                match_values["area_id._id"] = ObjectId(
                    dict_match["area_id"][0])

        if dict_match.get("site_id"):
            match_values["area_id.site_id._id"] = ObjectId(
                dict_match["site_id"])

        if dict_match.get("country_id"):
            match_values["area_id.site_id.country_id._id"] = ObjectId(
                dict_match["country_id"])

        if dict_match.get("booking_date"):
            day_of_week = dict_match.get("booking_date").strftime('%A')[0:3]
            match_values["category_id.available_days"] = {
                "$in": [day_of_week]
            }

    
        match_values["is_active"] = True

        response = __item__.get_all_data(values_dict=match_values, lookups=[
            ItemModel.__category_lookup, ItemModel.__area_lookup, ItemModel.__site_lookup, ItemModel.__country_lookup], with_unwind=True, with_preserve=False)
        for item in response:
            try:
                list_items.append(cls(**item))
            except:
                pass
        return list_items

    @ classmethod
    def delete_by_id(self, id):
        __item__.delete_by_id({
            "id": ObjectId(id)
        })
        return True

    @ classmethod
    def get_by_id(cls, id):
        values_dict = {"id": ObjectId(id)}
        response = __item__.get_data(values_dict=values_dict, lookups=[ItemModel.__category_lookup, ItemModel.__area_lookup,
                                                                       ItemModel.__site_lookup, ItemModel.__country_lookup], with_unwind=True, with_preserve=False)
        if response is None:
            return None
        item = cls(**response)
        return item

    @ classmethod
    def get_by_name(cls, name, category_id = None):
        match_dict = {"name": name}
        if category_id:
            match_dict["category_id._id"] = ObjectId(category_id)
        response = __item__.get_data(values_dict=match_dict, lookups=[ItemModel.__category_lookup, ItemModel.__area_lookup,
                                                                      ItemModel.__site_lookup, ItemModel.__country_lookup], with_unwind=True, with_preserve=False)
        if response is None:
            return None
        item = cls(**response)
        return item

    def insert(self):
        data = {
            "area_id": ObjectId(self.area_id),
            "capacity": self.capacity,
            "category_id": ObjectId(self.category_id),
            "is_active": bool(self.is_active),
            "name": self.name
        }
        response = __item__.insert_data(values_dict=data)
        self._id = response.inserted_id

    def update_item(self, item):
        self.__dict__.update(**item)
        return __item__.update_data(
            {
                "id": ObjectId(self._id)
            },
            {
                "capacity": self.capacity,
                "category_id": ObjectId(self.category_id),
                "area_id": ObjectId(self.area_id),
                "is_active": self.is_active,
                "name": self.name
            }
        )

    def delete_item(self):
        return __item__.delete_data(
            {
                "id": ObjectId(self._id)
            }
        )

    @ staticmethod
    def item_factory(item):
        try:
            return ItemModel(**item)
        except:
            if type(item) == ObjectId:
                item = str(item)
            return item

    @ staticmethod
    def get_count_records_by_category(category_id):
        result = __item__.get_all_data(
            values_dict={'category_id': ObjectId(category_id)}, only_count=True)
        try:
            count = list(result)[-1]['total_records']
        except:
            count = 0
        return count
