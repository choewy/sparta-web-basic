from bson import ObjectId
from pymongo import MongoClient


class MongoDB:
    def __init__(self,
                 host: str = "localhost",
                 port: int = 27017,
                 db: str = "dbsparta"):
        self.client = MongoClient(f"mongodb:{host}:{port}/")
        self.db = self.client[db]

    def find_all(self, collection: str) -> dict:
        response = {"success": True}

        try:
            rows = list(self.db[collection].find({}))
            for row in rows:
                row["_id"] = str(row['_id'])
            response["rows"] = rows
        except Exception as error:
            response["success"] = False
            response["error"] = f"{error}"

        return response

    def insert_one(self, collection: str, doc: dict) -> dict:
        response = {"success": True}

        try:
            self.db[collection].insert_one(doc)
        except Exception as error:
            response["success"] = False
            response["error"] = f"{error}"

        return response

    def update_one(self, collection: str, _id: str) -> dict:
        response = {"success": True}

        try:
            self.db[collection].update_one(
                {"_id": ObjectId(_id)}, {"$inc": {"like": 1}})
        except Exception as error:
            response["success"] = False
            response["error"] = f"{error}"

        return response

    def delete_one(self, collection: str, _id: str) -> dict:
        response = {"success": True}

        try:
            self.db[collection].delete_one({"_id": ObjectId(_id)})
        except Exception as error:
            response["success"] = False
            response["error"] = f"{error}"

        return response

    def init_dummy_data(self, collection: str, docs: list) -> dict:
        response = {"success": True}

        try:
            self.db[collection].drop()
            self.db[collection].insert_many(docs)
        except Exception as error:
            response["success"] = False
            response["error"] = f"{error}"

        return response
