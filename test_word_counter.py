"""
word_counter.py -- Run all unit tests for word_counter.py

Run from command line:
$ py.test test_word_counter.py
"""
from collections import Counter

import word_counter

def test_count_words_in_str():
    expected = Counter(['test', 'test', 'word'])
    output = word_counter.count_words_in_str('test word TEST')
    assert expected == output

def test_remove_common_words():
    input_counter = Counter(['are', 'the', 'and', 'test', 'hello', 'a', 'a'])
    expected = Counter(['test', 'hello'])
    output = word_counter.remove_common_words(input_counter)
    assert expected == output

def test_count_words_in_results_dict(monkeypatch):
    input_dict = {
        'title': 'test title',
        'description': 'this is a test description'
    }
    monkeypatch.setattr("word_counter.count_words_in_str", lambda value: value)
    expected = 'test title this is a test description'
    output = word_counter.count_words_in_results_dict(input_dict)
    assert expected == output

def test_pool_handler(monkeypatch):
    input_dict_list = [
        {
            'title': 'test title first',
            'description': 'this is a test description'
        }, {
            'title': 'test title second',
            'description': 'this is a test description again'
        }, {
            'title': 'test title third',
            'description': 'this is a test description again and again'
        }
    ]
    class TempClass:
        @staticmethod
        def map(arg1, arg2):
            return [Counter(['test']), Counter(['test'])]

    monkeypatch.setattr("multiprocessing.Pool", lambda value: TempClass)
    monkeypatch.setattr("word_counter.remove_common_words", lambda value: value)
    expected = Counter(['test', 'test']).most_common(
        word_counter.NUM_COMMON_WORDS
    )
    output = word_counter.pool_handler(input_dict_list)
    assert expected == output
