"""
word_counter.py -- Given a list of formatted dictionaries from the
                   etsy_api_wrapper module, count the occurrences of all
                   words in each dictionary, then sum these counts together.
                   Return the top five final word counts for a given list. 

                   Note: uses the multiprocessing library for parallel
                   execution
"""
import re
import multiprocessing
from collections import Counter

WORD_SEARCH_REGEX = re.compile(r'\w+')
PROCESSOR_POOL_SIZE = 8
IGNORE_LIST = ['to', 'are', 'the', 'and', 'in', 'is', 'if', 'your', 'my',
               'at', 'this', '__________________________________________',
               'for', 'quot', 'you', 'me', 'be', 'or', 'on', 'a', 'with',
               'of', 'so', 'it', 'http', 'https', 'com', 'www', 'i', 'we']

def count_words_in_str(input_str):
    """ Breaks string into list of words then loads them into a Counter """
    word_list = WORD_SEARCH_REGEX.findall(input_str.lower())
    return Counter(word_list)

def remove_common_words(input_counter):
    """ Removes common words and digits from a Counter """
    for word in list(input_counter):
        if word in IGNORE_LIST or word.isdigit():
            del input_counter[word]

    return input_counter

def count_words_in_results_dict(input_dict):
    """
    Combine the two string values from an etsy_api_wrapper dictionary into a
    single string, then break the string down into a list of words and load
    them into a Counter.
    """
    combined_str = "{} {}".format(
        input_dict['title'].encode('ascii', 'ignore'),
        input_dict['description'].encode('ascii', 'ignore')
    )
    return count_words_in_str(combined_str)

def pool_handler(input_dict_list):
    """
    Create a multiprocessing pool and have it process the list of dictionaries
    from etsy_api_wrapper.  Remove the common words from the returned Counter.
    """
    process_pool = multiprocessing.Pool(PROCESSOR_POOL_SIZE)
    counter_list = process_pool.map(count_words_in_results_dict,
                                    input_dict_list)

    counter_sum = Counter()
    for this_counter in counter_list:
        counter_sum += this_counter

    return remove_common_words(counter_sum).most_common(5)
