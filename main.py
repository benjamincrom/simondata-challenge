"""
main.py -- iterate through list of shops and for each shop return a counter
           of the five most commonly used words in the titles and descriptions
           of each item in that shop.
"""
import multiprocessing

import word_counter
import etsy_api_wrapper

DEFAULT_PROCESS_POOL_SIZE = 8

SHOP_LIST = [
    'DesignWithinYou',
    'HeritageWedding',
    'JoyfulMoose',
    'Vanijja',
    'forlovepolkadots',
    'ThePersonalWeddingCo',
    'SomethingYouGifts',
    'PersonalizedGiftsbyJ',
    'CreationsByAngel',
    'kutekiddo',
    'SouthernTradeMark',
    'MikesRevivals',
    'JuniperAndLace',
    'navesdesign',
    'sashesforlove',
    'EnchantedBrideUSA',
    'PersonalizedPoshy',
    'keeplifesimpledesign',
    'WearableArtz',
    'DavieandChiyo',
]

process_pool = multiprocessing.Pool(DEFAULT_PROCESS_POOL_SIZE)
shop_info_list = process_pool.map(etsy_api_wrapper.fetch_listing_info,
                                  SHOP_LIST)

for shop_tuple in shop_info_list:
    print "{} -- {}".format(shop_tuple[0],
                            word_counter.pool_handler(shop_tuple[1]))
