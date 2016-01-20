import word_counter
from etsy_api_wrapper import EtsyAPIWrapper

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
    input_dict_list = EtsyAPIWrapper.fetch_listing_titles_and_desc(shop)
    print word_counter.pool_handler(input_dict_list)
