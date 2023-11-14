import os

import pymongo
from dotenv import load_dotenv
from flask import Flask

from blueprint.book import book
from blueprint.user import user

load_dotenv()
app = Flask(__name__)

app.config["MASTER_DB_CON"] = pymongo.MongoClient(os.environ.get("MONGO_DB_URL"), maxPoolSize=300)["ad-gency"]
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY") or "this is a secret"


@app.route("/")
def home():
    return "<h1>Hello World</h1>"


app.register_blueprint(user)
app.register_blueprint(book)

if __name__ == "__main__":

    app.run(debug=True)
