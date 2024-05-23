from fastapi import HTTPException
from core.logger import logger
from core.auth import hash_password
from models.users import USER_COLLECTION
from infrastructure.mongodb import Client


class UserRepository:
    def get_obj(self, query, raise_exc=True):
        try:
            user_obj = Client.find_one(USER_COLLECTION, query)
            if user_obj:
                user_obj["_id"] = str(user_obj["_id"])
        except Exception as exc:
            logger.log_exc(exc)
            user_obj = None
            if raise_exc:
                raise HTTPException(500, "Error while get user, try again")


        return user_obj

    def create(self, data):
        try:
            data["password"] = hash_password(data.pop("password"))
            user_id = Client.insert_one(USER_COLLECTION, data)
        except Exception as exc:
            logger.log_exc(exc)
            user_id = ""

        return str(user_id)
