"""
settings.py -- contains methods which help create the proper python runtime
               environment
"""
import re
import os

def read_env():
    """ Pull environment variables in from .env file """
    with open('.env') as filehandle:
        content = filehandle.read()

    for line in content.splitlines():
        match = re.match(r'\A([A-Za-z_0-9]+)=(.*)\Z', line)
        if match:
            key, val = match.group(1).strip(), match.group(2).strip()
            os.environ.setdefault(key, val)
