from flask import Flask, request, Response
import pymongo
import os 
from blueprint.user import user

from blueprint.book import book
from dotenv import load_dotenv
from schema import UserRegisterSchema, LoginSchema
from http import HTTPStatus
from dto.User import User
from uuid import uuid4
from datetime import datetime
import json
from marshmallow.exceptions import ValidationError

load_dotenv()
app = Flask(__name__)

app.config["MASTER_DB_CON"] = pymongo.MongoClient(os.environ.get("MONGO_DB_URL"), maxPoolSize=300)["ad-gency"]
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'this is a secret'


@app.route("/")
def home():
    return "<h1>Hello World</h1>"



app.register_blueprint(user)
app.register_blueprint(book)

if __name__ == "__main__":

    app.run(debug=True)
