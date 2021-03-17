import os
import sys
import logging

from string import ascii_letters, digits

import redis
from flask import Flask, request, redirect

ROOT_URL = os.getenv('APP_URL') or 'http://127.0.0.1:5000/'
ENV = os.getenv('APP_ENV') or 'local'

app = Flask(__name__)

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
log.addHandler(handler)


class DataStore:
    def __init__(self, backend):
        self.backend = backend

    def set(self, key, value):
        self.backend.set(key, value)

    def get(self, key):
        return self.backend.get(key)

    def inc(self):
        return self.backend.inc()

    def __str__(self):
        return str(self.backend)


class RedisBackend:
    def __init__(self, url=None):
        if url is None:
            url = os.getenv('REDIS_URL')

        self.db = redis.Redis.from_url(url)
        # A key that will be used as a counter
        self.counter = 'COUNTER'

    def set(self, key, value):
        self.db.set(key, value)

    def get(self, key):
        return self.db.get(key)

    def inc(self):
        return self.db.incr(self.counter)


class InMemoryBackend:
    def __init__(self):
        self.db = {}
        self.counter = 0

    def set(self, key, value):
        self.db[key] = value

    def get(self, key):
        return self.db.get(key)

    def inc(self):
        self.counter += 1
        return self.counter

    def __str__(self):
        return str({'store': self.db, 'counter': self.counter})


class Encoder:
    CHARSET = [char for char in digits + ascii_letters]
    BASE = len(CHARSET)

    @classmethod
    def encode(cls, number):
        """
        Encode number in base62
        """
        string = ''
        while(number > 0):
            string = cls.CHARSET[number % cls.BASE] + string
            number //= cls.BASE
        return string
    
    @classmethod
    def decode(cls, shortcode):
        """
        Decode base62 number to base 10 number
        """
        number = 0
        for index, char in enumerate(shortcode[::-1]):
            number += cls.CHARSET.index(char) * cls.BASE ** index
        return number


def _get_store():
    if ENV == 'local':
        return DataStore(InMemoryBackend())
    elif ENV == 'prod':
        return DataStore(RedisBackend())

STORE = _get_store()

@app.route('/shorten', methods=['POST'])
def create():
    try:
        # TODO escape JS in url
        url = request.json.get('url')
    except AttributeError:
        message = "Could not parse URL"
        log.exception(message)
        return message, 400

    # increment counter
    counter = STORE.inc()

    # encode counter - this will be the shortcode
    encoded = Encoder.encode(counter)

    # set a new key: counter -> long url
    STORE.set(counter, url)

    if ENV == 'local':
        log.info(str(STORE))

    return ROOT_URL + encoded


@app.route('/<shortcode>')
def get(shortcode):
    decoded = Encoder.decode(shortcode)
    long_url = STORE.get(decoded)

    if long_url is None:
        return "Not found", 404

    return redirect(long_url)


if __name__ == '__main__':
    app.run(debug=True)
