import os
from flask import Flask, request, jsonify, Response
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://mongo:27017/dev"
mongo = PyMongo(app)
db = mongo.db

hostname = os.uname()[1]

PrometheusMetrics(app)


@app.route("/")
def index():
    return jsonify(message=f"Welcome to Movies app! I am running inside {hostname} pod!")


@app.route("/message1")
def message1():
    return jsonify(message=f"You've hit {hostname}. A very interesting message.")


@app.route("/message2")
def message2():
    return jsonify(message=f"You've hit {hostname}. A second very interesting message.")


@app.route("/message3")
def message3():
    return jsonify(message=f"You've hit {hostname}. A third very interesting message.")


@app.route("/movies", methods=["GET"])
def get_all_movies():
    movies = db.movies.find()
    data = []
    for movie in movies:
        item = {
            "id": str(movie["_id"]),
            "title": movie["title"],
            "year": movie["year"]
        }
        data.append(item)
    return jsonify(data=data)


@app.route("/movies", methods=["POST"])
def create_movie():
    data = request.get_json(force=True)
    db.movies.insert_one(
        {
            "title": data["title"],
            "year": data["year"]
        }
    )
    return jsonify(message="Movie saved successfully!")


@app.route("/movies/<id>", methods=["GET"])
def get_movie_by_id(id):
    movie = db.movies.find_one_or_404({"_id": ObjectId(id)})
    movie = {
        "id": str(movie["_id"]),
        "title": movie["title"],
        "year": movie["year"]
    }
    return jsonify(movie=movie)


if __name__ == "__main__":
    app.run()