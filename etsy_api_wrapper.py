"""
etsy_api_wrapper.py -- Wrap Etsy API functions so that when given a list of
                       stores, all listing titles and listing descriptions are
                       fetched for each store.

                       How to run this module from command line:
                       $ python etsy_api_wrapper.py [SHOP_ID]
"""
import json
import os
import sys
import requests


class EtsyAPIWrapper(object):
    """ See module docstring """
    ETSY_API_URL_ROOT = 'https://openapi.etsy.com/v2/'
    ETSY_API_KEY = os.environ['ETSY_API_KEY']

    @classmethod
    def format_url_and_params(cls, shop_id, offset=0):
        """
        Given a shop_id and offset, use the already defined url root and API key
        to construct a target URL and dictionary of query parameters.
        """
        target_api_url = "{}/shops/{}/listings/active".format(
            cls.ETSY_API_URL_ROOT,
            shop_id
        )

        query_parameters = {
            'api_key': cls.ETSY_API_KEY,
            'fields': 'title,description',
            'limit': 100,
            'offset': offset
        }

        return (target_api_url, query_parameters)

    @classmethod
    def execute_api_query(cls, shop_id, offset=0):
        """
        Execute a single API query and return the json response dictionary
        """
        (target_api_url, query_parameters) = cls.format_url_and_params(shop_id,
                                                                       offset)
        response = requests.get(target_api_url, params=query_parameters)
        response.raise_for_status()
        return response.json()

    @classmethod
    def fetch_listing_titles_and_desc(cls, shop_id):
        """
        Fetch all listings from a given shop.  Given a shop_id, return
        list of titles and descriptions of all items for that shop_id.
        This method will automatically paginate with 100 items per request.
        """
        first_response_dict = cls.execute_api_query(shop_id)
        results_list = first_response_dict['results']
        for offset in range(100, first_response_dict['count'], 100):
            # Paginate with 100 items/page and update dictionary
            this_response_dict = cls.execute_api_query(shop_id, offset)
            results_list += this_response_dict['results']

        return results_list


if __name__ == "__main__":
    print json.dumps(
        EtsyAPIWrapper().fetch_listing_titles_and_desc(sys.argv[1])
    )
