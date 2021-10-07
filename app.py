import os
from bson.objectid import (ObjectId, InvalidId)
from flask import (
    Flask, jsonify, request)
from dbconfig import mongo_config
if os.path.exists("env.py"):
    import env

app = Flask(__name__)

mongo = mongo_config(app)


@app.route("/")
def get_home():
    return jsonify({"message": "Cogitate API root."})


@app.route("/posts", methods=["GET", "POST"])
def get_posts():
    if request.method == "POST":
        try:
            response = mongo.db.posts.insert_one(request.get_json())
            new_post = mongo.db.posts.find_one(
                {"_id": ObjectId(response.inserted_id)})
            new_post["_id"] = str(new_post["_id"])
            return jsonify(new_post), 201
        except (ValueError, NameError, TypeError) as err:
            return jsonify({"error": f"{err}"}), 400
        except:
            return jsonify({"error": "Internal server error"}), 500

    else:
        try:
            limit = request.args.get("limit", default=20, type=int)
            posts_number = int(limit)
            if posts_number <= 0 or posts_number > 100:
                raise ValueError("Limit value out of range (1-100)")

            posts = mongo.db.posts.find().limit(posts_number)
            posts = [{**post, "_id": str(post['_id'])} for post in posts]
            if len(posts) == 0:
                return "", 204

            return jsonify(posts), 200

        except ValueError as err:
            return jsonify({"error": f"{err}"}), 400
        except:
            return jsonify({"error": "Internal server error"}), 500

@app.route("/posts/<string:_id>")
def get_post_by_id(_id):
    try:
        post = mongo.db.posts.find_one({"_id": ObjectId(_id)})
        if not post:
            raise FileNotFoundError("Post not found")
        post["_id"] = str(post["_id"])
        return jsonify(post), 200
    except (ValueError, NameError, TypeError, InvalidId) as err:
        return jsonify({"error": f"{err}"}), 400
    except FileNotFoundError as err:
        return jsonify({"error": f"{err}"}), 404
    except Exception as err:
        return jsonify({"error": "Internal server error"}), 500


class FileNotFoundError(Exception):
    pass


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")))