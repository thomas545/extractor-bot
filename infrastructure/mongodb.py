import os
import pymongo
from bson import ObjectId
from core.environment import get_environ
from core.logger import logger


class MongoClient:
    URI = get_environ("MONGO_URI")
    client = None
    database = "extractor"

    def __init__(self):
        logger.log("Initialising Mongodb Connection ...")
        self.client = pymongo.MongoClient(self.URI)
        logger.log("Mongo Client Is Running ...", self.client)

    def insert_one(self, collection, data, **kwargs):
        logger.log("insert_one", collection, data, kwargs)
        return (
            self.client[self.database][collection]
            .insert_one(data, **kwargs)
            .inserted_id
        )

    def insert_many(self, collection, data, **kwargs):
        logger.log("insert_many", collection, data, kwargs)
        return (
            self.client[self.database][collection]
            .insert_many(data, **kwargs)
            .inserted_ids
        )

    def find_one(self, collection, query, **kwargs):
        logger.log("find_one", collection, query, kwargs)
        return self.client[self.database][collection].find_one(query, **kwargs)

    def count(self, collection, query, **kwargs):
        logger.log("count", collection, query, kwargs)
        return self.client[self.database][collection].count_documents(query, **kwargs)

    def find(self, collection, query, skip=0, limit=None, sort=None, **kwargs):
        logger.log("find", collection, query, kwargs)
        if sort:
            if limit:
                return (
                    self.client[self.database][collection]
                    .find(query, **kwargs)
                    .skip(skip)
                    .sort(sort)
                    .limit(limit)
                )
            else:
                return (
                    self.client[self.database][collection]
                    .find(query, **kwargs)
                    .skip(skip)
                    .sort(sort)
                )
        else:
            if limit:
                return (
                    self.client[self.database][collection]
                    .find(query, **kwargs)
                    .skip(skip)
                    .limit(limit)
                )
            else:
                return (
                    self.client[self.database][collection]
                    .find(query, **kwargs)
                    .skip(skip)
                )

    def find_one_and_update(self, collection, query, update_query, **kwargs):
        logger.log("find_one_and_update", collection, query, kwargs)
        return self.client[self.database][collection].find_one_and_update(
            query, update_query, **kwargs
        )

    def update_one(self, collection, query, update_query, **kwargs):
        logger.log("update_one", collection, query, kwargs)
        return self.client[self.database][collection].update_one(
            query, update_query, **kwargs
        )

    def update_many(self, collection, query, update_query, **kwargs):
        logger.log("update_many", collection, query, kwargs)
        return self.client[self.database][collection].update_many(
            query, update_query, **kwargs
        )

    def delete_one(self, collection, query, **kwargs):
        logger.log("update_many", collection, query, kwargs)
        return self.client[self.database][collection].delete_one(query, **kwargs)

    def delete_many(self, collection, query, **kwargs):
        logger.log("delete_many", collection, query, kwargs)
        return self.client[self.database][collection].delete_many(query, **kwargs)

    @staticmethod
    def is_valid_id(_id):
        return ObjectId().is_valid(_id)


Client = MongoClient()
