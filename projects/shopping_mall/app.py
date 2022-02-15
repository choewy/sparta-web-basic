from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient


class MongoDB:
    def __init__(self) -> None:
        self.client = MongoClient('localhost', 27017)
        self.db = self.client.dbsparta['shopping_mall']

    def insert_one(self, doc: {}) -> bool:
        try:
            self.db.insert_one(doc)
            return True
        except Exception as error:
            print(error)
            return False

    def insert_many(self, docs: {}) -> bool:
        try:
            self.db.insert_many(docs)
            return True
        except Exception as error:
            print(error)
            return False

    def delete_one(self, search: {}) -> bool:
        try:
            self.db.delete_one(search)
            return True
        except Exception as error:
            print(error)
            return False

    def find_many(self, search: {}) -> []:
        try:
            return list(self.db.find(search, {"_id": False}))
        except Exception as error:
            print(error)
            return []


app = Flask(__name__)
mongodb = MongoDB()


@app.route('/')
def homework():
    return render_template('index.html')


@app.route('/order', methods=['POST'])
def save_order() -> {}:
    response = {"success": True}
    data = request.form
    try:
        mongodb.insert_one({"name": data['name'],
                            "size": data["size"],
                            "address": data["address"],
                            "phone": data["phone"]})
    except Exception as error:
        print(error)
        response["success"] = False
        response["error"] = error
    finally:
        return jsonify(response)


@app.route('/orders', methods=['GET'])
def view_orders() -> {}:
    response = {"success": True}
    try:
        response["rows"] = mongodb.find_many({})
    except Exception as error:
        print(error)
        response["success"] = False
        response["error"] = error
    finally:
        return jsonify(response)


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
