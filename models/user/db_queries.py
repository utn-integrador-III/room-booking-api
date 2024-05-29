from db.db_manager import Connection
from decouple import config

__user__ = Connection(config("MANAGMENT_USER_COLLECTION"))