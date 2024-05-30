from fastapi import HTTPException
from core.logger import logger
from models.files import FILES_COLLECTION
from infrastructure.mongodb import Client
from core.utils import covert_object_id_to_str_for_list


class FileRepository:
    def get_list(self, query, raise_exc=True):
        try:
            objs = Client.find(FILES_COLLECTION, query)
            objs = covert_object_id_to_str_for_list(objs)
        except Exception as exc:
            logger.log_exc(exc)
            obj = None
            if raise_exc:
                raise HTTPException(500, "Error while get file, try again")
        return obj

    def get_obj(self, query, raise_exc=True):
        try:
            obj = Client.find_one(FILES_COLLECTION, query)
            if obj:
                obj["_id"] = str(obj["_id"])
        except Exception as exc:
            logger.log_exc(exc)
            obj = {}
            if raise_exc:
                raise HTTPException(500, "Error while get file, try again")
        return obj

    def create(self, data):
        try:
            obj_id = Client.insert_one(FILES_COLLECTION, data)
        except Exception as exc:
            logger.log_exc(exc)
            obj_id = ""

        return str(obj_id)
