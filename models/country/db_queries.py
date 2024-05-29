from db.db_manager import Connection
from decouple import config


__country__ = Connection(config("MANAGMENT_COUNTRY_COLLECTION"))