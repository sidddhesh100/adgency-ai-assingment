from flask import Flask

app = Flask(__name__)


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


if __name__ == "__main__":
    app.run(debug=True)
