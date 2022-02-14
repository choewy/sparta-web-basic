import requests
from bs4 import BeautifulSoup


class GenieMusics:
    def __init__(self) -> None:
        self.agents = ["Mozilla/5.0",
                       "(Windows NT 10.0; Win64; x64)AppleWebKit/537.36",
                       "(KHTML, like Gecko)",
                       "Chrome/73.0.3683.86",
                       "Safari/537.36"]
        self.headers = {'User-Agent': " ".join(self.agents)}
        self.data = requests.get("https://www.genie.co.kr/chart/top200?ditc=D&ymd=20200403&hh=23&rtm=N&pg=1",
                                 headers=self.headers)
        self.soup = BeautifulSoup(self.data.text, 'html.parser')

    def scrap_musics(self) -> None:

        selectors = {"tr": "#body-content > div.newest-list > div > table > tbody > tr",
                     "rank": "td.number",
                     "title": "td.info > a.title",
                     "artist": "td.info > a.artist"}
        trs = self.soup.select(selectors['tr'])
        for tr in trs:
            rank_tag = tr.select_one(selectors['rank'])
            title_tag = tr.select_one(selectors['title'])
            artist_tag = tr.select_one(selectors['artist'])

            rank = "0" + rank_tag.text.strip()[:2].strip()
            rank = rank[-2:]
            title = title_tag.text.strip()
            artist = artist_tag.text.strip()
            print(f"{rank}\t{title}\t{artist}")


if __name__ == "__main__":
    crawler = GenieMusics()
    crawler.scrap_musics()
