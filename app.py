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


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")))