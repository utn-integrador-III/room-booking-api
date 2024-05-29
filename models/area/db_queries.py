from db.db_manager import Connection
from decouple import config


__area__ = Connection(config("MANAGMENT_AREA_COLLECTION"))