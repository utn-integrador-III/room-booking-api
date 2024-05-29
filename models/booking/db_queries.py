from db.db_manager import Connection
from decouple import config

__booking__ = Connection(config("RESERVATION_BOOKING_COLLECTION"))