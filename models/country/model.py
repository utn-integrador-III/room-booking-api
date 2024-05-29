import json

from bson.objectid import ObjectId
from models.country.db_queries import __country__


class CountryModel():

    def __init__(self, name, code, is_active=True, _id=0):
        self._id = str(_id)
        self.name = name
        self.is_active = is_active
        self.code = code

    def to_dict(self):
        return vars(self)

    @classmethod
    def get_all(cls):
        list_countries = []
        response = __country__.get_all_data()
        for country in response:
            try:
                list_countries.append(cls(**country))
            except:
                pass
        return list_countries

    @classmethod
    def delete_by_id(self, id):
        __country__.delete_by_id({
            "id": ObjectId(id)
        })
        return True

    @classmethod
    def get_by_id(cls, id):
        values_dict = {"id": ObjectId(id)}
        response = __country__.get_data(values_dict=values_dict)
        if response is None:
            return None
        country = cls(**response)
        return country

    @classmethod
    def get_by_name(cls, name):
        response = __country__.get_data(values_dict={"name": name})
        if response is None:
            return None
        country = cls(**response)
        return country

    @classmethod
    def get_by_code(cls, name):
        response = __country__.get_data(values_dict={"code": name})
        if response is None:
            return None
        country = cls(**response)
        return country

    def insert(self):
        data = {
            "name": self.name,
            "code": self.code,
            "is_active": bool(self.is_active)
        }
        response = __country__.insert_data(values_dict=data)
        self._id = response.inserted_id

    def update_country(self, country):
        self.__dict__.update(**country)
        return __country__.update_data(
            {
                "id": ObjectId(self._id)
            },
            {
                "name": self.name,
                "code": self.code,
                "is_active": self.is_active
            }
        )

    def delete_country(self):
        return __country__.delete_data(
            {
                "id": ObjectId(self._id)
            }
        )

    @staticmethod
    def country_factory(country):
        try:
            return CountryModel(**country)
        except:
            if type(country) == ObjectId:
                country = str(country)
            return country
