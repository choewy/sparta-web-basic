import requests
from bs4 import BeautifulSoup

url = "https://movie.naver.com/movie/sdb/rank/rmovie.nhn?sel=pnt&date=20200303"


class NaverMovies:
    def __init__(self) -> None:
        self.agents = ["Mozilla/5.0",
                       "(Windows NT 10.0; Win64; x64)AppleWebKit/537.36",
                       "(KHTML, like Gecko)",
                       "Chrome/73.0.3683.86",
                       "Safari/537.36"]
        self.headers = {'User-Agent': " ".join(self.agents)}
        self.data = requests.get(url, headers=self.headers)
        self.soup = BeautifulSoup(self.data.text, 'html.parser')

    def scrap_movies(self) -> None:
        selectors = {"tr": "#old_content > table > tbody > tr",
                     "title": "td.title > div > a",
                     "rank": "td.ac > img",
                     "point": "td.point"}

        trs = self.soup.select(selectors['tr'])

        for tr in trs:
            img_tag = tr.select_one(selectors['rank'])
            a_tag = tr.select_one(selectors['title'])
            td_tag = tr.select_one(selectors['point'])

            if a_tag is not None:
                rank = img_tag.attrs.get('alt')[:2]
                title = a_tag.text
                point = float(td_tag.text)
                print(f"{rank}\t{title}\t{point}")


if __name__ == "__main__":
    crawler = NaverMovies()
    crawler.scrap_movies()
