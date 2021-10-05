import os
from flask import (
    Flask, jsonify, request)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
if os.path.exists("env.py"):
    import env


app = Flask(__name__)


app.config.update(
    MONGO_DBNAME = os.environ.get("MONGO_DBNAME"),
    MONGO_URI = os.environ.get("MONGO_URI"),
    secret_key = os.environ.get("SECRET_KEY"))


mongo = PyMongo(app)


@app.route("/")
@app.route("/posts", methods=["GET", "POST"])
def get_posts():
    if request.method == "POST":
        response = mongo.db.posts.insert_one(request.get_json())
        new_post = mongo.db.posts.find_one({"_id": ObjectId(response.inserted_id)})
        new_post["_id"] = str(new_post["_id"])
        return jsonify(new_post), 201
        
    
    else:
        posts_number = int(request.args.get("limit")) if request.args.get("limit") else 20

        posts = mongo.db.posts.find().limit(posts_number)
        data = []
        for post in posts:
            post["_id"] = str(post["_id"])
            data.append(post)

        return jsonify(data)


@app.route("/posts/<_id>")
def get_post_by_id(_id):
    post = mongo.db.posts.find_one({"_id": ObjectId(_id)})
    post["_id"] = str(post["_id"])

    return jsonify(post)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")))