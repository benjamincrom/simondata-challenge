"""
main.py -- iterate through list of shops and for each shop return a counter
           of the five most commonly used words in the titles and descriptions
           of each item in that shop.
"""
import word_counter
import etsy_api_wrapper

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

for shop in SHOP_LIST:
    input_dict_list = etsy_api_wrapper.fetch_listing_titles_and_desc(shop)
    print word_counter.pool_handler(input_dict_list)
