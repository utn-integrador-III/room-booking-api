import datetime
from bson.objectid import ObjectId
from models.booking.db_queries import __booking__
from models.booking_details.model import BookingDetailsModel
from models.category.model import CategoryModel
from models.item.model import ItemModel
from models.user.model import UserModel


class BookingModel():

    __booking_group__ = [
        # user_id is not needed, user_id can be used for future user collection implementation on mongo
        # {
        #     '$lookup': {
        #         'from': 'user',
        #         'localField': 'user_id',
        #         'foreignField': '_id',
        #         'as': 'user_id'
        #     }
        # },
        # {
        #     '$unwind': {
        #         'path': '$user_id',
        #         'preserveNullAndEmptyArrays': False
        #     }
        # },
        {
            '$lookup': {
                'from': 'country',
                'localField': 'details.country_id',
                'foreignField': '_id',
                'as': 'details.country_id'
            }
        }, {
            '$unwind': {
                'path': '$details.country_id',
                'preserveNullAndEmptyArrays': False
            }
        }, {
            '$lookup': {
                'from': 'site',
                'localField': 'details.site_id',
                'foreignField': '_id',
                'as': 'details.site_id'
            }
        }, {
            '$unwind': {
                'path': '$details.site_id',
                'preserveNullAndEmptyArrays': False
            }
        }, {
            '$lookup': {
                'from': 'area',
                'localField': 'details.area_id',
                'foreignField': '_id',
                'as': 'details.area_id'
            }
        }, {
            '$unwind': {
                'path': '$details.area_id',
                'preserveNullAndEmptyArrays': False
            }
        }, {
            '$lookup': {
                'from': 'category',
                'localField': 'details.category_id',
                'foreignField': '_id',
                'as': 'details.category_id'
            }
        }, {
            '$unwind': {
                'path': '$details.category_id',
                'preserveNullAndEmptyArrays': False
            }
        }, {
            '$lookup': {
                'from': 'item',
                'localField': 'details.item_id',
                'foreignField': '_id',
                'as': 'details.item_id'
            }
        }, {
            '$unwind': {
                'path': '$details.item_id',
                'preserveNullAndEmptyArrays': False
            }
        }
    ]

    def __init__(self, booking_date: datetime, booking_time, status="B", comment="", details=None,_id=0, user_email="",user_name="", **kwargs):
        # Create properties
        self._id = str(_id)
        self.status = status
        self.booking_date = booking_date
        self.booking_time = booking_time
        self.comment = comment
        self.user_email = user_email
        self.user_name = user_name
        self.details = BookingDetailsModel(
            **details) if details else BookingDetailsModel()

    def to_dict(self):
        return {
            **vars(self),
            "booking_date": self.booking_date.strftime("%Y-%m-%d"),
            "user_email": self.user_email,
            "user_name": self.user_name,
            "details": {
                "country": self.details.country.__dict__,
                "site": self.details.site.__dict__,
                "area": self.details.area.__dict__,
                "category": self.details.category.__dict__,
                "item": self.details.item.__dict__,

            }
        }

    @classmethod
    def get_all(cls, dict_match):
        list_bookings = []
        response = __booking__.get_all_data(
            extra_params=BookingModel.__booking_group__, with_unwind=False, values_dict=dict_match)
        for item in response:
            try:
                list_bookings.append(cls(**item))
            except:
                pass
        return list_bookings

    @classmethod
    def get_all_by_status(cls, status="B"):
        list_bookings = []
        response = __booking__.get_all_data(values_dict={
                                            "status": status}, extra_params=BookingModel.__booking_group__, with_unwind=False)
        for booking in response:
            try:
                list_bookings.append(cls(**booking))
            except:
                pass
        return list_bookings

    @classmethod
    def get_all_by_email(cls, email,status=""):
        list_bookings = []
        values_dict={}
        if not status:
            values_dict={
                "user_email": email
            }
        else: 
            values_dict={
                "user_email": email, "status":status
            }
        response = __booking__.get_all_data(values_dict=values_dict, extra_params=BookingModel.__booking_group__, with_unwind=False)
        for booking in response:
            try:
                list_bookings.append(cls(**booking))
            except:
                pass
        return list_bookings

    @classmethod
    def get_by_id(cls, id):
        values_dict = {"id": ObjectId(id)}
        response = __booking__.get_data(
            values_dict=values_dict, extra_params=BookingModel.__booking_group__, with_unwind=False)
        if response is None:
            return None
        booking = cls(**response)
        return booking

    @classmethod
    def get_relation_booking_item_date_by_item_id(cls, id, date):
        list_bookings = []
        values_dict = {"details.item_id": ObjectId(
            id), "booking_date": date, "status": "B"}

        response = __booking__.get_all_data(
            values_dict=values_dict, extra_params=BookingModel.__booking_group__, with_unwind=False)
        for booking in response:
            try:
                list_bookings.append(cls(**booking))
            except Exception as ex:
                pass
        return list_bookings

    def insert_booking(self):
        response = __booking__.insert_data(values_dict={
            "status": self.status,
            "booking_date": self.booking_date,
            "booking_time": self.booking_time,
            "comment": self.comment,
            "user_email": self.user_email,
            "user_name": self.user_name,
            "details": {
                "country_id": ObjectId(self.details.country),
                "site_id": ObjectId(self.details.site),
                "area_id": ObjectId(self.details.area),
                "category_id": ObjectId(self.details.category),
                "item_id": ObjectId(self.details.item),
            },
        })
        self._id = response.inserted_id

    def update_booking(self, booking):
        self.__dict__.update(**booking)
        return __booking__.update_data(
            {
                "id": ObjectId(self._id)
            },
            {
                "status": self.status,
                "booking_date": self.booking_date,
                "booking_time": self.booking_time,
                "comment": self.comment,
                "details": {
                    "country_id": ObjectId(self.details.country._id),
                    "site_id": ObjectId(self.details.site._id),
                    "area_id": ObjectId(self.details.area._id),
                    "category_id": ObjectId(self.details.category._id),
                    "item_id": ObjectId(self.details.item._id),
                }, 
            }
        )

    def delete_booking(self):
        return __booking__.delete_data(
            {
                "id": ObjectId(self._id)
            }
        )

    @classmethod
    def get_available_times_list_with_booking(cls, all_times=[], bookinglist=[]):
        list_available = []
        list_booking_times = []
        for booking in bookinglist:
            list_booking_times.extend(booking.booking_time)

        list_available = list(set(all_times) - set(list_booking_times))
        list_available.sort()

        return list_available

    @classmethod
    def checkTimeAvailability(self, time_slot, current_time):
        current_time = datetime.time(current_time.hour, current_time.minute, 0)
        time_slot = time_slot.split("-",2)
        start = self.convertTime(time_slot[0])
        end = self.convertTime(time_slot[1])
        if start <= current_time <= end:
            return True
        return False    

    @classmethod
    def convertTime(self, str_time):
        str_time = str_time.split(":", 2)
        return datetime.time(int(str_time[0]), int(str_time[1]),0)