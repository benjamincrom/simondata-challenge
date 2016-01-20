"""
test_etsy_api_wrapper.py -- Run all unit tests for etsi_api_wrapper.py

Run from command line:
$ py.test test_etsi_api_wrapper.py
"""
import etsy_api_wrapper

TEST_SHOP_ID = 'DesignWithinYou'

def test_format_url_and_params():
   output = etsy_api_wrapper.format_url_and_params(TEST_SHOP_ID)
   assert output[0] == ('https://openapi.etsy.com/v2/shops/DesignWithinYou/'
                        'listings/active')
   assert output[1].get('api_key')
   assert output[1].get('fields') == 'title,description'
   assert output[1].get('offset') == 0
