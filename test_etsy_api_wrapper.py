"""
test_etsy_api_wrapper.py -- Run all unit tests for etsi_api_wrapper.py

Run from command line:
$ py.test test_etsi_api_wrapper.py
"""
from settings import read_env
read_env()

import etsy_api_wrapper

def test_format_url_and_params():
    output = etsy_api_wrapper.format_url_and_params('TestShop')
    assert output[0] == ('https://openapi.etsy.com/v2/shops/TestShop/'
                         'listings/active')
    assert output[1].get('api_key')
    assert output[1].get('fields') == 'title,description'
    assert output[1].get('offset') == 0

def test_execute_api_query_success(monkeypatch):
    class MockResponse:
        status_code = 200
        @staticmethod
        def raise_for_status():
            return 'status'
        @classmethod
        def json(cls):
            return cls.status_code

    monkeypatch.setattr("etsy_api_wrapper.format_url_and_params",
                        lambda input_1, input_2: ('test_url', {}))
    monkeypatch.setattr("requests.get", lambda value, **kwargs: MockResponse)
    output = etsy_api_wrapper.execute_api_query('test_shop_id')
    assert output == 200

def test_execute_api_query_failure(monkeypatch):
    class MockResponse:
        status_code = 400
        @staticmethod
        def raise_for_status():
            return 'status'
        @classmethod
        def json(cls):
            return cls.status_code

    #with pytest.raises():
    monkeypatch.setattr("etsy_api_wrapper.format_url_and_params",
                        lambda input_1, input_2: ('test_url', {}))
    monkeypatch.setattr("requests.get", lambda value, **kwargs: MockResponse)
    output = etsy_api_wrapper.execute_api_query('test_shop_id')
    assert output == 400

def test_fetch_listing_info(monkeypatch):
    monkeypatch.setattr("etsy_api_wrapper.execute_api_query",
                        lambda *args: {'results': [1, 2, 3],
                                       'count': 250})
    expected = ('test_shop_id', [1, 2, 3, 1, 2, 3, 1, 2, 3])
    output = etsy_api_wrapper.fetch_listing_info('test_shop_id')
    assert expected == output
