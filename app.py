import os
import random
from string import ascii_letters, digits

from flask import Flask, request, redirect

ROOT_URL = os.getenv('APP_URL') or 'http://127.0.0.1:5000/'

app = Flask(__name__)

# this could be eg.: Redis, or DynamoDB
STORE = {}

# this could be a counter in Redis, which can be atomically incremented
COUNTER = 0

ABC = [char for char in ascii_letters + digits]

def encode(number):
    string = ''
    while(number > 0):
        string = ABC[number % len(ABC)] + string
        number //= len(ABC)
    return string


@app.route('/shorten', methods=['POST'])
def create():
    global COUNTER

    # TODO escape JS in url
    url = request.json.get('url')

    COUNTER += 1

    encoded = encode(COUNTER)
    STORE[encoded] = url

    return ROOT_URL + encoded


@app.route('/<shortcode>')
def get(shortcode):
    long_url = STORE.get(shortcode)
    return redirect(long_url)


if __name__ == '__main__':
    app.run(debug=True)
