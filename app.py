import os
import random
from string import ascii_letters, digits

from flask import Flask, request, redirect

ROOT_URL = os.getenv('APP_URL') or 'http://127.0.0.1:5000/'

app = Flask(__name__)

# this could be eg.: Redis, or DynamoDB
STORE = {}

ABC = [char for char in ascii_letters + digits]

def generate_shortcode(length=4):
    chars = random.choices(ABC, k=length)
    shortcode = ''.join(chars)
    return shortcode


@app.route('/shorten', methods=['POST'])
def create():
    url = request.json.get('url')

    while True:
        shortcode = generate_shortcode()
        if shortcode not in STORE:
            # found an unused shortcode
            STORE[shortcode] = url
            break

    return ROOT_URL + shortcode


@app.route('/<shortcode>')
def get(shortcode):
    long_url = STORE.get(shortcode)
    return redirect(long_url)


if __name__ == '__main__':
    app.run(debug=True)
