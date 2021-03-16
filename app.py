import os

from string import ascii_letters, digits

import redis
from flask import Flask, request, redirect

ROOT_URL = os.getenv('APP_URL') or 'http://127.0.0.1:5000/'

app = Flask(__name__)

# this could be eg.: Redis, or DynamoDB
STORE = {}

# this could be a counter in Redis, which can be atomically incremented
COUNTER = 0

class DataStore:
    def __init__(self, backend):
        self.backend = backend

    def set(self, key, value):
        self.backend.set(key, value)

    def get(self, key):
        return self.backend.get(key)


class RedisBackend:
    def __init__(self, url=None):
        if url is None:
            url = os.getenv('REDIS_URL')

        self.db = redis.Redis.from_url(url)

    def set(self, key, value):
        self.db.set(key, value)

    def get(self, key):
        return self.db.get(key)


class InMemoryBackend:
    def __init__(self):
        self.db = {}

    def set(self, key, value):
        self.db[key] = value

    def get(self, key):
        return self.db.get(key)


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
    env = os.getenv('APP_ENV') or 'local'
    if env == 'local':
        return DataStore(InMemoryBackend())
    elif env == 'prod':
        return DataStore(RedisBackend())

STORE = _get_store()

@app.route('/shorten', methods=['POST'])
def create():
    global COUNTER
    # TODO escape JS in url
    url = request.json.get('url')

    COUNTER += 1
    encoded = Encoder.encode(COUNTER)
    STORE.set(COUNTER, url)

    return ROOT_URL + encoded


@app.route('/<shortcode>')
def get(shortcode):
    decoded = Encoder.decode(shortcode)
    long_url = STORE.get(decoded)
    return redirect(long_url)


if __name__ == '__main__':
    app.run(debug=True)
