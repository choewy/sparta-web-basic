import requests
from bs4 import BeautifulSoup


class Crawler:
    agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'

    def __init__(self) -> None:
        self.headers = {"User-Agent": self.agent}

    def scrap_urls(self, url: str, base_url: str = "https://movie.naver.com/") -> list:
        request = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(request.text, 'html.parser')

        selectors = {
            "tr": "#old_content > table > tbody > tr",
            "a": "td.title > a"
        }

        urls = []
        tr_tags = soup.select(selectors["tr"])
        for tr_tag in tr_tags:
            a_tag = tr_tag.select_one(selectors["a"])

            if a_tag is not None:
                urls.append(base_url + a_tag["href"])

        return urls

    def scrap_data(self, url: str) -> any:
        request = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(request.text, 'html.parser')

        selectors = {
            "name": "#content > div.article > div.mv_info_area > div.mv_info.character > h3 > a",
            "img": "#content > div.article > div.mv_info_area > div.poster > img",
            "recent": "#content > div.article > div.mv_info_area > div.mv_info.character > dl > dd > a:nth-child(1)"
        }

        return {
            "name": soup.select_one(selectors["name"]).text,
            "img": soup.select_one(selectors["img"])["src"],
            "recent": soup.select_one(selectors["recent"]).text,
            "url": url,
            "like": 0
        }
