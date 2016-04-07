'''
etsy_api_wrapper.py -- Wrap Etsy API functions so that when given a list of
                       stores, all listing titles and listing descriptions are
                       fetched for each store.

                       How to run this module from command line:
                       $ python etsy_api_wrapper.py [SHOP_ID]
'''
import os
import time
import requests

ETSY_API_URL_ROOT = 'https://openapi.etsy.com/v2'
ETSY_API_KEY = os.environ['ETSY_API_KEY']
QUERY_RETRIES = 2

def format_url_and_params(shop_id, offset=0):
    '''
    Given a shop_id and offset, use the already defined url root and API key
    to construct a target URL and dictionary of query parameters.
    '''
    target_api_url = "{}/shops/{}/listings/active".format(ETSY_API_URL_ROOT,
                                                          shop_id)

    query_parameters = {
        'api_key': ETSY_API_KEY,
        'fields': 'title,description',
        'limit': 100,
        'offset': offset
    }

    return (target_api_url, query_parameters)

def execute_api_query(shop_id, offset=0):
    '''
    Execute a single API query and return the json response dictionary
    '''
    (target_api_url, query_parameters) = format_url_and_params(shop_id, offset)
    response = requests.get(target_api_url, params=query_parameters)
    remaining_retries = QUERY_RETRIES
    while (response.status_code == 400) and (remaining_retries > 0):
        # Etsy REST API intermittently returns 400 errors
        time.sleep(1)
        response = requests.get(target_api_url, params=query_parameters)
        remaining_retries -= 1

    response.raise_for_status()
    return response.json()

def fetch_listing_info(shop_id):
    '''
    Fetch all listings from a given shop.  Given a shop_id, return
    list of titles and descriptions of all items for that shop_id.
    This method will automatically paginate with 100 items per request.
    '''
    first_response_dict = execute_api_query(shop_id)
    results_list = first_response_dict['results']
    for offset in range(100, first_response_dict['count'], 100):
        this_response_dict = execute_api_query(shop_id, offset)
        results_list += this_response_dict['results']

    return (shop_id, results_list)
