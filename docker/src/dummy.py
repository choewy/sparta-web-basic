from util.mongo import MongoDB
from util.crawler import Crawler


mongodb = MongoDB()
crawler = Crawler()


def create_dummy_data():
    url = "https://movie.naver.com/movie/sdb/rank/rpeople.nhn"
    urls = crawler.scrap_urls(url)
    docs = [crawler.scrap_data(u) for u in urls]
    done = mongodb.init_dummy_data("actors", docs)
    print(done)


if __name__ == "__main__":
    create_dummy_data()
