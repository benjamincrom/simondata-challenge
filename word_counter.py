""" TODO(bcrom) """
import re
import json
import multiprocessing
from collections import Counter

from etsy_api_wrapper import EtsyAPIWrapper

WORD_SEARCH_REGEX = re.compile(r'\w+')
INPUT_DICT_LIST = EtsyAPIWrapper.fetch_listing_titles_and_desc('DesignWithinYou')

def count_words_in_str(input_str):
    word_list = WORD_SEARCH_REGEX.findall(input_str.lower())
    return Counter(word_list)

def remove_common_words(input_counter):
    IGNORE_LIST = ['to', 'are', 'the', 'and', 'in', 'is', 'if', 'your', 'my',
                   'at', 'this', '__________________________________________',
                   'for', 'quot', 'you', 'me', 'be', 'or', 'on', 'a', 'with',
                   'of', 'so', 'it']

    for word in list(input_counter):
        if word in IGNORE_LIST:
            del input_counter[word]

    return input_counter

def count_words_in_results_dict(input_dict):
    full_counter = Counter()
    combined_str = "{} {}".format(
        input_dict['title'].encode('ascii', 'ignore'),
        input_dict['description'].encode('ascii', 'ignore')
    )
    this_counter = count_words_in_str(combined_str)
    full_counter = full_counter + this_counter

    return full_counter

def pool_worker(input_dict):
    return count_words_in_results_dict(input_dict)

def pool_handler():
    process_pool = multiprocessing.Pool(8)
    counter_list = process_pool.map(pool_worker, INPUT_DICT_LIST)
    counter_sum = Counter()
    for this_counter in counter_list:
        counter_sum = counter_sum + this_counter

    print remove_common_words(counter_sum)

pool_handler()
