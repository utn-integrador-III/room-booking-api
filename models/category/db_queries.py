from db.db_manager import Connection
from decouple import config

__category__ = Connection(config("MANAGMENT_CATEGORY_COLLECTION"))