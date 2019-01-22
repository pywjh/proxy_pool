import random
from flask import Flask
from Mongo_DB import MongoHelper

mongo = MongoHelper()

app = Flask(__name__)


@app.route('/')
def index():
    result = mongo.select()
    text = random.choice(result)
    return '{}:{}'.format(text[0],text[1])


def start_server():
    app.run(debug=True, host='0.0.0.0', port='9999')


if __name__ == '__main__':
    start_server()


