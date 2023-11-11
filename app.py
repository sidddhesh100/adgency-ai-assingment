from flask import Flask
import pymongo
import os 
from blueprint.user import user
from dotenv import load_dotenv


load_dotenv()
app = Flask(__name__)

app.config["MASTER_DB_CON"] = pymongo.MongoClient(os.environ.get("MONGO_DB_URL"), maxPoolSize=300)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'this is a secret'


@app.route("/")
def home():
    return "<h1>Hello World</h1>"

@app.route('/login')
def login():
    pass

@app.route('/logout')
def logout():
    pass

@app.route('/register')
def register():
    pass


app.register_blueprint(user)

if __name__ == "__main__":
    app.run(debug=True)
