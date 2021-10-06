import os
from flask import (
    Flask, jsonify, request)
from bson.objectid import ObjectId
from dbconfig import mongo_config
if os.path.exists("env.py"):
    import env

app = Flask(__name__)

mongo = mongo_config(app)

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