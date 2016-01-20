"""
test_settings.py -- Run all unit tests for settings.py

Run from command line:
$ py.test test_settings.py
"""
import os

import settings

def test_read_env():
    settings.read_env()
    assert 'ETSY_API_KEY' in os.environ
