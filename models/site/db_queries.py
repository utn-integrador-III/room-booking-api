from db.db_manager import Connection
from decouple import config


__site__ = Connection(config("MANAGMENT_SITE_COLLECTION"))