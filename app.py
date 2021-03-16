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

ABC = [char for char in digits + ascii_letters]
BASE = len(ABC)

def encode(number):
    """
    Encode number in base62
    """
    string = ''
    while(number > 0):
        string = ABC[number % BASE] + string
        number //= BASE
    return string


def decode(string):
    """
    Decode base62 number to base 10 number
    """
    number = 0
    for index, char in enumerate(string[::-1]):
        number += ABC.index(char) * BASE ** index
    return number


@app.route('/shorten', methods=['POST'])
def create():
    global COUNTER
    # TODO escape JS in url
    url = request.json.get('url')

    COUNTER += 1
    encoded = encode(COUNTER)
    STORE[COUNTER] = url

    return ROOT_URL + encoded


@app.route('/<shortcode>')
def get(shortcode):
    decoded = decode(shortcode)
    long_url = STORE.get(decoded)
    return redirect(long_url)


if __name__ == '__main__':
    app.run(debug=True)
