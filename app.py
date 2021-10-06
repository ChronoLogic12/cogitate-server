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
        try:
            limit = request.args.get("limit", default=20, type=int)
            posts_number = int(limit)
            if posts_number <= 0 or posts_number > 100:
                raise ValueError("Limit value out of range (1-100)")

            posts = mongo.db.posts.find().limit(posts_number)
            data = []
            for post in posts:
                post["_id"] = str(post["_id"])
                data.append(post)

            if len(data) == 0:
                return "", 204

            return jsonify(data)

        except ValueError as err:
            return jsonify({"error": f"{err}"}), 400
        except:
            return jsonify({"error": "Internal server error"}),500
            

@app.route("/posts/<_id>")
def get_post_by_id(_id):
    post = mongo.db.posts.find_one({"_id": ObjectId(_id)})
    post["_id"] = str(post["_id"])

    return jsonify(post)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")))