import requests


url = 'http://openapi.seoul.go.kr:8088/6d4d776b466c656533356a4b4b5872/json/RealtimeCityAir/1/99'


def request_GET() -> None:
    req = requests.get(url)
    res = req.json()
    rows = res["RealtimeCityAir"]["row"]

    for row in rows:
        name = row['MSRSTE_NM']
        value = row['IDEX_MVL']

        if value > 80:
            print(f'{name} : {value}')


if __name__ == "__main__":
    request_GET()
