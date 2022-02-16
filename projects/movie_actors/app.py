from flask import Flask, render_template, jsonify, request
from util.mongo import MongoDB
from util.crawler import Crawler


mongodb = MongoDB()
crawler = Crawler()
app = Flask(__name__)


def init_dummy_data():
    url = "https://movie.naver.com/movie/sdb/rank/rpeople.nhn"
    urls = crawler.scrap_urls(url)
    docs = [crawler.scrap_data(u) for u in urls]
    done = mongodb.init_dummy_data("actors", docs)
    print(done)


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/api/actors", methods=["GET"])
def get_actors():
    response = {"success": True}

    try:
        done = mongodb.find_all("actors")
        if done["success"]:
            response["rows"] = done["rows"]
        else:
            response["success"] = False
            response["error"] = done["error"]
    except Exception as error:
        response["success"] = False
        response["error"] = error

    return jsonify(response)


@app.route("/api/like", methods=["POST"])
def increase_like():
    response = {"success": True}
    data = request.form

    try:
        done = mongodb.update_one("actors", data["_id"])
        if done["success"] is False:
            response["success"] = done["success"]
            response["error"] = done["error"]
    except Exception as error:
        response["success"] = False
        response["error"] = error

    return jsonify(response)


@app.route("/api/delete", methods=["POST"])
def delete_actor():
    response = {"success": True}
    data = request.form

    try:
        done = mongodb.delete_one("actors", data["_id"])
        if done["success"] is False:
            response["success"] = done["success"]
            response["error"] = done["error"]
    except Exception as error:
        response["success"] = False
        response["error"] = error

    return jsonify(response)


if __name__ == "__main__":
    # init_dummy_data()
    app.run("0.0.0.0", port=5000, debug=True)

