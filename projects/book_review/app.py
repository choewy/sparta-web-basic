from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient


class MongoDB:
    def __init__(self) -> None:
        self.client = MongoClient('localhost', 27017)
        self.db = self.client.dbsparta["book_reviews"]

    def insert_one(self, doc: dict) -> None:
        self.db.insert_one(doc)

    def find_many(self, setting: dict = None) -> list:
        setting = {'_id': False} if setting is None else setting
        return list(self.db.find({}, setting))


mongodb = MongoDB()
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/reviews', methods=['GET'])
def get_reviews():
    response = {'success': True}
    try:
        response['rows'] = mongodb.find_many()
        # sample_receive = request.args.get('sample_give')
        # print(sample_receive)
    except Exception as error:
        response['success'] = False
        response['error'] = error
    finally:
        return jsonify(response)


@app.route('/review', methods=['POST'])
def post_review() -> jsonify:
    response = {'success': True}
    try:
        data = request.form
        mongodb.insert_one({
            'title': data['title'],
            'author': data['author'],
            'review': data['review']
        })
    except Exception as error:
        response['success'] = False
        response['error'] = error
    finally:
        return jsonify(response)


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
