import json

import pytest

from app import Encoder, app

test_client = app.test_client()


class TestShortener:
    @pytest.mark.parametrize(
        'nr_to_encode,result', [
            (0, ''),
            (1, '1'),
            (2, '2'),
            (10, 'a'),
            (61, 'Z'),
            (123, '1Z'),
        ]
    )
    def test_encoding(self, nr_to_encode, result):
        """
        Basic test for the base62 encoding
        """
        assert Encoder.encode(nr_to_encode) == result

    @pytest.mark.parametrize(
        'to_decode,result', [
            ('Z', 61),
            ('1', 1),
            ('', 0),
        ]
    )
    def test_decoding(self, to_decode, result):
        """
        Basic test for decoding base62 strings
        """
        assert Encoder.decode(to_decode) == result

    def test_end_to_end(self):
        """
        E2E test posting a URL and getting a shortcode back
        """
        res = test_client.post(
            '/shorten',
            data=json.dumps({'url': 'http://example.com'}),
            headers={"Content-Type": "application/json"}
        )
        url = [i for i in res.response][0]

        assert url == b'http://127.0.0.1:5000/1'

    def test_invalid_url(self):
        """
        Ensure invalid URLs are rejected
        """
        res = test_client.post(
            '/shorten',
            data=json.dumps({'url': 'asd'}),
            headers={"Content-Type": "application/json"}
        )

        assert res.status_code == 400
