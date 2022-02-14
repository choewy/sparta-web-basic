import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

url = "https://movie.naver.com/movie/sdb/rank/rmovie.nhn?sel=pnt&date=20200303"


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


class NaverMovies:
    def __init__(self, db: MongoDB = None) -> None:
        self.agents = ["Mozilla/5.0",
                       "(Windows NT 10.0; Win64; x64)AppleWebKit/537.36",
                       "(KHTML, like Gecko)",
                       "Chrome/73.0.3683.86",
                       "Safari/537.36"]
        self.headers = {'User-Agent': " ".join(self.agents)}
        self.data = requests.get(url, headers=self.headers)
        self.soup = BeautifulSoup(self.data.text, 'html.parser')
        self.db = db

    def scrap_movies(self) -> bool:
        docs = []

        selectors = {"tr": "#old_content > table > tbody > tr",
                     "title": "td.title > div > a",
                     "rank": "td.ac > img",
                     "point": "td.point"}

        trs = self.soup.select(selectors['tr'])

        for tr in trs:
            doc = {"rank": "",
                   "title": "",
                   "point": ""}

            img_tag = tr.select_one(selectors['rank'])
            a_tag = tr.select_one(selectors['title'])
            td_tag = tr.select_one(selectors['point'])

            if a_tag is not None:
                doc["rank"] = img_tag.attrs.get('alt')[:2]
                doc["title"] = a_tag.text
                doc["point"] = float(td_tag.text)
                docs.append(doc)

        return self.db.insert_many('movies', docs)


if __name__ == "__main__":
    mongodb = MongoDB()
    crawler = NaverMovies(db=mongodb)

    def create_collection() -> None:
        result = crawler.scrap_movies()
        print(f"결과 : 컬렉션 생성 {'완료' if result else '실패'}")

    def quiz_1() -> None:
        """ 영화 '매트릭스'의 평점 가져오기 """

        doc = mongodb.find_one('movies', {"title": "매트릭스"})

        if len(doc.keys()):
            point = doc["point"]
            print(point)
        else:
            print("영화 '매트릭스'를 찾을 수 없습니다.")

    def quiz_2() -> None:
        """ 영화 '매트릭스'와 같은 평점의 영화 가져오기 """

        doc = mongodb.find_one('movies', {"title": "매트릭스"})

        if len(doc.keys()):
            point = doc["point"]
            docs = mongodb.find_many('movies', {"point": point})

            if len(docs):
                for doc in docs:
                    print(doc['title'])
            else:
                print("영화 '매트릭스'와 평점이 같은 영화를 찾을 수 없습니다.")
        else:
            print("영화 '매트릭스'를 찾을 수 없습니다.")

    def quiz_3() -> None:
        """ 영화 '매트릭스'의 평점ㅇ을 0으로 만들기 """

        result = mongodb.update_one('movies',
                                    {'title': "매트릭스"},
                                    {'$set': {'point': 0}})
        print(f"결과 : doc 수정 {'완료' if result else '실패'}")
