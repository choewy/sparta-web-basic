import requests
from bs4 import BeautifulSoup

agents = ["Mozilla/5.0",
          "(Windows NT 10.0; Win64; x64)AppleWebKit/537.36",
          "(KHTML, like Gecko)",
          "Chrome/73.0.3683.86",
          "Safari/537.36"]
headers = {
    'User-Agent': " ".join(agents)
}


def naver_movie_ranks() -> None:
    uri = ["https://movie.naver.com/movie/sdb/rank/rmovie.nhn",
           "sel=pnt&date=20200303"]
    url = '?'.join(uri)

    data = requests.get(url, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')

    selectors = {
        "tr": ["#old_content",
               "table",
               "tbody",
               "tr"],
        "title": ["td.title",
                  "div",
                  "a"],
        "rank": ["td.ac",
                 "img"],
        "point": ["td.point"]
    }

    trs = soup.select(' > '.join(selectors['tr']))
    for tr in trs:
        rank_title_point = ['', '', '']

        # 순위
        img_tag = tr.select_one(' > '.join(selectors['rank']))
        if img_tag is not None:
            rank_title_point[0] = img_tag.attrs.get('alt')[:2]

        # 제목
        a_tag = tr.select_one(' > '.join(selectors['title']))
        if a_tag is not None:
            rank_title_point[1] = a_tag.text

        # 평점
        td_tag = tr.select_one(' > '.join(selectors['point']))
        if td_tag is not None:
            rank_title_point[2] = td_tag.text

        print("\t".join(rank_title_point))


if __name__ == "__main__":
    naver_movie_ranks()
