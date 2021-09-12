import os
import sys
import random
import logging
from typing import Text
from typing import Tuple

from abc import ABC, abstractmethod
from urllib.parse import urlparse

from string import ascii_letters, digits

import redis
from flask import Flask, request, redirect


ROOT_URL = os.getenv('APP_URL') or 'http://127.0.0.1:5005/'
ENV = os.getenv('APP_ENV') or 'local'

app = Flask(__name__)

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
log.addHandler(handler)


class URLInvalidError(Exception):
    pass


class DataStore:
    def __init__(self, backend):
        self.backend = backend

    def set(self, key, value) -> None:
        self.backend.set(key, value)

    def get(self, key) -> Text:
        return self.backend.get(key)

    def inc(self) -> int:
        return self.backend.inc()

    def __str__(self) -> Text:
        return str(self.backend)


class Backend(ABC):
    @abstractmethod
    def set(self, key, value) -> None:
        pass

    @abstractmethod
    def get(self, key) -> Text:
        pass

    @abstractmethod
    def inc(self) -> int:
        pass


class RedisBackend(Backend):
    def __init__(self, url=None):
        if url is None:
            url = os.getenv('REDIS_URL')

        self.db = redis.Redis.from_url(url)
        # A key that will be used as a counter
        self.counter = 'COUNTER'

    def set(self, key, value) -> None:
        self.db.set(key, value)

    def get(self, key) -> Text:
        return self.db.get(key)

    def inc(self) -> int:
        return self.db.incr(self.counter)


class InMemoryBackend(Backend):
    def __init__(self):
        self.db = {}
        self.counter = 0

    def set(self, key, value) -> None:
        self.db[key] = value

    def get(self, key) -> Text:
        return self.db.get(key)

    def inc(self) -> int:
        self.counter += 1
        return self.counter

    def __str__(self) -> Text:
        return str({'store': self.db, 'counter': self.counter})


class Encoder:
    CHARSET = [char for char in digits + ascii_letters]
    BASE = len(CHARSET)

    @classmethod
    def encode(cls, number) -> Text:
        """
        Encode number in base62
        """
        string = ''
        while(number > 0):
            string = cls.CHARSET[number % cls.BASE] + string
            number //= cls.BASE
        return string
    
    @classmethod
    def decode(cls, shortcode) -> int:
        """
        Decode base62 number to base 10 number
        """
        number = 0
        for index, char in enumerate(shortcode[::-1]):
            number += cls.CHARSET.index(char) * cls.BASE ** index
        return number


def _get_store() -> DataStore:
    if ENV == 'local':
        return DataStore(InMemoryBackend())
    elif ENV == 'prod':
        return DataStore(RedisBackend())
    raise RuntimeError("enviroment {ENV} is not supported")

STORE = _get_store()

@app.route('/shorten', methods=['POST'])
def create() -> Tuple[Text, int]:
    try:
        # TODO escape JS in url
        url = request.json.get('url')
        result = urlparse(url)
        if not all([result.scheme, result.netloc]):
            raise URLInvalidError
    except (AttributeError, URLInvalidError):
        message = "Could not parse URL"
        log.exception(message)
        return message, 400
    

    incremented_counter = STORE.inc()
    encoded_counter = Encoder.encode(incremented_counter)
    encoded_randomized = f"{encoded_counter}{random.randint(1,100)}"

    STORE.set(encoded_randomized, url)

    if ENV == 'local':
        log.info(str(STORE))

    return ROOT_URL + encoded_randomized, 201


@app.route('/<shortcode>')
def get(shortcode) -> Tuple[Text, int]:
    long_url = STORE.get(shortcode)

    if long_url is None:
        return "Not found", 404

    return redirect(long_url)


if __name__ == '__main__':
    app.run(debug=True, port=5005)
