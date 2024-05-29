from db.db_manager import Connection
from decouple import config


__item__ = Connection(config("MANAGMENT_ITEM_COLLECTION"))