import datetime
from bson.objectid import ObjectId
from models.user.db_queries import __user__


class UserModel():

    def __init__(self, _id=0, name=""):
        # Create properties
        self._id = str(_id)
        self.name = name

    def to_dict(self):
        return {
            **vars(self),
        }

    @classmethod
    def get_all(cls, dict_match):
        list_users = []
        response = __user__.get_all_data(with_unwind=False, values_dict=dict_match)
        for item in response:
            try:
                list_users.append(cls(**item))
            except:
                pass
        return list_users

    @classmethod

    def get_by_id(cls, _id):
        values_dict = {"_id": ObjectId(_id)}

        response = __user__.get_data(
            values_dict=values_dict, with_unwind=False)
        if response is None:
            return None
        user = cls(**response)
        return user

    def insert_user(self):
        response = __user__.insert_data(values_dict={
            "name": self.name,
        })
        self._id = response.inserted_id

    def update_user(self, user):
        self.__dict__.update(**user)
        return __user__.update_data(
            {
                "_id": ObjectId(self._id)
            },
            {
                "name": self.name, 
            }
        )

    def delete_user(self):
        return __user__.delete_data(
            {
                "_id": ObjectId(self._id)
            }
        )

    @staticmethod
    def user_factory(user):
        try:
            return UserModel(**user)
        except:
            if type(user) == ObjectId:
                user = str(user)
            return user