import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient


class MongoDB:
    def __init__(self) -> None:
        self.client = MongoClient('localhost', 27017)
        self.db = self.client.dbsparta["alone_memo"]

    def insert_one(self, doc: dict) -> None:
        self.db.insert_one(doc)

    def find_many(self, setting: dict = None) -> list:
        setting = {'_id': False} if setting is None else setting
        return list(self.db.find({}, setting))


class Crawler:
    def __init__(self) -> None:
        self.agents = ["Mozilla/5.0",
                       "(Windows NT 10.0; Win64; x64)AppleWebKit/537.36",
                       "(KHTML, like Gecko)",
                       "Chrome/73.0.3683.86",
                       "Safari/537.36"]
        self.headers = {'User-Agent': " ".join(self.agents)}

    def scrap_meta_data(self, url: str) -> dict:
        data = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(data.text, 'html.parser')

        og_image = soup.select_one('meta[property="og:image"]')
        og_title = soup.select_one('meta[property="og:title"]')
        og_description = soup.select_one('meta[property="og:description"]')

        return {"title": og_title['content'],
                "image": og_image['content'],
                'description': og_description['content']}


mongodb = MongoDB()
crawler = Crawler()
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/articles', methods=['GET'])
def read_memo():
    response = {'success': True}

    try:
        response['rows'] = mongodb.find_many()
    except Exception as error:
        response['success'] = False
        response['error'] = error
    finally:
        return jsonify(response)


@app.route('/article', methods=['POST'])
def post_memo():
    response = {'success': True}

    try:
        data = request.form
        url = data['url']
        meta = crawler.scrap_meta_data(url)

        mongodb.insert_one({
            'title': meta['title'],
            'description': meta['description'],
            'image': meta['image'],
            'url': url,
            'comment': data['comment']
        })
    except Exception as error:
        response['success'] = False
        response['error'] = error
    finally:
        return jsonify(response)


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
