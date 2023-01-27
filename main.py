from flask import Flask
import datasetMaker

if __name__ == "__main__":
    print("hello")
    exit(0)
    app = Flask(__name__)


@app.route('/')
def index():
    return 'hello, world'

@app.route('/countries')
def countries():
    return "{}"