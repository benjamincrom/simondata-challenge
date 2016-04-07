'''
app.py -- iterate through list of shops and for each shop return a counter
          of the five most commonly used words in the titles and descriptions
          of each item in that shop.

          Output results via Flask web template.
'''
import multiprocessing
from flask import render_template, Flask, request

# Load environment variables from .env
from settings import read_env
read_env()

import word_counter
import etsy_api_wrapper

DEFAULT_PROCESS_POOL_SIZE = 4

app = Flask(__name__)

def process_shop_list(sanitized_shop_list):
    '''
    Partition list of shops over process pool and let mapping function fetch
    data for each shop
    '''
    process_pool = multiprocessing.Pool(DEFAULT_PROCESS_POOL_SIZE)
    shop_tuple_list = process_pool.map(etsy_api_wrapper.fetch_listing_info,
                                       sanitized_shop_list)
    return shop_tuple_list

@app.route('/', methods=['GET', 'POST'])
def index():
    '''
    Fetch info for list of shops then analyze that info to get top five terms
    for each shop.
    '''
    shop_list = []
    result_list = []
    if 'search' in request.args and request.args['search'] != '':
        shop_list = request.args['search'].split(',')
        sanitized_shop_list = [shop.strip() for shop in shop_list]
        shop_tuple_list = process_shop_list(sanitized_shop_list)
        result_list = [(shop_tuple[0], word_counter.pool_handler(shop_tuple[1]))
                       for shop_tuple in shop_tuple_list]

    print result_list
    return render_template('index.html', results_list=result_list)

if __name__ == '__main__':
    app.debug = True
    app.run()
