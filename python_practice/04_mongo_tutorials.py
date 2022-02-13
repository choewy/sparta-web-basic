from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbsparta


def insert_one(collection: str, doc: {}) -> bool:
    """insert_one('users', {'name': 'bobby', 'age': 28})"""

    try:
        db[collection].insert_one(doc)
    except Exception as error:
        print(error)
        return False


def find(collection: str, search: dict = None, setting: dict = None) -> any:
    """find('users', {'name': 'bobby'}, {'_id': False})"""

    search = {} if search is None else search
    setting = {'_id': False} if setting is None else setting

    try:
        return list(db[collection].find(search, setting))
    except Exception as error:
        print(error)
        return {}


def update_one(collection: str, search: dict, doc: dict) -> bool:
    """update_one('users', {'name': 'bobby'}, {'$set': {'age': 27}})"""

    try:
        db[collection].update_one(search, doc)
        return True
    except Exception as e:
        print(e)
        return False


def delete_one(collection: str, search: dict) -> bool:
    """delete_one('users', {'name': 'bobby'})"""

    try:
        db[collection].delete_one(search)
        return True
    except Exception as e:
        print(e)
        return False


if __name__ == "__main__":
    print(delete_one("users", {"name": "bobby"}))
