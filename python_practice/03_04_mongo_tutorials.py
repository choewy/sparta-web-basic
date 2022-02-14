from pymongo import MongoClient


class MongoDB:
    def __init__(self) -> None:
        self.client = MongoClient('localhost', 27017)
        self.db = self.client.dbsparta

    def insert_one(self, collection: str, doc: {}) -> bool:
        """insert_one('users', {'name': 'bobby', 'age': 28})"""

        try:
            self.db[collection].insert_one(doc)
            return True
        except Exception as error:
            print(error)
            return False

    def insert_many(self, collection: str, docs: []) -> bool:
        """insert_many('users', [{'name': 'bobby', 'age': 28}]"""

        try:
            self.db[collection].insert_many(docs)
            return True
        except Exception as error:
            print(error)
            return False

    def find_many(self, collection: str, search: dict = None, setting: dict = None) -> list:
        """find_many('users', {'name': 'bobby'}, {'_id': False})"""

        search = {} if search is None else search
        setting = {'_id': False} if setting is None else setting

        try:
            return list(self.db[collection].find(search, setting))
        except Exception as error:
            print(error)
            return []

    def find_one(self, collection: str, search: dict = None, setting: dict = None) -> dict:
        """find_one('users', {'name': 'bobby'}, {'_id': False})"""

        search = {} if search is None else search
        setting = {'_id': False} if setting is None else setting

        try:
            return self.db[collection].find_one(search, setting)
        except Exception as error:
            print(error)
            return {}

    def update_one(self, collection: str, search: dict, how: dict) -> bool:
        """update_one('users', {'name': 'bobby'}, {'$set': {'age': 27}})"""

        try:
            self.db[collection].update_one(search, how)
            return True
        except Exception as e:
            print(e)
            return False

    def delete_one(self, collection: str, search: dict) -> bool:
        """delete_one('users', {'name': 'bobby'})"""

        try:
            self.db[collection].delete_one(search)
            return True
        except Exception as e:
            print(e)
            return False


if __name__ == "__main__":
    mongodb = MongoDB()

