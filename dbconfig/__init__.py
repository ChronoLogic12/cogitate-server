import os
from flask_pymongo import PyMongo

def mongo_config(app):

    app.config.update(
        MONGO_DBNAME = os.environ.get("MONGO_DBNAME"),
        MONGO_URI = os.environ.get("MONGO_URI"),
        secret_key = os.environ.get("SECRET_KEY"))
    return PyMongo(app)




